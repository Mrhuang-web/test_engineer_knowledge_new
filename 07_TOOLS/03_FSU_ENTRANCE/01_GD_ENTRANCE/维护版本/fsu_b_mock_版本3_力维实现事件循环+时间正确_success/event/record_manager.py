#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
记录区管理模块，负责力维协议时间类型事件的记录区管理
"""

from typing import Dict, List, Any

class RecordManager:
    """记录区管理类"""
    
    def __init__(self, max_len: int = 100):
        """初始化记录区管理器
        
        Args:
            max_len: 记录区最大深度，表示存储历史记录的最大空间(条数)
        """
        self.MAXLEN = max_len  # 柜桶最大深度
        self.BOTTOM = 0  # 最早(旧)记录的位置
        self.SAVEP = 0  # 下一条记录的存储位置
        self.LOADP = 0  # 最后读取指针
        self.MF = 0x00  # 标志位，D7: 是否已满，D0: LOADP是否被覆盖
        
        # 记录存储
        self.records: List[Dict[str, Any]] = []
        
        # 初始化记录区
        self._init_record_zone()
    
    def _init_record_zone(self):
        """初始化记录区"""
        self.records = []
        self.BOTTOM = 0
        self.SAVEP = 0
        self.LOADP = 0
        self.MF = 0x00
    
    def add_record(self, record: Dict[str, Any]):
        """添加一条记录
        
        Args:
            record: 记录数据
        """
        # 检查是否已满
        if self.SAVEP >= self.MAXLEN:
            # 记录已满，需要覆盖最早的记录
            self.MF |= 0x80  # 设置D7=1，表示已满
            
            # 计算覆盖位置
            overwrite_pos = self.SAVEP % self.MAXLEN
            
            # 检查是否覆盖了LOADP
            if overwrite_pos == self.LOADP:
                self.MF |= 0x01  # 设置D0=1，表示LOADP被覆盖
            
            # 覆盖最早的记录
            if overwrite_pos < len(self.records):
                self.records[overwrite_pos] = record
            else:
                self.records.append(record)
            
            # 更新SAVEP
            self.SAVEP += 1
        else:
            # 记录未满，直接添加
            self.records.append(record)
            self.SAVEP += 1
    
    def get_valid_records(self):
        """获取有效记录
        
        Returns:
            有效记录列表
        """
        valid_records = []
        
        if not self.is_full():
            # 记录未满，返回BOTTOM到SAVEP-1的记录
            if self.BOTTOM < len(self.records):
                valid_records = self.records[self.BOTTOM:self.SAVEP]
        else:
            # 记录已满，返回完整的记录区
            # 顺序：SAVEP → MAXLEN → BOTTOM → SAVEP-1
            savep_mod = self.SAVEP % self.MAXLEN
            
            # 从SAVEP到MAXLEN-1
            if savep_mod < len(self.records):
                valid_records.extend(self.records[savep_mod:])
            
            # 从BOTTOM到savep_mod-1
            if self.BOTTOM < savep_mod:
                valid_records.extend(self.records[self.BOTTOM:savep_mod])
        
        return valid_records
    
    def get_record_count(self):
        """获取有效记录数
        
        Returns:
            有效记录数
        """
        if not self.is_full():
            # 记录未满，N = SAVEP - BOTTOM
            return max(0, self.SAVEP - self.BOTTOM)
        else:
            # 记录已满，N = MAXLEN
            return self.MAXLEN
    
    def is_full(self):
        """检查记录区是否已满
        
        Returns:
            bool: 是否已满
        """
        return (self.MF & 0x80) != 0
    
    def is_loadp_continuous(self):
        """检查LOADP是否连续
        
        Returns:
            bool: LOADP是否连续
        """
        return (self.MF & 0x01) == 0
    
    def get_loadp_range(self):
        """获取LOADP的有效范围
        
        Returns:
            (start, end): LOADP的有效范围
        """
        if not self.is_full():
            # 记录未满，范围：BOTTOM 到 SAVEP-1
            return (self.BOTTOM, self.SAVEP - 1)
        else:
            # 记录已满，范围：BOTTOM 到 MAXLEN-1
            return (self.BOTTOM, self.MAXLEN - 1)
    
    def update_loadp(self, new_loadp: int):
        """更新LOADP
        
        Args:
            new_loadp: 新的LOADP值
        """
        # 检查是否在有效范围内
        loadp_start, loadp_end = self.get_loadp_range()
        if loadp_start <= new_loadp <= loadp_end:
            self.LOADP = new_loadp
    
    def get_record_at(self, position: int):
        """获取指定位置的记录
        
        Args:
            position: 位置索引
            
        Returns:
            记录数据，如果位置无效返回None
        """
        if 0 <= position < len(self.records):
            return self.records[position]
        return None
    
    def get_latest_record(self):
        """获取最新记录
        
        Returns:
            最新记录，如果没有记录返回None
        """
        if not self.records:
            return None
        
        if not self.is_full():
            # 记录未满，最新记录在SAVEP-1位置
            if self.SAVEP > 0 and self.SAVEP - 1 < len(self.records):
                return self.records[self.SAVEP - 1]
        else:
            # 记录已满，最新记录在SAVEP-1位置
            latest_pos = (self.SAVEP - 1) % self.MAXLEN
            return self.get_record_at(latest_pos)
        
        return None
    
    def get_oldest_record(self):
        """获取最早记录
        
        Returns:
            最早记录，如果没有记录返回None
        """
        if not self.records:
            return None
        
        if not self.is_full():
            # 记录未满，最早记录在BOTTOM位置
            return self.get_record_at(self.BOTTOM)
        else:
            # 记录已满，最早记录在SAVEP位置
            oldest_pos = self.SAVEP % self.MAXLEN
            return self.get_record_at(oldest_pos)
        
        return None
    
    def get_record_info(self):
        """获取记录区信息
        
        Returns:
            记录区信息字典
        """
        return {
            "MAXLEN": self.MAXLEN,
            "BOTTOM": self.BOTTOM,
            "SAVEP": self.SAVEP,
            "LOADP": self.LOADP,
            "MF": self.MF,
            "is_full": self.is_full(),
            "is_loadp_continuous": self.is_loadp_continuous(),
            "valid_record_count": self.get_record_count(),
            "loadp_range": self.get_loadp_range(),
            "record_count": len(self.records)
        }
