# 创建utils目录并移动工具脚本
import os
import shutil

# 设置当前目录为脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

# 创建utils目录
utils_dir = 'utils'
if not os.path.exists(utils_dir):
    os.makedirs(utils_dir)
    print(f"Created directory: {utils_dir}")
else:
    print(f"Directory already exists: {utils_dir}")

# 要移动的工具脚本列表
tool_scripts = ['create_dirs.py', 'rename_dirs.py', 'create_md_dir.py']

for script in tool_scripts:
    script_path = os.path.join(current_dir, script)
    new_script_path = os.path.join(utils_dir, script)
    if os.path.exists(script_path):
        if os.path.exists(new_script_path):
            os.remove(new_script_path)
        shutil.move(script_path, new_script_path)
        print(f"Moved {script} to {new_script_path}")
    else:
        print(f"File not found: {script}")

print("Operation completed successfully!")