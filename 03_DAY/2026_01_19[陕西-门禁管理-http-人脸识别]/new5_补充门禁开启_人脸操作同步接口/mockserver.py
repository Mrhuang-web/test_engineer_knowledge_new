# 人脸门禁系统mockserver主程序
# 使用Python原生库实现HTTP服务器

import http.server
import socketserver
import json
import urllib.parse
import logging
from logging.handlers import RotatingFileHandler
import os
import time
import sys
import subprocess
import threading
from configs.url_config import url_mapping, server_config, hot_restart_config
from configs.param_config import param_validation
from configs.log_config import log_config

# 初始化日志配置
def init_logger():
    """初始化日志系统"""
    # 清除已有的日志处理器
    logger = logging.getLogger()
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    if not log_config['log_enabled']:
        # 如果日志开关关闭，设置日志级别为CRITICAL，只记录严重错误
        logging.basicConfig(level=logging.CRITICAL)
        return
    
    # 创建日志目录
    log_dir = log_config['log_dir']
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # 配置日志格式
    file_formatter = logging.Formatter(log_config['log_format'])
    console_formatter = logging.Formatter(log_config['console_log_format'])
    
    # 创建文件日志处理器
    log_file = os.path.join(log_dir, log_config['log_filename'])
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=log_config['max_bytes'],
        backupCount=log_config['backup_count'],
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(getattr(logging, log_config['file_log_level']))
    
    # 配置根日志记录器，使用最低级别DEBUG，让各个处理器自己决定要记录的级别
    logger.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)
    
    # 添加控制台日志处理器
    if log_config['console_log_enabled']:
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(getattr(logging, log_config['console_log_level']))
        logger.addHandler(console_handler)

# 初始化日志
init_logger()
logger = logging.getLogger(__name__)

# 热启动相关导入和设置
from business_logic import device, person, face, record

class HotRestartManager:
    """热启动管理器，检测文件变化并自动重启服务器"""
    def __init__(self):
        self.config = hot_restart_config
        self.is_running = False
        self.watch_thread = None
        self.file_mtimes = self._get_initial_file_mtimes()
    
    def _get_initial_file_mtimes(self):
        """获取初始文件修改时间"""
        file_mtimes = {}
        for dir_name in self.config['monitored_dirs']:
            if os.path.exists(dir_name):
                for root, _, files in os.walk(dir_name):
                    for file in files:
                        if any(file.endswith(ext) for ext in self.config['monitored_extensions']):
                            file_path = os.path.join(root, file)
                            file_mtimes[file_path] = os.path.getmtime(file_path)
        return file_mtimes
    
    def _check_file_changes(self):
        """检查文件是否有变化"""
        new_file_mtimes = self._get_initial_file_mtimes()
        
        # 检查是否有文件被修改
        for file_path, mtime in new_file_mtimes.items():
            if file_path in self.file_mtimes:
                if mtime != self.file_mtimes[file_path]:
                    logger.info(f"文件已修改: {file_path}")
                    return True
        
        # 检查是否有新文件被添加
        for file_path in new_file_mtimes:
            if file_path not in self.file_mtimes:
                logger.info(f"新文件添加: {file_path}")
                return True
        
        # 检查是否有文件被删除
        for file_path in self.file_mtimes:
            if file_path not in new_file_mtimes:
                logger.info(f"文件已删除: {file_path}")
                return True
        
        return False
    
    def _watch_files(self):
        """监控文件变化"""
        logger.info(f"启动热启动监控，检测间隔: {self.config['check_interval']}秒")
        while self.is_running:
            time.sleep(self.config['check_interval'])
            if self._check_file_changes():
                # 延迟一段时间，确保文件完全写入
                time.sleep(self.config['restart_delay'])
                logger.info("检测到文件变化，重启服务器...")
                self._restart_server()
                break
    
    def _restart_server(self):
        """重启服务器"""
        # 重启当前脚本
        os.execv(sys.executable, [sys.executable] + sys.argv)
    
    def start(self):
        """启动热启动监控"""
        if self.config['enabled']:
            self.is_running = True
            self.watch_thread = threading.Thread(target=self._watch_files, daemon=True)
            self.watch_thread.start()
            logger.info("热启动功能已启用")
        else:
            logger.info("热启动功能已禁用")
    
    def stop(self):
        """停止热启动监控"""
        self.is_running = False
        if self.watch_thread:
            self.watch_thread.join()

# 创建热启动管理器实例
hot_restart_manager = HotRestartManager()

class MockServerHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.services = {
            'device': device.device_service,
            'person': person.person_service,
            'face': face.face_service,
            'record': record.record_service
        }
        super().__init__(*args, **kwargs)
    
    def _parse_params(self, method):
        """解析请求参数，所有请求都从body中获取参数"""
        params = {}
        
        # 无论GET还是POST，都从请求体中获取参数
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length > 0:
            body = self.rfile.read(content_length)
            
            # 检查Content-Type头
            content_type = self.headers.get('Content-Type', '')
            
            # 如果是JSON格式，直接解析为JSON
            if 'application/json' in content_type:
                try:
                    params = json.loads(body.decode('utf-8'))
                except json.JSONDecodeError:
                    pass
            else:
                # 否则尝试解析为表单数据
                try:
                    params = dict(urllib.parse.parse_qsl(body.decode('utf-8')))
                    # 处理JSON格式的参数
                    for key, value in params.items():
                        if value.startswith('{') or value.startswith('['):
                            try:
                                params[key] = json.loads(value)
                            except json.JSONDecodeError:
                                pass
                except Exception as e:
                    # 如果解析表单数据失败，尝试解析为纯JSON
                    try:
                        params = json.loads(body.decode('utf-8'))
                    except json.JSONDecodeError:
                        pass
        
        # 对于GET请求，仍然解析URL查询字符串作为备选，确保向后兼容
        if method == 'GET':
            if '?' in self.path:
                path, query_string = self.path.split('?', 1)
                self.path = path  # 更新path，去掉查询字符串
                url_params = dict(urllib.parse.parse_qsl(query_string))
                # 只有当body中没有参数时，才使用URL查询字符串的参数
                if not params:
                    params = url_params
        
        return params
    
    def _validate_params(self, url, method, params):
        """验证请求参数"""
        # 检查该URL是否需要参数验证
        if url not in param_validation:
            return True, None
        
        validation = param_validation[url]
        
        # 验证请求方法
        if validation['method'] != method:
            return False, {'code': 'LAN_EXP-1006', 'msg': f'The {method} method is not supported.'}
        
        # 验证必填参数
        for required_param in validation['required']:
            if required_param not in params:
                # 根据不同的API返回相应的参数异常错误码
                if url == '/device/setLanguage' and required_param == 'languageType':
                    return False, {'code': 'LAN_EXP-2188', 'msg': f'{required_param}参数异常'}
                elif url == '/device/setTimeZone' and required_param == 'timeZone':
                    return False, {'code': 'LAN_EXP-2201', 'msg': f'timezone参数异常'}
                else:
                    # 其他参数返回通用的参数异常错误码
                    return False, {'code': 'LAN_EXP-1002', 'msg': f'{required_param}参数异常'}
        
        # 验证参数类型
        for param_name, expected_type in validation['type_map'].items():
            if param_name in params:
                actual_value = params[param_name]
                # 特殊处理需要严格校验的参数：base64Enable和type
                if param_name == 'base64Enable' or (param_name == 'type' and url == '/device/openDoorControl'):
                    # 严格检查参数类型：必须为int类型
                    if not isinstance(actual_value, int):
                        return False, {'code': 'LAN_EXP-1002', 'msg': f'{param_name}参数异常'}
                    # 对于type参数，还需要校验值必须为1
                    if param_name == 'type' and actual_value != 1:
                        return False, {'code': 'LAN_EXP-1002', 'msg': f'{param_name}参数异常'}
                # 特殊处理JSON类型的参数
                elif expected_type == dict and not isinstance(actual_value, dict):
                    return False, {'code': 'LAN_EXP-1002', 'msg': f'{param_name}参数异常'}
                # 对于其他类型，尝试转换
                elif expected_type != dict:
                    # 特殊处理整数类型：支持int和float类型的整数
                    if expected_type == int:
                        if isinstance(actual_value, (int, float)) and actual_value == int(actual_value):
                            # 如果是float类型的整数，直接转换为int
                            params[param_name] = int(actual_value)
                        elif not isinstance(actual_value, int):
                            try:
                                # 尝试转换其他类型为int
                                params[param_name] = int(actual_value)
                            except (ValueError, TypeError):
                                # 根据不同的API返回相应的参数异常错误码
                                if url == '/device/setLanguage' and param_name == 'languageType':
                                    return False, {'code': 'LAN_EXP-2188', 'msg': f'{param_name}参数异常'}
                                elif url == '/device/setTimeZone' and param_name == 'timeZone':
                                    return False, {'code': 'LAN_EXP-2201', 'msg': f'timezone参数异常'}
                                else:
                                    # 其他参数返回通用的参数异常错误码
                                    return False, {'code': 'LAN_EXP-1002', 'msg': f'{param_name}参数异常'}
                    # 特殊处理布尔类型
                    elif expected_type == bool:
                        if not isinstance(actual_value, bool):
                            try:
                                # 处理布尔值
                                if isinstance(actual_value, str):
                                    actual_value = actual_value.lower()
                                    if actual_value in ['true', '1']:
                                        params[param_name] = True
                                    elif actual_value in ['false', '0']:
                                        params[param_name] = False
                                    else:
                                        return False, {'code': 'LAN_EXP-1002', 'msg': f'{param_name}参数异常'}
                                else:
                                    params[param_name] = bool(actual_value)
                            except (ValueError, TypeError):
                                return False, {'code': 'LAN_EXP-1002', 'msg': f'{param_name}参数异常'}
                    # 处理字符串类型
                    elif expected_type == str and not isinstance(actual_value, str):
                        try:
                            params[param_name] = str(actual_value)
                        except (ValueError, TypeError):
                            return False, {'code': 'LAN_EXP-1002', 'msg': f'{param_name}参数异常'}
        
        return True, None
    
    def _get_response(self, response_data):
        """生成HTTP响应"""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode('utf-8'))
    
    def _handle_request(self):
        """处理请求"""
        start_time = time.time()
        method = self.command
        
        # 获取请求URL路径（包含查询字符串）
        full_path = self.path
        path = full_path.split('?')[0].rstrip('/')
        
        # 记录请求开始
        logger.info(f"Received request: {method} {full_path} from {self.client_address[0]}")
        
        try:
            # 解析请求参数
            params = self._parse_params(method)
            logger.info(f"Parsed params for {method} {path}: {params}")
            
            # 检查URL是否在映射中
            if path not in url_mapping:
                response = {
                    'code': 'LAN_EXP-1006',
                    'msg': f'The {method} method is not supported.',
                    'result': 0,
                    'success': False
                }
                logger.warning(f"URL not found: {path} - Response: {response}")
                self._get_response(response)
                return
            
            # 验证请求方法
            if url_mapping[path]['method'] != method:
                response = {
                    'code': 'LAN_EXP-1006',
                    'msg': f'The {method} method is not supported.',
                    'result': 0,
                    'success': False
                }
                logger.warning(f"Method not allowed: {method} for {path} - Response: {response}")
                self._get_response(response)
                return
            
            # 验证参数
            is_valid, error_info = self._validate_params(path, method, params)
            if not is_valid:
                # 生成错误响应，不包含data字段
                response = {
                    'code': error_info['code'],
                    'msg': error_info['msg'],
                    'result': 0,
                    'success': False
                }
                logger.warning(f"Invalid params for {path}: {params} - Response: {response}")
                self._get_response(response)
                return
            
            # 获取处理函数
            handler_info = url_mapping[path]['handler']
            service_name, method_name = handler_info.split('.')
            
            # 调用处理函数
            if service_name in self.services:
                service = self.services[service_name]
                if hasattr(service, method_name):
                    handler = getattr(service, method_name)
                    response = handler(params)
                    logger.info(f"Request {method} {path} processed successfully - Response: {response}")
                    self._get_response(response)
                    return
            
            # 如果没有找到处理函数，返回错误
            response = {
                'code': 'LAN_EXP-1000',
                'msg': 'Internal Server Error',
                'result': 0,
                'success': False
            }
            logger.error(f"Handler not found for {path}: {handler_info} - Response: {response}")
            self._get_response(response)
        except Exception as e:
            # 记录异常
            logger.error(f"Exception handling request {method} {full_path}: {str(e)}", exc_info=True)
            # 返回错误响应
            response = {
                'code': 'LAN_EXP-1000',
                'msg': 'Internal Server Error',
                'result': 0,
                'success': False
            }
            self._get_response(response)
        finally:
            # 记录请求处理时间
            end_time = time.time()
            logger.info(f"Request {method} {full_path} processed in {end_time - start_time:.4f} seconds")
    
    def do_GET(self):
        """处理GET请求"""
        self._handle_request()
    
    def do_POST(self):
        """处理POST请求"""
        self._handle_request()

def run_server():
    """启动服务器"""
    host = server_config['host']
    port = server_config['port']
    
    # 启动热启动监控
    hot_restart_manager.start()
    
    with socketserver.TCPServer((host, port), MockServerHandler) as httpd:
        logger.info(f"MockServer running on http://{host}:{port}")
        logger.info(f"Press Ctrl+C to stop the server")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            logger.info("\nServer stopped by user")
            httpd.server_close()

if __name__ == '__main__':
    run_server()