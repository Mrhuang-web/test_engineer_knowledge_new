# 列出最终目录结构
import os

# 设置当前目录
base_dir = r'e:\SOFTWARE_TEST_ENGINEER\6、练习题\卓望-联合永道\08_日常杂物\2026_01_19[陕西-门禁管理-http-人脸识别]\new2'

print("=== Final Directory Structure ===")
for root, dirs, files in os.walk(base_dir):
    # 计算相对路径
    rel_path = os.path.relpath(root, base_dir)
    if rel_path == '.':
        rel_path = ''
    
    level = rel_path.count(os.sep)
    indent = ' ' * 2 * level
    
    # 打印目录名
    if rel_path:
        print(f"{indent}{os.path.basename(root)}/")
    else:
        print("./")
    
    subindent = ' ' * 2 * (level + 1)
    # 打印文件名
    for file in files:
        if not file.endswith('.pyc') and file != '__pycache__':
            print(f"{subindent}{file}")

print("=== Check Complete ===")