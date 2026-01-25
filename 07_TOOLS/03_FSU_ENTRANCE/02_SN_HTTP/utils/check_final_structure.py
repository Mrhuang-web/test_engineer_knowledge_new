# 检查最终目录结构
import os

# 设置当前目录为脚本所在目录
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)

print("=== Final Directory Structure ===")
for root, dirs, files in os.walk('.'):
    # 跳过隐藏目录
    if any(name.startswith('.') for name in root.split(os.sep)):
        continue
    level = root.replace('.', '').count(os.sep)
    indent = ' ' * 2 * level
    print(f"{indent}{os.path.basename(root)}/")
    subindent = ' ' * 2 * (level + 1)
    for file in files:
        # 跳过.pyc文件和__pycache__目录
        if file.endswith('.pyc') or file == '__pycache__':
            continue
        print(f"{subindent}{file}")
print("=== Check Complete ===")