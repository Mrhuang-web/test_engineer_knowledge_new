# 创建md目录并移动curl文档
import os
import shutil

# 设置当前目录为脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# 创建md目录
md_dir = 'md'
if not os.path.exists(md_dir):
    os.makedirs(md_dir)
    print(f"Created directory: {md_dir}")
else:
    print(f"Directory already exists: {md_dir}")

# 移动curl文档
curl_file = 'curl文档.md'
new_curl_path = os.path.join(md_dir, curl_file)
if os.path.exists(curl_file):
    if os.path.exists(new_curl_path):
        os.remove(new_curl_path)
    shutil.move(curl_file, new_curl_path)
    print(f"Moved {curl_file} to {new_curl_path}")
else:
    print(f"File not found: {curl_file}")

print("Operation completed successfully!")