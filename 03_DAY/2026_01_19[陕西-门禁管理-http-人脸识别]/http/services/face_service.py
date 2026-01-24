## 照片管理业务逻辑

from rules.response import base_response, ERROR_CODES
from models import face_data, person_data

class FaceService:
    """照片管理业务逻辑类"""
    
    @staticmethod
    def create_face(person_id, face_id, img_base64, is_easy_way=False):
        """照片注册"""
        import time
        import re
        import random
        import string
        
        # 1. 参数异常检查
        if person_id is None:
            return base_response(0, False, 'personId 参数异常', 'LAN_EXP-3015')
        if img_base64 is None:
            return base_response(0, False, 'imgBase64 参数异常', ERROR_CODES['IMG_BASE64_PARAM_ERROR'])
        
        # 2. 参数值检查
        # personId 不能为空
        if not person_id.strip():
            return base_response(0, False, 'personId 参数不能为空', 'LAN_EXP-3016')
        # personId 只允许数字和英文字母，长度限制255
        if not re.match(r'^[a-zA-Z0-9]{1,255}$', person_id):
            return base_response(0, False, '人员 ID(personId)只允许数字 0~9和英文字母，且最大长度为 255', 'LAN_EXP-4005')
        
        # 3. 检查人员是否存在
        if not person_data.get_person(person_id):
            return base_response(0, False, '人员 ID 不存在，请先调用人员注册接口', ERROR_CODES['PERSON_ID_NOT_EXISTS'])
        
        # 4. 检查该人员照片数量是否已达上限(3张)
        existing_faces = face_data.get_faces_by_person(person_id)
        if len(existing_faces) >= 3:
            return base_response(0, False, '注册照片已达到最大数量限定(3 张)', 'LAN_EXP-4012')
        
        # 5. faceId 处理
        if face_id.strip():
            # faceId 内容检查：只允许数字和英文字母，区分大小写，长度限制255个字符
            if not re.match(r'^[a-zA-Z0-9]{1,255}$', face_id):
                return base_response(0, False, '照片 ID(faceId)只允许数字 0~9 和英文字母，且最大长度为 255', ERROR_CODES['FACE_ID_ILLEGAL'])
            # 检查 faceId 是否已存在
            if face_data.get_face(face_id):
                return base_response(0, False, '照片 ID 已存在，请先调用删除或更新接口', ERROR_CODES['FACE_ID_EXISTS'])
        else:
            # 生成 32 位 faceId
            face_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        # 6. imgBase64 检查
        if not img_base64.strip():
            return base_response(0, False, 'imgBase64 不能为空', ERROR_CODES['IMG_BASE64_EMPTY'])
        # 去除 base64 头部
        if img_base64.startswith('data:image'):
            if ',' in img_base64:
                img_base64 = img_base64.split(',', 1)[1]
        
        # 7. isEasyWay 严格检查：只允许 true/false
        if isinstance(is_easy_way, str):
            is_easy_way = is_easy_way.lower()
            if is_easy_way not in ['true', 'false']:
                return base_response(0, False, 'isEasyWay 参数不合法', ERROR_CODES['IS_EASY_WAY_ILLEGAL'])
            is_easy_way = is_easy_way == 'true'
        else:
            # 非字符串类型，转换为布尔值，但确保它是有效的布尔类型
            try:
                is_easy_way = bool(is_easy_way)
            except:
                return base_response(0, False, 'isEasyWay 参数不合法', ERROR_CODES['IS_EASY_WAY_ILLEGAL'])
        
        # 8. imgBase64 详细验证
        import base64
        import re
        import random
        try:
            # 8.1 验证 base64 格式是否正确
            # 检查 base64 字符串是否只有有效的字符
            if not re.match(r'^[A-Za-z0-9+/=]*$', img_base64):
                return base_response(0, False, '提供的图片文件不完整或格式不正确', 'LAN_EXP-4035')
            
            # 8.2 尝试解码 base64
            img_bytes = base64.b64decode(img_base64)
            
            # 8.3 检查图片格式（通过文件头 magic bytes）
            # JPEG: FF D8
            # PNG: 89 50 4E 47
            # GIF: 47 49 46 38（不支持）
            # BMP: 42 4D（不支持）
            if img_bytes.startswith(b'\xff\xd8'):
                img_format = 'jpeg'
            elif img_bytes.startswith(b'\x89PNG'):
                img_format = 'png'
            else:
                # 检查是否是 JPG（另一种可能的 JPEG 头？不，JPEG 标准是 FF D8）
                # 其他格式不支持
                return base_response(0, False, '图片格式不支持', 'LAN_EXP-2218')
            
            # 8.4 尝试获取分辨率（简化处理，不使用PIL）
            # 只做基本的图片数据检查，确保不是空文件
            if len(img_bytes) < 100:
                return base_response(0, False, '提供的图片文件不完整或格式不正确', 'LAN_EXP-4035')
            
            # 8.5 简化的图像质量检查（不使用OpenCV和numpy）
            # 模拟人脸检测和质量评估
            # 注意：由于移除了OpenCV，这里简化了检测逻辑，实际应用中需要替换为其他人脸检测方案
            # 这里我们只做基本的模拟，确保业务流程正常
            
            # 模拟人脸检测成功
            # 假设图像质量检查通过，返回成功
            # 实际应用中，这里应该集成其他人脸检测方案
            
        except base64.binascii.Error:
            # base64 解码失败
            return base_response(0, False, '图片解析异常', 'LAN_EXP-4011')
        except Exception as e:
            # 其他异常，如文件不完整
            return base_response(0, False, '提供的图片文件不完整或格式不正确', 'LAN_EXP-4035')
        

        
        # 8. 模拟照片注册
        face = {
            'personId': person_id,
            'faceId': face_id,
            'imgBase64': img_base64[:100] + '...' if len(img_base64) > 100 else img_base64,
            'isEasyWay': is_easy_way,
            'createTime': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # 9. 尝试添加照片，检查是否成功
        if not face_data.add_face(face):
            # 存储已满
            return base_response(0, False, '设备存储空间已满', 'LAN_EXP-4030')
        
        # 10. 返回结果：data 为调用接口时填入的 faceId 或者生成的 faceId
        return base_response(data=face_id, msg='照片添加成功')
    
    @staticmethod
    def delete_face(face_id):
        """照片删除"""
        import re
        
        # 1. 参数异常检查
        if face_id is None:
            return base_response(0, False, 'faceId 参数异常', ERROR_CODES['FACE_ID_PARAM_ERROR'])
        
        # 2. 参数值检查
        # faceId 不能为空
        if not face_id.strip():
            return base_response(0, False, 'faceId 参数不能为空', 'LAN_EXP-4016')
        
        # faceId 只允许数字和英文字母，长度限制255
        if not re.match(r'^[a-zA-Z0-9]{1,255}$', face_id):
            return base_response(0, False, '照片 ID(faceId)只允许数字 0~9 和英文字母，且最大长度为 255', 'LAN_EXP-4006')
        
        # 3. 检查照片是否存在
        if not face_data.get_face(face_id):
            return base_response(0, False, '照片 ID 不存在，请先调用照片注册接口', 'LAN_EXP-4017')
        
        # 4. 执行删除操作
        if face_data.delete_face(face_id):
            return base_response(msg='照片删除成功')
        
        # 5. 数据库异常
        return base_response(0, False, '数据库异常，照片删除失败', 'LAN_EXP-4018')
    
    @staticmethod
    def find_face(person_id):
        """照片查询"""
        if not person_id:
            return base_response(0, False, '人员ID不能为空')
        
        faces = face_data.get_faces_by_person(person_id)
        return base_response(data=faces)
    
    @staticmethod
    def take_img(person_id):
        """拍照注册"""
        import re
        import time
        from models import device_data
        
        # 1. 通用设备状态检查
        # 1.1 检查设备是否被禁用
        if device_data.is_disabled():
            return base_response(0, False, '设备已被禁用，请先启用再做其它操作', 'LAN_EXP-1004')
        
        # 1.2 检查设备是否正忙
        if device_data.is_busy():
            return base_response(0, False, '设备正忙，请稍后再试', 'LAN_EXP-1005')
        
        # 2. 参数异常检查
        if person_id is None:
            return base_response(0, False, 'personId 参数异常', 'LAN_EXP-3015')
        
        # 3. 参数不合法检查
        # 3.1 personId 参数不能为空
        if not person_id.strip():
            return base_response(0, False, 'personId 参数不能为空', 'LAN_EXP-3016')
        
        # 3.2 人员 ID(personId)只允许数字 0~9 和英文字母，且最大长度为 255
        if not re.match(r'^[a-zA-Z0-9]{1,255}$', person_id):
            return base_response(0, False, '人员 ID(personId)只允许数字 0~9 和英文字母，且最大长度为 255', 'LAN_EXP-4005')
        
        # 4. 检查人员是否存在
        if not person_data.get_person(person_id):
            return base_response(0, False, '人员 ID 不存在，请先调用人员注册接口', 'LAN_EXP-3009')
        
        # 5. 检查该人员照片数量是否已达上限(3张)
        existing_faces = face_data.get_faces_by_person(person_id)
        if len(existing_faces) >= 3:
            return base_response(0, False, '注册照片已达到最大数量限定 (3 张)', 'LAN_EXP-4012')
        
        # 6. 生成随机ID
        import random
        import string
        face_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        # 7. 模拟拍照注册
        # 生成当前时间戳
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        
        # 模拟拍照，创建照片记录
        face = {
            'personId': person_id,
            'faceId': face_id,
            'imgBase64': 'MOCK_BASE64_IMAGE_DATA',
            'isEasyWay': False,
            'createTime': timestamp
        }
        
        # 8. 添加照片
        face_data.add_face(face)
        
        # 9. 返回正确的响应消息
        return base_response(data=None, msg='正在开启拍照注册模式，注册成功后可根据personId查询拍摄的照片。请根据引导完成注册')
    
    @staticmethod
    def delete_person_faces(person_id):
        """清空人员注册照片"""
        import re
        
        # 1. 参数异常检查
        if person_id is None:
            return base_response(0, False, 'personId 参数异常', 'LAN_EXP-3015')
        
        # 2. 参数不合法检查
        # personId 参数不能为空
        if not person_id.strip():
            return base_response(0, False, 'personId 参数不能为空', 'LAN_EXP-3016')
        
        # 人员 ID(personId)只允许数字 0~9 和英文字母，且最大长度为 255
        if not re.match(r'^[a-zA-Z0-9]{1,255}$', person_id):
            return base_response(0, False, '人员 ID(personId)只允许数字 0~9 和英文字母，且最大长度为 255', 'LAN_EXP-4005')
        
        # 3. 检查人员是否存在
        if not person_data.get_person(person_id):
            return base_response(0, False, '人员 ID 不存在，请先调用人员注册接口', 'LAN_EXP-3009')
        
        # 4. 检查该人员是否有注册照片
        existing_faces = face_data.get_faces_by_person(person_id)
        if len(existing_faces) == 0:
            return base_response(msg='该人员没有注册照片')
        
        # 5. 尝试清空照片
        try:
            face_data.delete_faces_by_person(person_id)
            return base_response(msg='照片清空成功')
        except Exception as e:
            # 数据库异常
            return base_response(0, False, '数据库异常', 'LAN_EXP-4025')
    
    @staticmethod
    def update_face(person_id, face_id, img_base64, is_easy_way=False):
        """照片更新"""
        import re
        import time
        
        # 1. 参数异常检查
        if person_id is None:
            return base_response(0, False, 'personId 参数异常', 'LAN_EXP-3015')
        if face_id is None:
            return base_response(0, False, 'faceId 参数异常', ERROR_CODES['FACE_ID_PARAM_ERROR'])
        if img_base64 is None:
            return base_response(0, False, 'imgBase64 参数异常', ERROR_CODES['IMG_BASE64_PARAM_ERROR'])
        
        # 2. 参数值检查
        # personId 不能为空
        if not person_id.strip():
            return base_response(0, False, 'personId 参数不能为空', 'LAN_EXP-3016')
        # personId 只允许数字和英文字母，长度限制255
        if not re.match(r'^[a-zA-Z0-9]{1,255}$', person_id):
            return base_response(0, False, '人员 ID(personId)只允许数字 0~9和英文字母，且最大长度为 255', 'LAN_EXP-4005')
        
        # faceId 不能为空
        if not face_id.strip():
            return base_response(0, False, 'faceId 参数不能为空', 'LAN_EXP-4016')
        # faceId 只允许数字和英文字母，长度限制255
        if not re.match(r'^[a-zA-Z0-9]{1,255}$', face_id):
            return base_response(0, False, '照片 ID(faceId)只允许数字 0~9 和英文字母，且最大长度为 255', ERROR_CODES['FACE_ID_ILLEGAL'])
        
        # 3. 检查人员是否存在
        if not person_data.get_person(person_id):
            return base_response(0, False, '人员 ID 不存在，请先调用人员注册接口', ERROR_CODES['PERSON_ID_NOT_EXISTS'])
        
        # 4. 检查照片是否存在，并且属于该人员
        face = face_data.get_face(face_id)
        if not face:
            return base_response(0, False, '照片 ID 不存在，请先调用照片注册接口', 'LAN_EXP-4017')
        # 检查照片是否属于该人员
        if face['personId'] != person_id:
            return base_response(0, False, '该人员没有这个照片 ID，请先调用照片注册接口', 'LAN_EXP-4031')
        
        # 5. imgBase64 检查
        if not img_base64.strip():
            return base_response(0, False, 'imgBase64 不能为空', 'LAN_EXP-4008')
        # 去除 base64 头部
        if img_base64.startswith('data:image'):
            if ',' in img_base64:
                img_base64 = img_base64.split(',', 1)[1]
        
        # 6. isEasyWay 严格检查：只允许 true/false
        if isinstance(is_easy_way, str):
            is_easy_way = is_easy_way.lower()
            if is_easy_way not in ['true', 'false']:
                return base_response(0, False, 'isEasyWay 参数不合法', 'LAN_EXP-4009')
            is_easy_way = is_easy_way == 'true'
        else:
            # 非字符串类型，转换为布尔值，但确保它是有效的布尔类型
            try:
                is_easy_way = bool(is_easy_way)
            except:
                return base_response(0, False, 'isEasyWay 参数不合法', 'LAN_EXP-4009')
        
        # 7. imgBase64 详细验证
        import base64
        import random
        try:
            # 7.1 验证 base64 格式是否正确
            # 检查 base64 字符串是否只有有效的字符
            if not re.match(r'^[A-Za-z0-9+/=]*$', img_base64):
                return base_response(0, False, '提供的图片文件不完整或格式不正确', 'LAN_EXP-4010')
            
            # 7.2 尝试解码 base64
            img_bytes = base64.b64decode(img_base64)
            
            # 7.3 检查图片格式（通过文件头 magic bytes）
            # JPEG: FF D8
            # PNG: 89 50 4E 47
            # GIF: 47 49 46 38（不支持）
            if img_bytes.startswith(b'\xff\xd8'):
                img_format = 'jpeg'
            elif img_bytes.startswith(b'\x89PNG'):
                img_format = 'png'
            elif img_bytes.startswith(b'\x47\x49\x46\x38'):
                # GIF 格式不支持
                return base_response(0, False, 'imgBase64 不能为 gif 图', 'LAN_EXP-4032')
            else:
                # 其他格式不支持
                return base_response(0, False, '图片格式不支持', 'LAN_EXP-2218')
            
            # 7.4 尝试获取分辨率（简化处理，不使用PIL）
            # 只做基本的图片数据检查，确保不是空文件
            if len(img_bytes) < 100:
                return base_response(0, False, '提供的图片文件不完整或格式不正确', 'LAN_EXP-4010')
            
            # 7.5 简化的图像质量检查（不使用OpenCV和numpy）
            # 模拟人脸检测和质量评估
            # 注意：由于移除了OpenCV，这里简化了检测逻辑，实际应用中需要替换为其他人脸检测方案
            # 这里我们只做基本的模拟，确保业务流程正常
            
            # 模拟人脸检测成功
            # 假设图像质量检查通过，返回成功
            # 实际应用中，这里应该集成其他人脸检测方案
            
        except base64.binascii.Error:
            # base64 解码失败
            return base_response(0, False, '图片解析异常', 'LAN_EXP-4011')
        except Exception as e:
            # 其他异常，如文件不完整
            return base_response(0, False, '提供的图片文件不完整或格式不正确', 'LAN_EXP-4010')
        
        # 更新照片
        updated_face = {
            'personId': person_id,
            'faceId': face_id,
            'imgBase64': img_base64[:100] + '...' if len(img_base64) > 100 else img_base64,
            'isEasyWay': is_easy_way,
            'createTime': face['createTime'],
            'updateTime': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        if face_data.update_face(updated_face):
            return base_response(data=updated_face, msg='照片更新成功')
        
        # 数据库异常
        return base_response(0, False, '数据库异常，照片更新失败', 'LAN_EXP-4020')

# 创建照片服务实例
face_service = FaceService()