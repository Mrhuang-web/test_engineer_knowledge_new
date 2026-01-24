# 运行热启动测试脚本
import os
import subprocess

# 获取当前脚本所在目录
script_dir = os.path.dirname(os.path.abspath(__file__))

# 切换到脚本目录
os.chdir(script_dir)

# 运行测试脚本
print(f"Running hot restart test from {script_dir}...")
subprocess.run(['python', 'test_hot_restart.py'])
