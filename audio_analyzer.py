"""
音频分析模块 - 使用ffprobe分析音频文件
"""
import subprocess
import json
import os
from pathlib import Path


class AudioAnalyzer:
    """音频分析器类，使用ffprobe获取音频文件信息"""
    
    def __init__(self, ffprobe_path="ffprobe.exe"):
        """
        初始化音频分析器
        
        Args:
            ffprobe_path: ffprobe可执行文件的路径
        """
        self.ffprobe_path = ffprobe_path
        
        # 检查ffprobe是否存在
        if not os.path.exists(self.ffprobe_path):
            raise FileNotFoundError(f"找不到ffprobe: {self.ffprobe_path}")
    
    def analyze(self, audio_file):
        """
        分析音频文件
        
        Args:
            audio_file: 音频文件路径
            
        Returns:
            dict: 包含音频信息的字典，包括：
                - format: 音频格式
                - sample_rate: 采样率
                - bit_rate: 比特率
                - duration: 时长
                - channels: 声道数
                - codec: 编码格式
                - error: 错误信息（如果有）
        """
        result = {
            'format': '未知',
            'sample_rate': '未知',
            'bit_rate': '未知',
            'duration': '未知',
            'channels': '未知',
            'codec': '未知',
            'file_size': '未知',
            'encoder': '未知',
            'bit_depth': '未知',
            'stream_count': '未知',
            'error': None
        }
        
        # 检查文件是否存在
        if not os.path.exists(audio_file):
            result['error'] = '文件不存在'
            return result
        
        try:
            # 构建ffprobe命令
            # 使用-v quiet隐藏警告信息
            # 使用-print_format json输出json格式
            # 使用-show_format显示格式信息
            # 使用-show_streams显示流信息
            cmd = [
                self.ffprobe_path,
                '-v', 'quiet',
                '-print_format', 'json',
                '-show_format',
                '-show_streams',
                audio_file
            ]
            
            # 执行命令，设置超时防止卡死
            # 使用CREATE_NO_WINDOW标志在Windows上隐藏控制台窗口
            startupinfo = None
            if os.name == 'nt':  # Windows系统
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                startupinfo.wShowWindow = subprocess.SW_HIDE
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                startupinfo=startupinfo
            )
            
            stdout, stderr = process.communicate(timeout=10)
            
            # 检查是否执行成功
            if process.returncode != 0:
                result['error'] = '不是有效的音频文件或格式不支持'
                return result
            
            # 解析JSON输出
            data = json.loads(stdout.decode('utf-8'))
            
            # 检查是否有音频流
            if 'streams' not in data or len(data['streams']) == 0:
                result['error'] = '文件中没有音频流'
                return result
            
            # 查找音频流（可能有多个流，我们取第一个音频流）
            audio_stream = None
            for stream in data['streams']:
                if stream.get('codec_type') == 'audio':
                    audio_stream = stream
                    break
            
            if not audio_stream:
                result['error'] = '文件中没有音频流'
                return result
            
            # 提取音频信息
            # 编码格式
            result['codec'] = audio_stream.get('codec_name', '未知').upper()
            
            # 编码器信息
            encoder = audio_stream.get('tags', {}).get('encoder')
            if not encoder and 'format' in data:
                encoder = data['format'].get('tags', {}).get('encoder')
            if encoder:
                result['encoder'] = encoder
            
            # 位深度（采样位深）
            bits_per_sample = audio_stream.get('bits_per_sample')
            bits_per_raw_sample = audio_stream.get('bits_per_raw_sample')
            if bits_per_sample and bits_per_sample > 0:
                result['bit_depth'] = f"{bits_per_sample} bit"
            elif bits_per_raw_sample and bits_per_raw_sample > 0:
                result['bit_depth'] = f"{bits_per_raw_sample} bit"
            
            # 采样率
            sample_rate = audio_stream.get('sample_rate', '未知')
            if sample_rate != '未知':
                result['sample_rate'] = f"{int(sample_rate)} Hz"
            
            # 比特率
            bit_rate = audio_stream.get('bit_rate')
            if not bit_rate and 'format' in data:
                bit_rate = data['format'].get('bit_rate')
            if bit_rate:
                result['bit_rate'] = f"{int(bit_rate) // 1000} kbps"
            
            # 声道数
            channels = audio_stream.get('channels')
            if channels:
                channel_names = {1: '单声道', 2: '立体声', 6: '5.1声道', 8: '7.1声道'}
                result['channels'] = channel_names.get(channels, f"{channels}声道")
            
            # 时长和格式信息
            if 'format' in data:
                duration = data['format'].get('duration')
                if duration:
                    duration_sec = float(duration)
                    minutes = int(duration_sec // 60)
                    seconds = int(duration_sec % 60)
                    result['duration'] = f"{minutes}分{seconds}秒"
                
                # 格式名称
                format_name = data['format'].get('format_name', '').upper()
                if format_name:
                    result['format'] = format_name
                
                # 流数量
                nb_streams = data['format'].get('nb_streams')
                if nb_streams:
                    result['stream_count'] = f"{nb_streams}个流"
            
            # 文件大小
            try:
                file_size_bytes = os.path.getsize(audio_file)
                if file_size_bytes < 1024:
                    result['file_size'] = f"{file_size_bytes} B"
                elif file_size_bytes < 1024 * 1024:
                    result['file_size'] = f"{file_size_bytes / 1024:.2f} KB"
                elif file_size_bytes < 1024 * 1024 * 1024:
                    result['file_size'] = f"{file_size_bytes / (1024 * 1024):.2f} MB"
                else:
                    result['file_size'] = f"{file_size_bytes / (1024 * 1024 * 1024):.2f} GB"
            except Exception:
                pass
            
            return result
            
        except subprocess.TimeoutExpired:
            result['error'] = '分析超时，文件可能已损坏'
            return result
        except json.JSONDecodeError:
            result['error'] = '解析ffprobe输出失败'
            return result
        except Exception as e:
            result['error'] = f'分析出错: {str(e)}'
            return result


def test_analyzer():
    """测试函数"""
    analyzer = AudioAnalyzer()
    
    # 测试一个示例文件
    test_file = "test.mp3"  # 替换为实际的测试文件
    if os.path.exists(test_file):
        result = analyzer.analyze(test_file)
        print("分析结果:")
        for key, value in result.items():
            print(f"  {key}: {value}")


if __name__ == "__main__":
    test_analyzer()

