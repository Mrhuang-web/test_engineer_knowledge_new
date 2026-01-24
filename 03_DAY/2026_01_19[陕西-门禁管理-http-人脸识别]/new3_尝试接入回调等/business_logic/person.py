# 人员管理类接口业务逻辑
from datastore.data_store import data_store
from dictionaries.code_dict import code_mapping

class PersonService:
    def __init__(self):
        self.data_store = data_store
    
    def create_person(self, params):
        """创建人员"""
        passwd = params.get('pass')
        person_info = params.get('person')
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person参数
        if not person_info or not isinstance(person_info, dict):
            return self._get_response('LAN_EXP-3002')
        
        # 获取人员ID
        person_id = person_info.get('id')
        if not person_id:
            return self._get_response('LAN_EXP-3008')
        
        # 验证人员ID格式
        if not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-3003')
        
        # 验证姓名
        if not person_info.get('name'):
            return self._get_response('LAN_EXP-3004')
        
        # 创建人员
        if not self.data_store.create_person(person_id, person_info):
            return self._get_response('LAN_EXP-3005')
        
        return self._get_response('LAN_SUS-0', msg='人员信息添加成功')
    
    def delete_person(self, params):
        """删除人员"""
        passwd = params.get('pass')
        person_id = params.get('id')
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person_id参数
        if not person_id:
            return self._get_response('LAN_EXP-3008')
        
        # 验证人员ID格式
        if person_id != '-1' and not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-3039')
        
        # 删除人员
        if not self.data_store.delete_person(person_id):
            return self._get_response('LAN_EXP-3009')
        
        return self._get_response('LAN_SUS-0', msg='删除成功')
    
    def update_person(self, params):
        """更新人员"""
        passwd = params.get('pass')
        person_info = params.get('person')
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person参数
        if not person_info or not isinstance(person_info, dict):
            return self._get_response('LAN_EXP-3002')
        
        # 获取人员ID
        person_id = person_info.get('id')
        if not person_id:
            return self._get_response('LAN_EXP-3008')
        
        # 验证人员ID格式
        if not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-3003')
        
        # 验证姓名
        if not person_info.get('name'):
            return self._get_response('LAN_EXP-3004')
        
        # 更新人员
        if not self.data_store.update_person(person_id, person_info):
            return self._get_response('LAN_EXP-3009')
        
        return self._get_response('LAN_SUS-0', msg='人员信息更新成功')
    
    def find_person(self, params):
        """查询人员"""
        passwd = params.get('pass')
        person_id = params.get('id')
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person_id参数
        if not person_id:
            return self._get_response('LAN_EXP-3008')
        
        # 验证人员ID格式
        if person_id != '-1' and not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-3039')
        
        # 查询人员
        persons = self.data_store.get_person(person_id)
        if not persons:
            if person_id == '-1':
                return self._get_response('LAN_SUS-0', msg='数据库人员数量为0', data=[])
            return self._get_response('LAN_EXP-3009')
        
        return self._get_response('LAN_SUS-0', msg='查询成功', data=persons)
    
    def find_person_by_page(self, params):
        """分页查询人员"""
        passwd = params.get('pass')
        person_id = params.get('personId')
        length = int(params.get('length', 1000))
        index = int(params.get('index', 0))
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person_id参数
        if not person_id:
            return self._get_response('LAN_EXP-3016')
        
        # 验证人员ID格式
        if person_id != '-1' and not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-3017')
        
        # 验证length参数
        if length <= 0 or length > 1000:
            return self._get_response('LAN_EXP-3018')
        
        # 查询人员
        if person_id == '-1':
            # 分页查询所有人员
            persons = self.data_store.get_person_by_page(index, length)
        else:
            # 查询单个人员
            person = self.data_store.get_person(person_id)
            persons = [person] if person else []
        
        if not persons:
            return self._get_response('LAN_SUS-0', msg='数据库人员数量为0', data=[])
        
        return self._get_response('LAN_SUS-0', msg='查询成功', data=persons)
    
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
person_service = PersonService()