# 人员管理业务逻辑

from rules.response import base_response, ERROR_CODES
from models import person_data, face_data

class PersonService:
    """人员管理业务逻辑类"""
    
    @staticmethod
    def create_person(person_json):
        """人员注册"""
        if not person_json:
            return base_response(0, False, '人员信息不能为空', ERROR_CODES['PERSON_PARAM_ERROR'])
        
        try:
            import json
            import re
            
            # 解析JSON
            person = json.loads(person_json)
            
            # 1. 检查person是否为空
            if not isinstance(person, dict) or not person:
                return base_response(0, False, 'person 类 json 格式错误', ERROR_CODES['PERSON_JSON_ERROR'])
            
            # 2. 处理ID：如果没有ID则生成，否则验证格式
            if 'id' not in person:
                import random
                import string
                person['id'] = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
            else:
                # 验证ID格式：只允许数字和英文字母，最大长度255
                person_id = person['id']
                if not re.match(r'^[a-zA-Z0-9]{1,255}$', person_id):
                    return base_response(0, False, '人员 ID(id)只允许数字 0~9 和英文字母，且最大长度为 255', ERROR_CODES['PERSON_ID_ILLEGAL'])
                
                # 检查ID是否已存在
                if person_data.get_person(person_id):
                    return base_response(0, False, '人员ID已存在，请调用人员删除或者更新接口', ERROR_CODES['PERSON_ID_EXISTS'])
            
            # 3. 验证name参数不能为空
            if 'name' not in person or not person['name'].strip():
                return base_response(0, False, 'name参数不能为空', ERROR_CODES['NAME_EMPTY'])
            
            # 4. 验证权限参数
            permission_params = {
                'facePermission': 'LAN_EXP-3011',
                'idCardPermission': 'LAN_EXP-3012',
                'faceAndCardPermission': 'LAN_EXP-3013'
            }
            for param, error_code in permission_params.items():
                if param in person:
                    value = person[param]
                    # 允许整数1/2或字符串'1'/'2'
                    if value not in [1, 2, '1', '2']:
                        return base_response(0, False, f'{param}参数不合法', error_code)
                else:
                    # 设置不同的默认值
                    if param == 'faceAndCardPermission':
                        person[param] = 1
                    else:
                        person[param] = 2
            
            # 5. 添加缺失的字段和默认值
            import time
            person.setdefault('createTime', int(time.time() * 1000))  # 当前时间戳（毫秒）
            person.setdefault('iDNumber', '')  # 身份证号码
            person.setdefault('iDPermission', person.get('idCardPermission'))  # 与idCardPermission保持一致
            person.setdefault('idcardNum', '')  # ID卡号码
            person.setdefault('phone', '')  # 电话号码
            person.setdefault('tag', '00')  # 标签
            
            # 6. 添加人员
            person_data.add_person(person)
            
            return base_response(data=person, msg='人员信息添加成功')
        except json.JSONDecodeError:
            return base_response(0, False, 'person类json格式错误', ERROR_CODES['PERSON_JSON_ERROR'])
        except Exception as e:
            # 数据库异常
            return base_response(0, False, '数据库异常，人员注册失败', 'LAN_EXP-3006')
    
    @staticmethod
    def delete_person(id_):
        """人员删除"""
        if not id_:
            return base_response(0, False, '人员ID不能为空')
        
        import re
        
        # 处理多个ID，用逗号分隔
        ids = id_.split(',')
        effective_ids = []
        invalid_ids = []
        
        # 检查是否包含-1（删除所有）
        if '-1' in ids:
            # 删除所有人员
            person_data.delete_person('-1')
            # 删除所有识别记录
            from models.record import record_data
            record_data.delete_records('-1')
            # 删除所有照片
            face_data.delete_faces_by_person('-1')
            # 有效的ID是-1，其他都是无效的
            effective_ids = ['-1']
            invalid_ids = [id_item for id_item in ids if id_item != '-1']
        else:
            # 处理单个或多个人员删除
            for id_item in ids:
                # 验证ID格式
                if id_item != '-1' and not re.match(r'^[a-zA-Z0-9]{1,255}$', id_item):
                    invalid_ids.append(id_item)
                else:
                    # 检查人员是否存在
                    if person_data.get_person(id_item):
                        # 删除人员
                        person_data.delete_person(id_item)
                        # 删除该人员的识别记录
                        from models.record import record_data
                        record_data.delete_records(id_item)
                        # 删除该人员的照片
                        face_data.delete_faces_by_person(id_item)
                        effective_ids.append(id_item)
                    else:
                        invalid_ids.append(id_item)
        
        # 生成返回数据
        effective_str = ','.join(effective_ids)
        invalid_str = ','.join(invalid_ids)
        
        # 构建返回消息
        msg = "effective中的内容代表已删余有效的ID；invalid中的内容代表无效或者不存在的ID"
        
        # 返回响应
        return base_response(
            data={
                'effective': effective_str,
                'invalid': invalid_str
            },
            msg=msg
        )
    
    @staticmethod
    def update_person(person_json):
        """人员更新"""
        if not person_json:
            return base_response(0, False, '人员信息不能为空', ERROR_CODES['PERSON_PARAM_ERROR'])
        
        try:
            import json
            import re
            
            # 解析JSON
            person = json.loads(person_json)
            
            # 1. 检查person是否为空
            if not isinstance(person, dict) or not person:
                return base_response(0, False, 'person 类 json 格式错误', ERROR_CODES['PERSON_JSON_ERROR'])
            
            # 2. 检查必要字段
            if 'id' not in person:
                return base_response(0, False, '人员ID不能为空', ERROR_CODES['PERSON_ID_EMPTY'])
            
            person_id = person['id']
            
            # 3. 验证ID格式
            if not re.match(r'^[a-zA-Z0-9]{1,255}$', person_id):
                return base_response(0, False, '人员 ID(id)只允许数字 0~9 和英文字母，且最大长度为 255', ERROR_CODES['PERSON_ID_ILLEGAL'])
            
            # 4. 检查人员是否存在
            existing_person = person_data.get_person(person_id)
            if not existing_person:
                return base_response(0, False, '未找到该人员', ERROR_CODES['PERSON_ID_NOT_EXISTS'])
            
            # 5. 验证name参数：name是必传参数且内容不能为空
            if 'name' not in person:
                return base_response(0, False, 'name参数不能为空', ERROR_CODES['NAME_EMPTY'])
            elif not person['name'].strip():
                return base_response(0, False, 'name参数不能为空', ERROR_CODES['NAME_EMPTY'])
            
            # 6. 验证权限参数
            permission_params = {
                'facePermission': 'LAN_EXP-3011',
                'idCardPermission': 'LAN_EXP-3012',
                'faceAndCardPermission': 'LAN_EXP-3013'
            }
            for param, error_code in permission_params.items():
                if param in person:
                    value = person[param]
                    # 允许整数1/2或字符串'1'/'2'
                    if value not in [1, 2, '1', '2']:
                        return base_response(0, False, f'{param}参数不合法', error_code)
            
            # 7. 创建更新数据副本，确保只更新有效字段
            update_data = {}
            
            # 复制所有字段 except iDNumber，我们单独处理
            for key, value in person.items():
                if key != 'iDNumber':
                    update_data[key] = value
            
            # 单独处理iDNumber：只有当它有实际有效内容时才更新
            if 'iDNumber' in person:
                current_id_num = person['iDNumber']
                # 检查是否有实际有效内容
                has_valid_content = (
                    current_id_num is not None and 
                    current_id_num != '' and 
                    not (isinstance(current_id_num, str) and not current_id_num.strip())
                )
                if has_valid_content:
                    update_data['iDNumber'] = current_id_num
            # 如果iDNumber未传入，或传入为空值，则不包含在update_data中，保留原有值
            
            # 8. 更新人员信息
            updated_person = person_data.update_person(person_id, update_data)
            if updated_person:
                # 确保所有必要字段都存在
                import time
                # 创建响应副本，避免修改原始数据
                response_person = updated_person.copy()
                response_person.setdefault('createTime', int(time.time() * 1000))
                response_person.setdefault('iDNumber', '')
                response_person.setdefault('iDPermission', response_person.get('idCardPermission'))
                response_person.setdefault('idcardNum', '')
                response_person.setdefault('phone', '')
                response_person.setdefault('tag', '00')
                
                # 确保权限字段存在且有正确的默认值
                response_person.setdefault('facePermission', 2)
                response_person.setdefault('idCardPermission', 2)
                response_person.setdefault('faceAndCardPermission', 1)
                
                return base_response(data=response_person, msg='人员更新成功')
            
            return base_response(0, False, '未找到该人员', ERROR_CODES['PERSON_ID_NOT_EXISTS'])
        except json.JSONDecodeError:
            return base_response(0, False, 'person类json格式错误', ERROR_CODES['PERSON_JSON_ERROR'])
        except Exception as e:
            # 数据库异常
            return base_response(0, False, '数据库异常，人员更新失败', 'LAN_EXP-3006')
    
    @staticmethod
    def find_person(id_):
        """人员查询"""
        if not id_:
            return base_response(0, False, '人员ID不能为空', ERROR_CODES['PERSON_ID_EMPTY'])
        
        if id_ == '-1':
            # 确保所有人员都有完整字段
            all_persons = person_data.get_all_persons()
            import time
            for person in all_persons:
                person.setdefault('createTime', int(time.time() * 1000))
                person.setdefault('iDNumber', '')
                person.setdefault('idcardNum', '')
                person.setdefault('phone', '')
                person.setdefault('tag', '00')
                # 确保权限字段存在且有正确的默认值
                person.setdefault('facePermission', 2)
                person.setdefault('idCardPermission', 2)
                person.setdefault('faceAndCardPermission', 1)
                person.setdefault('iDPermission', person.get('idCardPermission', 2))
            return base_response(data=all_persons, msg='查询成功')
        
        person = person_data.get_person(id_)
        if person:
            # 确保查询结果有完整字段
            import time
            # 创建响应副本，避免修改原始数据
            response_person = person.copy()
            response_person.setdefault('createTime', int(time.time() * 1000))
            response_person.setdefault('iDNumber', '')
            response_person.setdefault('idcardNum', '')
            response_person.setdefault('phone', '')
            response_person.setdefault('tag', '00')
            # 确保权限字段存在且有正确的默认值
            response_person.setdefault('facePermission', 2)
            response_person.setdefault('idCardPermission', 2)
            response_person.setdefault('faceAndCardPermission', 1)
            response_person.setdefault('iDPermission', response_person.get('idCardPermission', 2))
            return base_response(data=response_person, msg='查询成功')
        
        return base_response(0, False, '人员ID不存在，请先调用人员注册接口', ERROR_CODES['PERSON_ID_NOT_EXISTS'])
    
    @staticmethod
    def find_person_by_page(person_id, index, length):
        """人员分页查询"""
        import time
        
        if person_id == '-1':
            result = person_data.get_persons_by_page(index, length)
            # 确保分页结果中的人员都有完整字段
            for person in result['data']:
                person.setdefault('createTime', int(time.time() * 1000))
                person.setdefault('iDNumber', '')
                person.setdefault('idcardNum', '')
                person.setdefault('phone', '')
                person.setdefault('tag', '00')
                # 确保权限字段存在且有正确的默认值
                person.setdefault('facePermission', 2)
                person.setdefault('idCardPermission', 2)
                person.setdefault('faceAndCardPermission', 1)
                person.setdefault('iDPermission', person.get('idCardPermission', 2))
        else:
            # 查询单个人员
            person = person_data.get_person(person_id)
            if person:
                # 确保查询结果有完整字段
                # 创建响应副本，避免修改原始数据
                response_person = person.copy()
                response_person.setdefault('createTime', int(time.time() * 1000))
                response_person.setdefault('iDNumber', '')
                response_person.setdefault('idcardNum', '')
                response_person.setdefault('phone', '')
                response_person.setdefault('tag', '00')
                # 确保权限字段存在且有正确的默认值
                response_person.setdefault('facePermission', 2)
                response_person.setdefault('idCardPermission', 2)
                response_person.setdefault('faceAndCardPermission', 1)
                response_person.setdefault('iDPermission', response_person.get('idCardPermission', 2))
                person = response_person
            result = {
                'total': 1 if person else 0,
                'data': [person] if person else []
            }
        
        return base_response(data=result, msg='查询成功')

# 创建人员服务实例
person_service = PersonService()