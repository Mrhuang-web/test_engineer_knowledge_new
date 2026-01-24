# 基于http.server的HTTP服务器，替代Flask框架

import http.server
import socketserver
import json
import urllib.parse
import re
import sys
import traceback

# 导入服务层和模型
from rules.response import base_response, ERROR_CODES
from models import device_data

# 延迟导入服务层，避免初始化时出现问题
device_service = None
person_service = None
face_service = None
record_service = None

try:
    from services import device_service as ds
    from services import person_service as ps
    from services import face_service as fs
    from services import record_service as rs
    
    device_service = ds
    person_service = ps
    face_service = fs
    record_service = rs
except Exception as e:
    print(f"Error importing services: {e}")
    traceback.print_exc()

class HTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP请求处理类"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def _parse_request_body(self):
        """解析请求体"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
        except ValueError:
            # 无效的Content-Length值，返回空字典
            return {}
        
        if content_length > 0:
            try:
                body = self.rfile.read(content_length)
                content_type = self.headers.get('Content-Type', '')
                if 'application/x-www-form-urlencoded' in content_type:
                    return dict(urllib.parse.parse_qsl(body.decode('utf-8')))
                elif 'application/json' in content_type:
                    return json.loads(body.decode('utf-8'))
            except (UnicodeDecodeError, json.JSONDecodeError):
                # 无效的请求体，返回空字典
                return {}
        return {}
    
    def _parse_query_params(self):
        """解析查询参数"""
        if '?' in self.path:
            path, query = self.path.split('?', 1)
            return dict(urllib.parse.parse_qsl(query))
        return {}
    
    def _send_response(self, data, status_code=200, content_type='application/json'):
        """发送响应"""
        try:
            self.send_response(status_code)
            self.send_header('Content-Type', content_type)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            
            if isinstance(data, dict):
                data = json.dumps(data, ensure_ascii=False)
            self.wfile.write(data.encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError, ConnectionAbortedError):
            # 客户端断开连接相关错误，忽略并记录日志
            print(f"Client disconnected when sending response to {self.client_address}")
        except Exception as e:
            # 其他写入错误，记录但不崩溃
            print(f"Error sending response to {self.client_address}: {e}")
            traceback.print_exc()
    
    def _handle_options(self):
        """处理OPTIONS请求"""
        self._send_response('', 200)
    
    def _validate_param_type(self, params, param_name, expected_type, required=True, default=None):
        """验证参数类型
        
        Args:
            params: 参数字典
            param_name: 参数名
            expected_type: 期望的类型
            required: 是否必填
            default: 默认值
            
        Returns:
            tuple: (验证结果, 参数值, 错误信息)
        """
        if param_name not in params:
            if required:
                return False, None, f'{param_name} 参数缺失'
            else:
                return True, default, ''
        
        value = params[param_name]
        
        # 如果是字符串类型，处理各种异常情况
        if expected_type == str:
            if not isinstance(value, str):
                return False, None, f'{param_name} 参数类型错误，应为字符串'
            if '\n' in value or '\r' in value:
                return False, None, f'{param_name} 参数包含无效字符'
            if value.strip() == '' and required:
                return False, None, f'{param_name} 参数不能为空'
        # 如果是整数类型
        elif expected_type == int:
            try:
                int_value = int(value)
                return True, int_value, ''
            except (ValueError, TypeError):
                return False, None, f'{param_name} 参数类型错误，应为整数'
        # 如果是布尔类型
        elif expected_type == bool:
            if isinstance(value, bool):
                return True, value, ''
            elif isinstance(value, str):
                if value.lower() in ['true', 'false']:
                    return True, value.lower() == 'true', ''
            return False, None, f'{param_name} 参数类型错误，应为布尔值'
        # 其他类型直接检查
        elif not isinstance(value, expected_type):
            return False, None, f'{param_name} 参数类型错误'
        
        return True, value, ''
    
    def _require_password(self, handler_func):
        """密码验证装饰器"""
        def wrapper():
            try:
                # 获取所有参数 - 所有请求都从body获取参数
                all_params = self._parse_request_body()
                
                # 去掉查询参数，统一路径格式
                path = self.path.split('?')[0]
                
                # 设置密码接口特殊处理，不需要pass字段
                if path == '/setPassWord':
                    # 只检查设置密码需要的参数，不检查pass
                    return handler_func()
                
                # 其他接口需要密码验证
                # 检查设备是否有密码
                current_password = device_data.get_password()
                
                # 设备有密码，检查pass参数
                if current_password is not None:
                    # 检查pass参数是否存在
                    if 'pass' not in all_params:
                        response = base_response(0, False, 'pass 参数异常', ERROR_CODES['PASS_PARAM_ERROR'])
                        return self._send_response(response, 200)
                    
                    # 获取pass参数值
                    passwd = all_params['pass']
                    
                    # 检查pass参数值是否异常
                    if (passwd is None or 
                        not isinstance(passwd, str) or 
                        '\n' in passwd or 
                        '\r' in passwd or 
                        passwd.strip() == '' or
                        ' ' in passwd.strip()):
                        response = base_response(0, False, 'pass 参数异常', ERROR_CODES['PASS_PARAM_ERROR'])
                        return self._send_response(response, 200)
                    
                    # 检查密码是否正确
                    if passwd != current_password:
                        response = base_response(0, False, '密码错误，请检查密码正确性', ERROR_CODES['PASSWORD_ERROR'])
                        return self._send_response(response, 200)
                
                # 密码验证通过或设备无密码，调用处理函数
                return handler_func()
            except Exception as e:
                # 密码验证过程中发生错误
                print(f"Error in password validation: {e}")
                traceback.print_exc()
                response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
                return self._send_response(response, 500)
        return wrapper
    
    def do_OPTIONS(self):
        """处理OPTIONS请求"""
        self._handle_options()
    
    def do_GET(self):
        """处理GET请求"""
        try:
            # 路由映射
            routes = {
                '/device/information': self._device_information,
                '/getDoorSensor': self._get_door_sensor,
                '/device/status': self._device_status,
                '/newFindRecords': self._new_find_records
            }
            
            # 根据路径调用对应的处理函数
            path = self.path.split('?')[0]
            if path in routes:
                # 应用密码验证
                return self._require_password(routes[path])()
            else:
                # 404 Not Found
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        except Exception as e:
            # 内部错误
            print(f"Error in GET request: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            self._send_response(response, 500)
    
    def do_POST(self):
        """处理POST请求"""
        print(f"Received POST request for {self.path}")
        try:
            # 解析路径
            path = self.path.split('?')[0]
            print(f"Processing POST request for path: {path}")
            
            # 路由映射
            routes = {
                '/setPassWord': self._set_password,
                '/setTime': self._set_time,
                '/device/setLanguage': self._set_language,
                '/device/setTimeZone': self._set_timezone,
                '/restartDevice': self._restart_device,
                '/setIdentifyCallBack': self._set_identify_callback,
                '/setImgRegCallBack': self._set_img_reg_callback,
                '/device/openDoorControl': self._open_door,
                '/device/eventCallBack': self._set_event_callback,
                '/resetDevice': self._reset_device,
                '/device/setSignalInput': self._set_signal_input,
                '/meetAndWarnSet': self._set_meet_and_warn,
                '/cardInfoSet': self._set_card_info,
                '/person/create': self._create_person,
                '/person/delete': self._delete_person,
                '/person/update': self._update_person,
                '/person/find': self._find_person,
                '/person/findByPage': self._find_person_by_page,
                '/face/create': self._create_face,
                '/face/delete': self._delete_face,
                '/face/update': self._update_face,
                '/face/find': self._find_face,
                '/face/takeImg': self._take_img,
                '/face/deletePerson': self._delete_person_faces,
                '/newDeleteRecords': self._new_delete_records,
                '/simulateIdentify': self._simulate_identify
            }
            
            # 根据路径调用对应的处理函数
            if path in routes:
                print(f"Calling handler function for path: {path}")
                # 应用密码验证
                return self._require_password(routes[path])()
            else:
                # 404 Not Found
                print(f"Path {path} not found, returning 404")
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        except Exception as e:
            # 内部错误
            print(f"Error in POST request: {e}")
            traceback.print_exc()
            try:
                response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
                self._send_response(response, 500)
            except Exception as send_error:
                print(f"Error sending error response: {send_error}")
                traceback.print_exc()
    
    # 设备管理类接口
    def _set_password(self):
        """设置设备密码"""
        try:
            params = self._parse_request_body()
            
            # 验证参数类型
            valid, old_pass, msg = self._validate_param_type(params, 'oldPass', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PASS_PARAM_ERROR']))
            
            valid, new_pass, msg = self._validate_param_type(params, 'newPass', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PASS_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_password(old_pass, new_pass)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_password: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _device_information(self):
        """设备信息查询"""
        try:
            # 所有请求都从body获取参数，这里虽然不需要参数，但保持一致性
            self._parse_request_body()
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.get_device_info()
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _device_information: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _set_time(self):
        """设置设备时间"""
        try:
            params = self._parse_request_body()
            
            # 验证timestamp参数，应为整数
            valid, timestamp, msg = self._validate_param_type(params, 'timestamp', int, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['TIMESTAMP_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_time(timestamp)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_time: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _set_language(self):
        """语言切换"""
        try:
            params = self._parse_request_body()
            
            # 验证languageType参数，应为整数
            valid, language_type, msg = self._validate_param_type(params, 'languageType', int, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['LANGUAGE_TYPE_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_language(language_type)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_language: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _set_timezone(self):
        """设置时区"""
        try:
            params = self._parse_request_body()
            
            # 验证timeZone参数，应为整数
            valid, time_zone, msg = self._validate_param_type(params, 'timeZone', int, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['TIMEZONE_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_timezone(time_zone)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_timezone: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _restart_device(self):
        """设备重启"""
        try:
            # 所有请求都从body获取参数，这里虽然不需要参数，但保持一致性
            self._parse_request_body()
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.restart_device()
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _restart_device: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _set_identify_callback(self):
        """识别回调"""
        try:
            params = self._parse_request_body()
            callback_url = params.get('callbackUrl')
            base64_enable = params.get('base64Enable', 1)
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_identify_callback(callback_url, base64_enable)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_identify_callback: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _set_img_reg_callback(self):
        """注册照片回调"""
        try:
            params = self._parse_request_body()
            url = params.get('url')
            base64_enable = params.get('base64Enable', 1)
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_img_reg_callback(url, base64_enable)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_img_reg_callback: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _open_door(self):
        """远程控制输出"""
        try:
            params = self._parse_request_body()
            
            # 验证type参数，应为整数
            valid, type_, msg = self._validate_param_type(params, 'type', int, required=False, default=1)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['TYPE_ILLEGAL']))
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.open_door(type_)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _open_door: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _get_door_sensor(self):
        """获取门磁状态"""
        try:
            # 所有请求都从body获取参数，这里虽然不需要参数，但保持一致性
            self._parse_request_body()
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.get_door_status()
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _get_door_sensor: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _set_event_callback(self):
        """事件回调"""
        try:
            params = self._parse_request_body()
            url = params.get('url')
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_event_callback(url)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_event_callback: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _reset_device(self):
        """重置设备"""
        try:
            # 所有请求都从body获取参数，这里虽然不需要参数，但保持一致性
            self._parse_request_body()
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.reset_device()
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _reset_device: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _device_status(self):
        """获取设备状态"""
        try:
            # 所有请求都从body获取参数，这里虽然不需要参数，但保持一致性
            self._parse_request_body()
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.get_device_status()
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _device_status: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _set_signal_input(self):
        """信号输入设置"""
        try:
            params = self._parse_request_body()
            config = params.get('config')
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_signal_input(config)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_signal_input: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _set_meet_and_warn(self):
        """会议与关门告警设置"""
        try:
            params = self._parse_request_body()
            meet_enable = params.get('meetEnable')
            meet_free_time = params.get('meetFreeTime')
            door_warn_enable = params.get('doorWarnEnable')
            door_close_time = params.get('doorCloseTime')
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_meet_and_warn(meet_enable, meet_free_time, door_warn_enable, door_close_time)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_meet_and_warn: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _set_card_info(self):
        """卡片设置"""
        try:
            params = self._parse_request_body()
            read_data_enable = params.get('readDataEnable')
            read_sector = params.get('readSector')
            read_block = params.get('readBlock')
            read_shift = params.get('readShift')
            read_key_a = params.get('readKeyA')
            wg_out_type = params.get('wgOutType')
            
            # 检查服务层对象是否为空
            if device_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = device_service.set_card_info(read_data_enable, read_sector, read_block, read_shift, read_key_a, wg_out_type)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _set_card_info: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    # 人员管理类接口
    def _create_person(self):
        """人员注册"""
        try:
            params = self._parse_request_body()
            person_data = params.get('person')
            
            # 检查服务层对象是否为空
            if person_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = person_service.create_person(person_data)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _create_person: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _delete_person(self):
        """人员删除"""
        try:
            params = self._parse_request_body()
            
            # 验证id参数，应为字符串
            valid, id_, msg = self._validate_param_type(params, 'id', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if person_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = person_service.delete_person(id_)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _delete_person: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _update_person(self):
        """人员更新"""
        try:
            params = self._parse_request_body()
            person_data = params.get('person')
            
            # 检查服务层对象是否为空
            if person_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = person_service.update_person(person_data)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _update_person: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _find_person(self):
        """人员查询"""
        try:
            params = self._parse_request_body()
            
            # 验证id参数，应为字符串
            valid, id_, msg = self._validate_param_type(params, 'id', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if person_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = person_service.find_person(id_)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _find_person: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _find_person_by_page(self):
        """人员分页查询"""
        try:
            params = self._parse_request_body()
            
            # 验证参数类型
            valid, person_id, msg = self._validate_param_type(params, 'personId', str, required=False, default='-1')
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            valid, index, msg = self._validate_param_type(params, 'index', int, required=False, default=0)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['INDEX_ILLEGAL']))
            
            valid, length, msg = self._validate_param_type(params, 'length', int, required=False, default=1000)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['LENGTH_ILLEGAL']))
            
            # 检查服务层对象是否为空
            if person_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = person_service.find_person_by_page(person_id, index, length)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _find_person_by_page: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    # 照片管理类接口
    def _create_face(self):
        """照片注册"""
        try:
            params = self._parse_request_body()
            
            # 验证参数类型
            valid, person_id, msg = self._validate_param_type(params, 'personId', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            valid, face_id, msg = self._validate_param_type(params, 'faceId', str, required=False, default='')
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['FACE_ID_PARAM_ERROR']))
            
            valid, img_base64, msg = self._validate_param_type(params, 'imgBase64', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['IMG_BASE64_PARAM_ERROR']))
            
            # 验证 isEasyWay 参数
            valid, is_easy_way, msg = self._validate_param_type(params, 'isEasyWay', bool, required=False, default=False)
            if not valid:
                return self._send_response(base_response(0, False, 'isEasyWay 参数不合法', ERROR_CODES['IS_EASY_WAY_ILLEGAL']))
            
            # 检查服务层对象是否为空
            if face_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = face_service.create_face(person_id, face_id, img_base64, is_easy_way)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _create_face: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _delete_face(self):
        """照片删除"""
        try:
            params = self._parse_request_body()
            
            # 验证faceId参数，应为字符串
            valid, face_id, msg = self._validate_param_type(params, 'faceId', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['FACE_ID_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if face_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = face_service.delete_face(face_id)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _delete_face: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _update_face(self):
        """照片更新"""
        try:
            params = self._parse_request_body()
            
            # 验证参数类型
            valid, person_id, msg = self._validate_param_type(params, 'personId', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            valid, face_id, msg = self._validate_param_type(params, 'faceId', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['FACE_ID_PARAM_ERROR']))
            
            valid, img_base64, msg = self._validate_param_type(params, 'imgBase64', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['IMG_BASE64_PARAM_ERROR']))
            
            valid, is_easy_way, msg = self._validate_param_type(params, 'isEasyWay', bool, required=False, default=False)
            if not valid:
                return self._send_response(base_response(0, False, 'isEasyWay 参数不合法', ERROR_CODES['IS_EASY_WAY_ILLEGAL']))
            
            # 检查服务层对象是否为空
            if face_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = face_service.update_face(person_id, face_id, img_base64, is_easy_way)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _update_face: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _find_face(self):
        """照片查询"""
        try:
            params = self._parse_request_body()
            
            # 验证personId参数，应为字符串
            valid, person_id, msg = self._validate_param_type(params, 'personId', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if face_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = face_service.find_face(person_id)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _find_face: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _take_img(self):
        """拍照注册"""
        try:
            params = self._parse_request_body()
            
            # 验证personId参数，应为字符串
            valid, person_id, msg = self._validate_param_type(params, 'personId', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if face_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = face_service.take_img(person_id)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _take_img: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _delete_person_faces(self):
        """清空人员注册照片"""
        try:
            params = self._parse_request_body()
            
            # 验证personId参数，应为字符串
            valid, person_id, msg = self._validate_param_type(params, 'personId', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if face_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = face_service.delete_person_faces(person_id)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _delete_person_faces: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    # 识别记录接口
    def _new_find_records(self):
        """识别记录查询"""
        try:
            params = self._parse_request_body()
            
            # 验证参数类型
            valid, person_id, msg = self._validate_param_type(params, 'personId', str, required=False, default='-1')
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            valid, model, msg = self._validate_param_type(params, 'model', int, required=False, default=-1)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['MODEL_ILLEGAL']))
            
            valid, order, msg = self._validate_param_type(params, 'order', str, required=False, default='desc')
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['CONFIG_PARAM_ERROR']))
            
            valid, index, msg = self._validate_param_type(params, 'index', int, required=False, default=0)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['INDEX_ILLEGAL']))
            
            valid, length, msg = self._validate_param_type(params, 'length', int, required=False, default=1000)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['LENGTH_ILLEGAL']))
            
            # startTime和endTime可以是字符串或整数
            start_time = params.get('startTime', 0)
            end_time = params.get('endTime', 0)
            
            # 检查服务层对象是否为空
            if record_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = record_service.find_records(person_id, model, order, index, length, start_time, end_time)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _new_find_records: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _new_delete_records(self):
        """识别记录删除"""
        try:
            params = self._parse_request_body()
            
            # 验证参数类型
            valid, person_id, msg = self._validate_param_type(params, 'personId', str, required=False, default='-1')
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            valid, model, msg = self._validate_param_type(params, 'model', int, required=False, default=-1)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['MODEL_ILLEGAL']))
            
            # startTime和endTime可以是字符串或整数
            start_time = params.get('startTime', 0)
            end_time = params.get('endTime', 0)
            
            # 检查服务层对象是否为空
            if record_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = record_service.delete_records(person_id, model, start_time, end_time)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _new_delete_records: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)
    
    def _simulate_identify(self):
        """模拟识别记录生成"""
        try:
            params = self._parse_request_body()
            
            # 验证personId参数，应为字符串
            valid, person_id, msg = self._validate_param_type(params, 'personId', str, required=True)
            if not valid:
                return self._send_response(base_response(0, False, msg, ERROR_CODES['PERSON_ID_PARAM_ERROR']))
            
            # 检查服务层对象是否为空
            if record_service is None:
                return self._send_response(base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR']))
            
            response = record_service.simulate_identify(person_id)
            return self._send_response(response)
        except Exception as e:
            print(f"Error in _simulate_identify: {e}")
            traceback.print_exc()
            response = base_response(0, False, '内部服务器错误', ERROR_CODES['INTERNAL_ERROR'])
            return self._send_response(response)

def run_server(port=8091):
    """启动服务器"""
    with socketserver.TCPServer(('', port), HTTPRequestHandler) as httpd:
        print(f"Server running on port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        except Exception as e:
            print(f"Server error: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    port = 8101
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)
