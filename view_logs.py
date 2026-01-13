#!/usr/bin/env python3
"""
日志查看工具
用于查看音乐生成器应用的日志文件
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sys
import os
from datetime import datetime
from pathlib import Path

# 添加项目路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.music_generator.utils.logging_config import get_existing_logs, read_log_file


def main():
    """日志查看器主函数"""
    # 创建主窗口
    root = tk.Tk()
    root.title("音乐生成器 - 日志查看器")
    root.geometry("900x700")
    
    # 居中显示窗口
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - 900) // 2
    y = (screen_height - 700) // 2
    root.geometry(f"900x700+{x}+{y}")
    
    # 创建主框架
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # 标题
    title_label = ttk.Label(main_frame, text="🎵 音乐生成器 - 日志查看器 📋", 
                           font=("微软雅黑", 14, "bold"))
    title_label.pack(pady=(0, 20))
    
    # 日志文件选择区域
    selection_frame = ttk.LabelFrame(main_frame, text="选择日志文件", padding="10")
    selection_frame.pack(fill=tk.X, pady=(0, 10))
    
    # 获取日志文件列表
    log_files = get_existing_logs()
    
    if not log_files:
        ttk.Label(selection_frame, text="暂无日志文件", foreground="red").pack()
        ttk.Label(selection_frame, text="运行音乐生成器后将生成日志文件").pack()
    else:
        # 日志文件选择下拉框
        log_names = [log_file.name for log_file in log_files]
        log_var = tk.StringVar()
        log_combo = ttk.Combobox(selection_frame, textvariable=log_var, values=log_names, state="readonly", width=50)
        log_combo.pack(side=tk.LEFT, padx=(0, 10))
        log_combo.current(0)  # 默认选中第一个（最新的）
        
        # 刷新按钮
        def refresh_logs():
            nonlocal log_files, log_names
            log_files = get_existing_logs()
            if log_files:
                log_names = [log_file.name for log_file in log_files]
                log_combo['values'] = log_names
                log_combo.current(0)
                # 更新日志内容显示
                update_log_content()
            else:
                log_combo['values'] = []
                text_area.delete(1.0, tk.END)
                text_area.insert(tk.END, "暂无日志文件")
        
        refresh_btn = ttk.Button(selection_frame, text="刷新", command=refresh_logs)
        refresh_btn.pack(side=tk.LEFT)
    
    # 日志内容显示区域
    content_frame = ttk.LabelFrame(main_frame, text="日志内容", padding="10")
    content_frame.pack(fill=tk.BOTH, expand=True)
    
    # 创建文本框和滚动条
    text_area = scrolledtext.ScrolledText(content_frame, wrap=tk.WORD, width=80, height=30)
    text_area.pack(fill=tk.BOTH, expand=True)
    
    # 更新日志内容显示
    def update_log_content():
        if not log_files:
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, "暂无日志文件")
            return
            
        selected_name = log_var.get() if log_var.get() else log_names[0]
        selected_log = next((f for f in log_files if f.name == selected_name), log_files[0])
        
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        
        log_content = read_log_file(selected_log, max_lines=1000)  # 只显示最后1000行
        text_area.insert(tk.END, ''.join(log_content))
        text_area.config(state=tk.DISABLED)
        
        # 滚动到顶部
        text_area.yview_moveto(0)
    
    # 绑定下拉框选择事件
    def on_log_selected(event):
        update_log_content()
    
    if log_files:
        log_combo.bind("<<ComboboxSelected>>", on_log_selected)
        # 显示默认日志内容
        update_log_content()
    
    # 按钮区域
    button_frame = ttk.Frame(main_frame)
    button_frame.pack(fill=tk.X, pady=(10, 0))
    
    def copy_logs():
        """复制日志内容到剪贴板"""
        content = text_area.get(1.0, tk.END)
        root.clipboard_clear()
        root.clipboard_append(content.strip())
        messagebox.showinfo("复制成功", "日志内容已复制到剪贴板")
    
    def clear_logs():
        """清空日志目录"""
        if messagebox.askyesno("确认", "确定要清空所有日志文件吗？此操作不可撤销。"):
            for log_file in log_files:
                try:
                    log_file.unlink()  # 删除文件
                except Exception as e:
                    messagebox.showerror("错误", f"删除日志文件失败: {e}")
            
            # 刷新界面
            refresh_logs()
            messagebox.showinfo("完成", "日志文件已清空")
    
    copy_btn = ttk.Button(button_frame, text="复制日志", command=copy_logs)
    copy_btn.pack(side=tk.LEFT, padx=(0, 10))
    
    clear_btn = ttk.Button(button_frame, text="清空日志", command=clear_logs)
    clear_btn.pack(side=tk.LEFT)
    
    # 关闭按钮
    close_btn = ttk.Button(button_frame, text="关闭", command=root.destroy)
    close_btn.pack(side=tk.RIGHT)
    
    # 启动主循环
    root.mainloop()


if __name__ == "__main__":
    main()