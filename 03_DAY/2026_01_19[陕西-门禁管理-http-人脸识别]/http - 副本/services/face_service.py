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
            
            # 8.4 尝试打开图片获取分辨率和进行人脸检测
            try:
                from io import BytesIO
                from PIL import Image
                
                img = Image.open(BytesIO(img_bytes))
                width, height = img.size
                
                # 8.5 检查分辨率是否超过 1080p (1920x1080)
                if width > 1920 or height > 1080:
                    return base_response(0, False, '图片分辨率大于 1080p', 'LAN_EXP-2241')
                
                # 8.6 真实人脸检测和质量检查
                # 使用OpenCV进行实际的人脸检测和质量评估
                import cv2
                import numpy as np
                
                try:
                    # 将图片转换为OpenCV格式
                    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
                    if img is None:
                        return base_response(0, False, '提供的图片文件不完整或格式不正确', 'LAN_EXP-4035')
                    
                    # 加载人脸检测模型
                    # 使用OpenCV内置的Haar级联分类器（轻量级，适合快速检测）
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    
                    # 将图片转换为灰度图用于检测
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    
                    # 检测人脸
                    faces = face_cascade.detectMultiScale(
                        gray, 
                        scaleFactor=1.1, 
                        minNeighbors=5, 
                        minSize=(30, 30),
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )
                    
                    # 1. 检查是否检测到人脸
                    if len(faces) == 0:
                        return base_response(0, False, '未检测到面部', 'LAN_EXP-8006')
                    
                    # 2. 检查是否检测到多个面部
                    if len(faces) > 1:
                        return base_response(0, False, '检测到多个面部', 'LAN_EXP-8007')
                    
                    # 获取人脸坐标和大小
                    x, y, w, h = faces[0]
                    face_area = w * h
                    img_area = img.shape[0] * img.shape[1]
                    
                    # 3. 检查人脸大小：人脸应占图片的1/3以上
                    face_ratio = face_area / img_area
                    if face_ratio < 1/3:
                        return base_response(0, False, '人像过小，人像应占1/3以上', 'LAN_EXP-8010')
                    
                    # 4. 检查人脸是否完整：人脸应在图片内，不超出边界
                    # 检查人脸是否太靠近边缘（留出10%的边缘余量）
                    margin = 0.1
                    img_h, img_w = img.shape[:2]
                    if (x < img_w * margin or 
                        y < img_h * margin or 
                        x + w > img_w * (1 - margin) or 
                        y + h > img_h * (1 - margin)):
                        return base_response(0, False, '面部过大或面部不完整', 'LAN_EXP-8013')
                    
                    # 5. 检查人脸亮度和对比度
                    # 提取人脸区域
                    face_roi = gray[y:y+h, x:x+w]
                    
                    # 计算人脸区域的亮度（均值）
                    face_brightness = np.mean(face_roi)
                    
                    # 计算人脸区域的对比度（标准差）
                    face_contrast = np.std(face_roi)
                    
                    # 6. 检查亮度是否合适（100-180之间为理想范围）
                    if face_brightness < 50 or face_brightness > 200:
                        return base_response(0, False, '人像面部太暗或太亮', 'LAN_EXP-8015')
                    
                    # 7. 检查对比度是否合适（对比度太低表示图像模糊）
                    if face_contrast < 20:
                        return base_response(0, False, '人像清晰度过低', 'LAN_EXP-8016')
                    
                    # 8. 检查光线均匀度（计算人脸区域的梯度）
                    # 使用Sobel算子计算梯度
                    grad_x = cv2.Sobel(face_roi, cv2.CV_64F, 1, 0, ksize=3)
                    grad_y = cv2.Sobel(face_roi, cv2.CV_64F, 0, 1, ksize=3)
                    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
                    
                    # 计算梯度的标准差（表示光线变化程度）
                    grad_std = np.std(grad_mag)
                    if grad_std > 100:
                        return base_response(0, False, '人像面部光线不均匀', 'LAN_EXP-8017')
                    
                    # 8. 检查人脸偏转角度
                    # 简单模拟：基于人脸宽度和高度的比例判断偏转角度
                    # 正常正面人脸的宽高比约为 0.8-1.2
                    face_aspect_ratio = w / h
                    if face_aspect_ratio < 0.6 or face_aspect_ratio > 1.4:
                        return base_response(0, False, '人像偏转角度过大', 'LAN_EXP-8014')
                    
                    # 9. 更精确的特征提取模拟
                    # 在实际应用中，这里会调用真正的FaceSDK进行特征提取
                    # 这里我们基于更全面的图像质量指标计算成功率
                    # 权重分配：
                    # - 人脸大小占30%
                    # - 亮度占20%
                    # - 对比度占20%
                    # - 光线均匀度占15%
                    # - 人脸完整性占15%
                    
                    # 计算各项得分（0-100分）
                    # 1. 人脸大小得分：越大越好，但不超过50%
                    size_score = min(face_ratio / 0.5 * 100, 100) if face_ratio > 0.2 else 0
                    
                    # 2. 亮度得分：100-160为最佳
                    if face_brightness >= 100 and face_brightness <= 160:
                        brightness_score = 100
                    elif face_brightness < 100:
                        brightness_score = max(face_brightness / 100 * 100, 0)
                    else:
                        brightness_score = max((220 - face_brightness) / 60 * 100, 0)
                    
                    # 3. 对比度得分：越高越好
                    contrast_score = min(face_contrast / 100 * 100, 100)
                    
                    # 4. 光线均匀度得分：越低越好
                    lighting_uniformity_score = max((150 - grad_std) / 150 * 100, 0)
                    
                    # 5. 人脸完整性得分：根据边缘距离计算
                    # 计算人脸中心到边缘的最小距离
                    center_x = x + w/2
                    center_y = y + h/2
                    min_margin = min(center_x, img_w - center_x, center_y, img_h - center_y)
                    # 计算完整性得分：最小距离越大越好
                    integrity_score = min(min_margin / (min(img_w, img_h)/4) * 100, 100)
                    
                    # 计算总得分，加权平均
                    total_score = (
                        size_score * 0.3 +
                        brightness_score * 0.2 +
                        contrast_score * 0.2 +
                        lighting_uniformity_score * 0.15 +
                        integrity_score * 0.15
                    )
                    
                    # 特征提取成功率：总得分大于60分为成功
                    feature_success = total_score > 60
                    
                    if not feature_success:
                        # 根据得分确定具体错误类型
                        if size_score < 50:
                            # 人脸太小
                            return base_response(0, False, '人像过小，人像应占1/3以上', 'LAN_EXP-8010')
                        elif brightness_score < 50:
                            # 亮度问题
                            return base_response(0, False, '人像面部太暗或太亮', 'LAN_EXP-8015')
                        elif contrast_score < 50:
                            # 清晰度问题
                            return base_response(0, False, '人像清晰度过低', 'LAN_EXP-8016')
                        elif lighting_uniformity_score < 50:
                            # 光线均匀度问题
                            return base_response(0, False, '人像面部光线不均匀', 'LAN_EXP-8017')
                        elif integrity_score < 50:
                            # 完整性问题
                            return base_response(0, False, '面部过大或面部不完整', 'LAN_EXP-8013')
                        else:
                            # 随机选择一个特征提取相关的错误
                            feature_error = random.choice(['LAN_EXP-8011', 'LAN_EXP-8012'])
                            error_msg = 'FaceSDK 无法从照片中提取特征' if feature_error == 'LAN_EXP-8011' else 'FaceSDK 提取特征异常'
                            return base_response(0, False, error_msg, feature_error)
                    
                    # 10. 成功通过所有检查
                    # 人脸检测和质量检查通过
                    pass
                    
                except Exception as e:
                    # 处理任何异常，返回通用的图像解析异常
                    return base_response(0, False, '图片解析异常', 'LAN_EXP-4011')
                    
            except ImportError:
                # PIL 未安装，跳过分辨率和人脸检测检查
                # 但仍返回成功，因为这是可选检查
                pass
            except Exception as e:
                # 图片解析异常
                return base_response(0, False, '图片解析异常', 'LAN_EXP-4011')
                
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
            
            # 7.4 尝试打开图片获取分辨率和进行人脸检测
            try:
                from io import BytesIO
                from PIL import Image
                
                img = Image.open(BytesIO(img_bytes))
                width, height = img.size
                
                # 7.5 检查分辨率是否超过 1080p (1920x1080)
                if width > 1920 or height > 1080:
                    return base_response(0, False, '图片分辨率大于 1080p', 'LAN_EXP-2241')
                
                # 7.6 真实人脸检测和质量检查
                # 使用OpenCV进行实际的人脸检测和质量评估
                import cv2
                import numpy as np
                
                try:
                    # 将图片转换为OpenCV格式
                    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
                    if img is None:
                        return base_response(0, False, '提供的图片文件不完整或格式不正确', 'LAN_EXP-4010')
                    
                    # 加载人脸检测模型
                    # 使用OpenCV内置的Haar级联分类器（轻量级，适合快速检测）
                    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
                    
                    # 将图片转换为灰度图用于检测
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    
                    # 检测人脸
                    faces = face_cascade.detectMultiScale(
                        gray, 
                        scaleFactor=1.1, 
                        minNeighbors=5, 
                        minSize=(30, 30),
                        flags=cv2.CASCADE_SCALE_IMAGE
                    )
                    
                    # 1. 检查是否检测到人脸
                    if len(faces) == 0:
                        return base_response(0, False, '未检测到面部', 'LAN_EXP-8006')
                    
                    # 2. 检查是否检测到多个面部
                    if len(faces) > 1:
                        return base_response(0, False, '检测到多个面部', 'LAN_EXP-8007')
                    
                    # 获取人脸坐标和大小
                    x, y, w, h = faces[0]
                    face_area = w * h
                    img_area = img.shape[0] * img.shape[1]
                    
                    # 3. 检查人脸大小：人脸应占图片的1/3以上
                    face_ratio = face_area / img_area
                    if face_ratio < 1/3:
                        return base_response(0, False, '人像过小，人像应占1/3以上', 'LAN_EXP-8010')
                    
                    # 4. 检查人脸是否完整：人脸应在图片内，不超出边界
                    # 检查人脸是否太靠近边缘（留出10%的边缘余量）
                    margin = 0.1
                    img_h, img_w = img.shape[:2]
                    if (x < img_w * margin or 
                        y < img_h * margin or 
                        x + w > img_w * (1 - margin) or 
                        y + h > img_h * (1 - margin)):
                        return base_response(0, False, '面部过大或面部不完整', 'LAN_EXP-8013')
                    
                    # 5. 检查人脸亮度和对比度
                    # 提取人脸区域
                    face_roi = gray[y:y+h, x:x+w]
                    
                    # 计算人脸区域的亮度（均值）
                    face_brightness = np.mean(face_roi)
                    
                    # 计算人脸区域的对比度（标准差）
                    face_contrast = np.std(face_roi)
                    
                    # 6. 检查亮度是否合适（100-180之间为理想范围）
                    if face_brightness < 50 or face_brightness > 200:
                        return base_response(0, False, '人像面部太暗或太亮', 'LAN_EXP-8015')
                    
                    # 7. 检查对比度是否合适（对比度太低表示图像模糊）
                    if face_contrast < 20:
                        return base_response(0, False, '人像清晰度过低', 'LAN_EXP-8016')
                    
                    # 8. 检查光线均匀度（计算人脸区域的梯度）
                    # 使用Sobel算子计算梯度
                    grad_x = cv2.Sobel(face_roi, cv2.CV_64F, 1, 0, ksize=3)
                    grad_y = cv2.Sobel(face_roi, cv2.CV_64F, 0, 1, ksize=3)
                    grad_mag = np.sqrt(grad_x**2 + grad_y**2)
                    
                    # 计算梯度的标准差（表示光线变化程度）
                    grad_std = np.std(grad_mag)
                    if grad_std > 100:
                        return base_response(0, False, '人像面部光线不均匀', 'LAN_EXP-8017')
                    
                    # 8. 检查人脸偏转角度
                    # 简单模拟：基于人脸宽度和高度的比例判断偏转角度
                    # 正常正面人脸的宽高比约为 0.8-1.2
                    face_aspect_ratio = w / h
                    if face_aspect_ratio < 0.6 or face_aspect_ratio > 1.4:
                        return base_response(0, False, '人像偏转角度过大', 'LAN_EXP-8014')
                    
                    # 9. 更精确的特征提取模拟
                    # 在实际应用中，这里会调用真正的FaceSDK进行特征提取
                    # 这里我们基于更全面的图像质量指标计算成功率
                    # 权重分配：
                    # - 人脸大小占30%
                    # - 亮度占20%
                    # - 对比度占20%
                    # - 光线均匀度占15%
                    # - 人脸完整性占15%
                    
                    # 计算各项得分（0-100分）
                    # 1. 人脸大小得分：越大越好，但不超过50%
                    size_score = min(face_ratio / 0.5 * 100, 100) if face_ratio > 0.2 else 0
                    
                    # 2. 亮度得分：100-160为最佳
                    if face_brightness >= 100 and face_brightness <= 160:
                        brightness_score = 100
                    elif face_brightness < 100:
                        brightness_score = max(face_brightness / 100 * 100, 0)
                    else:
                        brightness_score = max((220 - face_brightness) / 60 * 100, 0)
                    
                    # 3. 对比度得分：越高越好
                    contrast_score = min(face_contrast / 100 * 100, 100)
                    
                    # 4. 光线均匀度得分：越低越好
                    lighting_uniformity_score = max((150 - grad_std) / 150 * 100, 0)
                    
                    # 5. 人脸完整性得分：根据边缘距离计算
                    # 计算人脸中心到边缘的最小距离
                    center_x = x + w/2
                    center_y = y + h/2
                    min_margin = min(center_x, img_w - center_x, center_y, img_h - center_y)
                    # 计算完整性得分：最小距离越大越好
                    integrity_score = min(min_margin / (min(img_w, img_h)/4) * 100, 100)
                    
                    # 计算总得分，加权平均
                    total_score = (
                        size_score * 0.3 +
                        brightness_score * 0.2 +
                        contrast_score * 0.2 +
                        lighting_uniformity_score * 0.15 +
                        integrity_score * 0.15
                    )
                    
                    # 特征提取成功率：总得分大于60分为成功
                    feature_success = total_score > 60
                    
                    if not feature_success:
                        # 根据得分确定具体错误类型
                        if size_score < 50:
                            # 人脸太小
                            return base_response(0, False, '人像过小，人像应占1/3以上', 'LAN_EXP-8010')
                        elif brightness_score < 50:
                            # 亮度问题
                            return base_response(0, False, '人像面部太暗或太亮', 'LAN_EXP-8015')
                        elif contrast_score < 50:
                            # 清晰度问题
                            return base_response(0, False, '人像清晰度过低', 'LAN_EXP-8016')
                        elif lighting_uniformity_score < 50:
                            # 光线均匀度问题
                            return base_response(0, False, '人像面部光线不均匀', 'LAN_EXP-8017')
                        elif integrity_score < 50:
                            # 完整性问题
                            return base_response(0, False, '面部过大或面部不完整', 'LAN_EXP-8013')
                        else:
                            # 随机选择一个特征提取相关的错误
                            feature_error = random.choice(['LAN_EXP-8011', 'LAN_EXP-8012'])
                            error_msg = 'FaceSDK 无法从照片中提取特征' if feature_error == 'LAN_EXP-8011' else 'FaceSDK 提取特征异常'
                            return base_response(0, False, error_msg, feature_error)
                    
                    # 10. 成功通过所有检查
                    # 人脸检测和质量检查通过
                    pass
                    
                except Exception as e:
                    # 处理任何异常，返回通用的图像解析异常
                    return base_response(0, False, '图片解析异常', 'LAN_EXP-4011')
                    
            except ImportError:
                # PIL 未安装，跳过分辨率和人脸检测检查
                pass
            except Exception as e:
                # 图片解析异常
                return base_response(0, False, '图片解析异常', 'LAN_EXP-4011')
                
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