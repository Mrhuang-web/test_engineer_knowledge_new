# 数据存储模块
# 处理各个接口带来的数据逻辑

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
    
    # 设备密码管理
    def set_password(self, password):
        """设置设备密码"""
        self.device_pass = password
    
    def get_password(self):
        """获取设备密码"""
        return self.device_pass
    
    def verify_password(self, password):
        """验证设备密码"""
        return self.device_pass is not None and self.device_pass == password
    
    # 设备时间管理
    def set_device_time(self, time_str):
        """设置设备时间"""
        self.device_time = time_str
    
    def get_device_time(self):
        """获取设备时间"""
        return self.device_time
    
    def set_device_timestamp(self, timestamp):
        """设置设备时间戳（毫秒级）"""
        self.device_timestamp = timestamp
    
    def get_device_timestamp(self):
        """获取设备时间戳（毫秒级）"""
        return self.device_timestamp
    
    # 人员信息管理
    def create_person(self, person_id, person_info):
        """创建人员信息"""
        if person_id in self.persons:
            return False
        self.persons[person_id] = person_info
        return True
    
    def delete_person(self, person_id):
        """删除人员信息"""
        if person_id == '-1':
            # 删除所有人员
            self.persons.clear()
            # 同时删除所有照片
            self.faces.clear()
            return True
        
        if person_id in self.persons:
            del self.persons[person_id]
            # 同时删除该人员的所有照片
            faces_to_delete = [face_id for face_id, face_info in self.faces.items() if face_info['personId'] == person_id]
            for face_id in faces_to_delete:
                del self.faces[face_id]
            return True
        return False
    
    def update_person(self, person_id, person_info):
        """更新人员信息"""
        if person_id in self.persons:
            self.persons[person_id].update(person_info)
            return True
        return False
    
    def get_person(self, person_id):
        """获取人员信息"""
        if person_id == '-1':
            return list(self.persons.values())
        return self.persons.get(person_id)
    
    def get_all_persons(self):
        """获取所有人员信息"""
        return list(self.persons.values())
    
    def get_person_by_page(self, page=0, page_size=1000):
        """分页获取人员信息"""
        person_list = list(self.persons.values())
        start = page * page_size
        end = start + page_size
        return person_list[start:end]
    
    # 照片信息管理
    def create_face(self, face_id, face_info):
        """创建照片信息"""
        if face_id in self.faces:
            return False
        
        # 检查该人员的照片数量是否超过3张
        person_id = face_info['personId']
        person_faces = [f for f in self.faces.values() if f['personId'] == person_id]
        if len(person_faces) >= 3:
            return False
        
        self.faces[face_id] = face_info
        return True
    
    def delete_face(self, face_id):
        """删除照片信息"""
        if face_id in self.faces:
            del self.faces[face_id]
            return True
        return False
    
    def update_face(self, face_id, face_info):
        """更新照片信息"""
        if face_id in self.faces:
            self.faces[face_id].update(face_info)
            return True
        return False
    
    def get_face(self, face_id):
        """获取照片信息"""
        return self.faces.get(face_id)
    
    def get_faces_by_person(self, person_id):
        """获取指定人员的所有照片"""
        return [face_info for face_info in self.faces.values() if face_info['personId'] == person_id]
    
    def delete_person_faces(self, person_id):
        """删除指定人员的所有照片"""
        if person_id not in self.persons:
            return False
        
        faces_to_delete = [face_id for face_id, face_info in self.faces.items() if face_info['personId'] == person_id]
        for face_id in faces_to_delete:
            del self.faces[face_id]
        return True
    
    # 识别记录管理
    def add_record(self, record):
        """添加识别记录"""
        self.records.append(record)
    
    def get_records(self, person_id=None, start_time=None, end_time=None, page=0, page_size=1000):
        """获取识别记录"""
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
        if person_id == '-1':
            # 删除所有记录
            self.records.clear()
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
        return True
    
    # 回调管理
    def set_identify_callback(self, callback_url):
        """设置识别回调"""
        self.callbacks['identify'] = callback_url
    
    def set_img_reg_callback(self, callback_url):
        """设置照片注册回调"""
        self.callbacks['img_reg'] = callback_url
    
    def set_event_callback(self, callback_url):
        """设置事件回调"""
        self.callbacks['event'] = callback_url
    
    def get_callback(self, callback_type):
        """获取回调地址"""
        return self.callbacks.get(callback_type)
    
    # 信号输入配置管理
    def set_signal_input_config(self, input_no, config):
        """设置信号输入配置"""
        self.signal_inputs[input_no] = config
    
    def get_signal_input_config(self, input_no=None):
        """获取信号输入配置
        如果input_no为None，则返回所有配置
        """
        if input_no is None:
            return self.signal_inputs
        return self.signal_inputs.get(input_no)

# 创建全局数据存储实例
data_store = DataStore()