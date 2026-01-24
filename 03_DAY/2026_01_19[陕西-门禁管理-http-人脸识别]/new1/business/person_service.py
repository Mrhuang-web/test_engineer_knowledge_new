#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人员管理业务逻辑模块
"""

import uuid
from data.data_store import JSONDataStore
from business.logger import global_logger

class PersonService:
    """人员管理业务逻辑类"""
    
    def __init__(self):
        self.data_store = JSONDataStore()
        self.logger = global_logger
    
    def generate_person_id(self):
        """生成人员ID"""
        return str(uuid.uuid4()).replace("-", "")[:16]
    
    def add_person(self, person_data):
        """添加人员"""
        # 自动生成人员ID（如果未提供）
        person_id = person_data.get("id")
        if not person_id:
            person_id = self.generate_person_id()
            person_data["id"] = person_id
            self.logger.info(f"自动生成人员ID：{person_id}")
        
        if not person_data.get("name"):
            self.logger.warning(f"人员添加失败：姓名不能为空")
            return False, "姓名不能为空"
        
        # 检查人员ID是否已存在
        existing_person = self.data_store.get_person(person_id)
        if existing_person:
            self.logger.warning(f"人员添加失败：人员ID已存在 {person_id}")
            return False, "人员ID已存在"
        
        success = self.data_store.save_person(person_id, person_data)
        if success:
            self.logger.info(f"人员添加成功：{person_id} - {person_data.get('name')}")
            return True, "人员添加成功"
        else:
            self.logger.error(f"人员添加失败：保存失败 {person_id}")
            return False, "保存失败"
    
    def delete_person(self, person_id):
        """删除人员"""
        if person_id == "-1":
            # 删除所有人员
            success1 = self.data_store.clear_persons()
            # 同时删除所有照片
            success2 = self.data_store.clear_faces()
            if success1 and success2:
                self.logger.info(f"删除所有人员成功")
                return True, "所有人员删除成功"
            else:
                self.logger.error(f"删除所有人员失败")
                return False, "删除失败"
        
        # 检查人员ID是否存在
        existing_person = self.data_store.get_person(person_id)
        if not existing_person:
            self.logger.warning(f"人员删除失败：人员ID不存在 {person_id}")
            return False, "人员ID不存在"
        
        # 删除人员
        success1 = self.data_store.delete_person(person_id)
        # 删除该人员的所有照片
        success2 = self.data_store.delete_person_faces(person_id)
        
        if success1 and success2:
            self.logger.info(f"人员删除成功：{person_id}")
            return True, "人员删除成功"
        else:
            self.logger.error(f"人员删除失败：保存失败 {person_id}")
            return False, "删除失败"
    
    def update_person(self, person_data):
        """更新人员信息"""
        person_id = person_data.get("id")
        if not person_id:
            self.logger.warning(f"人员更新失败：人员ID不能为空")
            return False, "人员ID不能为空"
        
        if not person_data.get("name"):
            self.logger.warning(f"人员更新失败：姓名不能为空")
            return False, "姓名不能为空"
        
        # 检查人员ID是否存在
        existing_person = self.data_store.get_person(person_id)
        if not existing_person:
            self.logger.warning(f"人员更新失败：人员ID不存在 {person_id}")
            return False, "人员ID不存在"
        
        # 更新人员信息
        updated_person = existing_person.copy()
        updated_person.update(person_data)
        
        success = self.data_store.save_person(person_id, updated_person)
        if success:
            self.logger.info(f"人员更新成功：{person_id} - {updated_person.get('name')}")
            return True, "人员信息更新成功"
        else:
            self.logger.error(f"人员更新失败：保存失败 {person_id}")
            return False, "保存失败"
    
    def get_person(self, person_id):
        """获取人员信息"""
        if person_id == "-1":
            # 获取所有人员
            persons = self.data_store.get_persons()
            self.logger.info(f"获取所有人员成功：共 {len(persons)} 人")
            return list(persons.values()), "查询成功"
        
        # 获取指定人员
        person = self.data_store.get_person(person_id)
        if person:
            self.logger.info(f"获取人员成功：{person_id}")
            return person, "查询成功"
        else:
            self.logger.warning(f"获取人员失败：人员ID不存在 {person_id}")
            return None, "人员ID不存在"
    
    def person_exists(self, person_id):
        """检查人员是否存在"""
        return self.data_store.get_person(person_id) is not None
