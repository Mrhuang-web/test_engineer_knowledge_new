# 数据存储模块
# 用于模拟数据存储功能

class DataStore:
    def __init__(self):
        # 初始化数据存储
        self.access_control_records = []
        self.face_operation_results = []
    
    def save_access_control_info(self, record):
        """保存门禁开启信息"""
        self.access_control_records.append(record)
        return True
    
    def get_access_control_info(self, work_ord_num=None):
        """获取门禁开启信息"""
        if work_ord_num:
            return [record for record in self.access_control_records if record.get('workOrdNum') == work_ord_num]
        return self.access_control_records
    
    def save_face_operation_result(self, result):
        """保存人脸操作结果"""
        self.face_operation_results.append(result)
        return True
    
    def get_face_operation_result(self, work_ord_num=None):
        """获取人脸操作结果"""
        if work_ord_num:
            return [result for result in self.face_operation_results if result.get('workOrdNum') == work_ord_num]
        return self.face_operation_results
    
    def clear_all(self):
        """清空所有数据"""
        self.access_control_records.clear()
        self.face_operation_results.clear()
        return True

# 创建数据存储实例
data_store = DataStore()