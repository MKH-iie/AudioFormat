## 项目说明

这是一个分析音频格式的可视化软件，前端可视化使用python的PySimpleGUI开发，音频格式分析通过ffprobe实现

## 功能特性

1. ✅ 支持多种音频格式：MP3, WAV, FLAC, AAC, M4A, OGG, WMA, APE, OPUS等
2. ✅ 显示详细音频信息：格式、编码、采样率、比特率、声道数、时长
3. ✅ 支持中文路径和特殊字符
4. ✅ 智能识别非法音频文件并给出提示
5. ✅ 美观的图形界面，操作简单直观

## 项目结构

```
AudioFormat/
├── ffprobe.exe          # FFmpeg音频分析工具
├── audio_gui.py         # GUI界面模块（主程序）
├── audio_analyzer.py    # 音频分析核心模块
├── AudioAnalyzer.spec   # PyInstaller打包配置文件
├── build.bat            # Windows打包脚本
├── requirements.txt     # 依赖包列表
├── README.md            # 项目说明文档
├── 开发文档.md          # 开发需求文档
└── source/              # 资源文件夹
    └── PySimpleGUI-4.60.5.7z  # PySimpleGUI安装包
```

## 环境需求

### Python运行与调试环境

1. **Python 3.6+**

2. **PySimpleGUI 4.60.5**
    - PySimpleGUI需要低版本，高版本收费，无法直接使用
    - 可以直接解压 `source/PySimpleGUI-4.60.5.7z`，然后进入文件目录执行：
      ```bash
      python setup.py install
      ```
    - 如果没有安装setuptools，就先执行：
      ```bash
      pip install setuptools
      ```

3. **PyInstaller（可选，用于打包）**
    - 如需打包成exe文件，安装pyinstaller：
      ```bash
      pip install pyinstaller
      ```

## 使用方法

### 开发运行

1. 安装依赖（见上方"环境需求"）
2. 运行程序：
   ```bash
   python audio_gui.py
   ```

### 打包成可执行文件

#### 方法1：使用批处理脚本（推荐）
在Windows系统上，双击运行 `build.bat` 或在命令行执行：
```bash
build.bat
```

#### 方法2：直接使用spec文件
```bash
pyinstaller AudioAnalyzer.spec
```

打包完成后，可执行文件位于 `dist/AudioAnalyzer.exe`

**注意**：ffprobe.exe已经打包到可执行文件中，无需额外复制

## 使用说明

1. 启动程序后，点击"浏览"按钮选择音频文件
2. 选择文件后，点击"开始分析"按钮
3. 程序将显示音频的详细信息
4. 点击"清除结果"可以清空当前显示的信息
5. 点击"退出"关闭程序

## 技术架构

- **前端界面**：PySimpleGUI - 轻量级Python GUI框架
- **音频分析**：FFprobe - FFmpeg的音频分析工具
- **代码架构**：采用模块化设计，前端与后端逻辑分离

## 打包说明

项目使用 `.spec` 配置文件进行打包，具有以下特点：

1. **单文件打包**：所有依赖（包括ffprobe.exe）都打包到一个exe文件中
2. **无控制台窗口**：打包后的程序运行时不显示黑色控制台窗口
3. **资源路径处理**：使用 `get_resource_path()` 函数自动处理开发环境和打包环境的路径差异
4. **UPX压缩**：使用UPX压缩减小文件体积（如果系统中有UPX）

## 注意事项

1. **开发环境**：确保 `ffprobe.exe` 与程序文件在同一目录下
2. **打包环境**：ffprobe.exe会自动打包到可执行文件中，无需手动复制
3. 支持中文路径，无需担心路径编码问题
4. 如果分析失败，程序会给出明确的错误提示
5. 建议使用常见的音频格式以获得最佳兼容性