import logging
import os
from datetime import datetime
from pathlib import Path


def setup_logging(log_level=logging.INFO):
    """
    设置应用程序日志记录
    """
    # 确保日志目录存在
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 创建日志文件名（带时间戳）
    log_filename = log_dir / f"music_generator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # 配置日志格式
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 设置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # 清除现有的处理器
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # 创建文件处理器
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(log_level)
    file_formatter = logging.Formatter(log_format)
    file_handler.setFormatter(file_formatter)
    
    # 创建控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_formatter = logging.Formatter("%(levelname)s - %(message)s")
    console_handler.setFormatter(console_formatter)
    
    # 添加处理器到根记录器
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # 记录日志配置信息
    logging.info("="*60)
    logging.info("音乐生成器日志系统初始化")
    logging.info(f"日志文件: {log_filename}")
    logging.info(f"日志级别: {logging.getLevelName(log_level)}")
    logging.info("="*60)
    
    return log_filename


def get_existing_logs():
    """
    获取现有的日志文件列表
    """
    log_dir = Path("logs")
    if not log_dir.exists():
        return []
    
    log_files = list(log_dir.glob("*.log"))
    # 按修改时间排序（最新的在前）
    log_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    return log_files


def read_log_file(log_file_path, max_lines=100):
    """
    读取日志文件的最后几行
    """
    try:
        with open(log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            # 返回最后max_lines行
            return lines[-max_lines:] if len(lines) > max_lines else lines
    except Exception as e:
        return [f"无法读取日志文件: {str(e)}"]