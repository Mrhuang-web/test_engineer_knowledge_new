# 照片管理类接口业务逻辑
import random
import string
import base64
from datastore.data_store import data_store
from dictionaries.code_dict import code_mapping

class FaceService:
    def __init__(self):
        self.data_store = data_store
    
    def create_face(self, params):
        """创建照片"""
        # 验证参数是否存在（参数异常验证）
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002')
        if 'personId' not in params:
            return self._get_response('LAN_EXP-3015')
        if 'imgBase64' not in params:
            return self._get_response('LAN_EXP-2024')
        
        passwd = params.get('pass')
        person_id = params.get('personId')
        face_id = params.get('faceId')
        img_base64 = params.get('imgBase64')
        is_easy_way = params.get('isEasyWay', False)
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证参数不能为空（参数不合法验证）
        if not person_id:
            return self._get_response('LAN_EXP-3016')
        
        if not img_base64:
            return self._get_response('LAN_EXP-4008')
        
        # 验证人员ID格式
        if not self._is_valid_id(person_id):
            return self._get_response('LAN_EXP-4005')
        
        # 验证人员是否存在
        if not self.data_store.get_person(person_id):
            return self._get_response('LAN_EXP-3009')
        
        # 验证isEasyWay参数
        if is_easy_way not in [True, False, 'true', 'false']:
            return self._get_response('LAN_EXP-4009')
        # 转换为布尔值
        is_easy_way = is_easy_way in [True, 'true']
        
        # 处理faceId：如果为空则自动生成32位
        if not face_id:
            try:
                face_id = self._generate_face_id()
            except Exception as e:
                return self._get_response('LAN_EXP-4013')
        else:
            # 验证照片ID格式
            if not self._is_valid_id(face_id):
                return self._get_response('LAN_EXP-4006')
            # 验证照片ID是否已存在
            if face_id in self.data_store.faces:
                return self._get_response('LAN_EXP-4007')
        
        # 验证照片数量是否超过3张
        person_faces = self.data_store.get_faces_by_person(person_id)
        if len(person_faces) >= 3:
            return self._get_response('LAN_EXP-4012')
        
        # 验证并处理base64图片
        if not self._is_valid_base64(img_base64):
            return self._get_response('LAN_EXP-4010')
        
        # 验证图片格式
        img_format = self._get_image_format(img_base64)
        if img_format not in ['png', 'jpg', 'jpeg']:
            if img_format == 'gif':
                return self._get_response('LAN_EXP-4032')
            else:
                return self._get_response('LAN_EXP-4010')
        
        # 验证图片大小（小于2M）
        try:
            img_size = len(base64.b64decode(img_base64))
        except Exception:
            return self._get_response('LAN_EXP-4011')
        
        if img_size > 2 * 1024 * 1024:
            return self._get_response('LAN_EXP-4010')
        
        # 验证图片分辨率（简化处理：实际项目中需要解析图片获取真实分辨率）
        # 这里假设如果能解码且格式正确，分辨率就在112*112到1080p之间
        
        # 创建照片信息
        face_info = {
            'personId': person_id,
            'faceId': face_id,
            'imgBase64': img_base64,
            'isEasyWay': is_easy_way
        }
        
        # 保存照片信息
        if not self.data_store.create_face(face_id, face_info):
            return self._get_response('LAN_EXP-4013')
        
        # 返回生成的faceId
        return self._get_response('LAN_SUS-0', msg='照片添加成功', data={'faceId': face_id})
    
    def _generate_face_id(self):
        """生成32位随机faceId，由数字和字母组成，确保唯一性"""
        chars = string.ascii_letters + string.digits
        max_attempts = 100
        
        for _ in range(max_attempts):
            face_id = ''.join(random.choice(chars) for _ in range(32))
            # 检查生成的faceId是否唯一
            if face_id not in self.data_store.faces:
                return face_id
        
        # 如果多次尝试都无法生成唯一的faceId，抛出异常
        raise Exception("无法生成唯一的faceId")
    
    def _is_valid_base64(self, base64_str):
        """验证base64字符串是否合法"""
        try:
            # 尝试解码
            base64.b64decode(base64_str, validate=True)
            return True
        except:
            return False
    
    def _get_image_format(self, base64_str):
        """从base64字符串中获取图片格式"""
        try:
            # 解码base64获取前几个字节判断格式
            img_data = base64.b64decode(base64_str)
            if img_data.startswith(b'\x89PNG'):
                return 'png'
            elif img_data.startswith(b'\xff\xd8\xff'):
                return 'jpg'
            elif img_data.startswith(b'\xff\xd8\xff\xe0') or img_data.startswith(b'\xff\xd8\xff\xe1'):
                return 'jpeg'
            else:
                return 'unknown'
        except:
            return 'unknown'
    
    def _is_valid_id(self, id_str):
        """验证ID格式是否合法"""
        # ID只允许数字0~9和英文字母，且最大长度为255
        return len(id_str) <= 255 and all(c.isalnum() for c in id_str)
    
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
        # 验证参数是否存在（参数异常验证）
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002')
        if 'personId' not in params:
            return self._get_response('LAN_EXP-3015')
        if 'faceId' not in params:
            return self._get_response('LAN_EXP-4002')
        if 'imgBase64' not in params:
            return self._get_response('LAN_EXP-2024')
        
        passwd = params.get('pass')
        person_id = params.get('personId')
        face_id = params.get('faceId')
        img_base64 = params.get('imgBase64')
        is_easy_way = params.get('isEasyWay', False)
        
        # 验证密码
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证参数不能为空（参数不合法验证）
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
        if is_easy_way not in [True, False, 'true', 'false']:
            return self._get_response('LAN_EXP-4009')
        # 转换为布尔值
        is_easy_way = is_easy_way in [True, 'true']
        
        # 验证并处理base64图片
        if not self._is_valid_base64(img_base64):
            return self._get_response('LAN_EXP-4010')
        
        # 验证图片格式
        img_format = self._get_image_format(img_base64)
        if img_format not in ['png', 'jpg', 'jpeg']:
            if img_format == 'gif':
                return self._get_response('LAN_EXP-4032')
            else:
                return self._get_response('LAN_EXP-4010')
        
        # 验证图片大小（小于2M）
        try:
            img_size = len(base64.b64decode(img_base64))
        except Exception:
            return self._get_response('LAN_EXP-4011')
        
        if img_size > 2 * 1024 * 1024:
            return self._get_response('LAN_EXP-4010')
        
        # 这里简化处理：不实际解析图片分辨率，假设符合要求
        # 实际项目中需要解析图片获取分辨率并验证
        
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
        # 验证参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002')
        if 'personId' not in params:
            return self._get_response('LAN_EXP-3015')
        
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
        
        # 格式化照片数据
        formatted_faces = []
        for face in faces:
            formatted_faces.append(self._format_face_data(face))
        
        return self._get_response('LAN_SUS-0', msg='照片查询成功', data=formatted_faces)
    
    def _format_face_data(self, face):
        """格式化照片数据，生成符合要求的返回字段"""
        person_id = face['personId']
        face_id = face['faceId']
        
        # 生成模拟的路径
        base_path = f"ftp://192.168.19.73:8010/RegisterPhoto/{person_id}_{face_id}"
        
        # 生成模拟的人脸框坐标
        rect = '{"bottom":696,"empty":false,"left":241,"right":706,"top":231}'
        
        # 生成模拟的特征值
        feature = "qrC1AAAAAAAAA==" if len(face_id) == 3 else "qrC1AAAAAAAAAQAA5u+Uug=="
        
        # 构建格式化的照片数据
        formatted_face = {
            'cropImgPath': f"{base_path}_crop.jpg",
            'faceId': face_id,
            'feature': feature,
            'SDKVersion': "general_2.0.10.0",
            'featureKey': "",
            'path': f"{base_path}.jpg",
            'personId': person_id,
            'rect': rect
        }
        
        return formatted_face
    
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