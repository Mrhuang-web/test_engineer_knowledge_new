#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
照片管理业务逻辑模块
"""

import uuid
from data.data_store import JSONDataStore
from business.logger import global_logger
from business.person_service import PersonService

class FaceService:
    """照片管理业务逻辑类"""
    
    def __init__(self):
        self.data_store = JSONDataStore()
        self.person_service = PersonService()
        self.logger = global_logger
    
    def generate_face_id(self):
        """生成照片ID"""
        return str(uuid.uuid4()).replace("-", "")
    
    def add_face(self, face_data):
        """添加照片"""
        person_id = face_data.get("personId")
        face_id = face_data.get("faceId")
        img_base64 = face_data.get("imgBase64")
        
        if not person_id:
            self.logger.warning(f"照片添加失败：人员ID不能为空")
            return False, "人员ID不能为空"
        
        # 检查人员是否存在
        if not self.person_service.person_exists(person_id):
            self.logger.warning(f"照片添加失败：人员ID不存在 {person_id}")
            return False, "人员ID不存在"
        
        # 自动生成照片ID（如果未提供）
        if not face_id:
            face_id = self.generate_face_id()
            face_data["faceId"] = face_id
            self.logger.info(f"自动生成照片ID：{face_id}")
        
        # 检查照片ID是否已存在
        existing_face = self.data_store.get_face(face_id)
        if existing_face:
            self.logger.warning(f"照片添加失败：照片ID已存在 {face_id}")
            return False, "照片ID已存在"
        
        if not img_base64:
            self.logger.warning(f"照片添加失败：照片数据不能为空 {face_id}")
            return False, "照片数据不能为空"
        
        # 检查该人员的照片数量（最多3张）
        person_faces = self.data_store.get_person_faces(person_id)
        if len(person_faces) >= 3:
            self.logger.warning(f"照片添加失败：该人员照片数量已达上限 {person_id}")
            return False, "注册照片已达到最大数量限定(3张)"
        
        # 保存照片
        success = self.data_store.save_face(face_id, face_data)
        if success:
            self.logger.info(f"照片添加成功：{face_id} -> {person_id}")
            return True, "照片添加成功"
        else:
            self.logger.error(f"照片添加失败：保存失败 {face_id}")
            return False, "保存失败"
    
    def delete_face(self, face_id):
        """删除照片"""
        # 检查照片ID是否存在
        existing_face = self.data_store.get_face(face_id)
        if not existing_face:
            self.logger.warning(f"照片删除失败：照片ID不存在 {face_id}")
            return False, "照片ID不存在"
        
        # 删除照片
        success = self.data_store.delete_face(face_id)
        if success:
            self.logger.info(f"照片删除成功：{face_id}")
            return True, "照片删除成功"
        else:
            self.logger.error(f"照片删除失败：保存失败 {face_id}")
            return False, "保存失败"
    
    def update_face(self, face_data):
        """更新照片"""
        person_id = face_data.get("personId")
        face_id = face_data.get("faceId")
        img_base64 = face_data.get("imgBase64")
        
        if not person_id or not face_id:
            self.logger.warning(f"照片更新失败：人员ID或照片ID不能为空")
            return False, "人员ID和照片ID不能为空"
        
        # 检查人员是否存在
        if not self.person_service.person_exists(person_id):
            self.logger.warning(f"照片更新失败：人员ID不存在 {person_id}")
            return False, "人员ID不存在"
        
        # 检查照片ID是否存在
        existing_face = self.data_store.get_face(face_id)
        if not existing_face:
            self.logger.warning(f"照片更新失败：照片ID不存在 {face_id}")
            return False, "照片ID不存在"
        
        # 检查照片是否属于该人员
        if existing_face.get("personId") != person_id:
            self.logger.warning(f"照片更新失败：照片不属于该人员 {face_id} -> {person_id}")
            return False, "该人员没有这个照片ID"
        
        if not img_base64:
            self.logger.warning(f"照片更新失败：照片数据不能为空 {face_id}")
            return False, "照片数据不能为空"
        
        # 更新照片
        updated_face = existing_face.copy()
        updated_face.update(face_data)
        
        success = self.data_store.save_face(face_id, updated_face)
        if success:
            self.logger.info(f"照片更新成功：{face_id} -> {person_id}")
            return True, "照片更新成功"
        else:
            self.logger.error(f"照片更新失败：保存失败 {face_id}")
            return False, "保存失败"
    
    def get_face(self, person_id):
        """获取人员照片"""
        # 检查人员是否存在
        if not self.person_service.person_exists(person_id):
            self.logger.warning(f"照片查询失败：人员ID不存在 {person_id}")
            return None, "人员ID不存在"
        
        # 获取照片
        faces = self.data_store.get_person_faces(person_id)
        if not faces:
            self.logger.info(f"照片查询成功：该人员没有注册照片 {person_id}")
            return [], "该人员没有注册照片"
        
        self.logger.info(f"照片查询成功：{person_id} -> {len(faces)}张照片")
        return faces, "照片查询成功"
    
    def clear_person_faces(self, person_id):
        """清空人员照片"""
        # 检查人员是否存在
        if not self.person_service.person_exists(person_id):
            self.logger.warning(f"清空照片失败：人员ID不存在 {person_id}")
            return False, "人员ID不存在"
        
        # 清空照片
        success = self.data_store.delete_person_faces(person_id)
        if success:
            self.logger.info(f"清空人员照片成功：{person_id}")
            return True, "照片清空成功"
        else:
            self.logger.error(f"清空人员照片失败：保存失败 {person_id}")
            return False, "保存失败"
    
    def take_img(self, person_id):
        """拍照注册"""
        # 检查人员是否存在
        if not self.person_service.person_exists(person_id):
            self.logger.warning(f"拍照注册失败：人员ID不存在 {person_id}")
            return False, "人员ID不存在"
        
        # 检查该人员的照片数量（最多3张）
        person_faces = self.data_store.get_person_faces(person_id)
        if len(person_faces) >= 3:
            self.logger.warning(f"拍照注册失败：该人员照片数量已达上限 {person_id}")
            return False, "注册照片已达到最大数量限定(3张)"
        
        self.logger.info(f"拍照注册操作：{person_id}")
        return True, "正在开启拍照注册模式，注册成功后可根据personId查询拍摄的照片。请根据引导完成注册"
