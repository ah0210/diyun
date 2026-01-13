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
│           └── audio_processor.py   # 音频处理工具
├── tests/
├── requirements.txt
├── pyproject.toml
├── nuitka_build.py                # Nuitka构建脚本
└── README.md
```

## 功能特性

- 🎵 文本到音乐生成
- 🔧 ModelScope API Token配置
- 💾 音频保存和播放
- 🎨 友好的图形用户界面
- ⚡ 使用Nuitka编译，性能更佳

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行应用

```bash
python -m src.music_generator.main
```

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

## 许可证

MIT License