# 日志配置文件

log_config = {
    # 日志开关，True开启日志记录，False关闭日志记录
    'log_enabled': True,
    
    # 日志目录，相对于项目根目录
    'log_dir': 'logs',
    
    # 日志文件名
    'log_filename': 'mockserver.log',
    
    # 文件日志级别，可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL
    'file_log_level': 'DEBUG',
    
    # 控制台日志开关
    'console_log_enabled': True,
    
    # 控制台日志级别，可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL
    'console_log_level': 'INFO',
    
    # 日志格式
    'log_format': '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
    
    # 控制台日志格式
    'console_log_format': '%(asctime)s - %(levelname)s - %(message)s',
    
    # 日志文件最大大小，单位：字节，默认10MB
    'max_bytes': 10 * 1024 * 1024,
    
    # 备份日志文件数量
    'backup_count': 5
}
