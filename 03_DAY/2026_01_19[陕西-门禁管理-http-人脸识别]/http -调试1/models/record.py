# 识别记录相关数据存储

import json
import os

class RecordData:
    """识别记录数据管理类"""
    
    # 存储配置
    STORAGE_TYPE = 'file'  # 当前存储类型：file，预留：database, cache
    STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'storage', 'records.json')
    
    def __init__(self):
        # 初始化识别记录列表
        self._records = []
        
        # 加载数据
        self.load_data()
    
    def load_data(self):
        """从存储中加载数据"""
        if self.STORAGE_TYPE == 'file':
            try:
                if os.path.exists(self.STORAGE_PATH):
                    with open(self.STORAGE_PATH, 'r', encoding='utf-8') as f:
                        self._records = json.load(f)
            except Exception as e:
                print(f"加载识别记录数据失败: {e}")
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
                    json.dump(self._records, f, ensure_ascii=False, indent=2)
            except Exception as e:
                print(f"保存识别记录数据失败: {e}")
        # 预留数据库或缓存保存逻辑
        elif self.STORAGE_TYPE == 'database':
            # 数据库保存逻辑
            pass
        elif self.STORAGE_TYPE == 'cache':
            # 缓存保存逻辑
            pass
    
    def add_record(self, record):
        """添加识别记录"""
        self._records.append(record)
        self.save_data()
    
    def get_records(self, person_id='-1', model=-1, order='desc', start_time=0, end_time=0):
        """获取识别记录
        
        Args:
            person_id: 人员ID，-1查询所有，STRANGERBABY查询陌生人，IDCARD查询所有人证比对记录
            model: 记录类型，-1所有类型，0刷脸等
            order: 排序方式，1升序，其他降序
            start_time: 开始时间戳（毫秒），0表示不限制
            end_time: 结束时间戳（毫秒），0表示不限制
            
        Returns:
            list: 筛选后的记录列表
        """
        # 筛选记录
        filtered = self._records
        
        # 按人员ID筛选
        if person_id == 'IDCARD':
            # 查询所有人证比对记录
            filtered = [r for r in filtered if r['model'] == 2]
        elif person_id != '-1':
            filtered = [r for r in filtered if r['personId'] == person_id]
        
        # 按记录类型筛选（如果不是IDCARD，因为IDCARD已经按model=2筛选了）
        if person_id != 'IDCARD' and model != -1:
            filtered = [r for r in filtered if r['model'] == model]
        
        # 按时间范围筛选
        if start_time != 0:
            filtered = [r for r in filtered if r['time'] >= start_time]
        if end_time != 0:
            filtered = [r for r in filtered if r['time'] <= end_time]
        
        # 排序
        if order == '1':
            filtered.sort(key=lambda x: x['time'])
        else:
            filtered.sort(key=lambda x: x['time'], reverse=True)
        
        return filtered
    
    def get_records_by_page(self, person_id='-1', model=-1, order='desc', index=0, length=1000, start_time=0, end_time=0):
        """分页获取识别记录"""
        filtered = self.get_records(person_id, model, order, start_time, end_time)
        
        # 分页
        start = index * length
        end = start + length
        paginated = filtered[start:end]
        
        return {
            'pageInfo': {
                'index': index,
                'length': length,
                'size': len(paginated),
                'total': len(filtered)
            },
            'records': paginated
        }
    
    def delete_records(self, person_id='-1', model=-1, start_time=0, end_time=0):
        """删除识别记录"""
        if person_id == '-1' and model == -1 and start_time == 0 and end_time == 0:
            # 删除所有记录
            self._records = []
            self.save_data()
            return True
        
        # 删除指定条件的记录
        original_length = len(self._records)
        
        self._records = [
            r for r in self._records 
            if not (
                ((person_id == '-1') or 
                 (person_id == 'STRANGERBABY' and r['personId'] == 'STRANGERBABY') or 
                 (person_id == 'IDCARD' and r['model'] == 2) or 
                 (r['personId'] == person_id)) and 
                (model == -1 or r['model'] == model) and 
                (start_time == 0 or r['time'] >= start_time) and 
                (end_time == 0 or r['time'] <= end_time)
            )
        ]
        
        if len(self._records) < original_length:
            self.save_data()
            return True
        return False
    
    def update_record_state(self, record_id, state):
        """更新记录状态
        
        Args:
            record_id: 记录ID
            state: 状态，1=成功，2=回调失败
        """
        for record in self._records:
            if record['id'] == record_id:
                record['state'] = state
                self.save_data()
                return True
        return False
    
    def get_record_by_id(self, record_id):
        """根据ID获取记录
        
        Args:
            record_id: 记录ID
        
        Returns:
            dict: 记录信息，None表示未找到
        """
        for record in self._records:
            if record['id'] == record_id:
                return record
        return None

# 创建识别记录数据实例
record_data = RecordData()