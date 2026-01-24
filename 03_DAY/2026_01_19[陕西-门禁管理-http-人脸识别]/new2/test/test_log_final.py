import logging
import os
import time

# 清除已有的日志处理器
logger = logging.getLogger()
for handler in logger.handlers[:]:
    logger.removeHandler(handler)

# 手动配置日志
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# 配置日志格式
file_format = '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
console_format = '%(asctime)s - %(levelname)s - %(message)s'

file_formatter = logging.Formatter(file_format)
console_formatter = logging.Formatter(console_format)

# 创建文件日志处理器
file_handler = logging.handlers.RotatingFileHandler(
    'logs/mockserver.log',
    maxBytes=10*1024*1024,
    backupCount=5,
    encoding='utf-8'
)
file_handler.setFormatter(file_formatter)
file_handler.setLevel(logging.DEBUG)  # 日志文件记录DEBUG及以上

# 创建控制台日志处理器
console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)
console_handler.setLevel(logging.INFO)  # 控制台输出INFO及以上

# 配置根日志记录器
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 测试不同级别的日志输出
print("=== 测试日志功能 ===")
print("控制台应只显示INFO及以上级别的日志，日志文件应记录所有级别（包括DEBUG）")
print("\n正在记录日志...")

# 记录不同级别的日志
logger.debug("这是一条DEBUG级别的日志")
logger.info("这是一条INFO级别的日志")
logger.warning("这是一条WARNING级别的日志")
logger.error("这是一条ERROR级别的日志")
logger.critical("这是一条CRITICAL级别的日志")

# 等待日志写入
time.sleep(1)

# 检查日志文件
print("\n=== 检查日志文件 ===")
log_file = 'logs/mockserver.log'
if os.path.exists(log_file):
    print(f"✓ 日志文件已生成: {log_file}")
    print(f"  大小: {os.path.getsize(log_file)} 字节")
    
    # 读取日志文件内容（使用utf-8编码）
    with open(log_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查不同级别的日志
    debug_found = 'DEBUG' in content
    info_found = 'INFO' in content
    warning_found = 'WARNING' in content
    error_found = 'ERROR' in content
    critical_found = 'CRITICAL' in content
    
    print(f"  ✓ DEBUG日志: {'找到' if debug_found else '未找到'}")
    print(f"  ✓ INFO日志: {'找到' if info_found else '未找到'}")
    print(f"  ✓ WARNING日志: {'找到' if warning_found else '未找到'}")
    print(f"  ✓ ERROR日志: {'找到' if error_found else '未找到'}")
    print(f"  ✓ CRITICAL日志: {'找到' if critical_found else '未找到'}")
    
    if debug_found:
        print("  ✓ 日志文件记录了DEBUG级别的日志")
    else:
        print("  ✗ 日志文件未记录DEBUG级别的日志")
else:
    print(f"✗ 日志文件不存在: {log_file}")

print("\n=== 测试完成！ ===")
