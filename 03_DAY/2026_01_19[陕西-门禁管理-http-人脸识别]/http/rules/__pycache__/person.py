# 人员相关数据存储

import json
import os

class PersonData:
    """人员数据管理类"""
    
    # 存储配置
    STORAGE_TYPE = 'file'  # 当前存储类型：file，预留：database, cache
    STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage', 'persons.json')
    
    def __init__(self):
        # 初始化人员数据列表
        self._persons = []
        
        # 加载数据
        self.load_data()
    
    def load_data(self):
        """从存储中加载数据"""
        if self.STORAGE_TYPE == 'file':
            try:
                if os.path.exists(self.STORAGE_PATH):
                    with open(self.STORAGE_PATH, 'r', encoding='utf-8') as f:
                        self._persons = json.load(f)
            except Exception as e:
                print(f"加载人员数据失败: {e}")
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
                    json.dump(self._persons, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存人员数据失败: {e}")
        # 预留数据库或缓存保存逻辑
        elif self.STORAGE_TYPE == 'database':
            # 数据库保存逻辑
            pass
        elif self.STORAGE_TYPE == 'cache':
            # 缓存保存逻辑
            pass
    
    def add_person(self, person):
        """添加人员"""
        self._persons.append(person)
        self.save_data()
    
    def get_person(self, person_id):
        """根据ID获取人员"""
        for person in self._persons:
            if person['id'] == person_id:
                return person
        return None
    
    def get_all_persons(self):
        """获取所有人员"""
        return self._persons
    
    def update_person(self, person_id, person_data):
        """更新人员信息"""
        for i, person in enumerate(self._persons):
            if person['id'] == person_id:
                self._persons[i].update(person_data)
                self.save_data()
                return self._persons[i]
        return None
    
    def delete_person(self, person_id):
        """删除人员"""
        if person_id == '-1':
            # 删除所有人员
            self._persons = []
            self.save_data()
            return True
        
        # 删除指定人员
        original_length = len(self._persons)
        self._persons = [p for p in self._persons if p['id'] != person_id]
        if len(self._persons) < original_length:
            self.save_data()
            return True
        return False
    
    def get_persons_by_page(self, index, length):
        """分页获取人员"""
        start = index * length
        end = start + length
        return {
            'total': len(self._persons),
            'data': self._persons[start:end]
        }

# 创建人员数据实例
person_data = PersonData()