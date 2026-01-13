"""
DiffRhythm谛韵音乐生成器
使用ModelScope平台的DiffRhythm模型进行文本到音乐生成
"""
import sys
import os
import logging

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from .gui.main_window import MainWindow
from .utils.logging_config import setup_logging


def main():
    """主入口函数"""
    # 初始化日志系统
    log_file = setup_logging(logging.INFO)
    
    try:
        logging.info("启动 DiffRhythm谛韵音乐生成器")
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        logging.info("用户中断应用")
        print("\n👋 应用已退出")
        sys.exit(0)
    except Exception as e:
        logging.error(f"应用运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()