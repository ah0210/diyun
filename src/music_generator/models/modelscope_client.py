import logging
import os
from typing import Dict, Any, Optional
from ..config.config_manager import ConfigManager


class ModelScopeClient:
    """ModelScope客户端，用于调用DiffRhythm模型"""
    
    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.logger = logging.getLogger(__name__)
        self._pipeline = None
        
    def initialize_model(self):
        """初始化模型，使用配置文件中的token"""
        try:
            self.logger.info("开始初始化云端DiffRhythm音乐生成模型...")
            from modelscope.pipelines import pipeline
            from modelscope.utils.constant import Tasks
            
            # 设置环境变量，使用配置文件中的token
            token = self.config_manager.get_token()
            if token:
                os.environ['MODELSCOPE_TOKEN'] = token
                self.logger.info("✅ 已使用配置文件中的token")
            else:
                self.logger.warning("⚠️ 未找到配置文件中的token，请在设置中配置API Token")
            
            # 从配置中获取模型ID，如果配置中没有则使用默认值
            model_id = self.config_manager.get_value('modelscope', 'model_id', 'damo/text-to-music-synthesis')
            
            # 创建模型管道
            self._pipeline = pipeline(
                task=Tasks.text_to_audio_synthesis,
                model=model_id,
                model_revision='v1.0.0',
                trust_remote_code=True  # 信任远程代码
            )
            
            self.logger.info("✅ 模型初始化成功")
            return self._pipeline
        except ImportError as e:
            error_message = str(e)
            if "datasets" in error_message:
                # 特别处理datasets相关错误
                self.logger.error(f"❌ 模型初始化失败: 缺少必要的数据集库 - {error_message}")
                raise Exception(f"缺少数据集库，请尝试安装: pip install datasets") from e
            elif "modelscope" in error_message:
                self.logger.error(f"❌ 模型初始化失败: 未安装modelscope库 - {error_message}")
                raise Exception(f"未安装modelscope库，请先安装: pip install modelscope") from e
            else:
                self.logger.error(f"❌ 模型初始化失败: 导入错误 - {error_message}")
                raise Exception(f"导入错误: {error_message}") from e
        except Exception as e:
            # 统一处理所有异常
            error_message = str(e)
            if "datasets" in error_message:
                self.logger.error(f"❌ 模型初始化失败: 数据集相关错误 - {error_message}")
                raise Exception(f"数据集相关错误: 请尝试安装兼容版本的datasets库") from e
            elif "LargeList" in error_message:
                self.logger.error(f"❌ 模型初始化失败: LargeList模块错误 - {error_message}")
                raise Exception(f"数据集库版本不兼容") from e
            elif "HubDatasetModuleFactoryWithoutScript" in error_message:
                self.logger.error(f"❌ 模型初始化失败: HubDatasetModuleFactoryWithoutScript错误 - {error_message}")
                raise Exception(f"数据集库版本不兼容") from e
            elif "MODELSCOPE_TOKEN" in error_message or "token" in error_message.lower():
                self.logger.error(f"❌ 模型初始化失败: Token验证失败 - {error_message}")
                raise Exception(f"Token验证失败，请检查API Token是否正确") from e
            else:
                self.logger.error(f"❌ 模型初始化失败: {error_message}")
                raise Exception(f"模型初始化失败: {error_message}") from e
            
    def get_pipeline(self):
        """获取模型管道"""
        if self._pipeline is None:
            self.logger.info("模型管道尚未初始化，正在初始化...")
            self._pipeline = self.initialize_model()
        else:
            self.logger.debug("使用已初始化的模型管道")
        return self._pipeline
        
    def generate_music(self, prompt: str) -> Dict[str, Any]:
        """生成音乐"""
        self.logger.info(f"开始生成音乐，提示词: {prompt}")
        pipeline = self.get_pipeline()
        result = pipeline(input=prompt)
        self.logger.info("✅ 音乐生成完成")
        return result