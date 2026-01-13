import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
from ..config.config_manager import ConfigManager
from ..models.modelscope_client import ModelScopeClient
from ..utils.audio_processor import AudioProcessor


class MainWindow:
    """主窗口类"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.config_manager = ConfigManager()
        self.model_client = ModelScopeClient(self.config_manager)
        self.current_audio = None
        
        self.setup_ui()
        self.load_configs()
        
    def setup_ui(self):
        """设置用户界面"""
        self.root.title("DiffRhythm谛韵 - AI音乐生成器")
        
        # 从配置获取窗口尺寸
        width = int(self.config_manager.get_value("app", "window_width", "650"))
        height = int(self.config_manager.get_value("app", "window_height", "320"))
        
        # 设置窗口居中
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.resizable(True, True)  # 允许调整窗口大小
        
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🎵 DiffRhythm谛韵 - AI音乐生成器 🎵", 
                               font=("微软雅黑", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # 音乐描述输入
        ttk.Label(main_frame, text="音乐描述:", font=("微软雅黑", 10)).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.entry_prompt = ttk.Entry(main_frame, font=("微软雅黑", 10))
        self.entry_prompt.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        self.entry_prompt.insert(0, "例如：舒缓的钢琴曲，古风纯音乐")
        
        # 示例按钮
        example_btn = ttk.Button(main_frame, text="示例", command=self.fill_example)
        example_btn.grid(row=1, column=3, padx=(10, 0), pady=5)
        
        # 生成按钮
        self.btn_generate = ttk.Button(main_frame, text="生成音乐", command=self.generate_music_threaded)
        self.btn_generate.grid(row=2, column=0, columnspan=2, pady=20)
        
        # 保存按钮
        self.btn_save = ttk.Button(main_frame, text="保存音乐", command=self.save_music)
        self.btn_save.grid(row=2, column=2, columnspan=2, pady=20, padx=(10, 0))
        
        # 设置按钮
        btn_settings = ttk.Button(main_frame, text="设置", command=self.open_settings)
        btn_settings.grid(row=3, column=0, pady=10)
        
        # 说明标签
        info_label = ttk.Label(main_frame, text="💡 提示：输入音乐风格描述，点击生成音乐", 
                              foreground="gray", font=("微软雅黑", 9))
        info_label.grid(row=4, column=0, columnspan=4, pady=(20, 0))
        
        # 绑定回车键到生成音乐
        self.root.bind('<Return>', lambda event: self.generate_music_threaded())
        
    def load_configs(self):
        """加载配置"""
        pass  # 可以在这里加载额外的配置
        
    def fill_example(self):
        """填充示例文本"""
        examples = [
            "舒缓的钢琴曲，古风纯音乐",
            "欢快的电子音乐，节拍强劲",
            "轻柔的吉他独奏，乡村风格",
            "激昂的交响乐，史诗感",
            "宁静的冥想音乐，自然声音"
        ]
        import random
        self.entry_prompt.delete(0, tk.END)
        self.entry_prompt.insert(0, random.choice(examples))
        
    def generate_music_threaded(self):
        """在线程中生成音乐，防止UI冻结"""
        threading.Thread(target=self.generate_music, daemon=True).start()
        
    def generate_music(self):
        """生成音乐的核心函数"""
        prompt = self.entry_prompt.get().strip()
        if not prompt or prompt == "例如：舒缓的钢琴曲，古风纯音乐":
            messagebox.showwarning("提示", "请输入音乐描述（比如：舒缓的钢琴曲，古风纯音乐）！")
            return
        
        # 更新按钮状态
        self.root.after(0, lambda: self.btn_generate.config(state=tk.DISABLED, text="生成中...(云端处理，无需显卡)"))
        
        try:
            # 调用云端DiffRhythm生成音乐
            result = self.model_client.generate_music(prompt)
            audio_data = result["output_audio"]
            
            self.root.after(0, lambda: messagebox.showinfo("生成成功", "✅ 音乐生成完成！已自动播放，可点击保存按钮导出MP3"))
            
            # 临时保存播放
            temp_mp3 = "temp_music.mp3"
            temp_path = AudioProcessor.create_temp_audio(audio_data, temp_mp3)
            
            # 播放音乐
            AudioProcessor.play_audio(temp_path)
            
            # 保存引用供后续保存使用
            self.current_audio = audio_data
            
        except Exception as e:
            error_info = str(e)
            def show_error():
                if "network" in error_info or "timeout" in error_info.lower():
                    messagebox.showerror("生成失败", "网络异常！请检查网络连接后重试")
                else:
                    messagebox.showerror("生成失败", f"生成出错：{error_info}\n✅ 重试即可，无额度限制")
            self.root.after(0, show_error)
        finally:
            # 恢复按钮状态
            self.root.after(0, lambda: self.btn_generate.config(state=tk.NORMAL, text="生成音乐"))
    
    def save_music(self):
        """保存音乐文件"""
        if not self.current_audio:
            messagebox.showwarning("提示", "请先生成音乐再保存！")
            return
        
        # 从配置获取默认保存路径
        default_save_path = self.config_manager.get_value("app", "default_save_path", 
                                                         os.path.join(os.path.expanduser("~"), "Desktop", "DiffRhythm生成音乐.mp3"))
        # 处理 ~ 路径变量
        default_save_path = os.path.expanduser(default_save_path)
        
        save_path = filedialog.asksaveasfilename(
            title="保存音乐",
            defaultextension=".mp3",
            filetypes=[("MP3音频文件", "*.mp3"), ("所有文件", "*.*")],
            initialfile="DiffRhythm-音乐生成.mp3",
            initialdir=os.path.dirname(default_save_path) if os.path.dirname(default_save_path) != "~" else os.path.expanduser("~")
        )
        if save_path:
            try:
                AudioProcessor.save_audio(self.current_audio, save_path)
                messagebox.showinfo("保存成功", f"音乐已保存到：\n{save_path}")
            except Exception as e:
                messagebox.showerror("保存失败", f"保存出错：{str(e)}")

    def open_settings(self):
        """打开设置界面，允许用户输入API token"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("设置")
        settings_window.geometry("500x300")
        settings_window.resizable(False, False)
        
        # 居中显示设置窗口
        parent_x = self.root.winfo_x()
        parent_y = self.root.winfo_y()
        parent_width = self.root.winfo_width()
        parent_height = self.root.winfo_height()
        x = parent_x + (parent_width - 500) // 2
        y = parent_y + (parent_height - 300) // 2
        settings_window.geometry(f"500x300+{x}+{y}")
        
        # 创建框架
        frame = ttk.Frame(settings_window, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # API Token 配置
        ttk.Label(frame, text="ModelScope API Token:", font=("微软雅黑", 10)).pack(anchor=tk.W, pady=(0, 5))
        
        token_var = tk.StringVar(value=self.config_manager.get_token())
        token_entry = ttk.Entry(frame, textvariable=token_var, width=50)
        token_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Token 获取说明
        info_text = ("💡 获取Token方法：\n"
                    "1. 访问 https://www.modelscope.cn/\n"
                    "2. 登录账号，进入个人中心\n"
                    "3. 在账号信息页面找到API Token\n"
                    "4. 复制并粘贴到这里")
        
        info_label = ttk.Label(frame, text=info_text, font=("微软雅黑", 9), foreground="gray")
        info_label.pack(anchor=tk.W, pady=(0, 20))
        
        # 保存按钮
        def save_token():
            token = token_var.get().strip()
            self.config_manager.set_token(token)
            messagebox.showinfo("保存成功", "✅ Token已保存，重启应用后生效")
            settings_window.destroy()
        
        save_btn = ttk.Button(frame, text="保存Token", command=save_token)
        save_btn.pack(pady=10)
        
        # 确保设置窗口在顶层
        settings_window.transient(self.root)
        settings_window.grab_set()
        
    def run(self):
        """运行主窗口"""
        self.root.mainloop()