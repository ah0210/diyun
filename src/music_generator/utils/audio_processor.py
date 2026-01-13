from typing import Any
import soundfile as sf
import numpy as np
import os


class AudioProcessor:
    """音频处理工具类"""
    
    @staticmethod
    def save_audio(audio_data: Any, file_path: str, sample_rate: int = 44100):
        """保存音频数据到文件"""
        try:
            # 如果音频数据有write_audio方法（如ModelScope的输出），则直接使用
            if hasattr(audio_data, 'write_audio'):
                audio_data.write_audio(file_path, samplerate=sample_rate)
            else:
                # 否则使用soundfile保存
                sf.write(file_path, audio_data, sample_rate)
            print(f"✅ 音频已保存到: {file_path}")
        except Exception as e:
            print(f"❌ 保存音频失败: {e}")
            raise
            
    @staticmethod
    def play_audio(file_path: str):
        """播放音频文件"""
        try:
            from playsound import playsound
            playsound(file_path)
        except ImportError:
            print("⚠️ 未安装playsound，跳过播放")
        except Exception as e:
            print(f"❌ 播放失败: {e}")
            
    @staticmethod
    def create_temp_audio(audio_data: Any, temp_path: str = "temp_music.mp3", sample_rate: int = 44100):
        """创建临时音频文件"""
        AudioProcessor.save_audio(audio_data, temp_path, sample_rate)
        return temp_path