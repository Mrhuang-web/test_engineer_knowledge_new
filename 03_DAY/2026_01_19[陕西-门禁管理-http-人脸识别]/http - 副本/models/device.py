# 设备相关数据存储

import json
import os
import time

class DeviceData:
    """设备数据管理类"""
    
    # 存储配置
    STORAGE_TYPE = 'file'  # 当前存储类型：file，预留：database, cache
    STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage', 'device.json')
    
    def __init__(self):
        # 初始化设备数据
        self._data = {
            'password': None,  # 初始无密码
            'disabled': False,  # 设备禁用状态，初始未禁用
            'busy': False,  # 设备忙碌状态，初始不忙碌
            'information': {
                'SDKVersion': '109',
                'cpuTemperature': '48',
                'cpuUsageRate': '37%',
                'deviceKey': 'E03C1CB214AC1801',
                'faceCount': '4',
                'fingerCount': '0',
                'freeDiskSpace': '5624M',
                'ip': '192.168.1.89',
                'languageType': 'zh_CN',
                'memoryUsageRate': '50%',
                'personCount': '7',
                'time': str(int(time.time() * 1000)),
                'timeZone': '',
                'version': 'GD-V216.2130'
            },
            'callbacks': {
                'identify': {
                    'url': '',
                    'base64Enable': 1
                },
                'imgReg': {
                    'url': '',
                    'base64Enable': 1
                },
                'event': {
                    'url': ''
                }
            },
            'doorStatus': 3,  # 3门磁闭合
            'system_time': int(time.time() * 1000),  # 系统时间，毫秒级时间戳
            'last_sync_time': None,  # 上次同步时间
            'network_available': False  # 是否有网络连接
        }
        
        # 加载数据
        self.load_data()
    
    def load_data(self):
        """从存储中加载数据"""
        if self.STORAGE_TYPE == 'file':
            try:
                if os.path.exists(self.STORAGE_PATH):
                    with open(self.STORAGE_PATH, 'r', encoding='utf-8') as f:
                        loaded_data = json.load(f)
                        self._data.update(loaded_data)
            except Exception as e:
                print(f"加载设备数据失败: {e}")
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
                    json.dump(self._data, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存设备数据失败: {e}")
        # 预留数据库或缓存保存逻辑
        elif self.STORAGE_TYPE == 'database':
            # 数据库保存逻辑
            pass
        elif self.STORAGE_TYPE == 'cache':
            # 缓存保存逻辑
            pass
    
    def get_password(self):
        """获取设备密码"""
        return self._data['password']
    
    def set_password(self, password):
        """设置设备密码"""
        self._data['password'] = password
        self.save_data()
    
    def get_information(self):
        """获取设备信息"""
        return self._data['information']
    
    def update_information(self, key, value):
        """更新设备信息"""
        if key in self._data['information']:
            self._data['information'][key] = value
            self.save_data()
    
    def get_callbacks(self):
        """获取回调配置"""
        return self._data['callbacks']
    
    def set_callback(self, callback_type, url, base64_enable=1):
        """设置回调地址"""
        if callback_type in self._data['callbacks']:
            # 验证URL格式
            import re
            if url and url.strip():
                # 回调URL正则表达式
                url_pattern = r'^((http|ftp|https)://)(([a-zA-Z0-9\._-]+\.[a-zA-Z]{2,6})|([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}))(:[0-9]{1,5})*(/[a-zA-Z0-9\&%_\./-~-]*)?$'
                if not re.match(url_pattern, url):
                    return False
            
            # 更新回调信息
            callback_info = self._data['callbacks'][callback_type]
            callback_info['url'] = url.strip() if url else ''
            if 'base64Enable' in callback_info:
                callback_info['base64Enable'] = int(base64_enable)
            
            # 保存数据
            self.save_data()
        return True
    
    def get_door_status(self):
        """获取门磁状态"""
        return self._data['doorStatus']
    
    def set_door_status(self, status):
        """设置门磁状态"""
        self._data['doorStatus'] = status
        self.save_data()
    
    def get_system_time(self):
        """获取系统时间"""
        return self._data['system_time']
    
    def set_system_time(self, timestamp):
        """设置系统时间"""
        self._data['system_time'] = int(timestamp)
        # 更新设备信息中的时间
        self._data['information']['time'] = str(int(timestamp))
        self.save_data()
    
    def update_time(self):
        """更新时间信息"""
        # 如果没有网络，时间按照设置的时间增长
        if not self._data['network_available']:
            # 增加1分钟的时间（60*1000毫秒）
            self._data['system_time'] += 60 * 1000
            self._data['information']['time'] = str(self._data['system_time'])
            self.save_data()
    
    def is_network_available(self):
        """检查网络是否可用"""
        return self._data['network_available']
    
    def set_network_available(self, available):
        """设置网络可用性"""
        self._data['network_available'] = available
        self.save_data()
    
    def is_disabled(self):
        """检查设备是否被禁用"""
        return self._data['disabled']
    
    def set_disabled(self, disabled):
        """设置设备禁用状态"""
        self._data['disabled'] = disabled
        self.save_data()
    
    def is_busy(self):
        """检查设备是否正忙"""
        return self._data['busy']
    
    def set_busy(self, busy):
        """设置设备忙碌状态"""
        self._data['busy'] = busy
        self.save_data()
    
    def get_last_sync_time(self):
        """获取上次同步时间"""
        return self._data['last_sync_time']
    
    def set_last_sync_time(self, timestamp):
        """设置上次同步时间"""
        self._data['last_sync_time'] = timestamp
        self.save_data()

# 创建设备数据实例
device_data = DeviceData()