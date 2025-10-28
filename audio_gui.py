"""
音频格式分析器 - GUI界面
使用PySimpleGUI实现可视化界面
"""
import PySimpleGUI as sg
import os
import sys
from audio_analyzer import AudioAnalyzer


def get_resource_path(relative_path):
    """
    获取资源文件的绝对路径，兼容开发环境和PyInstaller打包后的环境
    
    Args:
        relative_path: 相对路径
        
    Returns:
        资源文件的绝对路径
    """
    try:
        # PyInstaller创建临时文件夹，将路径存储在_MEIPASS中
        base_path = sys._MEIPASS
    except Exception:
        # 开发环境中使用当前目录
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)


class AudioAnalyzerGUI:
    """音频分析器图形界面类"""
    
    def __init__(self):
        """初始化GUI"""
        # 设置自定义颜色方案：白色背景，黑色文字
        sg.theme('Default1')
        sg.set_options(
            background_color='white',
            text_element_background_color='white',
            element_background_color='white',
            text_color='black',
            input_elements_background_color='white',
            input_text_color='black',
            button_color=('black', '#E0E0E0')
        )
        
        # 初始化音频分析器
        # 使用get_resource_path获取ffprobe的正确路径（兼容打包后的exe）
        try:
            ffprobe_path = get_resource_path('ffprobe.exe')
            self.analyzer = AudioAnalyzer(ffprobe_path)
        except FileNotFoundError as e:
            sg.popup_error(f'错误：{str(e)}', title='初始化失败')
            raise
        
        # 创建窗口布局
        self.layout = [
            [sg.Text('音频格式分析器', font=('微软雅黑', 18, 'bold'), justification='center', 
                     expand_x=True, text_color='black', background_color='white')],
            [sg.HorizontalSeparator()],
            
            # 文件选择区域
            [sg.Text('音频文件:', font=('微软雅黑', 12), text_color='black', background_color='white')],
            [
                sg.Input(key='-FILE-', enable_events=True, expand_x=True, font=('微软雅黑', 12),
                        text_color='black', background_color='white'),
                sg.FileBrowse('浏览本地文件', font=('微软雅黑', 12), button_color=('black', '#E0E0E0'), 
                             file_types=(
                    ("音频文件", "*.mp3 *.wav *.flac *.aac *.m4a *.ogg *.wma *.ape *.opus"),
                    ("所有文件", "*.*")
                ))
            ],
            
            # 分析按钮
            [sg.Button('开始分析', font=('微软雅黑', 12), size=(15, 1), button_color=('white', '#4CAF50'))],
            [sg.Text('')],  # 空行
            
            # 结果显示区域
            [sg.Text('分析结果:', font=('微软雅黑', 13, 'bold'), text_color='black', background_color='white')],
            [sg.HorizontalSeparator()],
            [
                sg.Column([
                    [sg.Text('文件大小:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('音频格式:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('编码格式:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('编码器:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('采样率:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('位深度:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('比特率:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('声道:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('时长:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('流数量:', size=(10, 1), font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                ], background_color='white'),
                sg.Column([
                    [sg.Text('', size=(25, 1), key='-FILESIZE-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('', size=(25, 1), key='-FORMAT-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('', size=(25, 1), key='-CODEC-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('', size=(25, 1), key='-ENCODER-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('', size=(25, 1), key='-SAMPLE-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('', size=(25, 1), key='-BITDEPTH-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('', size=(25, 1), key='-BITRATE-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('', size=(25, 1), key='-CHANNELS-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('', size=(25, 1), key='-DURATION-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                    [sg.Text('', size=(25, 1), key='-STREAMCOUNT-', font=('微软雅黑', 12), 
                            text_color='black', background_color='white')],
                ], background_color='white')
            ],
            [sg.Text('')],  # 空行
            [sg.HorizontalSeparator()],
            
            # 底部按钮
            [
                sg.Button('清除结果', font=('微软雅黑', 12), size=(12, 1), button_color=('black', '#E0E0E0')),
                sg.Push(),
                sg.Button('退出', font=('微软雅黑', 12), size=(12, 1), button_color=('white', '#f44336'))
            ]
        ]
        
        # 创建窗口
        self.window = sg.Window(
            '音频格式分析器',
            self.layout,
            size=(650, 650),
            finalize=True,
            resizable=False,
            background_color='white',
            icon=None  # 可以添加自定义图标
        )
    
    def clear_results(self):
        """清除分析结果显示"""
        self.window['-FILESIZE-'].update('')
        self.window['-FORMAT-'].update('')
        self.window['-CODEC-'].update('')
        self.window['-ENCODER-'].update('')
        self.window['-SAMPLE-'].update('')
        self.window['-BITDEPTH-'].update('')
        self.window['-BITRATE-'].update('')
        self.window['-CHANNELS-'].update('')
        self.window['-DURATION-'].update('')
        self.window['-STREAMCOUNT-'].update('')
    
    def display_results(self, results):
        """
        显示分析结果
        
        Args:
            results: 分析结果字典
        """
        if results.get('error'):
            # 如果有错误，显示错误信息
            sg.popup_error(
                f"分析失败！\n\n错误信息：{results['error']}",
                title='分析错误',
                font=('微软雅黑', 10)
            )
            self.clear_results()
        else:
            # 显示正常结果
            self.window['-FILESIZE-'].update(results['file_size'])
            self.window['-FORMAT-'].update(results['format'])
            self.window['-CODEC-'].update(results['codec'])
            self.window['-ENCODER-'].update(results['encoder'])
            self.window['-SAMPLE-'].update(results['sample_rate'])
            self.window['-BITDEPTH-'].update(results['bit_depth'])
            self.window['-BITRATE-'].update(results['bit_rate'])
            self.window['-CHANNELS-'].update(results['channels'])
            self.window['-DURATION-'].update(results['duration'])
            self.window['-STREAMCOUNT-'].update(results['stream_count'])
    
    def analyze_file(self, file_path):
        """
        分析音频文件
        
        Args:
            file_path: 文件路径
        """
        if not file_path:
            sg.popup_warning('请先选择一个音频文件！', title='提示', font=('微软雅黑', 10))
            return
        
        if not os.path.exists(file_path):
            sg.popup_error('文件不存在！', title='错误', font=('微软雅黑', 10))
            return
        
        # 显示正在分析的提示（使用非阻塞窗口）
        sg.popup_animated(sg.DEFAULT_BASE64_LOADING_GIF, 
                          message='正在分析音频文件，请稍候...',
                          time_between_frames=100)
        
        # 执行分析
        results = self.analyzer.analyze(file_path)
        
        # 关闭加载动画
        sg.popup_animated(None)
        
        # 显示结果
        self.display_results(results)
    
    def run(self):
        """运行GUI主循环"""
        while True:
            event, values = self.window.read()
            
            # 窗口关闭或退出按钮
            if event in (sg.WIN_CLOSED, '退出'):
                break
            
            # 文件选择事件
            elif event == '-FILE-':
                # 用户选择了文件后自动清除之前的结果
                pass
            
            # 开始分析按钮
            elif event == '开始分析':
                file_path = values['-FILE-']
                self.analyze_file(file_path)
            
            # 清除结果按钮
            elif event == '清除结果':
                self.clear_results()
                self.window['-FILE-'].update('')
        
        # 关闭窗口
        self.window.close()


def main():
    """主函数"""
    try:
        app = AudioAnalyzerGUI()
        app.run()
    except Exception as e:
        sg.popup_error(
            f'程序启动失败：\n{str(e)}',
            title='错误',
            font=('微软雅黑', 10)
        )


if __name__ == '__main__':
    main()

