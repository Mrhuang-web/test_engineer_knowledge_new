# 识别记录类接口业务逻辑
from datastore.data_store import data_store
from dictionaries.code_dict import code_mapping

class RecordService:
    def __init__(self):
        self.data_store = data_store
    
    def find_records(self, params):
        """查询识别记录"""
        passwd = params.get('pass')
        person_id = params.get('personId')
        start_time = params.get('startTime')
        end_time = params.get('endTime')
        length = int(params.get('length', 1000))
        model = int(params.get('model', -1))
        order = params.get('order', 'desc')
        index = int(params.get('index', 0))
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person_id参数
        if not person_id:
            return self._get_response('LAN_EXP-3016')
        
        # 验证人员ID格式
        if person_id != '-1' and person_id != 'STRANGERBABY' and not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-3017')
        
        # 验证length参数
        if length <= 0 or length > 1000:
            return self._get_response('LAN_EXP-3018')
        
        # 验证时间格式（简化处理）
        if start_time != '0' and end_time != '0':
            # 这里可以添加更严格的时间格式验证
            pass
        
        # 查询记录
        records = self.data_store.get_records(person_id, start_time, end_time, index, length)
        
        if not records:
            return self._get_response('LAN_SUS-0', msg='该查询条件对应的识别记录数量为0', data=[])
        
        return self._get_response('LAN_SUS-0', msg='查询成功', data=records)
    
    def delete_records(self, params):
        """删除识别记录"""
        passwd = params.get('pass')
        person_id = params.get('personId')
        start_time = params.get('startTime')
        end_time = params.get('endTime')
        model = int(params.get('model', -1))
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person_id参数
        if not person_id:
            return self._get_response('LAN_EXP-3016')
        
        # 验证人员ID格式
        if person_id != '-1' and person_id != 'STRANGERBABY' and not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-3017')
        
        # 验证时间格式（简化处理）
        if start_time != '0' and end_time != '0':
            # 这里可以添加更严格的时间格式验证
            pass
        
        # 删除记录
        self.data_store.delete_records(person_id, start_time, end_time)
        
        return self._get_response('LAN_SUS-0', msg='删除成功')
    
    def _is_valid_id(self, id_str):
        """验证ID格式是否合法"""
        # ID只允许数字0~9和英文字母，且最大长度为255
        return len(id_str) <= 255 and all(c.isalnum() for c in id_str)
    
    def _get_response(self, code, msg=None, data=None):
        """生成统一格式的响应，确保返回参数顺序为code、data、msg、result、success
        如果data为None，则从响应中移除data字段"""
        base_response = code_mapping.get(code, code_mapping['LAN_EXP-1000'])
        
        # 构建响应字典，确保顺序正确
        response = {
            'code': code,
            'msg': msg if msg is not None else base_response['msg'],
            'result': base_response['result'],
            'success': base_response['success']
        }
        
        # 只有当data不为None时，才添加到响应中
        if data is not None:
            # 将data插入到code之后
            response = {
                'code': code,
                'data': data,
                'msg': response['msg'],
                'result': response['result'],
                'success': response['success']
            }
        elif base_response.get('data', None) is not None:
            # 如果base_response中有data，也添加到响应中
            response = {
                'code': code,
                'data': base_response['data'],
                'msg': response['msg'],
                'result': response['result'],
                'success': response['success']
            }
        
        return response

# 创建全局实例
record_service = RecordService()