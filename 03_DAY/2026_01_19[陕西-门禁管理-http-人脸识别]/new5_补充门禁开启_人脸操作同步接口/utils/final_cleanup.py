# 最终清理，移动剩余的临时脚本到utils目录
import os
import shutil

# 设置当前目录
base_dir = r'e:\SOFTWARE_TEST_ENGINEER\6、练习题\卓望-联合永道\08_日常杂物\2026_01_19[陕西-门禁管理-http-人脸识别]\new2'
os.chdir(base_dir)

# 剩余的临时脚本
remaining_scripts = ['check_final_structure.py', 'create_utils_dir.py', 'list_structure.py', 'final_cleanup.py']
utils_dir = 'utils'

for script in remaining_scripts:
    if os.path.exists(script):
        new_path = os.path.join(utils_dir, script)
        if os.path.exists(new_path):
            os.remove(new_path)
        shutil.move(script, new_path)
        print(f"Moved {script} to {new_path}")

print("=== Final Directory Structure ===")
for root, dirs, files in os.walk('.'):
    rel_path = os.path.relpath(root, base_dir)
    if rel_path == '.':
        rel_path = ''
    
    level = rel_path.count(os.sep)
    indent = ' ' * 2 * level
    
    if rel_path:
        print(f"{indent}{os.path.basename(root)}/")
    else:
        print("./")
    
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        if not file.endswith('.pyc') and file != '__pycache__':
            print(f"{subindent}{file}")

print("=== Cleanup Complete ===")