# 数据存储配置文件

storage_config = {
    # 数据存储开关
    # False: 使用内存存储（默认）
    # True: 使用JSON文件存储
    'use_json_storage': False,
    
    # JSON文件存储路径，相对于项目根目录
    'json_storage_dir': 'data',
    
    # 各数据类型对应的JSON文件名
    'json_files': {
        'device_pass': 'device_pass.json',
        'persons': 'persons.json',
        'faces': 'faces.json',
        'records': 'records.json',
        'callbacks': 'callbacks.json',
        'device_time': 'device_time.json',
        'signal_inputs': 'signal_inputs.json'
    }
}