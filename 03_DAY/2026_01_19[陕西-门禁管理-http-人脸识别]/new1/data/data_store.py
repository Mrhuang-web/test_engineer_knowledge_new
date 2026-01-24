#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据存储模块，负责JSON格式的数据存储和读取
"""

import json
import os
import uuid
from datetime import datetime

class JSONDataStore:
    """JSON数据存储类"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.ensure_dir_exists()
        
        # 初始化数据文件路径
        self.device_file = os.path.join(self.data_dir, "device.json")
        self.persons_file = os.path.join(self.data_dir, "persons.json")
        self.faces_file = os.path.join(self.data_dir, "faces.json")
        self.records_file = os.path.join(self.data_dir, "records.json")
        self.callbacks_file = os.path.join(self.data_dir, "callbacks.json")
        
        # 初始化数据结构
        self.initialize_data()
    
    def ensure_dir_exists(self):
        """确保数据目录存在"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def initialize_data(self):
        """初始化数据文件"""
        # 初始化设备数据
        if not os.path.exists(self.device_file):
            device_data = {
                "device_info": {
                    "deviceId": "84E0F420893301FA",
                    "sdkVersion": "V4.0.20",
                    "cpuTemp": "45°C",
                    "serialNumber": "SN1234567890"
                },
                "device_password": "12345678",
                "door_sensor": 3  # 2开启，3闭合
            }
            self.save_json(self.device_file, device_data)
        
        # 初始化人员数据
        if not os.path.exists(self.persons_file):
            self.save_json(self.persons_file, {})
        
        # 初始化照片数据
        if not os.path.exists(self.faces_file):
            self.save_json(self.faces_file, {})
        
        # 初始化识别记录
        if not os.path.exists(self.records_file):
            self.save_json(self.records_file, [])
        
        # 初始化回调地址
        if not os.path.exists(self.callbacks_file):
            callbacks_data = {
                "identify": None,
                "img_reg": None,
                "event": None
            }
            self.save_json(self.callbacks_file, callbacks_data)
    
    def load_json(self, file_path):
        """加载JSON文件"""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None
    
    def save_json(self, file_path, data):
        """保存JSON文件"""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False
    
    # 设备相关操作
    def get_device_info(self):
        """获取设备信息"""
        device_data = self.load_json(self.device_file)
        return device_data.get("device_info", {})
    
    def get_password(self):
        """获取设备密码"""
        device_data = self.load_json(self.device_file)
        return device_data.get("device_password", "12345678")
    
    def set_password(self, new_password):
        """设置设备密码"""
        device_data = self.load_json(self.device_file)
        device_data["device_password"] = new_password
        return self.save_json(self.device_file, device_data)
    
    def get_door_sensor(self):
        """获取门磁状态"""
        device_data = self.load_json(self.device_file)
        return device_data.get("door_sensor", 3)
    
    def set_door_sensor(self, status):
        """设置门磁状态"""
        device_data = self.load_json(self.device_file)
        device_data["door_sensor"] = status
        return self.save_json(self.device_file, device_data)
    
    # 人员相关操作
    def get_persons(self):
        """获取所有人员"""
        return self.load_json(self.persons_file) or {}
    
    def get_person(self, person_id):
        """获取指定人员"""
        persons = self.get_persons()
        return persons.get(person_id)
    
    def save_person(self, person_id, person_data):
        """保存人员信息"""
        persons = self.get_persons()
        persons[person_id] = person_data
        return self.save_json(self.persons_file, persons)
    
    def delete_person(self, person_id):
        """删除人员"""
        persons = self.get_persons()
        if person_id in persons:
            del persons[person_id]
            return self.save_json(self.persons_file, persons)
        return True
    
    def clear_persons(self):
        """清空所有人员"""
        return self.save_json(self.persons_file, {})
    
    # 照片相关操作
    def get_faces(self):
        """获取所有照片"""
        return self.load_json(self.faces_file) or {}
    
    def get_face(self, face_id):
        """获取指定照片"""
        faces = self.get_faces()
        return faces.get(face_id)
    
    def get_person_faces(self, person_id):
        """获取指定人员的所有照片"""
        faces = self.get_faces()
        person_faces = []
        for face_id, face_data in faces.items():
            if face_data.get("personId") == person_id:
                person_faces.append(face_data)
        return person_faces
    
    def save_face(self, face_id, face_data):
        """保存照片信息"""
        faces = self.get_faces()
        faces[face_id] = face_data
        return self.save_json(self.faces_file, faces)
    
    def delete_face(self, face_id):
        """删除照片"""
        faces = self.get_faces()
        if face_id in faces:
            del faces[face_id]
            return self.save_json(self.faces_file, faces)
        return True
    
    def delete_person_faces(self, person_id):
        """删除指定人员的所有照片"""
        faces = self.get_faces()
        updated_faces = {}
        for face_id, face_data in faces.items():
            if face_data.get("personId") != person_id:
                updated_faces[face_id] = face_data
        return self.save_json(self.faces_file, updated_faces)
    
    def clear_faces(self):
        """清空所有照片"""
        return self.save_json(self.faces_file, {})
    
    # 识别记录相关操作
    def get_records(self):
        """获取所有识别记录"""
        return self.load_json(self.records_file) or []
    
    def add_record(self, record_data):
        """添加识别记录"""
        records = self.get_records()
        record_data["id"] = len(records) + 1
        record_data["time"] = int(datetime.now().timestamp() * 1000)
        records.append(record_data)
        return self.save_json(self.records_file, records)
    
    def delete_records(self, filter_func=None):
        """删除识别记录"""
        records = self.get_records()
        if filter_func:
            updated_records = [record for record in records if not filter_func(record)]
        else:
            updated_records = []
        return self.save_json(self.records_file, updated_records)
    
    # 回调地址相关操作
    def get_callbacks(self):
        """获取回调地址"""
        return self.load_json(self.callbacks_file) or {}
    
    def set_callback(self, callback_type, url):
        """设置回调地址"""
        callbacks = self.get_callbacks()
        callbacks[callback_type] = url
        return self.save_json(self.callbacks_file, callbacks)
