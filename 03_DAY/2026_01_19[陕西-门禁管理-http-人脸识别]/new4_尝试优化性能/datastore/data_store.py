# 数据存储模块
# 处理各个接口带来的数据逻辑

import json
import os
import time
import threading
import concurrent.futures
from configs.storage_config import storage_config

class DataStore:
    def __init__(self):
        # 初始化数据存储
        self.device_pass = None  # 设备密码
        self.persons = {}  # 人员信息，key为personId
        self.faces = {}  # 照片信息，key为faceId
        self.records = []  # 识别记录
        self.callbacks = {
            'identify': None,  # 识别回调
            'img_reg': None,  # 照片注册回调
            'event': None  # 事件回调
        }
        self.device_time = None  # 设备时间
        self.device_timestamp = None  # 设备设置的毫秒级时间戳
        self.signal_inputs = {}  # 信号输入配置，key为inputNo
        
        # 为每个数据结构添加独立的锁，使用细粒度锁提高并发性能
        self._pass_lock = threading.RLock()
        self._persons_lock = threading.RLock()
        self._faces_lock = threading.RLock()
        self._records_lock = threading.RLock()
        self._callbacks_lock = threading.RLock()
        self._time_lock = threading.RLock()
        self._signal_lock = threading.RLock()
        
        # 初始化JSON存储目录
        self.json_storage_dir = storage_config['json_storage_dir']
        if not os.path.exists(self.json_storage_dir):
            os.makedirs(self.json_storage_dir)
        
        # 创建线程池用于异步JSON写入，减少I/O阻塞
        self._executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        
        # 如果启用JSON存储，从文件加载数据
        if storage_config['use_json_storage']:
            self._load_all_data_from_json()
    
    def _get_json_file_path(self, data_type):
        """获取JSON文件路径"""
        filename = storage_config['json_files'].get(data_type)
        if not filename:
            return None
        return os.path.join(self.json_storage_dir, filename)
    
    def _save_to_json(self, data_type, data):
        """保存数据到JSON文件（异步执行，减少I/O阻塞）"""
        if not storage_config['use_json_storage']:
            # 内存存储模式下，仅在调试模式下打印数据状态
            # 移除不必要的打印，减少I/O开销
            return
        
        def _write_json():
            """实际执行JSON写入的内部函数"""
            file_path = self._get_json_file_path(data_type)
            if not file_path:
                return
            
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)  # 移除indent=2，使用紧凑格式
            except Exception as e:
                print(f"保存{data_type}到JSON文件失败: {e}")
        
        # 使用线程池异步执行JSON写入，不阻塞主线程
        self._executor.submit(_write_json)
    
    def _load_from_json(self, data_type, default=None):
        """从JSON文件加载数据"""
        file_path = self._get_json_file_path(data_type)
        if not file_path or not os.path.exists(file_path):
            return default
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"从JSON文件加载{data_type}失败: {e}")
            return default
    
    def _load_all_data_from_json(self):
        """从JSON文件加载所有数据"""
        # 加载数据时需要锁定所有数据结构
        with self._pass_lock, self._persons_lock, self._faces_lock, self._records_lock, self._callbacks_lock, self._time_lock, self._signal_lock:
            self.device_pass = self._load_from_json('device_pass', None)
            self.persons = self._load_from_json('persons', {})
            self.faces = self._load_from_json('faces', {})
            self.records = self._load_from_json('records', [])
            self.callbacks = self._load_from_json('callbacks', {
                'identify': None,
                'img_reg': None,
                'event': None
            })
            self.device_time = self._load_from_json('device_time', None)
            self.signal_inputs = self._load_from_json('signal_inputs', {})
    
    # 设备密码管理
    def set_password(self, password):
        """设置设备密码"""
        with self._pass_lock:
            self.device_pass = password
            self._save_to_json('device_pass', self.device_pass)
    
    def get_password(self):
        """获取设备密码"""
        with self._pass_lock:
            return self.device_pass
    
    def verify_password(self, password):
        """验证设备密码"""
        with self._pass_lock:
            return self.device_pass is not None and self.device_pass == password
    
    # 设备时间管理
    def set_device_time(self, time_str):
        """设置设备时间"""
        with self._time_lock:
            self.device_time = time_str
            self._save_to_json('device_time', {
                'device_time': self.device_time,
                'device_timestamp': self.device_timestamp
            })
    
    def get_device_time(self):
        """获取设备时间"""
        with self._time_lock:
            return self.device_time
    
    def set_device_timestamp(self, timestamp):
        """设置设备时间戳（毫秒级）"""
        with self._time_lock:
            self.device_timestamp = timestamp
            self._save_to_json('device_time', {
                'device_time': self.device_time,
                'device_timestamp': self.device_timestamp
            })
    
    def get_device_timestamp(self):
        """获取设备时间戳（毫秒级）"""
        with self._time_lock:
            return self.device_timestamp
    
    # 人员信息管理
    def create_person(self, person_id, person_info):
        """创建人员信息"""
        with self._persons_lock:
            if person_id in self.persons:
                return False
            self.persons[person_id] = person_info
            self._save_to_json('persons', self.persons)
            return True
    
    def delete_person(self, person_id):
        """删除人员信息"""
        # 需要同时操作persons和faces，所以需要同时锁定两个锁
        with self._persons_lock, self._faces_lock:
            if person_id == '-1':
                # 删除所有人员
                self.persons.clear()
                # 同时删除所有照片
                self.faces.clear()
                self._save_to_json('persons', self.persons)
                self._save_to_json('faces', self.faces)
                return True
            
            if person_id in self.persons:
                del self.persons[person_id]
                # 同时删除该人员的所有照片
                faces_to_delete = [face_id for face_id, face_info in self.faces.items() if face_info['personId'] == person_id]
                for face_id in faces_to_delete:
                    del self.faces[face_id]
                self._save_to_json('persons', self.persons)
                self._save_to_json('faces', self.faces)
                return True
            return False
    
    def update_person(self, person_id, person_info):
        """更新人员信息"""
        with self._persons_lock:
            if person_id in self.persons:
                self.persons[person_id].update(person_info)
                self._save_to_json('persons', self.persons)
                return True
            return False
    
    def get_person(self, person_id):
        """获取人员信息"""
        with self._persons_lock:
            if person_id == '-1':
                return list(self.persons.values())
            return self.persons.get(person_id)
    
    def get_all_persons(self):
        """获取所有人员信息"""
        with self._persons_lock:
            return list(self.persons.values())
    
    def get_person_by_page(self, page=0, page_size=1000):
        """分页获取人员信息"""
        with self._persons_lock:
            person_list = list(self.persons.values())
            start = page * page_size
            end = start + page_size
            return person_list[start:end]
    
    # 照片信息管理
    def create_face(self, face_id, face_info):
        """创建照片信息"""
        with self._faces_lock:
            if face_id in self.faces:
                return False
            
            # 检查该人员的照片数量是否超过3张
            person_id = face_info['personId']
            person_faces = [f for f in self.faces.values() if f['personId'] == person_id]
            if len(person_faces) >= 3:
                return False
            
            self.faces[face_id] = face_info
            self._save_to_json('faces', self.faces)
            return True
    
    def delete_face(self, face_id):
        """删除照片信息"""
        with self._faces_lock:
            if face_id in self.faces:
                del self.faces[face_id]
                self._save_to_json('faces', self.faces)
                return True
            return False
    
    def update_face(self, face_id, face_info):
        """更新照片信息"""
        with self._faces_lock:
            if face_id in self.faces:
                self.faces[face_id].update(face_info)
                self._save_to_json('faces', self.faces)
                return True
            return False
    
    def get_face(self, face_id):
        """获取照片信息"""
        with self._faces_lock:
            return self.faces.get(face_id)
    
    def get_faces_by_person(self, person_id):
        """获取指定人员的所有照片"""
        with self._faces_lock:
            return [face_info for face_info in self.faces.values() if face_info['personId'] == person_id]
    
    def delete_person_faces(self, person_id):
        """删除指定人员的所有照片"""
        with self._faces_lock:
            if person_id not in self.persons:
                return False
            
            faces_to_delete = [face_id for face_id, face_info in self.faces.items() if face_info['personId'] == person_id]
            for face_id in faces_to_delete:
                del self.faces[face_id]
            self._save_to_json('faces', self.faces)
            return True
    
    # 识别记录管理
    def add_record(self, record):
        """添加识别记录"""
        with self._records_lock:
            self.records.append(record)
            self._save_to_json('records', self.records)
    
    def get_records(self, person_id=None, start_time=None, end_time=None, page=0, page_size=1000):
        """获取识别记录"""
        with self._records_lock:
            filtered_records = self.records
            
            if person_id and person_id != '-1' and person_id != 'STRANGERBABY':
                filtered_records = [r for r in filtered_records if r['personId'] == person_id]
            elif person_id == 'STRANGERBABY':
                filtered_records = [r for r in filtered_records if r['personId'] == 'STRANGERBABY']
            
            # 时间过滤（简化处理）
            if start_time and start_time != '0' and end_time and end_time != '0':
                filtered_records = [r for r in filtered_records if start_time <= r['time'] <= end_time]
            
            # 分页
            start = page * page_size
            end = start + page_size
            return filtered_records[start:end]
    
    def delete_records(self, person_id=None, start_time=None, end_time=None):
        """删除识别记录"""
        with self._records_lock:
            if person_id == '-1':
                # 删除所有记录
                self.records.clear()
                self._save_to_json('records', self.records)
                return True
            
            # 保留不符合删除条件的记录
            filtered_records = []
            for record in self.records:
                if person_id and person_id != 'STRANGERBABY' and record['personId'] != person_id:
                    filtered_records.append(record)
                elif person_id == 'STRANGERBABY' and record['personId'] != 'STRANGERBABY':
                    filtered_records.append(record)
                elif start_time and start_time != '0' and end_time and end_time != '0':
                    if not (start_time <= record['time'] <= end_time):
                        filtered_records.append(record)
                else:
                    filtered_records.append(record)
            
            self.records = filtered_records
            self._save_to_json('records', self.records)
            return True
    
    # 回调管理
    def set_identify_callback(self, callback_url):
        """设置识别回调"""
        with self._callbacks_lock:
            self.callbacks['identify'] = callback_url
            self._save_to_json('callbacks', self.callbacks)
    
    def set_img_reg_callback(self, callback_url):
        """设置照片注册回调"""
        with self._callbacks_lock:
            self.callbacks['img_reg'] = callback_url
            self._save_to_json('callbacks', self.callbacks)
    
    def set_event_callback(self, callback_url):
        """设置事件回调"""
        with self._callbacks_lock:
            self.callbacks['event'] = callback_url
            self._save_to_json('callbacks', self.callbacks)
    
    def get_callback(self, callback_type):
        """获取回调地址"""
        with self._callbacks_lock:
            return self.callbacks.get(callback_type)
    
    # 信号输入配置管理
    def set_signal_input_config(self, input_no, config):
        """设置信号输入配置"""
        with self._signal_lock:
            self.signal_inputs[input_no] = config
            self._save_to_json('signal_inputs', self.signal_inputs)
    
    def get_signal_input_config(self, input_no=None):
        """获取信号输入配置
        如果input_no为None，则返回所有配置
        """
        with self._signal_lock:
            if input_no is None:
                return self.signal_inputs
            return self.signal_inputs.get(input_no)

# 创建全局数据存储实例
data_store = DataStore()