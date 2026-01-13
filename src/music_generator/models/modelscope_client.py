import os
from typing import Dict, Any, Optional
from ..config.config_manager import ConfigManager


class ModelScopeClient:
    """ModelScope客户端，用于调用DiffRhythm模型"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self._pipeline = None
        
    def initialize_model(self):
        """初始化模型，使用配置文件中的token"""
        try:
            from modelscope.pipelines import pipeline
            from modelscope.utils.constant import Tasks
            
            # 设置环境变量，使用配置文件中的token
            token = self.config_manager.get_token()
            if token:
                os.environ['MODELSCOPE_TOKEN'] = token
                print("✅ 已使用配置文件中的token")
            
            # 从配置获取模型参数
            model_id = self.config_manager.get_value("modelscope", "model_id", "damo/audio_diff_rhythm_text_to_music")
            model_revision = self.config_manager.get_value("modelscope", "model_revision", "v1.0.0")
            device = self.config_manager.get_value("modelscope", "device", "cpu")
            
            print("正在初始化云端DiffRhythm音乐生成模型...")
            self._pipeline = pipeline(
                task=Tasks.text_to_audio_synthesis,  # 音乐生成固定任务类型
                model=model_id,
                model_revision=model_revision,
                device=device  # 使用配置文件中的设备设置
            )
            print("✅ 模型初始化成功！无硬件要求，无限生成音乐")
            return self._pipeline
            
        except ImportError as e:
            print(f"❌ 未安装modelscope库，请先安装: pip install modelscope")
            raise
        except Exception as e:
            print(f"❌ 模型初始化失败: {str(e)}")
            raise
            
    def get_pipeline(self):
        """获取模型管道"""
        if self._pipeline is None:
            self._pipeline = self.initialize_model()
        return self._pipeline
        
    def generate_music(self, prompt: str) -> Dict[str, Any]:
        """生成音乐"""
        pipeline = self.get_pipeline()
        result = pipeline(input=prompt)
        return result