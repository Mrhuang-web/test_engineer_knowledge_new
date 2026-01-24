# 简单测试脚本：测试日志功能
import logging
import os
import time

# 导入日志配置和初始化函数
import sys
sys.path.append('.')
from configs.log_config import log_config

# 模拟日志初始化
import logging
from logging.handlers import RotatingFileHandler

def init_logger_test():
    """初始化日志系统（测试版本）"""
    # 清除已有的日志处理器
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    if not log_config['log_enabled']:
        logging.basicConfig(level=logging.CRITICAL)
        return
    
    # 创建日志目录
    log_dir = log_config['log_dir']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志格式
    file_formatter = logging.Formatter(log_config['log_format'])
    console_formatter = logging.Formatter(log_config['console_log_format'])
    
    # 创建文件日志处理器
    log_file = os.path.join(log_dir, log_config['log_filename'])
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=log_config['max_bytes'],
        backupCount=log_config['backup_count'],
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(getattr(logging, log_config['file_log_level']))
    
    # 配置根日志记录器
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    
    # 添加控制台日志处理器
    if log_config['console_log_enabled']:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(getattr(logging, log_config['console_log_level']))
        logger.addHandler(console_handler)

# 初始化日志
init_logger_test()
logger = logging.getLogger(__name__)

# 测试不同级别的日志输出
print("=== 测试不同级别的日志输出 ===")
print("控制台应只显示INFO及以上级别的日志，日志文件应记录所有级别（包括DEBUG）")

# 记录不同级别的日志
logger.debug("这是一条DEBUG级别的日志")
logger.info("这是一条INFO级别的日志")
logger.warning("这是一条WARNING级别的日志")
logger.error("这是一条ERROR级别的日志")
logger.critical("这是一条CRITICAL级别的日志")

# 等待日志写入
time.sleep(1)

# 检查日志文件内容
log_file = 'logs/mockserver.log'
print(f"\n=== 检查日志文件内容：{log_file} ===")

if os.path.exists(log_file):
    print(f"日志文件已生成，大小：{os.path.getsize(log_file)} 字节")
    
    # 统计不同级别的日志数量
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    debug_count = content.count('DEBUG')
    info_count = content.count('INFO')
    warning_count = content.count('WARNING')
    error_count = content.count('ERROR')
    critical_count = content.count('CRITICAL')
    
    print(f"DEBUG日志数量：{debug_count}")
    print(f"INFO日志数量：{info_count}")
    print(f"WARNING日志数量：{warning_count}")
    print(f"ERROR日志数量：{error_count}")
    print(f"CRITICAL日志数量：{critical_count}")
    
    if debug_count > 0:
        print("✓ 日志文件记录了DEBUG级别的日志")
    else:
        print("✗ 日志文件未记录DEBUG级别的日志")
else:
    print("✗ 日志文件未生成")

print("\n=== 测试完成！ ===")
