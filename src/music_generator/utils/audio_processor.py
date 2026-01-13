import logging
from typing import Any
import soundfile as sf
import numpy as np
import os


class AudioProcessor:
    """音频处理工具类"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def save_audio(self, audio_data: Any, file_path: str, sample_rate: int = 44100):
        """保存音频数据到文件"""
        try:
            self.logger.info(f"开始保存音频到: {file_path}")
            # 如果音频数据有write_audio方法（如ModelScope的输出），则直接使用
            if hasattr(audio_data, 'write_audio'):
                audio_data.write_audio(file_path, samplerate=sample_rate)
            else:
                # 否则使用soundfile保存
                sf.write(file_path, audio_data, sample_rate)
            self.logger.info(f"✅ 音频已成功保存到: {file_path}")
        except Exception as e:
            self.logger.error(f"❌ 保存音频失败: {e}")
            raise
            
    def play_audio(self, file_path: str):
        """播放音频文件"""
        try:
            self.logger.info(f"开始播放音频: {file_path}")
            from playsound import playsound
            playsound(file_path)
            self.logger.info(f"✅ 音频播放完成: {file_path}")
        except ImportError:
            self.logger.warning("⚠️ 未安装playsound，跳过播放")
        except Exception as e:
            self.logger.error(f"❌ 播放失败: {e}")
            
    def create_temp_audio(self, audio_data: Any, temp_path: str = "temp_music.mp3", sample_rate: int = 44100):
        """创建临时音频文件"""
        self.logger.info(f"创建临时音频文件: {temp_path}")
        self.save_audio(audio_data, temp_path, sample_rate)
        return temp_path