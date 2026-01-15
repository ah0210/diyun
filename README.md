# DiffRhythm谛韵音乐生成器

基于ModelScope平台的AI音乐生成应用，使用DiffRhythm模型将文本描述转换为音乐。

## 项目结构

```
diyun/
├── src/
│   └── music_generator/
│       ├── __init__.py
│       ├── main.py                 # 主入口
│       ├── gui/
│       │   ├── __init__.py
│       │   └── main_window.py      # GUI界面
│       ├── config/
│       │   ├── __init__.py
│       │   └── config_manager.py   # 配置管理
│       ├── models/
│       │   ├── __init__.py
│       │   └── modelscope_client.py # ModelScope客户端
│       └── utils/
│           ├── __init__.py
│           ├── audio_processor.py   # 音频处理工具
│           └── logging_config.py    # 日志配置
├── tests/
├── logs/                         # 日志文件目录
├── dist/                         # 构建产物目录
├── requirements.txt
├── pyproject.toml
├── nuitka_build.py               # Nuitka构建脚本
├── view_logs.py                  # 日志查看工具
├── debug_app.py                  # 调试工具
└── README.md
```

## 功能特性

- 🎵 文本到音乐生成
- 🔧 ModelScope API Token配置
- 💾 音频保存和播放
- 🎨 友好的图形用户界面
- 📋 完整的日志记录和查看功能
- 🔍 详细的调试信息
- ⚡ 使用Nuitka编译，性能更佳

## 安装依赖

```bash
pip install -r requirements.txt
```

如果遇到依赖问题，请按以下顺序安装：
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

对于Windows用户，如果遇到pyarrow编译问题：
```bash
pip install pyarrow==14.0.0 --only-binary=all
```

## 运行应用

```bash
python -m src.music_generator.main
```

## 调试步骤

### 1. 使用调试模式运行
```bash
python debug_app.py
```
调试模式会显示详细的系统信息和日志记录。

### 2. 查看运行日志
方式一：使用日志查看工具
```bash
python view_logs.py
```

方式二：在应用界面中点击"查看日志"按钮

方式三：直接查看logs目录下的日志文件

### 3. 日志文件位置
日志文件保存在 `logs/` 目录下，文件名格式为 `music_generator_YYYYMMDD_HHMMSS.log`

## 使用Nuitka构建

```bash
# 安装Nuitka
python nuitka_build.py --install

# 构建可执行文件
python nuitka_build.py
```

构建后的可执行文件将位于 `dist/` 目录。

## 配置说明

应用使用 `config/config.ini` 文件存储配置，包括：

- ModelScope API Token
- 模型参数
- 应用设置

首次运行时会自动创建默认配置文件。

## API Token获取

1. 访问 [ModelScope官网](https://www.modelscope.cn/)
2. 注册并登录账号
3. 进入个人中心
4. 在账号信息页面找到API Token
5. 在应用设置中配置Token

## 故障排除

如果遇到问题，请检查以下几点：
- 确保Python版本为3.8或更高
- 确保已正确安装所有依赖项
- 确保ModelScope API Token已正确配置
- 检查网络连接是否正常

### 常见问题及解决方案

1. **PyArrow相关错误**:
     ```bash
     pip uninstall pyarrow -y
     pip install pyarrow==18.0.0 --only-binary=pyarrow
     ```
     或者尝试更新到最新版本
     ```bash
     pip install --upgrade pyarrow
     ```

2. **Torch相关错误**:
   ```bash
   pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
   ```

3. **权限错误**:
    - 确保目标目录有足够的写入权限
    - 尝试以管理员身份运行

 4. **网络连接问题**:
    - 检查防火墙设置
    - 确保能够访问ModelScope服务器
    - 检查API Token是否有效

 5. **Datasets库兼容性问题**:
    ```bash
    pip install datasets>=3.0.0,<=3.6.0
    ```
 目前 modelscope 版本对 datasets的支持必须在3.0.0到3.6.0之间
 ```
 https://github.com/modelscope/modelscope/tree/master/requirements
addict
attrs
datasets>=3.0.0,<=3.6.0
einops
oss2
Pillow
python-dateutil>=2.1
scipy
setuptools
simplejson>=3.3.0
sortedcontainers>=1.5.9
urllib3>=1.26
```

## 许可证

MIT License