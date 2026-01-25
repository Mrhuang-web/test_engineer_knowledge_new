# 人员管理类接口业务逻辑
import time
from datastore.data_store import data_store
from dictionaries.code_dict import code_mapping

class PersonService:
    def __init__(self):
        self.data_store = data_store
    
    def create_person(self, params):
        """创建人员"""
        passwd = params.get('pass')
        person_info = params.get('person')
        
        # 验证pass参数
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person参数
        if 'person' not in params:
            return self._get_response('LAN_EXP-3001')
        
        # 验证person参数是否为空
        if not person_info:
            return self._get_response('LAN_EXP-3002')
        
        # 验证person是否为dict类型
        if not isinstance(person_info, dict):
            return self._get_response('LAN_EXP-3002')
        
        # 获取人员ID
        person_id = person_info.get('id')
        
        # 如果personId未传入或为空，则系统生成32位的personId
        if not person_id:
            import uuid
            person_id = str(uuid.uuid4()).replace('-', '')
            person_info['id'] = person_id
        else:
            # 验证人员ID格式：只允许数字和英文字母，区分大小写，长度限制255个字符
            if not self._is_valid_id(person_id):
                return self._get_response('LAN_EXP-3003')
        
        # 验证姓名
        name = person_info.get('name')
        if not name or name.strip() == '':
            return self._get_response('LAN_EXP-3004')
        
        # 处理权限参数
        # facePermission: 1：关 2：开 (默认)
        if 'facePermission' in person_info:
            face_permission = person_info['facePermission']
            if not self._validate_permission('facePermission', face_permission):
                return self._get_response('LAN_EXP-3011', msg='facePermission 参数不合法')
        else:
            person_info['facePermission'] = 2
        
        # idCardPermission: 1：关 2：开 (默认)
        if 'idCardPermission' in person_info:
            id_card_permission = person_info['idCardPermission']
            if not self._validate_permission('idCardPermission', id_card_permission):
                return self._get_response('LAN_EXP-3012', msg='idCardPermission 参数不合法')
        else:
            person_info['idCardPermission'] = 2
        
        # faceAndCardPermission: 1：关(默认) 2：开
        if 'faceAndCardPermission' in person_info:
            face_and_card_permission = person_info['faceAndCardPermission']
            if not self._validate_permission('faceAndCardPermission', face_and_card_permission):
                return self._get_response('LAN_EXP-3013', msg='faceAndCardPermission 参数不合法')
        else:
            person_info['faceAndCardPermission'] = 1
        
        # 添加创建时间
        person_info['createTime'] = int(time.time() * 1000)
        # 添加iDPermission字段，默认值为1
        person_info['iDPermission'] = person_info.get('iDPermission', 1)
        
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
        
        # 验证人员是否存在
        existing_person = self.data_store.get_person(person_id)
        if not existing_person:
            return self._get_response('LAN_EXP-3009')
        
        # 验证姓名
        if not person_info.get('name'):
            return self._get_response('LAN_EXP-3004')
        
        # 验证权限参数
        # facePermission: 1：关 2：开，不传保留上一次的值
        if 'facePermission' in person_info:
            face_permission = person_info['facePermission']
            if not self._validate_permission('facePermission', face_permission):
                return self._get_response('LAN_EXP-3011', msg='facePermission 参数不合法')
        else:
            # 不传保留上一次的值
            person_info['facePermission'] = existing_person.get('facePermission', 2)
        
        # idCardPermission: 1：关 2：开，不传保留上一次的值
        if 'idCardPermission' in person_info:
            id_card_permission = person_info['idCardPermission']
            if not self._validate_permission('idCardPermission', id_card_permission):
                return self._get_response('LAN_EXP-3012', msg='idCardPermission 参数不合法')
        else:
            # 不传保留上一次的值
            person_info['idCardPermission'] = existing_person.get('idCardPermission', 2)
        
        # faceAndCardPermission: 1：关 2：开，不传保留上一次的值
        if 'faceAndCardPermission' in person_info:
            face_and_card_permission = person_info['faceAndCardPermission']
            if not self._validate_permission('faceAndCardPermission', face_and_card_permission):
                return self._get_response('LAN_EXP-3013', msg='faceAndCardPermission 参数不合法')
        else:
            # 不传保留上一次的值
            person_info['faceAndCardPermission'] = existing_person.get('faceAndCardPermission', 1)
        
        # 保留iDPermission字段
        if 'iDPermission' not in person_info:
            person_info['iDPermission'] = existing_person.get('iDPermission', 1)
        
        # 保留createTime字段
        if 'createTime' not in person_info:
            person_info['createTime'] = existing_person.get('createTime', int(time.time() * 1000))
        
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
        
        # 格式化人员数据，添加缺失的字段
        formatted_persons = []
        if isinstance(persons, list):
            for person in persons:
                formatted_persons.append(self._format_person_data(person))
        else:
            formatted_persons = [self._format_person_data(persons)]
        
        return self._get_response('LAN_SUS-0', msg='查询成功', data=formatted_persons)
    
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
        
        # 格式化人员数据，添加缺失的字段
        formatted_persons = []
        for person in persons:
            formatted_persons.append(self._format_person_data(person))
        
        return self._get_response('LAN_SUS-0', msg='查询成功', data=formatted_persons)
    
    def _is_valid_id(self, id_str):
        """验证ID格式是否合法"""
        # ID只允许数字0~9和英文字母，且最大长度为255
        return len(id_str) <= 255 and all(c.isalnum() for c in id_str)
    
    def _format_person_data(self, person):
        """格式化人员数据，添加缺失的字段"""
        # 确保所有必需的字段都存在
        formatted_person = {
            'id': person.get('id', ''),
            'name': person.get('name', ''),
            'idcardNum': person.get('idcardNum', ''),
            'iDNumber': person.get('iDNumber', ''),
            'facePermission': person.get('facePermission', 2),
            'idCardPermission': person.get('idCardPermission', 2),
            'faceAndCardPermission': person.get('faceAndCardPermission', 1),
            'createTime': person.get('createTime', int(time.time() * 1000)),
            'iDPermission': person.get('iDPermission', 1)
        }
        return formatted_person
    
    def _validate_permission(self, param_name, value):
        """验证权限参数是否合法
        
        Args:
            param_name: 参数名
            value: 参数值
        
        Returns:
            bool: 是否合法
        """
        # 权限参数只允许传1、2
        if value not in [1, 2]:
            return False
        return True
    
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