# 简化版HTTP服务器，用于测试基本功能

import http.server
import socketserver
from socketserver import ThreadingTCPServer
import json
import urllib.parse
import sys
import traceback

# 基础响应格式
class BaseHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    """HTTP请求处理类"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
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
            except Exception as e:
                print(f"Error parsing request body: {e}")
                return {}
        return {}
    
    def _parse_query_params(self):
        """解析查询参数"""
        if '?' in self.path:
            path, query = self.path.split('?', 1)
            return dict(urllib.parse.parse_qsl(query))
        return {}
    
    def do_GET(self):
        """处理GET请求"""
        try:
            # 简单的GET请求处理
            path = self.path.split('?')[0]
            if path == '/device/information':
                # 返回设备信息
                response = {
                    'result': 1,
                    'success': True,
                    'msg': '操作成功',
                    'code': 'LAN_SUS-0',
                    'data': {
                        'deviceName': 'Test Device',
                        'deviceType': 'Face Access Control',
                        'firmwareVersion': '1.0.0'
                    }
                }
                self._send_response(response)
            else:
                # 404 Not Found
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        except Exception as e:
            # 内部错误
            print(f"Error in GET request: {e}")
            traceback.print_exc()
            response = {
                'result': 0,
                'success': False,
                'msg': '内部服务器错误',
                'code': 'LAN_EXP-5001',
                'data': ''
            }
            self._send_response(response, 500)
    
    def do_POST(self):
        """处理POST请求"""
        try:
            # 简单的POST请求处理
            path = self.path.split('?')[0]
            
            if path == '/setPassWord':
                # 设置密码请求
                params = self._parse_request_body()
                
                # 检查参数
                old_pass = params.get('oldPass')
                new_pass = params.get('newPass')
                
                if not old_pass or not new_pass:
                    response = {
                        'result': 0,
                        'success': False,
                        'msg': '密码参数异常',
                        'code': 'LAN_EXP-1002',
                        'data': ''
                    }
                    self._send_response(response)
                else:
                    # 模拟设置密码
                    response = {
                        'result': 1,
                        'success': True,
                        'msg': '密码设置成功',
                        'code': 'LAN_SUS-0',
                        'data': ''
                    }
                    self._send_response(response)
            elif path == '/device/openDoorControl':
                # 远程开门请求
                params = self._parse_request_body()
                
                # 检查参数
                type_ = params.get('type', 1)
                pass_ = params.get('pass')
                
                if not pass_:
                    response = {
                        'result': 0,
                        'success': False,
                        'msg': 'pass 参数异常',
                        'code': 'LAN_EXP-1002',
                        'data': ''
                    }
                    self._send_response(response)
                else:
                    # 模拟远程开门
                    response = {
                        'result': 1,
                        'success': True,
                        'msg': '远程开门成功',
                        'code': 'LAN_SUS-0',
                        'data': ''
                    }
                    self._send_response(response)
            else:
                # 404 Not Found
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'404 Not Found')
        except Exception as e:
            # 内部错误
            print(f"Error in POST request: {e}")
            traceback.print_exc()
            response = {
                'result': 0,
                'success': False,
                'msg': '内部服务器错误',
                'code': 'LAN_EXP-5001',
                'data': ''
            }
            self._send_response(response, 500)
    
    def do_OPTIONS(self):
        """处理OPTIONS请求"""
        self._send_response('', 200)

def run_server(port=8090):
    """启动服务器"""
    print(f"Starting server on port {port}...")
    with ThreadingTCPServer(('', port), BaseHTTPRequestHandler) as httpd:
        print(f"Server running on port {port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user")
        except Exception as e:
            print(f"Server error: {e}")
            traceback.print_exc()

if __name__ == "__main__":
    port = 8090
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    run_server(port)