# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindowsYzbWPQ.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QGroupBox, QHBoxLayout, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPlainTextEdit, QProgressBar,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget)
import icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(638, 435)
        font = QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/svg/icons/img.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.header_frame = QFrame(self.centralwidget)
        self.header_frame.setObjectName(u"header_frame")
        self.header_frame.setFont(font)
        self.header_frame.setStyleSheet(u"")
        self.header_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.header_frame.setFrameShadow(QFrame.Shadow.Plain)
        self.horizontalLayout = QHBoxLayout(self.header_frame)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, -1, 0)
        self.header_left_frame = QFrame(self.header_frame)
        self.header_left_frame.setObjectName(u"header_left_frame")
        self.header_left_frame.setFont(font)
        self.header_left_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.header_left_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.header_left_frame)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.btn_Unfold = QPushButton(self.header_left_frame)
        self.btn_Unfold.setObjectName(u"btn_Unfold")
        self.btn_Unfold.setFont(font)
        self.btn_Unfold.setStyleSheet(u"*{border:None}")
        icon1 = QIcon()
        icon1.addFile(u":/svg/icons/PanelToggle.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Unfold.setIcon(icon1)
        self.btn_Unfold.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.btn_Unfold, 0, Qt.AlignmentFlag.AlignLeft)

        self.btn_Run = QPushButton(self.header_left_frame)
        self.btn_Run.setObjectName(u"btn_Run")
        self.btn_Run.setStyleSheet(u"*{border:None}")
        icon2 = QIcon()
        icon2.addFile(u":/svg/icons/play.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Run.setIcon(icon2)

        self.horizontalLayout_2.addWidget(self.btn_Run)

        self.btn_History_Path = QPushButton(self.header_left_frame)
        self.btn_History_Path.setObjectName(u"btn_History_Path")
        self.btn_History_Path.setStyleSheet(u"*{border:None}")
        icon3 = QIcon()
        icon3.addFile(u":/svg/icons/PanelHistory.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_History_Path.setIcon(icon3)
        self.btn_History_Path.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.btn_History_Path)

        self.btn_GenScript = QPushButton(self.header_left_frame)
        self.btn_GenScript.setObjectName(u"btn_GenScript")
        self.btn_GenScript.setFont(font)
        self.btn_GenScript.setStyleSheet(u"*{border:None}")
        icon4 = QIcon()
        icon4.addFile(u":/svg/icons/MailRenderingMethod.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_GenScript.setIcon(icon4)
        self.btn_GenScript.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.btn_GenScript)

        self.btn_Settings = QPushButton(self.header_left_frame)
        self.btn_Settings.setObjectName(u"btn_Settings")
        self.btn_Settings.setFont(font)
        self.btn_Settings.setStyleSheet(u"*{border:None}")
        icon5 = QIcon()
        icon5.addFile(u":/svg/icons/Settings.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Settings.setIcon(icon5)
        self.btn_Settings.setIconSize(QSize(30, 30))

        self.horizontalLayout_2.addWidget(self.btn_Settings)

        self.btn_About = QPushButton(self.header_left_frame)
        self.btn_About.setObjectName(u"btn_About")
        self.btn_About.setFont(font)
        self.btn_About.setStyleSheet(u"*{border:None}")
        icon6 = QIcon()
        icon6.addFile(u":/svg/icons/question.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_About.setIcon(icon6)
        self.btn_About.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.btn_About)


        self.horizontalLayout.addWidget(self.header_left_frame, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.header_right_frame = QFrame(self.header_frame)
        self.header_right_frame.setObjectName(u"header_right_frame")
        self.header_right_frame.setFont(font)
        self.header_right_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.header_right_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.header_right_frame)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_Top = QPushButton(self.header_right_frame)
        self.btn_Top.setObjectName(u"btn_Top")
        self.btn_Top.setStyleSheet(u"*{border:None\n"
"}")
        icon7 = QIcon()
        icon7.addFile(u":/svg/icons/pushpin.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Top.setIcon(icon7)
        self.btn_Top.setIconSize(QSize(20, 20))

        self.horizontalLayout_5.addWidget(self.btn_Top)

        self.cbox_Finish = QComboBox(self.header_right_frame)
        self.cbox_Finish.addItem("")
        self.cbox_Finish.addItem("")
        self.cbox_Finish.setObjectName(u"cbox_Finish")
        self.cbox_Finish.setMinimumSize(QSize(155, 0))
        self.cbox_Finish.setFont(font)
        self.cbox_Finish.setStyleSheet(u"QComboBox::drop-down { border: none; }\n"
"QComboBox { border: none; }")

        self.horizontalLayout_5.addWidget(self.cbox_Finish)


        self.horizontalLayout.addWidget(self.header_right_frame, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout.addWidget(self.header_frame, 0, Qt.AlignmentFlag.AlignTop)

        self.main_body_frame = QFrame(self.centralwidget)
        self.main_body_frame.setObjectName(u"main_body_frame")
        self.main_body_frame.setStyleSheet(u"background-color: rgb(243, 243, 243);")
        self.main_body_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.main_body_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_3 = QGridLayout(self.main_body_frame)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setVerticalSpacing(2)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame_8 = QFrame(self.main_body_frame)
        self.frame_8.setObjectName(u"frame_8")
        font1 = QFont()
        font1.setPointSize(9)
        self.frame_8.setFont(font1)
        self.frame_8.setStyleSheet(u"")
        self.frame_8.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_8.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_4 = QGridLayout(self.frame_8)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.lbl_TargetFolderNum = QLabel(self.frame_8)
        self.lbl_TargetFolderNum.setObjectName(u"lbl_TargetFolderNum")
        self.lbl_TargetFolderNum.setFont(font)

        self.gridLayout_4.addWidget(self.lbl_TargetFolderNum, 2, 4, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.lbl_SourceFolderNum = QLabel(self.frame_8)
        self.lbl_SourceFolderNum.setObjectName(u"lbl_SourceFolderNum")
        self.lbl_SourceFolderNum.setFont(font)

        self.gridLayout_4.addWidget(self.lbl_SourceFolderNum, 1, 4, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.lbl_TargetPath = QLabel(self.frame_8)
        self.lbl_TargetPath.setObjectName(u"lbl_TargetPath")
        self.lbl_TargetPath.setFont(font1)

        self.gridLayout_4.addWidget(self.lbl_TargetPath, 2, 1, 1, 2)

        self.btn_Source = QPushButton(self.frame_8)
        self.btn_Source.setObjectName(u"btn_Source")
        self.btn_Source.setFont(font)
        self.btn_Source.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_4.addWidget(self.btn_Source, 1, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.btn_Filters = QPushButton(self.frame_8)
        self.btn_Filters.setObjectName(u"btn_Filters")
        self.btn_Filters.setFont(font)
        self.btn_Filters.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_4.addWidget(self.btn_Filters, 0, 0, 1, 1)

        self.cbox_GroupName01 = QComboBox(self.frame_8)
        self.cbox_GroupName01.setObjectName(u"cbox_GroupName01")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbox_GroupName01.sizePolicy().hasHeightForWidth())
        self.cbox_GroupName01.setSizePolicy(sizePolicy)
        self.cbox_GroupName01.setMinimumSize(QSize(240, 0))
        self.cbox_GroupName01.setFont(font)
        self.cbox_GroupName01.setStyleSheet(u"background-color: rgb(250, 250, 250);")

        self.gridLayout_4.addWidget(self.cbox_GroupName01, 0, 1, 1, 2)

        self.prg_Source = QProgressBar(self.frame_8)
        self.prg_Source.setObjectName(u"prg_Source")
        self.prg_Source.setFont(font)
        self.prg_Source.setValue(0)

        self.gridLayout_4.addWidget(self.prg_Source, 1, 3, 1, 1)

        self.btn_Target = QPushButton(self.frame_8)
        self.btn_Target.setObjectName(u"btn_Target")
        self.btn_Target.setFont(font)
        self.btn_Target.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout_4.addWidget(self.btn_Target, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.prg_Target = QProgressBar(self.frame_8)
        self.prg_Target.setObjectName(u"prg_Target")
        self.prg_Target.setFont(font)
        self.prg_Target.setValue(0)

        self.gridLayout_4.addWidget(self.prg_Target, 2, 3, 1, 1)

        self.lbl_SourcePath = QLabel(self.frame_8)
        self.lbl_SourcePath.setObjectName(u"lbl_SourcePath")
        self.lbl_SourcePath.setFont(font1)

        self.gridLayout_4.addWidget(self.lbl_SourcePath, 1, 1, 1, 2)

        self.horizontalSpacer = QSpacerItem(12, 20, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        self.gridLayout_4.addItem(self.horizontalSpacer, 1, 5, 1, 1)


        self.gridLayout_3.addWidget(self.frame_8, 0, 0, 1, 1)


        self.verticalLayout.addWidget(self.main_body_frame)

        self.footer_frame = QFrame(self.centralwidget)
        self.footer_frame.setObjectName(u"footer_frame")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.footer_frame.sizePolicy().hasHeightForWidth())
        self.footer_frame.setSizePolicy(sizePolicy1)
        self.footer_frame.setFont(font)
        self.footer_frame.setStyleSheet(u"background-color: rgb(243, 243, 243);")
        self.footer_frame.setFrameShape(QFrame.Shape.NoFrame)
        self.footer_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.footer_frame)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.tabWidget = QTabWidget(self.footer_frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setFont(font)
        self.tab_FolderList = QWidget()
        self.tab_FolderList.setObjectName(u"tab_FolderList")
        self.tab_FolderList.setFont(font)
        self.verticalLayout_3 = QVBoxLayout(self.tab_FolderList)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.frame = QFrame(self.tab_FolderList)
        self.frame.setObjectName(u"frame")
        self.frame.setMinimumSize(QSize(300, 0))
        self.frame.setFont(font)
        self.frame.setFrameShape(QFrame.Shape.NoFrame)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.btn_Menu = QPushButton(self.frame)
        self.btn_Menu.setObjectName(u"btn_Menu")
        self.btn_Menu.setFont(font)
        self.btn_Menu.setStyleSheet(u"*{border:None}")
        icon8 = QIcon()
        icon8.addFile(u":/svg/icons/WorkspaceButton.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Menu.setIcon(icon8)
        self.btn_Menu.setIconSize(QSize(30, 30))

        self.horizontalLayout_3.addWidget(self.btn_Menu)

        self.edit_GroupName = QLineEdit(self.frame)
        self.edit_GroupName.setObjectName(u"edit_GroupName")
        self.edit_GroupName.setFont(font)
        self.edit_GroupName.setStyleSheet(u"background-color: rgb(250, 250, 250);")

        self.horizontalLayout_3.addWidget(self.edit_GroupName)

        self.cbox_GroupName02 = QComboBox(self.frame)
        self.cbox_GroupName02.setObjectName(u"cbox_GroupName02")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.cbox_GroupName02.sizePolicy().hasHeightForWidth())
        self.cbox_GroupName02.setSizePolicy(sizePolicy2)
        self.cbox_GroupName02.setMinimumSize(QSize(240, 24))
        self.cbox_GroupName02.setFont(font)
        self.cbox_GroupName02.setStyleSheet(u"background-color: rgb(250, 250, 250);")
        self.cbox_GroupName02.setIconSize(QSize(32, 32))

        self.horizontalLayout_3.addWidget(self.cbox_GroupName02)

        self.btn_Save = QPushButton(self.frame)
        self.btn_Save.setObjectName(u"btn_Save")
        self.btn_Save.setFont(font)
        self.btn_Save.setStyleSheet(u"*{border:None}")
        icon9 = QIcon()
        icon9.addFile(u":/svg/icons/UpdateButton.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Save.setIcon(icon9)
        self.btn_Save.setIconSize(QSize(25, 25))

        self.horizontalLayout_3.addWidget(self.btn_Save)

        self.btn_Del = QPushButton(self.frame)
        self.btn_Del.setObjectName(u"btn_Del")
        self.btn_Del.setFont(font)
        self.btn_Del.setStyleSheet(u"*{border:None}")
        icon10 = QIcon()
        icon10.addFile(u":/svg/icons/MailMsgTrash.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Del.setIcon(icon10)
        self.btn_Del.setIconSize(QSize(30, 30))

        self.horizontalLayout_3.addWidget(self.btn_Del)

        self.edit_Search = QLineEdit(self.frame)
        self.edit_Search.setObjectName(u"edit_Search")
        self.edit_Search.setFont(font)
        self.edit_Search.setStyleSheet(u"background-color: rgb(250, 250, 250);")

        self.horizontalLayout_3.addWidget(self.edit_Search)

        self.btn_Goto = QPushButton(self.frame)
        self.btn_Goto.setObjectName(u"btn_Goto")
        self.btn_Goto.setFont(font)
        self.btn_Goto.setStyleSheet(u"*{border:None}")
        icon11 = QIcon()
        icon11.addFile(u":/svg/icons/MailMsgForward.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_Goto.setIcon(icon11)
        self.btn_Goto.setIconSize(QSize(26, 26))

        self.horizontalLayout_3.addWidget(self.btn_Goto)


        self.verticalLayout_3.addWidget(self.frame, 0, Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)

        self.table_FolderName = QTableWidget(self.tab_FolderList)
        self.table_FolderName.setObjectName(u"table_FolderName")
        self.table_FolderName.setFont(font)
        self.table_FolderName.setStyleSheet(u"/*\u8868\u53f3\u4fa7\u7684\u6ed1\u6761*/\n"
"QScrollBar:vertical{\n"
"background:rgb(250, 250, 250);\n"
"padding:0px;\n"
"border-radius:6px;\n"
"max-width:12px;\n"
"}\n"
"\n"
"/*\u6ed1\u5757*/\n"
"QScrollBar::handle:vertical{\n"
"background:rgb(240, 240, 240);\n"
"\n"
"}")

        self.verticalLayout_3.addWidget(self.table_FolderName)

        self.tabWidget.addTab(self.tab_FolderList, "")
        self.tab_History = QWidget()
        self.tab_History.setObjectName(u"tab_History")
        self.tab_History.setFont(font)
        self.gridLayout = QGridLayout(self.tab_History)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, 0)
        self.groupBox = QGroupBox(self.tab_History)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setFont(font1)
        self.groupBox.setStyleSheet(u"*{\n"
"	border:None;\n"
"}")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.groupBox)
        self.label.setObjectName(u"label")
        font2 = QFont()
        font2.setPointSize(10)
        font2.setBold(True)
        self.label.setFont(font2)

        self.verticalLayout_2.addWidget(self.label)

        self.table_RecentlyUsed = QTableWidget(self.groupBox)
        self.table_RecentlyUsed.setObjectName(u"table_RecentlyUsed")
        self.table_RecentlyUsed.setFont(font)

        self.verticalLayout_2.addWidget(self.table_RecentlyUsed)


        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 2)

        self.btn_Clear = QPushButton(self.tab_History)
        self.btn_Clear.setObjectName(u"btn_Clear")
        self.btn_Clear.setFont(font)
        self.btn_Clear.setStyleSheet(u"background-color: rgb(204, 204, 204);")

        self.gridLayout.addWidget(self.btn_Clear, 0, 1, 1, 1, Qt.AlignmentFlag.AlignRight)

        self.tabWidget.addTab(self.tab_History, "")
        self.tab_Script = QWidget()
        self.tab_Script.setObjectName(u"tab_Script")
        self.tab_Script.setFont(font)
        self.gridLayout_2 = QGridLayout(self.tab_Script)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_2 = QFrame(self.tab_Script)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFont(font)
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.gridLayout_5 = QGridLayout(self.frame_2)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_GenBatchScript = QPushButton(self.frame_2)
        self.btn_GenBatchScript.setObjectName(u"btn_GenBatchScript")
        self.btn_GenBatchScript.setFont(font)
        self.btn_GenBatchScript.setStyleSheet(u"*{border:None\n"
"}")
        icon12 = QIcon()
        icon12.addFile(u":/svg/icons/batch.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_GenBatchScript.setIcon(icon12)
        self.btn_GenBatchScript.setIconSize(QSize(24, 24))

        self.gridLayout_5.addWidget(self.btn_GenBatchScript, 0, 0, 1, 1)

        self.btn_GenPSScript = QPushButton(self.frame_2)
        self.btn_GenPSScript.setObjectName(u"btn_GenPSScript")
        self.btn_GenPSScript.setFont(font)
        self.btn_GenPSScript.setStyleSheet(u"*{border:None\n"
"}")
        icon13 = QIcon()
        icon13.addFile(u":/svg/icons/powershell.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.btn_GenPSScript.setIcon(icon13)
        self.btn_GenPSScript.setIconSize(QSize(24, 24))

        self.gridLayout_5.addWidget(self.btn_GenPSScript, 0, 1, 1, 1)


        self.gridLayout_2.addWidget(self.frame_2, 0, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)

        self.plainTextEdit = QPlainTextEdit(self.tab_Script)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setStyleSheet(u"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"}")

        self.gridLayout_2.addWidget(self.plainTextEdit, 1, 0, 1, 1)

        self.tabWidget.addTab(self.tab_Script, "")

        self.horizontalLayout_7.addWidget(self.tabWidget)


        self.verticalLayout.addWidget(self.footer_frame)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QuickFold", None))
#if QT_CONFIG(tooltip)
        self.btn_Unfold.setToolTip(QCoreApplication.translate("MainWindow", u"\u5c55\u5f00", None))
#endif // QT_CONFIG(tooltip)
        self.btn_Unfold.setText("")
#if QT_CONFIG(tooltip)
        self.btn_Run.setToolTip(QCoreApplication.translate("MainWindow", u"\u6267\u884c", None))
#endif // QT_CONFIG(tooltip)
        self.btn_Run.setText("")
#if QT_CONFIG(tooltip)
        self.btn_History_Path.setToolTip(QCoreApplication.translate("MainWindow", u"\u5386\u53f2\u8bb0\u5f55", None))
#endif // QT_CONFIG(tooltip)
        self.btn_History_Path.setText("")
#if QT_CONFIG(tooltip)
        self.btn_GenScript.setToolTip(QCoreApplication.translate("MainWindow", u"\u751f\u6210\u811a\u672c", None))
#endif // QT_CONFIG(tooltip)
        self.btn_GenScript.setText("")
#if QT_CONFIG(tooltip)
        self.btn_Settings.setToolTip(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e", None))
#endif // QT_CONFIG(tooltip)
        self.btn_Settings.setText("")
#if QT_CONFIG(tooltip)
        self.btn_About.setToolTip(QCoreApplication.translate("MainWindow", u"\u5173\u4e8e", None))
#endif // QT_CONFIG(tooltip)
        self.btn_About.setText("")
#if QT_CONFIG(tooltip)
        self.btn_Top.setToolTip(QCoreApplication.translate("MainWindow", u"\u7f6e\u9876", None))
#endif // QT_CONFIG(tooltip)
        self.btn_Top.setText("")
        self.cbox_Finish.setItemText(0, QCoreApplication.translate("MainWindow", u"\u5b8c\u6210\u540e\uff1a\u5173\u95ed\u5e94\u7528", None))
        self.cbox_Finish.setItemText(1, QCoreApplication.translate("MainWindow", u"\u5b8c\u6210\u540e\uff1a\u4fdd\u6301\u5e94\u7528\u6253\u5f00", None))

        self.lbl_TargetFolderNum.setText(QCoreApplication.translate("MainWindow", u"0/0", None))
        self.lbl_SourceFolderNum.setText(QCoreApplication.translate("MainWindow", u"0/0", None))
        self.lbl_TargetPath.setText("")
        self.btn_Source.setText(QCoreApplication.translate("MainWindow", u"\u6e90", None))
        self.btn_Filters.setText(QCoreApplication.translate("MainWindow", u"\u7b5b\u9009\u5668", None))
        self.btn_Target.setText(QCoreApplication.translate("MainWindow", u"\u76ee\u6807", None))
        self.lbl_SourcePath.setText("")
#if QT_CONFIG(tooltip)
        self.btn_Menu.setToolTip(QCoreApplication.translate("MainWindow", u"\u83dc\u5355", None))
#endif // QT_CONFIG(tooltip)
        self.btn_Menu.setText("")
        self.edit_GroupName.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u5206\u7ec4\u540d\u79f0\u2026", None))
#if QT_CONFIG(tooltip)
        self.btn_Save.setToolTip(QCoreApplication.translate("MainWindow", u"\u66f4\u65b0\u7ec4\u540d", None))
#endif // QT_CONFIG(tooltip)
        self.btn_Save.setText("")
#if QT_CONFIG(tooltip)
        self.btn_Del.setToolTip(QCoreApplication.translate("MainWindow", u"\u5220\u9664\u7ec4\u540d", None))
#endif // QT_CONFIG(tooltip)
        self.btn_Del.setText("")
        self.edit_Search.setPlaceholderText(QCoreApplication.translate("MainWindow", u"\u641c\u7d22\u2026", None))
#if QT_CONFIG(tooltip)
        self.btn_Goto.setToolTip(QCoreApplication.translate("MainWindow", u"\u8f6c\u5230", None))
#endif // QT_CONFIG(tooltip)
        self.btn_Goto.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_FolderList), QCoreApplication.translate("MainWindow", u"\u6587\u4ef6\u5217\u8868", None))
        self.groupBox.setTitle("")
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u6700\u8fd1\u4f7f\u7528", None))
#if QT_CONFIG(tooltip)
        self.btn_Clear.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.btn_Clear.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7406", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_History), QCoreApplication.translate("MainWindow", u"\u5386\u53f2\u8bb0\u5f55", None))
#if QT_CONFIG(tooltip)
        self.btn_GenBatchScript.setToolTip(QCoreApplication.translate("MainWindow", u"Batch\u811a\u672c", None))
#endif // QT_CONFIG(tooltip)
        self.btn_GenBatchScript.setText(QCoreApplication.translate("MainWindow", u"Batch Script", None))
#if QT_CONFIG(tooltip)
        self.btn_GenPSScript.setToolTip(QCoreApplication.translate("MainWindow", u"Power Shell\u811a\u672c", None))
#endif // QT_CONFIG(tooltip)
        self.btn_GenPSScript.setText(QCoreApplication.translate("MainWindow", u"Power Shell Script", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_Script), QCoreApplication.translate("MainWindow", u"\u6279\u5904\u7406\u811a\u672c", None))
    # retranslateUi

