"""
临时修复 ModelScope LargeList 导入错误的脚本
"""
import sys
from dataclasses import dataclass, field
from typing import Any, Optional, ClassVar

# 导入必要的 datasets 组件
from datasets import Sequence as SequenceHf

@dataclass(repr=False)
class LargeList(SequenceHf):
    """Feature type for large list data composed of child feature data type.
    
    这是一个临时的 LargeList 实现，用于修复 ModelScope 1.33.0 的导入错误。
    它基于 PyArrow 的 LargeListType，支持超过 32 位偏移量的大型列表。
    
    Args:
        feature: Child feature data type of each item within the large list.
        length: Length of the list if it is fixed. Defaults to -1 (arbitrary length).
    """
    
    feature: Any
    length: int = -1
    id: Optional[str] = field(default=None, repr=False)
    # Automatically constructed
    pa_type: ClassVar[Any] = None
    _type: str = field(default='LargeList', init=False, repr=False)

    def __repr__(self):
        if self.length != -1:
            return f'{type(self).__name__}({self.feature}, length={self.length})'
        else:
            return f'{type(self).__name__}({self.feature})'

def patch_datasets_largelist():
    """将 LargeList 类添加到 datasets 模块中"""
    import datasets
    
    # 添加 LargeList 到 datasets 模块
    datasets.LargeList = LargeList
    sys.modules['datasets'].LargeList = LargeList
    
    print("✅ 已成功修补 datasets.LargeList")
    return True

if __name__ == "__main__":
    patch_datasets_largelist()
    
    # 测试导入
    try:
        from datasets import LargeList
        print("✅ LargeList 导入测试成功")
        
        # 测试 ModelScope 导入
        from modelscope.pipelines import pipeline
        from modelscope.utils.constant import Tasks
        print("✅ ModelScope 导入测试成功")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")