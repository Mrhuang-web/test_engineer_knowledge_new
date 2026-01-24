# 设备状态管理

import json
import os
import time

class DeviceStatus:
    """设备状态管理类"""
    
    # 存储配置
    STORAGE_TYPE = 'file'  # 当前存储类型：file，预留：database, cache
    STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage', 'device_status.json')
    
    def __init__(self):
        # 初始状态设置
        self._status = {
            'is_first_setup': True,  # 是否首次设置
            'reset_count': 0,        # 重置次数
            'last_reset_time': None  # 最后重置时间
        }
        
        # 加载数据
        self.load_data()
    
    def load_data(self):
        """从存储中加载数据"""
        if self.STORAGE_TYPE == 'file':
            try:
                if os.path.exists(self.STORAGE_PATH):
                    with open(self.STORAGE_PATH, 'r', encoding='utf-8') as f:
                        self._status = json.load(f)
            except Exception as e:
                print(f"加载设备状态数据失败: {e}")
        # 预留数据库或缓存加载逻辑
        elif self.STORAGE_TYPE == 'database':
            # 数据库加载逻辑
            pass
        elif self.STORAGE_TYPE == 'cache':
            # 缓存加载逻辑
            pass
    
    def save_data(self):
        """将数据保存到存储中"""
        if self.STORAGE_TYPE == 'file':
            try:
                with open(self.STORAGE_PATH, 'w', encoding='utf-8') as f:
                    json.dump(self._status, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存设备状态数据失败: {e}")
        # 预留数据库或缓存保存逻辑
        elif self.STORAGE_TYPE == 'database':
            # 数据库保存逻辑
            pass
        elif self.STORAGE_TYPE == 'cache':
            # 缓存保存逻辑
            pass
    
    def is_first_setup(self):
        """检查是否首次设置"""
        return self._status['is_first_setup']
    
    def set_first_setup_completed(self):
        """设置首次设置完成"""
        self._status['is_first_setup'] = False
        self.save_data()
    
    def get_reset_count(self):
        """获取重置次数"""
        return self._status['reset_count']
    
    def increment_reset_count(self):
        """增加重置次数"""
        self._status['reset_count'] += 1
        self._status['last_reset_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        self.save_data()
    
    def get_last_reset_time(self):
        """获取最后重置时间"""
        return self._status['last_reset_time']
    
    def get_status(self):
        """获取完整状态"""
        return self._status.copy()

# 创建设备状态实例
device_status = DeviceStatus()