## 识别记录业务逻辑

import time
import re
from rules.response import base_response, ERROR_CODES
from models import record_data, person_data

class RecordService:
    """识别记录业务逻辑类"""
    
    @staticmethod
    def find_records(person_id='-1', model=-1, order='desc', index=0, length=1000, start_time=0, end_time=0):
        """识别记录查询"""
        import re
        import time
        
        # 1. 参数验证
        # personId 验证：允许-1、STRANGERBABY、IDCARD或字母数字组合，长度限制255
        if not re.match(r'^(-1|STRANGERBABY|IDCARD|[a-zA-Z0-9]{1,255})$', person_id):
            return base_response(0, False, '人员 ID(personId)只允许数字-1，0~9和英文字母，且最大长度为 255', 'LAN_EXP-3017')
        
        # length 验证：(0,1000]的正整数
        if not isinstance(length, int) or length <= 0 or length > 1000:
            return base_response(0, False, '每页显示数量length要求为(0,1000]的正整数', 'LAN_EXP-3018')
        
        # index 验证：从0开始计数的整数
        if not isinstance(index, int) or index < 0:
            return base_response(0, False, '页码index为从0开始计数的整数，必须小于总页码', 'LAN_EXP-3019')
        
        # model 验证：必须是整数
        if not isinstance(model, int):
            try:
                model = int(model)
            except:
                return base_response(0, False, 'model参数不合法', 'LAN_EXP-5007')
        
        # startTime 验证和转换：允许0或字符串格式时间
        # 先处理字符串"0"的情况
        if isinstance(start_time, str):
            if start_time == '0':
                start_time = 0
            else:
                try:
                    # 解析字符串格式时间为时间戳（毫秒）
                    struct_time = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                    start_time = int(time.mktime(struct_time) * 1000)
                except ValueError:
                    return base_response(0, False, 'startTime时间格式错误', 'LAN_EXP-3033')
        elif start_time != 0:
            # 非字符串且非0，确保是整数
            try:
                start_time = int(start_time)
            except:
                return base_response(0, False, 'startTime时间格式错误', 'LAN_EXP-3033')
        
        # endTime 验证和转换：允许0或字符串格式时间
        # 先处理字符串"0"的情况
        if isinstance(end_time, str):
            if end_time == '0':
                end_time = 0
            else:
                try:
                    # 解析字符串格式时间为时间戳（毫秒）
                    struct_time = time.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                    end_time = int(time.mktime(struct_time) * 1000)
                except ValueError:
                    return base_response(0, False, 'endTime时间格式错误', 'LAN_EXP-3034')
        elif end_time != 0:
            # 非字符串且非0，确保是整数
            try:
                end_time = int(end_time)
            except:
                return base_response(0, False, 'endTime时间格式错误', 'LAN_EXP-3034')
        
        # 验证endTime是否大于startTime
        try:
            if start_time != 0 and end_time != 0:
                # 确保start_time和end_time是整数
                if isinstance(start_time, str):
                    start_time = int(start_time)
                if isinstance(end_time, str):
                    end_time = int(end_time)
                if end_time <= start_time:
                    return base_response(0, False, 'endTime应大于startTime', 'LAN_EXP-3035')
        except ValueError:
            # 如果转换失败，会被前面的时间格式验证捕获
            pass
        
        # 2. 检查人员是否存在（如果不是查询所有人员、陌生人或人证比对）
        if person_id not in ['-1', 'STRANGERBABY', 'IDCARD']:
            if not person_data.get_person(person_id):
                return base_response(0, False, '人员ID不存在，请先调用人员注册接口', 'LAN_EXP-3009')
        
        # 3. 查询记录
        records = record_data.get_records_by_page(person_id, model, order, index, length, start_time, end_time)
        
        # 4. 检查记录数量
        if not records:
            return base_response(0, True, '该查询条件对应的识别记录数量为0', 'LAN_SUS-0')
        
        return base_response(data=records, msg='查询成功')
    
    @staticmethod
    def delete_records(person_id='-1', model=-1, start_time=0, end_time=0):
        """识别记录删除"""
        import re
        import time
        
        # 1. 参数验证
        # personId 验证：允许-1、STRANGERBABY、IDCARD或字母数字组合，长度限制255
        if not re.match(r'^(-1|STRANGERBABY|IDCARD|[a-zA-Z0-9]{1,255})$', person_id):
            return base_response(0, False, '人员 ID(personId)只允许数字-1，0~9和英文字母，且最大长度为 255', 'LAN_EXP-3017')
        
        # 检查personId是否为空
        if not person_id:
            return base_response(0, False, 'personId 参数不能为空', 'LAN_EXP-3016')
        
        # model 验证：必须是整数，且范围在-1,0-5
        if not isinstance(model, int):
            try:
                model = int(model)
            except:
                return base_response(0, False, 'model参数不合法', 'LAN_EXP-5007')
        
        # 验证model值是否在合法范围内
        if model not in [-1, 0, 1, 2, 3, 4, 5]:
            return base_response(0, False, 'model参数不合法', 'LAN_EXP-5007')
        
        # startTime 验证和转换：允许0、日期时间字符串或时间戳字符串
        if isinstance(start_time, str):
            if start_time == '0':
                start_time = 0
            else:
                try:
                    # 尝试直接转换为整数时间戳
                    start_time = int(start_time)
                except ValueError:
                    # 如果转换失败，尝试解析为日期时间字符串
                    try:
                        struct_time = time.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                        # 捕获mktime可能抛出的OverflowError
                        try:
                            start_time = int(time.mktime(struct_time) * 1000)
                        except OverflowError:
                            # 如果日期超出范围，使用系统最大时间戳
                            import sys
                            start_time = sys.maxsize
                    except ValueError:
                        return base_response(0, False, 'startTime时间格式错误', 'LAN_EXP-3033')
        elif start_time != 0:
            # 非字符串且非0，确保是整数
            try:
                start_time = int(start_time)
            except:
                return base_response(0, False, 'startTime时间格式错误', 'LAN_EXP-3033')
        
        # endTime 验证和转换：允许0、日期时间字符串或时间戳字符串
        if isinstance(end_time, str):
            if end_time == '0':
                end_time = 0
            else:
                try:
                    # 尝试直接转换为整数时间戳
                    end_time = int(end_time)
                except ValueError:
                    # 如果转换失败，尝试解析为日期时间字符串
                    try:
                        struct_time = time.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                        # 捕获mktime可能抛出的OverflowError
                        try:
                            end_time = int(time.mktime(struct_time) * 1000)
                        except OverflowError:
                            # 如果日期超出范围，使用系统最大时间戳
                            import sys
                            end_time = sys.maxsize
                    except ValueError:
                        return base_response(0, False, 'endTime时间格式错误', 'LAN_EXP-3034')
        elif end_time != 0:
            # 非字符串且非0，确保是整数
            try:
                end_time = int(end_time)
            except:
                return base_response(0, False, 'endTime时间格式错误', 'LAN_EXP-3034')
        
        # 验证endTime是否大于startTime
        if start_time != 0 and end_time != 0 and end_time <= start_time:
            return base_response(0, False, 'endTime应大于startTime', 'LAN_EXP-3035')
        
        # 2. 检查人员是否存在（如果不是删除所有人员、陌生人或人证比对）
        if person_id not in ['-1', 'STRANGERBABY', 'IDCARD']:
            if not person_data.get_person(person_id):
                return base_response(0, False, '人员ID不存在，请先调用人员注册接口', 'LAN_EXP-3009')
        
        # 3. 获取原始记录数量，用于计算删除数量
        original_count = len(record_data.get_records(person_id, model, 'desc', start_time, end_time))
        
        # 4. 删除记录
        if record_data.delete_records(person_id, model, start_time, end_time):
            deleted_count = original_count - len(record_data.get_records(person_id, model, 'desc', start_time, end_time))
            return base_response(data=f"删除识别记录数量：{deleted_count}", msg='删除成功')
        
        # 数据库异常
        return base_response(0, False, '数据库异常，识别记录删除失败', 'LAN_EXP-5013')
    
    @staticmethod
    def simulate_identify(person_id=None):
        """模拟识别记录生成"""
        # 生成随机ID
        import random
        import string
        import json
        record_id = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        
        # 设置默认值
        if not person_id:
            # 模拟陌生人识别
            person_id = 'STRANGERBABY'
            person_name = '陌生人'
        else:
            # 查找人员名称
            person = person_data.get_person(person_id)
            person_name = person['name'] if person else '未知人员'
        
        # 生成当前时间戳（毫秒）
        timestamp = int(time.time() * 1000)
        
        # 生成身份证信息data字段，包含完整的默认数据
        id_card_data = {
            "address": "浙江省 XX 市 XX 镇 XX 村 XX 区 XX 号",
            "birthday": "1995-11-22",
            "compareResult": False,
            "createTime": timestamp,
            "id": 0,
            "idNum": "33108119000000000",
            "issuingOrgan": "XXX公安局",
            "name": person_name,
            "nation": "汉",
            "photoPath": f'ftp://192.168.18.17:8010/IdentifyRecords/{time.strftime("%Y-%m-%d")}/{record_id}_idcard.jpg',
            "sex": "男",
            "usefulLife": "2012.02.12-2032.02.12"
        }
        
        # 生成识别记录，包含所有必要字段
        record = {
            'id': record_id,  # 记录ID
            'personId': person_id,  # 人员ID
            'name': person_name,  # 姓名
            'time': timestamp,  # 识别时间戳（毫秒）
            'path': f'ftp://192.168.18.17:8010/IdentifyRecords/{time.strftime("%Y-%m-%d")}/{record_id}_rgb.jpg',  # 现场照路径
            'aliveType': 1,  # 是否是活体：1=活体，2=非活体
            'idcardNum': '',  # 卡号
            'identifyType': 1,  # 识别记录类型：1=识别成功，2=识别失败
            'isImgDeleted': 0,  # 现场照是否删除：0=未删除，1=删除
            'isPass': True,  # 是否有权限
            'model': 0,  # 识别模式：0=刷脸，1=人卡合一，2=人证比对，3=刷卡
            'passTimeType': 3,  # 是否通过passtime权限：1=通过，2=未通过，3=未检测
            'permissionTimeType': 3,  # 是否通过permissionTimeType权限：1=通过，2=未通过，3=未检测
            'recModeType': 1,  # 识别模式判断：1=模式正确，2=模式不正确，3=未进行判断
            'recType': 1,  # 识别方式：1=本地识别，2=云端识别
            'state': 1,  # 是否回调成功：0=回调失败，1=回调成功
            'type': 0,  # 识别结果：0=成功/时间段内，1=权限不足，2=识别失败
            'data': json.dumps(id_card_data)  # 身份证信息JSON字符串
        }
        
        # 添加记录
        record_data.add_record(record)
        
        # 触发识别回调（如果已设置）
        from models import device_data
        callback_url = device_data.get_identify_callback_url()
        if callback_url:
            RecordService._trigger_identify_callback(record, callback_url)
        
        return base_response(data=record, msg='模拟识别成功')
    
    @staticmethod
    def _trigger_identify_callback(record, callback_url):
        """触发识别回调"""
        import threading
        import urllib.request
        import urllib.parse
        import json
        
        # 异步发送回调请求
        def send_callback():
            try:
                # 构建回调数据
                callback_data = {
                    'deviceKey': '84E0F420893301FA',  # 模拟设备Key
                    'path': record['path'],
                    'personId': record['personId'],
                    'time': str(record['time']),
                    'type': record['type']
                }
                
                # 发送POST请求
                data = json.dumps(callback_data).encode('utf-8')
                req = urllib.request.Request(
                    callback_url,
                    data=data,
                    headers={'Content-Type': 'application/json'}
                )
                with urllib.request.urlopen(req, timeout=5) as response:
                    # 检查响应
                    if response.status == 200:
                        response_body = response.read().decode('utf-8')
                        response_data = json.loads(response_body)
                        if response_data.get('result') == 1 and response_data.get('success') is True:
                            # 回调成功，更新记录状态
                            record_data.update_record_state(record['id'], 1)
                            return
                
                # 回调失败，更新记录状态
                record_data.update_record_state(record['id'], 2)
                
            except Exception as e:
                # 回调失败，更新记录状态
                record_data.update_record_state(record['id'], 2)
        
        # 启动线程发送回调
        thread = threading.Thread(target=send_callback)
        thread.daemon = True
        thread.start()

# 创建识别记录服务实例
record_service = RecordService()