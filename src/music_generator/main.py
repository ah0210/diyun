"""
DiffRhythm谛韵音乐生成器
使用ModelScope平台的DiffRhythm模型进行文本到音乐生成
"""
import sys
import os
# 添加项目根目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from .gui.main_window import MainWindow


def main():
    """主入口函数"""
    try:
        app = MainWindow()
        app.run()
    except KeyboardInterrupt:
        print("\n👋 应用已退出")
        sys.exit(0)
    except Exception as e:
        print(f"❌ 应用运行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()