# 照片管理类接口业务逻辑
from datastore.data_store import data_store
from dictionaries.code_dict import code_mapping

class FaceService:
    def __init__(self):
        self.data_store = data_store
    
    def create_face(self, params):
        """创建照片"""
        passwd = params.get('pass')
        person_id = params.get('personId')
        face_id = params.get('faceId')
        img_base64 = params.get('imgBase64')
        is_easy_way = params.get('isEasyWay', False)
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证参数
        if not person_id:
            return self._get_response('LAN_EXP-3016')
        
        if not face_id:
            return self._get_response('LAN_EXP-4002')
        
        if not img_base64:
            return self._get_response('LAN_EXP-4008')
        
        # 验证人员ID格式
        if not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-4005')
        
        # 验证照片ID格式
        if not self._is_valid_id(face_id):
            return self._get_response('LAN_EXP-4006')
        
        # 验证人员是否存在
        if not self.data_store.get_person(person_id):
            return self._get_response('LAN_EXP-3009')
        
        # 验证isEasyWay参数
        if not isinstance(is_easy_way, bool):
            return self._get_response('LAN_EXP-4009')
        
        # 创建照片信息
        face_info = {
            'personId': person_id,
            'faceId': face_id,
            'imgBase64': img_base64,
            'isEasyWay': is_easy_way
        }
        
        if not self.data_store.create_face(face_id, face_info):
            # 检查是照片ID已存在还是照片数量超过限制
            if face_id in self.data_store.faces:
                return self._get_response('LAN_EXP-4007')
            else:
                return self._get_response('LAN_EXP-4012')
        
        return self._get_response('LAN_SUS-0', msg='照片添加成功')
    
    def delete_face(self, params):
        """删除照片"""
        passwd = params.get('pass')
        face_id = params.get('faceId')
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证face_id参数
        if not face_id:
            return self._get_response('LAN_EXP-4016')
        
        # 验证照片ID格式
        if not self._is_valid_id(face_id):
            return self._get_response('LAN_EXP-4006')
        
        # 删除照片
        if not self.data_store.delete_face(face_id):
            return self._get_response('LAN_EXP-4017')
        
        return self._get_response('LAN_SUS-0', msg='照片删除成功')
    
    def update_face(self, params):
        """更新照片"""
        passwd = params.get('pass')
        person_id = params.get('personId')
        face_id = params.get('faceId')
        img_base64 = params.get('imgBase64')
        is_easy_way = params.get('isEasyWay', False)
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证参数
        if not person_id:
            return self._get_response('LAN_EXP-3016')
        
        if not face_id:
            return self._get_response('LAN_EXP-4016')
        
        if not img_base64:
            return self._get_response('LAN_EXP-4008')
        
        # 验证人员ID格式
        if not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-4005')
        
        # 验证照片ID格式
        if not self._is_valid_id(face_id):
            return self._get_response('LAN_EXP-4006')
        
        # 验证人员是否存在
        if not self.data_store.get_person(person_id):
            return self._get_response('LAN_EXP-3009')
        
        # 验证照片是否存在且属于该人员
        face = self.data_store.get_face(face_id)
        if not face or face['personId'] != person_id:
            return self._get_response('LAN_EXP-4031')
        
        # 验证isEasyWay参数
        if not isinstance(is_easy_way, bool):
            return self._get_response('LAN_EXP-4009')
        
        # 更新照片信息
        face_info = {
            'personId': person_id,
            'faceId': face_id,
            'imgBase64': img_base64,
            'isEasyWay': is_easy_way
        }
        
        if not self.data_store.update_face(face_id, face_info):
            return self._get_response('LAN_EXP-4020')
        
        return self._get_response('LAN_SUS-0', msg='照片更新成功')
    
    def find_face(self, params):
        """查询照片"""
        passwd = params.get('pass')
        person_id = params.get('personId')
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person_id参数
        if not person_id:
            return self._get_response('LAN_EXP-3016')
        
        # 验证人员ID格式
        if not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-4005')
        
        # 验证人员是否存在
        if not self.data_store.get_person(person_id):
            return self._get_response('LAN_EXP-3009')
        
        # 查询照片
        faces = self.data_store.get_faces_by_person(person_id)
        if not faces:
            return self._get_response('LAN_SUS-0', msg='该人员没有注册照片')
        
        return self._get_response('LAN_SUS-0', msg='照片查询成功', data=faces)
    
    def take_img(self, params):
        """拍照注册"""
        passwd = params.get('pass')
        person_id = params.get('personId')
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person_id参数
        if not person_id:
            return self._get_response('LAN_EXP-3016')
        
        # 验证人员ID格式
        if not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-4005')
        
        # 验证人员是否存在
        if not self.data_store.get_person(person_id):
            return self._get_response('LAN_EXP-3009')
        
        # 验证该人员的照片数量是否超过3张
        faces = self.data_store.get_faces_by_person(person_id)
        if len(faces) >= 3:
            return self._get_response('LAN_EXP-4012')
        
        # 简化处理，直接返回成功
        return self._get_response('LAN_SUS-0', msg='正在开启拍照注册模式，注册成功后可根据personId查询拍摄的照片。请根据引导完成注册')
    
    def delete_person_faces(self, params):
        """清空人员注册照片"""
        passwd = params.get('pass')
        person_id = params.get('personId')
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证person_id参数
        if not person_id:
            return self._get_response('LAN_EXP-3016')
        
        # 验证人员ID格式
        if not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-4005')
        
        # 验证人员是否存在
        if not self.data_store.get_person(person_id):
            return self._get_response('LAN_EXP-3009')
        
        # 删除该人员的所有照片
        self.data_store.delete_person_faces(person_id)
        return self._get_response('LAN_SUS-0', msg='照片清空成功')
    
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
face_service = FaceService()