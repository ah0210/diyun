#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试日志功能的脚本
"""

import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def test_logging():
    """测试日志功能"""
    print("正在测试日志功能...")
    
    # 导入日志配置
    from src.music_generator.utils.logging_config import setup_logging
    
    # 设置日志
    log_file = setup_logging()
    print(f"日志文件已创建: {log_file}")
    
    # 测试记录一些日志
    import logging
    
    logger = logging.getLogger(__name__)
    logger.info("测试信息日志")
    logger.debug("测试调试日志")
    logger.warning("测试警告日志")
    logger.error("测试错误日志")
    
    print("日志测试完成！")
    print(f"日志文件位置: {log_file}")

if __name__ == "__main__":
    test_logging()