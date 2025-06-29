import sys
import os
import sqlite3
import datetime
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidget,
    QTableWidgetItem, QMenu, QAbstractItemView, QHeaderView, QSizePolicy
)
from PySide6.QtCore import Qt, QDir, QPropertyAnimation, QEasingCurve, QSettings
from PySide6.QtGui import QAction, QIcon
from ui_MainWindows import Ui_MainWindow
import threading
from PySide6.QtCore import Signal, QObject


class FolderManagerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # 处理打包后的资源路径
        if getattr(sys, 'frozen', False):
            # 打包后的可执行文件路径
            base_path = os.path.dirname(sys.executable)
        else:
            # 开发环境中的脚本路径
            base_path = os.path.dirname(os.path.abspath(__file__))

        # 设置数据库路径
        db_path = os.path.join(base_path, "folder_configs.db")
        self.db_connection = sqlite3.connect(db_path)

        # 设置图标路径
        self.icons_dir = os.path.join(base_path, "icons")

        # 更新图标路径引用
        self.ui.btn_Unfold.setIcon(QIcon(os.path.join(self.icons_dir, "PanelToggle.svg")))
        self.ui.btn_Top.setIcon(QIcon(os.path.join(self.icons_dir, "pushpin.svg")))

        # 初始化折叠状态
        self.footer_collapsed = False
        self.original_height = self.height()  # 保存原始窗口高度
        self.ui.footer_frame.setMaximumHeight(16777215)  # QT默认的最大值

        # 初始化数据库
        self.db_connection = sqlite3.connect("folder_configs.db")
        self.create_tables()

        # 设置窗口标题和图标
        self.setWindowTitle("QuickFold")

        # 设置表格
        self.setup_table()

        # 加载分组
        self.load_groups()

        # 连接信号槽
        self.connect_signals()

        # 初始化状态
        self.ui.prg_Source.setValue(0)
        self.ui.prg_Target.setValue(0)
        self.source_path = ""  # 存储当前源路径
        self.target_path = ""  # 存储当前目标路径
        self.is_topmost = False  # 窗口置顶状态

        # 加载历史记录
        self.load_recent_groups()

        # 设置plainTextEdit为可编辑
        self.ui.plainTextEdit.setReadOnly(False)

        # 多线程相关属性
        self.multithread_enabled = False
        self.current_worker = None

        # 初始化设置对象
        self.settings = QSettings("MyCompany", "QuickFold")

        # 从设置加载多线程配置
        self.multithread_enabled = self.settings.value("multithread_enabled", False, type=bool)

    def create_tables(self):
        """创建数据库表"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                last_used TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS folders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                folder_name TEXT NOT NULL,
                FOREIGN KEY (group_id) REFERENCES groups(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_name TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.db_connection.commit()

    def setup_table(self):
        """设置表格属性"""
        # 设置文件夹列表表格
        self.ui.table_FolderName.setColumnCount(2)
        self.ui.table_FolderName.setHorizontalHeaderLabels(["文件夹名称", "相对路径"])
        self.ui.table_FolderName.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.ui.table_FolderName.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.ui.table_FolderName.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.table_FolderName.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.table_FolderName.customContextMenuRequested.connect(self.show_context_menu)
        self.ui.table_FolderName.setAlternatingRowColors(True)

        # 设置历史记录表格
        self.ui.table_RecentlyUsed.setColumnCount(2)
        self.ui.table_RecentlyUsed.setHorizontalHeaderLabels(["分组名称", "最后使用时间"])
        self.ui.table_RecentlyUsed.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.ui.table_RecentlyUsed.setSelectionBehavior(QAbstractItemView.SelectRows)

        # 设置脚本生成标签页的文本框为可编辑
        self.ui.plainTextEdit.setReadOnly(False)

    def load_groups(self):
        """加载所有配置组到下拉框"""
        # 清空下拉框
        self.ui.cbox_GroupName02.clear()
        self.ui.cbox_GroupName01.clear()

        # 添加空白项作为默认选项
        self.ui.cbox_GroupName02.addItem("")
        self.ui.cbox_GroupName01.addItem("")

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT name FROM groups ORDER BY last_used DESC")
        groups = cursor.fetchall()

        for group in groups:
            self.ui.cbox_GroupName02.addItem(group[0])
            self.ui.cbox_GroupName01.addItem(group[0])

        # 确保默认为空白项
        self.ui.cbox_GroupName02.setCurrentIndex(0)
        self.ui.cbox_GroupName01.setCurrentIndex(0)

        # 连接同步信号
        self.ui.cbox_GroupName01.currentIndexChanged.connect(self.sync_group_names)
        self.ui.cbox_GroupName02.currentIndexChanged.connect(self.sync_group_names)

    def sync_group_names(self):
        """同步两个分组下拉框的选中状态"""
        # 获取当前选中的分组名称
        group_name = self.sender().currentText()

        # 同步另一个下拉框
        if self.sender() == self.ui.cbox_GroupName01:
            index = self.ui.cbox_GroupName02.findText(group_name)
            if index >= 0:
                self.ui.cbox_GroupName02.setCurrentIndex(index)
        else:
            index = self.ui.cbox_GroupName01.findText(group_name)
            if index >= 0:
                self.ui.cbox_GroupName01.setCurrentIndex(index)

        # 加载对应的分组数据
        self.load_selected_group()

    def load_recent_groups(self):
        """加载最近使用的分组到历史记录表"""
        cursor = self.db_connection.cursor()
        cursor.execute("""
            SELECT groups.name, MAX(history.timestamp) as last_used 
            FROM history 
            JOIN groups ON history.group_name = groups.name 
            GROUP BY groups.name 
            ORDER BY last_used DESC 
            LIMIT 10
        """)
        recent_groups = cursor.fetchall()

        # 清空表格
        self.ui.table_RecentlyUsed.setRowCount(0)

        # 添加最近使用的分组
        for i, (group_name, timestamp) in enumerate(recent_groups):
            self.ui.table_RecentlyUsed.insertRow(i)
            self.ui.table_RecentlyUsed.setItem(i, 0, QTableWidgetItem(group_name))

            # 格式化时间戳
            if timestamp:
                dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                formatted_time = dt.strftime("%Y-%m-%d %H:%M")
                self.ui.table_RecentlyUsed.setItem(i, 1, QTableWidgetItem(formatted_time))

    def record_group_usage(self, group_name):
        """记录分组使用历史"""
        if not group_name:
            return

        cursor = self.db_connection.cursor()

        # 更新组的使用时间
        cursor.execute("UPDATE groups SET last_used = datetime('now') WHERE name = ?", (group_name,))

        # 添加到历史记录
        cursor.execute("INSERT INTO history (group_name) VALUES (?)", (group_name,))

        self.db_connection.commit()

        # 重新加载历史记录
        self.load_recent_groups()

    def connect_signals(self):
        """连接所有信号和槽"""
        # 源和目标按钮
        self.ui.btn_Source.clicked.connect(self.select_source_path)
        self.ui.btn_Target.clicked.connect(self.select_target_path)

        # 分组管理按钮
        self.ui.btn_Save.clicked.connect(self.save_group)
        self.ui.btn_Del.clicked.connect(self.delete_group)

        # 创建文件夹按钮
        self.ui.btn_Run.clicked.connect(self.create_folders)
        self.ui.btn_Goto.clicked.connect(self.create_filtered_folders)  # 新增：创建过滤后的文件夹

        # 分组下拉框
        self.ui.cbox_GroupName02.currentIndexChanged.connect(self.load_selected_group)
        self.ui.cbox_GroupName01.currentIndexChanged.connect(self.load_selected_group_for_script)

        # 过滤器按钮
        self.ui.btn_Filters.clicked.connect(self.show_filters_dialog)

        # 脚本生成按钮
        self.ui.btn_GenBatchScript.clicked.connect(self.generate_batch_script)
        self.ui.btn_GenPSScript.clicked.connect(self.generate_powershell_script)
        self.ui.btn_GenScript.clicked.connect(self.save_generated_script)

        # 折叠按钮
        self.ui.btn_Unfold.clicked.connect(self.toggle_footer)

        # 历史记录按钮
        self.ui.btn_History_Path.clicked.connect(self.show_recent_groups_menu)

        # 设置按钮
        self.ui.btn_Settings.clicked.connect(self.show_settings)

        # 关于按钮
        self.ui.btn_About.clicked.connect(self.show_about)

        # 菜单按钮
        self.ui.btn_Menu.clicked.connect(self.show_main_menu)

        # 置顶按钮
        self.ui.btn_Top.clicked.connect(self.toggle_topmost)

        # 搜索框文本变化
        self.ui.edit_Search.textChanged.connect(self.filter_folders)

        # 连接清理历史记录按钮
        self.ui.btn_Clear.clicked.connect(self.clear_history)

    def toggle_topmost(self):
        """切换窗口置顶状态"""
        self.is_topmost = not self.is_topmost

        # 保存当前窗口的几何信息和焦点状态
        geometry = self.saveGeometry()
        is_active = self.isActiveWindow()

        # 更新窗口标志
        if self.is_topmost:
            flags = self.windowFlags() | Qt.WindowStaysOnTopHint
            self.ui.btn_Top.setIcon(QIcon(":/svg/icons/pushpin_filled.svg"))  # 使用填充图标表示置顶
        else:
            flags = self.windowFlags() & ~Qt.WindowStaysOnTopHint
            self.ui.btn_Top.setIcon(QIcon(":/svg/icons/pushpin.svg"))  # 使用普通图标表示非置顶

        # 重新创建窗口
        self.hide()  # 先隐藏窗口
        self.setWindowFlags(flags)
        self.show()  # 重新显示窗口

        # 恢复窗口状态
        self.restoreGeometry(geometry)
        if is_active:
            self.activateWindow()

    def filter_folders(self):
        """根据搜索框内容过滤文件夹列表"""
        search_text = self.ui.edit_Search.text().lower()

        for row in range(self.ui.table_FolderName.rowCount()):
            name_item = self.ui.table_FolderName.item(row, 0)
            path_item = self.ui.table_FolderName.item(row, 1)

            if name_item and path_item:
                folder_name = name_item.text().lower()
                rel_path = path_item.text().lower()

                # 检查文件夹名称或路径是否包含搜索文本
                visible = search_text in folder_name or search_text in rel_path

                # 设置行可见性
                self.ui.table_FolderName.setRowHidden(row, not visible)

    def toggle_footer(self):
        """切换底部区域的折叠状态并调整窗口高度"""
        self.footer_collapsed = not self.footer_collapsed

        if self.footer_collapsed:
            # 折叠底部区域
            self.ui.footer_frame.setMaximumHeight(0)
            self.ui.btn_Unfold.setIcon(QIcon(":/svg/icons/PanelToggle.svg"))

            # 调整窗口高度为100
            self.setFixedHeight(100)
        else:
            # 展开底部区域
            self.ui.footer_frame.setMaximumHeight(16777215)  # QT默认的最大值
            self.ui.btn_Unfold.setIcon(QIcon(":/svg/icons/PanelToggle.svg"))

            # 恢复窗口高度
            self.setFixedHeight(self.original_height)

    def show_main_menu(self):
        """显示主菜单"""
        menu = QMenu(self)

        # 源菜单项
        source_action = QAction("源", self)
        source_action.triggered.connect(self.select_source_path)
        menu.addAction(source_action)

        # 导入菜单项
        import_action = QAction("导入", self)
        import_action.triggered.connect(self.import_config)
        menu.addAction(import_action)

        # 导出菜单项
        export_action = QAction("导出", self)
        export_action.triggered.connect(self.export_config)
        menu.addAction(export_action)

        # 在按钮下方显示菜单
        menu.exec(self.ui.btn_Menu.mapToGlobal(self.ui.btn_Menu.rect().bottomLeft()))

    def show_recent_groups_menu(self):
        """显示最近使用的分组菜单"""
        # 获取最近使用的分组（最多3个）
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT DISTINCT group_name FROM history ORDER BY timestamp DESC LIMIT 3")
        recent_groups = cursor.fetchall()

        if not recent_groups:
            QMessageBox.information(self, "历史记录", "没有最近使用的分组")
            return

        menu = QMenu("最近使用的分组", self)

        # 添加每个分组到菜单
        for group in recent_groups:
            group_name = group[0]
            action = QAction(group_name, self)
            action.triggered.connect(lambda checked, name=group_name: self.select_group_by_name(name))
            menu.addAction(action)

        # 在按钮下方显示菜单
        menu.exec(self.ui.btn_History_Path.mapToGlobal(self.ui.btn_History_Path.rect().bottomLeft()))

    def select_group_by_name(self, group_name):
        """通过名称选择分组"""
        # 在文件夹列表下拉框中选择
        index = self.ui.cbox_GroupName01.findText(group_name)
        if index >= 0:
            self.ui.cbox_GroupName01.setCurrentIndex(index)

        # 在脚本生成下拉框中选择
        index = self.ui.cbox_GroupName01.findText(group_name)
        if index >= 0:
            self.ui.cbox_GroupName01.setCurrentIndex(index)

        # 记录使用历史
        self.record_group_usage(group_name)

    def select_source_path(self):
        """选择源文件夹路径"""
        path = QFileDialog.getExistingDirectory(self, "选择源文件夹", QDir.homePath())
        if path:
            self.source_path = path
            self.ui.lbl_SourcePath.setText(path)
            self.load_folders_from_path(path)

    def select_target_path(self):
        """选择目标文件夹路径"""
        path = QFileDialog.getExistingDirectory(self, "选择目标文件夹", QDir.homePath())
        if path:
            self.target_path = path
            self.ui.lbl_TargetPath.setText(path)

    def load_folders_from_path(self, path):
        """从指定路径递归加载所有子文件夹名称"""
        if not os.path.exists(path):
            QMessageBox.warning(self, "路径错误", "指定的路径不存在！")
            return

        self.source_path = path
        self.ui.lbl_SourcePath.setText(path)

        # 重置UI状态
        self.ui.table_FolderName.setRowCount(0)
        self.ui.prg_Source.setValue(0)
        self.ui.prg_Source.setMaximum(0)
        self.ui.lbl_SourceFolderNum.setText("0/0")

        # 计算文件夹总数
        folder_count = 0
        for root, dirs, files in os.walk(path):
            folder_count += len(dirs)

        self.ui.prg_Source.setMaximum(folder_count)
        self.ui.prg_Source.setValue(0)
        self.ui.lbl_SourceFolderNum.setText(f"0/{folder_count}")

        # 递归遍历所有子文件夹
        current_count = 0
        for root, dirs, files in os.walk(path):
            for dir_name in dirs:
                folder_path = os.path.join(root, dir_name)

                # 关键修正：计算相对于源路径的完整路径
                rel_path = os.path.relpath(folder_path, path)

                row = self.ui.table_FolderName.rowCount()
                self.ui.table_FolderName.insertRow(row)
                self.ui.table_FolderName.setItem(row, 0, QTableWidgetItem(dir_name))
                self.ui.table_FolderName.setItem(row, 1, QTableWidgetItem(rel_path))

                current_count += 1
                self.ui.prg_Source.setValue(current_count)
                self.ui.lbl_SourceFolderNum.setText(f"{current_count}/{folder_count}")
                QApplication.processEvents()

    def load_folders_single_threaded(self, path):
        """单线程加载文件夹"""
        self.ui.table_FolderName.setRowCount(0)

        # 计算文件夹总数
        folder_count = 0
        for root, dirs, files in os.walk(path):
            folder_count += len(dirs)

        self.ui.prg_Source.setMaximum(folder_count)
        self.ui.prg_Source.setValue(0)
        self.ui.lbl_SourceFolderNum.setText(f"0/{folder_count}")

        # 递归遍历所有子文件夹
        current_count = 0
        for root, dirs, files in os.walk(path):
            for dir_name in dirs:
                folder_path = os.path.join(root, dir_name)
                rel_path = os.path.relpath(folder_path, path)

                row = self.ui.table_FolderName.rowCount()
                self.ui.table_FolderName.insertRow(row)
                self.ui.table_FolderName.setItem(row, 0, QTableWidgetItem(dir_name))
                self.ui.table_FolderName.setItem(row, 1, QTableWidgetItem(rel_path))

                current_count += 1
                self.ui.prg_Source.setValue(current_count)
                self.ui.lbl_SourceFolderNum.setText(f"{current_count}/{folder_count}")
                QApplication.processEvents()

    def create_folders_single_threaded(self, folders_to_create):
        """单线程创建文件夹"""
        total = len(folders_to_create)
        self.ui.prg_Target.setMaximum(total)
        self.ui.prg_Target.setValue(0)

        success_count = 0
        fail_count = 0

        for i, rel_path in enumerate(folders_to_create):
            # 直接使用相对路径创建完整路径
            full_path = os.path.join(self.target_path, rel_path)

            try:
                os.makedirs(full_path, exist_ok=True)
                success_count += 1
            except Exception as e:
                fail_count += 1
                print(f"创建文件夹失败: {full_path} - {str(e)}")

            self.ui.prg_Target.setValue(i + 1)
            self.ui.lbl_TargetFolderNum.setText(f"{i + 1}/{total}")
            QApplication.processEvents()

        result_msg = f"文件夹创建完成！\n成功: {success_count}, 失败: {fail_count}"
        QMessageBox.information(self, "完成", result_msg)

        group_name = self.ui.cbox_GroupName02.currentText()
        if group_name:
            self.record_group_usage(group_name)

        completion_behavior = self.ui.cbox_Finish.currentIndex()
        if completion_behavior == 0:
            self.close()

    def load_folders_threaded(self, path):
        """使用多线程加载文件夹"""
        # 创建并启动工作线程
        self.current_worker = FolderWorker(path, 'load')
        thread = threading.Thread(target=self.current_worker.run)

        # 连接信号
        self.current_worker.progress_updated.connect(self.update_folder_progress)
        self.current_worker.finished.connect(self.on_folder_loading_complete)
        self.current_worker.error_occurred.connect(self.on_folder_error)

        thread.start()

    def update_folder_progress(self, current, total):
        """更新文件夹加载进度"""
        self.ui.prg_Source.setMaximum(total)
        self.ui.prg_Source.setValue(current)
        self.ui.lbl_SourceFolderNum.setText(f"{current}/{total}")
        QApplication.processEvents()

    def on_folder_loading_complete(self):
        """文件夹加载完成时的处理"""
        # 清理工作线程引用
        self.current_worker = None
        QMessageBox.information(self, "完成", "文件夹加载完成！")

    def on_folder_error(self, error_msg):
        """处理文件夹操作中的错误"""
        QMessageBox.critical(self, "错误", error_msg)
        # 清理工作线程引用
        self.current_worker = None

    def create_folders(self):
        """创建选中的文件夹"""
        if not self.target_path:
            QMessageBox.warning(self, "目标路径错误", "请先选择目标路径！")
            return

        # 获取要创建的文件夹列表
        folders_to_create = []
        for row in range(self.ui.table_FolderName.rowCount()):
            if self.ui.table_FolderName.isRowHidden(row):
                continue

            path_item = self.ui.table_FolderName.item(row, 1)

            if path_item:
                # 直接使用相对路径
                folders_to_create.append(path_item.text())

        if not folders_to_create:
            QMessageBox.warning(self, "无数据", "没有要创建的文件夹！")
            return

        # 根据设置选择单线程或多线程模式
        if self.multithread_enabled:
            self.create_folders_threaded(folders_to_create)
        else:
            self.create_folders_single_threaded(folders_to_create)

    def create_folders_threaded(self, folders_to_create):
        """使用多线程创建文件夹"""
        # 创建并启动工作线程
        self.current_worker = FolderWorker(self.target_path, 'create')
        self.current_worker.folders_to_create = folders_to_create
        thread = threading.Thread(target=self.current_worker.run)

        # 连接信号
        self.current_worker.progress_updated.connect(self.update_creation_progress)
        self.current_worker.finished.connect(self.on_folder_creation_complete)
        self.current_worker.error_occurred.connect(self.on_folder_error)

        thread.start()

    def update_creation_progress(self, current, total):
        """更新文件夹创建进度"""
        self.ui.prg_Target.setMaximum(total)
        self.ui.prg_Target.setValue(current)
        self.ui.lbl_TargetFolderNum.setText(f"{current}/{total}")
        QApplication.processEvents()

    def on_folder_creation_complete(self):
        """文件夹创建完成时的处理"""
        # 清理工作线程引用
        self.current_worker = None
        group_name = self.ui.cbox_GroupName02.currentText()
        if group_name:
            self.record_group_usage(group_name)

        # 检查完成后的行为设置
        completion_behavior = self.ui.cbox_Finish.currentIndex()
        if completion_behavior == 0:  # 完成后关闭应用
            self.close()
        else:
            QMessageBox.information(self, "完成", "文件夹创建完成！")

    def save_group(self):
        """保存当前配置组"""
        # 使用 edit_GroupName 的文本作为分组名称
        group_name = self.ui.edit_GroupName.text().strip()
        if not group_name:
            QMessageBox.warning(self, "输入错误", "请输入配置组名称！")
            return

        cursor = self.db_connection.cursor()

        # 检查组名是否已存在
        cursor.execute("SELECT id FROM groups WHERE name = ?", (group_name,))
        existing_group = cursor.fetchone()

        if existing_group:
            # 更新现有组
            group_id = existing_group[0]
            # 删除旧文件夹
            cursor.execute("DELETE FROM folders WHERE group_id = ?", (group_id,))
        else:
            # 创建新组
            cursor.execute("INSERT INTO groups (name) VALUES (?)", (group_name,))
            group_id = cursor.lastrowid

        # 添加新文件夹 - 关键修正：只存储相对路径
        for row in range(self.ui.table_FolderName.rowCount()):
            path_item = self.ui.table_FolderName.item(row, 1)

            if path_item:
                # 只存储相对路径
                rel_path = path_item.text()
                cursor.execute("INSERT INTO folders (group_id, folder_name) VALUES (?, ?)",
                               (group_id, f"|{rel_path}"))

        self.db_connection.commit()
        self.load_groups()
        self.ui.edit_GroupName.clear()

        # 更新下拉框选中新保存的组
        index = self.ui.cbox_GroupName02.findText(group_name)
        if index >= 0:
            self.ui.cbox_GroupName02.setCurrentIndex(index)
        else:
            self.ui.cbox_GroupName02.addItem(group_name)
            self.ui.cbox_GroupName02.setCurrentText(group_name)

        # 记录使用历史
        self.record_group_usage(group_name)

        QMessageBox.information(self, "成功", "配置已保存！")

    def load_selected_group(self):
        """加载选中的配置组"""
        group_name = self.ui.cbox_GroupName02.currentText()
        # 处理空白项
        if not group_name:
            self.ui.table_FolderName.setRowCount(0)
            self.ui.lbl_SourceFolderNum.setText("0/0")
            self.ui.prg_Source.setValue(0)
            return

        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM groups WHERE name = ?", (group_name,))
        result = cursor.fetchone()
        if not result:
            return

        group_id = result[0]

        cursor.execute("SELECT folder_name FROM folders WHERE group_id = ? ORDER BY id", (group_id,))
        folders = cursor.fetchall()

        self.ui.table_FolderName.setRowCount(0)
        for folder in folders:
            # 分割文件夹名称和相对路径
            folder_data = folder[0].split("|")
            if len(folder_data) >= 2:
                rel_path = folder_data[1]
                # 从路径中提取文件夹名称
                folder_name = os.path.basename(rel_path)

                row = self.ui.table_FolderName.rowCount()
                self.ui.table_FolderName.insertRow(row)
                self.ui.table_FolderName.setItem(row, 0, QTableWidgetItem(folder_name))
                self.ui.table_FolderName.setItem(row, 1, QTableWidgetItem(rel_path))

        self.ui.prg_Source.setValue(0)

        # 记录使用历史
        self.record_group_usage(group_name)

    def load_selected_group_for_script(self):
        """为脚本标签页加载选中的配置组"""
        group_name = self.ui.cbox_GroupName01.currentText()
        # 处理空白项
        if not group_name:
            self.ui.table_FolderName.setRowCount(0)
            self.ui.lbl_SourceFolderNum.setText("0/0")
            self.ui.prg_Source.setValue(0)
            return

        # # 更新分组名称到编辑框
        # self.ui.edit_GroupName.setText(group_name)

        # 加载分组数据
        self.load_selected_group()

    def delete_group(self):
        """删除选中的配置组"""
        group_name = self.ui.cbox_GroupName02.currentText()
        if not group_name:
            return

        reply = QMessageBox.question(
            self, "确认删除",
            f"确定要删除配置组 '{group_name}' 吗？此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM groups WHERE name = ?", (group_name,))
            cursor.execute("DELETE FROM history WHERE group_name = ?", (group_name,))
            self.db_connection.commit()
            self.load_groups()  # 重新加载组，此时下拉框将为空
            self.ui.table_FolderName.setRowCount(0)
            self.ui.lbl_SourceFolderNum.setText("0/0")
            self.ui.prg_Source.setValue(0)
            self.load_recent_groups()

    def create_folders(self):
        """创建选中的文件夹"""
        if not self.target_path:
            QMessageBox.warning(self, "目标路径错误", "请先选择目标路径！")
            return

        # 获取要创建的文件夹列表
        folders_to_create = []
        for row in range(self.ui.table_FolderName.rowCount()):
            if self.ui.table_FolderName.isRowHidden(row):
                continue

            name_item = self.ui.table_FolderName.item(row, 0)
            path_item = self.ui.table_FolderName.item(row, 1)

            if name_item and path_item:
                # 修正：不再添加额外的文件夹名称
                folders_to_create.append(path_item.text())

        if not folders_to_create:
            QMessageBox.warning(self, "无数据", "没有要创建的文件夹！")
            return

        # 根据设置选择单线程或多线程模式
        if self.multithread_enabled:
            self.create_folders_threaded(folders_to_create)
        else:
            self.create_folders_single_threaded(folders_to_create)

    def create_filtered_folders(self):
        """创建过滤后的文件夹（多选）"""
        if not self.target_path:
            QMessageBox.warning(self, "目标路径错误", "请先选择目标路径！")
            return

        # 获取选中的行
        selected_rows = set()
        for index in self.ui.table_FolderName.selectedIndexes():
            row = index.row()
            # 只添加未隐藏的行
            if not self.ui.table_FolderName.isRowHidden(row):
                selected_rows.add(row)

        # 如果没有选中行，则使用所有未隐藏的行
        if not selected_rows:
            for row in range(self.ui.table_FolderName.rowCount()):
                if not self.ui.table_FolderName.isRowHidden(row):
                    selected_rows.add(row)

        # 获取相对路径
        folders_to_create = []
        for row in sorted(selected_rows):
            path_item = self.ui.table_FolderName.item(row, 1)
            if path_item:
                folders_to_create.append(path_item.text())

        total = len(folders_to_create)
        if total == 0:
            QMessageBox.warning(self, "无数据", "没有要创建的文件夹！")
            return

        self.ui.prg_Target.setMaximum(total)
        self.ui.prg_Target.setValue(0)

        success_count = 0
        fail_count = 0
        current_count = 0

        for rel_path in folders_to_create:
            # 直接使用相对路径创建完整路径
            full_path = os.path.join(self.target_path, rel_path)

            try:
                os.makedirs(full_path, exist_ok=True)
                success_count += 1
            except Exception as e:
                fail_count += 1
                print(f"创建文件夹失败: {full_path} - {str(e)}")

            # 更新进度
            current_count += 1
            self.ui.prg_Target.setValue(current_count)
            self.ui.lbl_TargetFolderNum.setText(f"{current_count}/{total}")
            QApplication.processEvents()  # 更新UI

        result_msg = f"已创建 {len(folders_to_create)} 个文件夹！\n成功: {success_count}, 失败: {fail_count}"
        QMessageBox.information(self, "完成", result_msg)

        # 记录使用历史
        group_name = self.ui.cbox_GroupName01.currentText()
        if group_name:
            self.record_group_usage(group_name)

        # 检查完成后的行为设置
        completion_behavior = self.ui.cbox_Finish.currentIndex()
        if completion_behavior == 0:  # 完成后关闭应用
            self.close()

    def show_filters_dialog(self):
        """显示过滤器对话框（简化版）"""
        QMessageBox.information(self, "过滤器", "过滤器功能待实现")

    def generate_batch_script(self):
        """生成批处理脚本（仅显示，不保存）"""
        group_name = self.ui.cbox_GroupName01.currentText()
        if not group_name:
            QMessageBox.warning(self, "错误", "请先选择一个分组！")
            return

        # 获取分组数据
        folders = self.get_group_folders(group_name)
        if not folders:
            QMessageBox.warning(self, "错误", "该分组没有文件夹数据！")
            return

        # 生成批处理脚本内容
        script = "@echo off\n"
        script += "REM 批量创建文件夹脚本\n"
        script += "REM 分组: " + group_name + "\n\n"
        script += "REM 使用方法: 将此脚本放在目标目录下运行\n\n"

        # 直接使用相对路径
        for rel_path in folders:
            # 确保路径使用正确的分隔符
            path_for_script = rel_path.replace("/", "\\")
            script += f'mkdir "{path_for_script}"\n'

        script += "\necho 文件夹创建完成！\npause\n"

        # 显示在文本框中
        self.ui.tabWidget.setCurrentWidget(self.ui.tab_Script)
        self.ui.plainTextEdit.setPlainText(script)

        # 记录使用历史
        self.record_group_usage(group_name)

    def generate_powershell_script(self):
        """生成PowerShell脚本（仅显示，不保存）"""
        group_name = self.ui.cbox_GroupName01.currentText()
        if not group_name:
            QMessageBox.warning(self, "错误", "请先选择一个分组！")
            return

        # 获取分组数据
        folders = self.get_group_folders(group_name)
        if not folders:
            QMessageBox.warning(self, "错误", "该分组没有文件夹数据！")
            return

        # 生成PowerShell脚本内容
        script = "# PowerShell 文件夹创建脚本\n"
        script += "# 分组: " + group_name + "\n"
        script += "# 使用方法: 在PowerShell中运行此脚本\n\n"

        # 直接使用相对路径
        for rel_path in folders:
            # 确保路径使用正确的分隔符
            path_for_script = rel_path.replace("\\", "/")
            script += f'New-Item -Path "{path_for_script}" -ItemType Directory -Force\n'

        script += "\nWrite-Host \"文件夹创建完成！\" -ForegroundColor Green\n"
        script += "Read-Host \"按Enter键退出\"\n"

        # 显示在文本框中
        self.ui.tabWidget.setCurrentWidget(self.ui.tab_Script)
        self.ui.plainTextEdit.setPlainText(script)

        # 记录使用历史
        self.record_group_usage(group_name)

    def save_generated_script(self):
        """保存生成的脚本到文件"""
        # 获取当前脚本内容
        script = self.ui.plainTextEdit.toPlainText()
        if not script.strip():
            QMessageBox.warning(self, "空脚本", "脚本内容为空！")
            return

        # 获取默认文件名
        default_name = "folder_script"

        # 尝试获取当前分组名称
        group_name = self.ui.cbox_GroupName01.currentText()
        if group_name:
            default_name = group_name.replace(" ", "_")

        # 获取文件扩展名
        if "New-Item" in script:
            extension = "ps1"
        else:
            extension = "bat"

        # 获取保存路径
        path, _ = QFileDialog.getSaveFileName(
            self, "保存脚本文件",
            os.path.join(QDir.homePath(), f"{default_name}.{extension}"),
            f"Script Files (*.{extension})"
        )

        if not path:
            return

        try:
            with open(path, "w", encoding="ANSI") as f:
                f.write(script)

            QMessageBox.information(self, "成功", f"脚本已保存到:\n{path}")

            # 如果保存的是脚本，记录使用历史
            if group_name:
                self.record_group_usage(group_name)
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存脚本失败:\n{str(e)}")

    def get_group_folders(self, group_name):
        """获取分组中的文件夹数据（返回相对路径列表）"""
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT id FROM groups WHERE name = ?", (group_name,))
        result = cursor.fetchone()
        if not result:
            return []

        group_id = result[0]
        cursor.execute("SELECT folder_name FROM folders WHERE group_id = ?", (group_id,))
        folders = cursor.fetchall()

        result = []
        for folder in folders:
            # 分割文件夹名称和相对路径
            folder_data = folder[0].split("|")
            if len(folder_data) >= 2:
                # 直接使用相对路径
                result.append(folder_data[1])
            else:
                # 处理旧数据格式
                result.append(folder_data[0])

        return result

    def import_config(self):
        """导入配置文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "导入配置文件", QDir.homePath(), "文本文件 (*.txt)"
        )

        if not file_path:
            return

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                folders = [line.strip().split("|") for line in f if line.strip()]

            self.ui.table_FolderName.setRowCount(0)
            for folder_data in folders:
                folder_name = folder_data[0]
                rel_path = folder_data[1] if len(folder_data) > 1 else ""

                row = self.ui.table_FolderName.rowCount()
                self.ui.table_FolderName.insertRow(row)
                self.ui.table_FolderName.setItem(row, 0, QTableWidgetItem(folder_name))
                self.ui.table_FolderName.setItem(row, 1, QTableWidgetItem(rel_path))

            self.ui.lbl_SourceFolderNum.setText(f"0/{len(folders)}")
            self.ui.prg_Source.setMaximum(len(folders))
            self.ui.prg_Source.setValue(0)

            QMessageBox.information(self, "导入成功", f"已导入 {len(folders)} 个文件夹")
        except Exception as e:
            QMessageBox.critical(self, "导入错误", f"导入文件失败: {str(e)}")

    def export_config(self):
        """导出配置文件"""
        if self.ui.table_FolderName.rowCount() == 0:
            QMessageBox.warning(self, "无数据", "没有可导出的数据！")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "导出配置文件", QDir.homePath(), "文本文件 (*.txt)"
        )

        if not file_path:
            return

        try:
            folders = []
            for row in range(self.ui.table_FolderName.rowCount()):
                name_item = self.ui.table_FolderName.item(row, 0)
                path_item = self.ui.table_FolderName.item(row, 1)

                if name_item and path_item:
                    folder_name = name_item.text()
                    rel_path = path_item.text()
                    folders.append(f"{folder_name}|{rel_path}")

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(folders))

            QMessageBox.information(self, "导出成功", "配置文件已成功导出！")
        except Exception as e:
            QMessageBox.critical(self, "导出错误", f"导出文件失败: {str(e)}")

    def show_settings(self):
        """显示设置菜单"""
        menu = QMenu(self)

        # 添加多线程选项
        multithread_action = QAction("开启多线程", self)
        multithread_action.setCheckable(True)
        multithread_action.setChecked(self.multithread_enabled)
        menu.addAction(multithread_action)

        # 添加不保存历史记录选项
        no_history_action = QAction("不保存历史记录", self)
        no_history_action.setCheckable(True)
        no_history_action.setChecked(self.settings.value("no_history", False, type=bool))
        menu.addAction(no_history_action)

        # 添加上下文菜单集成选项
        context_menu_action = QAction("集成到右键菜单", self)
        context_menu_action.setCheckable(True)
        context_menu_action.setChecked(self.settings.value("context_menu", False, type=bool))
        menu.addAction(context_menu_action)

        # 添加分隔线
        menu.addSeparator()

        # 添加应用设置按钮
        apply_action = QAction("应用设置", self)
        apply_action.triggered.connect(lambda: self.apply_settings(
            multithread_action.isChecked(),
            no_history_action.isChecked(),
            context_menu_action.isChecked()
        ))
        menu.addAction(apply_action)

        # 在设置按钮下方显示菜单
        menu.exec(self.ui.btn_Settings.mapToGlobal(self.ui.btn_Settings.rect().bottomLeft()))

    def apply_settings(self, multithread_enabled, no_history, integrate_context_menu):
        """应用用户设置"""
        # 保存多线程设置
        self.multithread_enabled = multithread_enabled
        self.settings.setValue("multithread_enabled", multithread_enabled)

        # 保存历史记录设置
        self.settings.setValue("no_history", no_history)

        # 处理上下文菜单集成
        self.settings.setValue("context_menu", integrate_context_menu)
        if integrate_context_menu:
            self.integrate_to_context_menu()
        else:
            self.remove_from_context_menu()

        QMessageBox.information(self, "设置已应用", "新设置将在下次操作中生效")

    def integrate_to_context_menu(self):
        """将应用集成到系统右键菜单"""
        try:
            # 在实际应用中，这里会修改注册表添加右键菜单项
            # 以下代码仅为示例，实际实现需要根据操作系统进行适配

            # Windows注册表操作示例（需要管理员权限）
            # import winreg
            # key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, r"Directory\\Background\\shell\\QuickFold")
            # winreg.SetValue(key, "", winreg.REG_SZ, "使用QuickFold创建文件夹")
            # command_key = winreg.CreateKey(key, "command")
            # winreg.SetValue(command_key, "", winreg.REG_SZ, f'"{sys.executable}" "{os.path.abspath(__file__)}" "%V"')

            QMessageBox.information(self, "集成成功", "应用已添加到系统右键菜单")
        except Exception as e:
            QMessageBox.critical(self, "集成失败", f"添加到右键菜单失败:\n{str(e)}")

    def remove_from_context_menu(self):
        """从系统右键菜单移除应用"""
        try:
            # 在实际应用中，这里会删除注册表中的相关项

            # Windows注册表操作示例（需要管理员权限）
            # import winreg
            # winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\\Background\\shell\\QuickFold\\command")
            # winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, r"Directory\\Background\\shell\\QuickFold")

            QMessageBox.information(self, "移除成功", "应用已从系统右键菜单移除")
        except Exception as e:
            QMessageBox.warning(self, "移除失败", f"从右键菜单移除失败:\n{str(e)}")

    def clear_history(self):
        """清除所有历史记录"""
        reply = QMessageBox.question(
            self, "确认清除",
            "确定要清除所有历史记录吗？此操作不可恢复！",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            cursor = self.db_connection.cursor()
            cursor.execute("DELETE FROM history")
            self.db_connection.commit()
            self.load_recent_groups()  # 刷新历史记录表格
            QMessageBox.information(self, "成功", "历史记录已清除！")

    def show_about(self):
        """显示关于对话框"""
        QMessageBox.about(self, "关于",
                          "QuickFold\n"
                          "Version: 1.0\n"
                          "Author: BrassBook"
                          )

    def show_context_menu(self, position):
        """显示表格的右键菜单"""
        selected_rows = set(index.row() for index in self.ui.table_FolderName.selectedIndexes())
        if not selected_rows:
            return

        menu = QMenu(self)
        delete_action = QAction("删除选中项", self)
        delete_action.triggered.connect(lambda: self.delete_selected_items(selected_rows))
        menu.addAction(delete_action)
        menu.exec(self.ui.table_FolderName.viewport().mapToGlobal(position))

    def delete_selected_items(self, rows):
        """删除选中的表格项"""
        # 从后往前删除，避免索引变化
        for row in sorted(rows, reverse=True):
            self.ui.table_FolderName.removeRow(row)

        # 更新计数
        total = self.ui.table_FolderName.rowCount()
        self.ui.lbl_SourceFolderNum.setText(f"0/{total}")
        self.ui.prg_Source.setMaximum(total)
        self.ui.prg_Source.setValue(0)

    def closeEvent(self, event):
        """关闭应用时关闭数据库连接"""
        self.db_connection.close()
        event.accept()


# 多线程线程
class FolderWorker(QObject):
    progress_updated = Signal(int, int)  # current, total
    finished = Signal()
    error_occurred = Signal(str)

    def __init__(self, path, operation):
        super().__init__()
        self.path = path
        self.operation = operation  # 'load' or 'create'
        self.stop_requested = False

    def run(self):
        try:
            if self.operation == 'load':
                self.load_folders()
            elif self.operation == 'create':
                self.create_folders()
            self.finished.emit()
        except Exception as e:
            self.error_occurred.emit(str(e))

    def load_folders(self):
        """线程安全的加载文件夹方法"""
        if not os.path.exists(self.path):
            self.error_occurred.emit("指定的路径不存在！")
            return

        # 计算文件夹总数
        folder_count = 0
        for root, dirs, files in os.walk(self.path):
            folder_count += len(dirs)

        self.progress_updated.emit(0, folder_count)

        # 递归遍历所有子文件夹
        current_count = 0
        for root, dirs, files in os.walk(self.path):
            if self.stop_requested:
                return

            for dir_name in dirs:
                folder_path = os.path.join(root, dir_name)
                rel_path = os.path.relpath(folder_path, self.path)

                # 使用信号发送数据到主线程更新UI
                self.progress_updated.emit(current_count, folder_count)

                current_count += 1

        # 完成时发送最终状态
        self.progress_updated.emit(folder_count, folder_count)

    def create_folders(self):
        """线程安全的创建文件夹方法"""
        # 这里需要根据您的实际数据结构实现
        # 示例代码，具体实现需要根据您的数据结构调整
        total = len(self.folders_to_create)
        for i, (folder_name, rel_path) in enumerate(self.folders_to_create):
            if self.stop_requested:
                return

            full_path = os.path.join(self.path, rel_path, folder_name)
            try:
                os.makedirs(full_path, exist_ok=True)
                self.progress_updated.emit(i + 1, total)
            except Exception as e:
                self.error_occurred.emit(f"创建文件夹失败: {full_path} - {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FolderManagerApp()
    # 设置Fusion样式
    app.setStyle("windows11")
    window.show()
    sys.exit(app.exec())



