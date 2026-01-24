import os
import sys

# 获取当前脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 要创建的目录列表
dirs = ['data', 'business', 'dict', 'config']

for dir_name in dirs:
    dir_path = os.path.join(current_dir, dir_name)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Created directory: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")

print("All directories created successfully!")