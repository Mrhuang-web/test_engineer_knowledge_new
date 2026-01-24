#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
识别记录业务逻辑模块
"""

from data.data_store import JSONDataStore
from business.logger import global_logger
from business.person_service import PersonService

class RecordService:
    """识别记录业务逻辑类"""
    
    def __init__(self):
        self.data_store = JSONDataStore()
        self.person_service = PersonService()
        self.logger = global_logger
    
    def get_records(self, person_id, start_time, end_time):
        """获取识别记录"""
        # 检查人员是否存在（如果不是查询所有人员）
        if person_id != "-1" and person_id != "STRANGERBABY":
            if not self.person_service.person_exists(person_id):
                self.logger.warning(f"记录查询失败：人员ID不存在 {person_id}")
                return None, "人员ID不存在"
        
        # 获取所有记录
        all_records = self.data_store.get_records()
        
        # 根据条件过滤记录
        filtered_records = []
        for record in all_records:
            # 按人员ID过滤
            if person_id != "-1" and record.get("personId") != person_id:
                continue
            
            # 按时间范围过滤（简化实现）
            record_time = record.get("time", 0)
            # 这里可以根据实际需要实现时间范围过滤
            
            filtered_records.append(record)
        
        self.logger.info(f"记录查询成功：{person_id} -> {len(filtered_records)}条记录")
        return filtered_records, "查询成功"
    
    def delete_records(self, person_id, start_time, end_time):
        """删除识别记录"""
        # 检查人员是否存在（如果不是删除所有人员）
        if person_id != "-1" and person_id != "STRANGERBABY":
            if not self.person_service.person_exists(person_id):
                self.logger.warning(f"记录删除失败：人员ID不存在 {person_id}")
                return False, "人员ID不存在"
        
        # 定义过滤函数
        def filter_func(record):
            if person_id != "-1" and record.get("personId") != person_id:
                return False
            # 这里可以根据实际需要实现时间范围过滤
            return True
        
        # 删除记录
        success = self.data_store.delete_records(filter_func)
        if success:
            self.logger.info(f"记录删除成功：{person_id}")
            return True, "删除成功"
        else:
            self.logger.error(f"记录删除失败：保存失败 {person_id}")
            return False, "删除失败"
    
    def add_record(self, record_data):
        """添加识别记录"""
        success = self.data_store.add_record(record_data)
        if success:
            self.logger.info(f"记录添加成功：{record_data.get('personId')}")
            return True, "添加成功"
        else:
            self.logger.error(f"记录添加失败：保存失败 {record_data.get('personId')}")
            return False, "添加失败"
