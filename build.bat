@echo off
chcp 65001 >nul
echo ================================
echo 音频格式分析器 - 打包脚本
echo ================================
echo.

REM 检查ffprobe.exe是否存在
if not exist ffprobe.exe (
    echo 错误：找不到 ffprobe.exe 文件！
    echo 请确保 ffprobe.exe 在当前目录下
    echo.
    pause
    exit /b 1
)

echo 开始打包程序...
echo 使用 AudioAnalyzer.spec 配置文件
echo.

pyinstaller AudioAnalyzer.spec

if %errorlevel% == 0 (
    echo.
    echo ================================
    echo 打包成功！
    echo 可执行文件位置: dist\AudioAnalyzer.exe
    echo ================================
    echo.
    echo ffprobe.exe 已打包到可执行文件中
    echo 可以直接运行 dist\AudioAnalyzer.exe
) else (
    echo.
    echo ================================
    echo 打包失败！请检查错误信息
    echo ================================
)

echo.
pause

