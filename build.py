import os
import sys
import shutil
import subprocess
from pathlib import Path


def main():
    # 1. 配置参数
    app_name = "QuickFold"
    main_script = "QuickFold.py"  # 你的主程序文件
    icon_path = "app.ico"  # 应用图标文件
    db_file = "folder_configs.db"  # SQLite数据库文件
    icons_dir = "icons"  # SVG图标目录
    output_dir = "dist"  # 输出目录

    # 2. 清理旧构建
    print("清理旧构建...")
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    # 3. 准备资源文件
    print("准备资源文件...")
    # 确保所有必要资源文件存在
    required_files = [main_script, icon_path, db_file]
    for file in required_files:
        if not os.path.exists(file):
            print(f"错误: 找不到必需文件 {file}")
            sys.exit(1)

    # 4. 构建Nuitka命令
    print("构建Nuitka命令...")
    nuitka_cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--windows-disable-console",  # 隐藏控制台窗口
        "--plugin-enable=pyside6",
        "--include-qt-plugins=all",
        f"--output-dir={output_dir}",
        f"--windows-icon-from-ico={icon_path}",
        f"--windows-company-name=BrassBook",
        f"--windows-product-name={app_name}",
        f"--windows-file-version=1.0.0",
        f"--windows-product-version=1.0.0",
        "--assume-yes-for-downloads",
        "--follow-imports",
        "--include-package=sqlite3",
        "--enable-plugin=upx",  # 使用UPX压缩
        "--lto=yes",  # 链接时优化
        "--jobs=4",  # 使用4个核心
        "--remove-output",  # 清理临时文件
        # 包含UI文件
        "--include-module=ui_MainWindows",
        # 包含资源目录
        f"--include-data-dir={icons_dir}={icons_dir}",
        # 包含数据文件
        f"--include-data-files={db_file}=.",
        main_script
    ]

    # 5. 执行打包命令
    print("开始打包...")
    print("运行命令:", " ".join(nuitka_cmd))

    try:
        process = subprocess.Popen(
            nuitka_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # 实时输出进度
        for line in process.stdout:
            print(line, end='')

        # 等待完成
        process.wait()

        if process.returncode != 0:
            print(f"打包失败，错误代码: {process.returncode}")
            print("错误输出:")
            for line in process.stderr:
                print(line, end='')
            sys.exit(1)

    except Exception as e:
        print(f"打包过程中出错: {str(e)}")
        sys.exit(1)

    # 6. 检查输出文件
    exe_name = f"{app_name}.exe"
    dist_exe = os.path.join(output_dir, exe_name)

    if os.path.exists(dist_exe):
        print(f"\n成功! 可执行文件已创建: {dist_exe}")
        print(f"大小: {os.path.getsize(dist_exe) / (1024 * 1024):.2f} MB")
    else:
        print(f"\n错误: 未找到生成的可执行文件 {dist_exe}")
        sys.exit(1)

    # 7. 创建可发布的zip包
    print("\n创建可发布包...")
    dist_files = [
        dist_exe,
        db_file
    ]

    # 添加图标目录
    for root, dirs, files in os.walk(icons_dir):
        for file in files:
            dist_files.append(os.path.join(root, file))

    # 创建zip包
    import zipfile
    zip_path = os.path.join(output_dir, f"{app_name}_release.zip")

    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in dist_files:
            # 保持目录结构
            arcname = os.path.relpath(file, os.path.dirname(output_dir))
            zipf.write(file, arcname)
            print(f"添加: {arcname}")

    print(f"\n发布包已创建: {zip_path}")
    print("打包过程完成!")


if __name__ == "__main__":
    main()