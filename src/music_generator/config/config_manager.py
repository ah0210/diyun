import os
import logging
import configparser
from pathlib import Path
from typing import Optional

class ConfigManager:
    """配置管理类"""
    
    def __init__(self, config_file: str = "config/config.ini"):
        self.config_file = Path(config_file)
        self.logger = logging.getLogger(__name__)
        self.config = configparser.ConfigParser()
        self._ensure_config_exists()
        
    def _ensure_config_exists(self):
        """确保配置文件存在，如果不存在则创建默认配置"""
        if not self.config_file.exists():
            self.logger.info(f"配置文件不存在，创建默认配置: {self.config_file}")
            self._create_default_config()
        else:
            self.logger.info(f"加载现有配置文件: {self.config_file}")
            
        self.config.read(self.config_file, encoding='utf-8')
        
    def _create_default_config(self):
        """创建默认配置文件"""
        self.logger.info("创建默认配置文件")
        # 确保配置目录存在
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        
        # 设置默认配置
        self.config['modelscope'] = {
            'token': '',
            'model_id': 'damo/text-to-music-synthesis',  # 更新为实际使用的模型ID
            'device': 'cpu',
            'model_revision': 'v1.0.0'
        }
        
        self.config['app'] = {
            'default_save_path': os.path.join('~', 'Desktop', 'DiffRhythm生成音乐.mp3'),
            'window_width': '650',
            'window_height': '320'
        }
        
        # 保存配置文件
        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
            
        self.logger.info(f"✅ 已创建默认配置文件: {self.config_file}")
        
    def get_value(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """获取配置值"""
        value = self.config.get(section, key, fallback=fallback)
        self.logger.debug(f"获取配置值 - [{section}]{key} = {value}")
        return value
        
    def set_value(self, section: str, key: str, value: str):
        """设置配置值"""
        self.logger.debug(f"设置配置值 - [{section}]{key} = {value}")
        if not self.config.has_section(section):
            self.config.add_section(section)
            
        self.config.set(section, key, value)
        
        # 保存配置文件
        with open(self.config_file, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
            
    def get_token(self) -> str:
        """获取ModelScope token"""
        return self.get_value('modelscope', 'token', '')
        
    def set_token(self, token: str):
        """设置ModelScope token"""
        self.set_value('modelscope', 'token', token)