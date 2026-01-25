# 日志配置文件
# 定义日志的各项配置参数
import os

# 获取项目根目录
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_config = {
    # 是否启用日志
    'log_enabled': True,
    # 日志目录（使用绝对路径）
    'log_dir': os.path.join(project_root, 'logs'),
    # 日志文件名
    'log_filename': 'mockserver.log',
    # 日志格式
    'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    # 文件日志级别
    'file_log_level': 'INFO',
    # 控制台日志是否启用
    'console_log_enabled': True,
    # 控制台日志格式
    'console_log_format': '%(asctime)s - %(levelname)s - %(message)s',
    # 控制台日志级别
    'console_log_level': 'INFO',
    # 日志文件最大字节数
    'max_bytes': 10485760,  # 10MB
    # 日志文件备份数量
    'backup_count': 5
}