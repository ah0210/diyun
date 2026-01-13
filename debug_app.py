#!/usr/bin/env python3
"""
调试脚本
用于测试音乐生成器的应用日志功能
"""

import os
import sys
import logging
from datetime import datetime

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.music_generator.utils.logging_config import setup_logging
from src.music_generator.main import main as run_app


def debug_info():
    """显示调试信息"""
    print("="*60)
    print("🎵 音乐生成器 - 调试信息")
    print("="*60)
    print(f"Python 版本: {sys.version}")
    print(f"当前工作目录: {os.getcwd()}")
    print(f"系统路径: {sys.path[:3]}...")  # 只显示前几个路径
    print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查日志目录
    log_dir = os.path.join(os.getcwd(), "logs")
    print(f"日志目录: {log_dir}")
    if os.path.exists(log_dir):
        log_files = os.listdir(log_dir)
        print(f"日志文件数量: {len(log_files)}")
        if log_files:
            print(f"最近的日志文件: {sorted(log_files)[-1]}")
    else:
        print("日志目录不存在，将在首次运行应用后创建")
    
    print("="*60)


def main():
    """调试主函数"""
    print("启动音乐生成器调试模式...")
    
    # 显示调试信息
    debug_info()
    
    # 初始化日志
    print("\n初始化日志系统...")
    log_file = setup_logging(logging.DEBUG)
    logging.info("调试模式启动")
    
    print(f"日志文件位置: {log_file}")
    print("\n即将启动音乐生成器应用...")
    print("提示：应用运行后，您可以使用 'view_logs.py' 查看日志")
    print("或者在应用界面中点击 '查看日志' 按钮")
    
    try:
        # 运行主应用
        run_app()
    except KeyboardInterrupt:
        logging.info("调试模式被用户中断")
        print("\n调试模式已退出")
    except Exception as e:
        logging.error(f"调试模式运行错误: {e}")
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()