# 目录重命名脚本
import os
import shutil
import sys

# 设置当前目录为脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 目录重命名映射
# 原目录名: 新目录名
dir_mapping = {
    'config': 'configs',            # 配置目录
    'dict': 'dictionaries',        # 字典目录
    'data': 'datastore',           # 数据目录
    'business': 'business_logic'    # 业务目录
}

# 执行目录重命名
for old_dir, new_dir in dir_mapping.items():
    if os.path.exists(old_dir):
        # 如果新目录已存在，先删除
        if os.path.exists(new_dir):
            shutil.rmtree(new_dir)
        
        # 重命名目录
        shutil.move(old_dir, new_dir)
        print(f"Renamed directory: {old_dir} -> {new_dir}")
    else:
        print(f"Directory not found: {old_dir}")

# 更新主程序中的导入路径
main_file = 'mockserver.py'
if os.path.exists(main_file):
    with open(main_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新导入路径
    content = content.replace('from config.url_config', 'from configs.url_config')
    content = content.replace('from config.param_config', 'from configs.param_config')
    content = content.replace('from dict.code_dict', 'from dictionaries.code_dict')
    content = content.replace('from data.data_store', 'from datastore.data_store')
    
    with open(main_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated import paths in {main_file}")

# 更新业务目录中的导入路径
business_files = ['device.py', 'person.py', 'face.py', 'record.py']
for file_name in business_files:
    old_path = os.path.join('business_logic', file_name)
    if os.path.exists(old_path):
        with open(old_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 更新导入路径
        content = content.replace('from data.data_store', 'from datastore.data_store')
        content = content.replace('from dict.code_dict', 'from dictionaries.code_dict')
        
        with open(old_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated import paths in {old_path}")

print("All directories renamed and import paths updated successfully!")