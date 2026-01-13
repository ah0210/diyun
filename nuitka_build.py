#!/usr/bin/env python3
"""
Nuitka构建脚本
用于将Python应用程序编译为独立的可执行文件
"""

import subprocess
import sys
import os
from pathlib import Path


def install_nuitka():
    """安装Nuitka"""
    print("正在安装Nuitka...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "nuitka"], check=True)
        print("✅ Nuitka安装成功")
    except subprocess.CalledProcessError as e:
        print(f"❌ Nuitka安装失败: {e}")
        sys.exit(1)


def build_with_nuitka_minimal():
    """使用最小配置构建应用程序"""
    print("开始使用最小配置构建应用程序...")
    
    # 构建命令参数 - 只包含必要的包
    build_args = [
        sys.executable,
        "-m", "nuitka",
        "--standalone",
        "--onefile",  # 生成单个可执行文件
        "--enable-plugin=tk-inter",  # 启用tkinter插件
        "--output-dir=dist",  # 输出目录
        "--remove-output",  # 构建后删除中间文件
        "--include-data-dir=config=config",  # 包含配置目录
        "--nofollow-import-to=PIL",  # 不跟随不必要包
        "--nofollow-import-to=matplotlib",
        "--nofollow-import-to=sklearn",
        "--nofollow-import-to=h5py",
        "--nofollow-import-to=cv2",
        "--nofollow-import-to=pygame",
        "--nofollow-import-to=pyglet",
        "--windows-console-mode=disable",  # Windows下禁用控制台窗口
        "src/music_generator/main.py"
    ]
    
    try:
        print("执行最小配置构建命令...")
        result = subprocess.run(build_args, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 最小配置构建成功！可执行文件位于 dist/ 目录")
            print(result.stdout)
        else:
            print("❌ 最小配置构建失败:")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ 构建过程中出现异常: {e}")
        return False


def build_with_nuitka_selective():
    """使用选择性包含包的方式构建"""
    print("开始使用选择性包含包构建应用程序...")
    
    # 构建命令参数 - 有选择地包含包
    build_args = [
        sys.executable,
        "-m", "nuitka",
        "--standalone",
        "--onefile",
        "--enable-plugin=tk-inter",
        "--output-dir=dist",
        "--remove-output",
        "--include-data-dir=config=config",
        # 只包含明确需要的包
        "--include-package=modelscope",
        "--include-package=torch",
        "--include-package=torchvision", 
        "--include-package=torchaudio",
        # 避免transformers的复杂语法问题
        "--include-package=librosa",
        "--include-package=soundfile",
        "--include-package=numpy",
        "--include-package=scipy",
        "--include-package=requests",
        "--include-package=urllib3",
        "--include-package=certifi",
        "--include-package=charset-normalizer",
        "--include-package=idna",
        "--include-package=configparser",
        "--include-package=threading",
        "--include-package=json",
        "--include-package=pathlib",
        "--include-package=logging",  # 包含日志模块
        "--include-package=tkinter",  # 包含GUI模块
        "--nofollow-import-to=transformers",  # 不包含transformers，避免语法错误
        "--nofollow-import-to=PIL",
        "--nofollow-import-to=matplotlib",
        "--nofollow-import-to=sklearn",
        "--windows-console-mode=disable",
        "src/music_generator/main.py"
    ]
    
    try:
        print("执行选择性包含包构建命令...")
        result = subprocess.run(build_args, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ 选择性包含包构建成功！可执行文件位于 dist/ 目录")
            print(result.stdout)
            return True
        else:
            print("❌ 选择性包含包构建失败:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ 构建过程中出现异常: {e}")
        return False


def main():
    """主函数"""
    if len(sys.argv) > 1 and sys.argv[1] == "--install":
        install_nuitka()
        return
    
    # 检查是否已安装Nuitka
    try:
        import nuitka
        print("✅ 检测到Nuitka已安装")
    except ImportError:
        print("⚠️ Nuitka未安装，正在安装...")
        install_nuitka()
    
    # 首先尝试最小配置构建
    success = build_with_nuitka_minimal()
    
    if not success:
        print("\n尝试选择性包含包构建...")
        success = build_with_nuitka_selective()
    
    if success:
        print("\n🎉 构建成功完成！")
        print("📦 可执行文件位于 dist/ 目录")
        print("📁 请检查 dist 目录中的生成文件")
    else:
        print("\n❌ 所有构建尝试均失败")
        print("🔧 可能需要进一步调整Nuitka参数")


if __name__ == "__main__":
    main()