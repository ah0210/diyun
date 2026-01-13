#!/usr/bin/env python3
"""测试 ModelScope 可用的任务类型"""

import sys
import os

# 激活虚拟环境
sys.path.insert(0, os.path.join(os.getcwd(), 'venv-py311', 'Lib', 'site-packages'))

try:
    from modelscope.utils.constant import Tasks
    
    print("ModelScope Tasks 类中可用的任务类型:")
    print("=" * 50)
    
    # 获取所有任务类型
    task_attrs = [attr for attr in dir(Tasks) if not attr.startswith('_')]
    
    for attr in sorted(task_attrs):
        value = getattr(Tasks, attr)
        print(f"{attr}: {value}")
        
    print(f"\n总共找到 {len(task_attrs)} 个任务类型")
    
    # 特别检查音乐相关的任务类型
    music_related = [attr for attr in task_attrs if any(keyword in attr.lower() for keyword in ['music', 'audio', 'sound', 'speech', 'tts'])]
    
    if music_related:
        print("\n音频/音乐相关的任务类型:")
        print("-" * 30)
        for attr in music_related:
            value = getattr(Tasks, attr)
            print(f"{attr}: {value}")
    else:
        print("\n未找到明显的音频/音乐相关任务类型")
        
except ImportError as e:
    print(f"导入错误: {e}")
except Exception as e:
    print(f"其他错误: {e}")