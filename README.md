# QuickFold - 文件夹结构管理工具

QuickFold 是一个强大的文件夹结构管理工具，专为需要快速创建复杂文件夹结构的用户设计。它使用 PySide6 构建，提供直观的图形界面，简化文件夹管理流程。

![image-20250629111440537](C:\Users\Zhoushen\AppData\Roaming\Typora\typora-user-images\image-20250629111440537.png)

## 功能特性

- 🔍 **批量扫描文件夹**：快速扫描整个目录结构
- 📁 **分组管理**：将常用文件夹结构保存为可重用的分组
- 🧩 **智能过滤**：按名称快速筛选所需文件夹
- 📜 **脚本生成**：一键生成批处理或 PowerShell 脚本
- 🚀 **高效创建**：支持单线程/多线程文件夹创建模式
- 💾 **数据持久化**：使用 SQLite 存储分组信息
- 📦 **打包部署**：支持打包为独立可执行文件

## 系统要求

- **操作系统**：Windows 7 或更高版本 (64位)
- **内存**：至少 2GB RAM
- **磁盘空间**：50MB 可用空间

## 安装与使用

### 方法1：直接运行源代码

1. 确保已安装 Python 3.9+

2. 安装依赖：

    ```bash
    pip install PySide6 pywin32
    ```

3. 克隆仓库：

    ```bash
    git clone https://github.com/BrassBook/QuickFold.git
    ```

4. 运行主程序：

    ```bash
    cd QuickFold
    python Main.py
    ```

### 方法2：使用预编译版本

1. 从 Release 页面 下载最新版本的 `QuickFold.exe`
2. 解压 ZIP 文件到任意位置
3. 运行 `QuickFold.exe`

## 使用指南

1. **设置源路径**：点击 "选择源路径" 按钮选择要扫描的目录
2. **扫描文件夹**：点击 "扫描" 扫描所有子文件夹
3. **管理分组**：
    - 创建新分组：输入名称并点击 "保存为新的配置组"
    - 加载现有分组：从下拉菜单中选择
4. **创建文件夹**：
    - 选择目标路径
    - 选择创建模式（单线程/多线程）
    - 点击 "开始创建"
5. **生成脚本**：
    - 切换到 "脚本" 标签页
    - 选择分组和脚本类型（批处理/PowerShell）
    - 点击生成脚本按钮

## 打包指南

要将应用程序打包为独立可执行文件：

1. 安装 Nuitka：

    ```bash
    pip install nuitka zstandard ordered-set
    ```

2. 下载并配置 UPX (可选，减小文件大小)

3. 运行打包脚本：

    ```bash
    python build.py
    ```

打包后的文件将在 `dist` 目录中生成。

## 命令行参数

```markdown
QuickFold.exe [选项]

选项:
  --target <路径>    设置初始目标路径
  --source <路径>    设置初始源路径
  --group <名称>     加载指定的分组
  --log-level <级别> 设置日志级别 (debug, info, warning, error)
```

## 常见问题解答

### Q: 为什么扫描大型目录时程序卡顿？

A: 扫描大量文件夹时会占用系统资源，建议：

- 启用多线程模式
- 使用过滤功能减少显示数量
- 避免扫描系统关键目录

### Q: 如何迁移我的分组数据？

A: 分组数据存储在 `folder_configs.db` 文件中，将此文件复制到新安装位置即可。

### Q: 程序运行后没有任何反应

A: 请尝试：

1. 确保解压所有文件
2. 尝试在管理员模式下运行
3. 检查防火墙是否阻止程序运行

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 项目仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

## 技术支持

遇到问题或需要帮助？请：

- 提交 Issue

## 许可证

本项目采用 MIT License

Copyright © 2023 BrassBook
