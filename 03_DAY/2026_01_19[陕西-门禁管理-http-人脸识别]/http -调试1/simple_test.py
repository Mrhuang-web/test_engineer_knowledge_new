import socket
import json

# 测试服务器地址和端口
HOST = '127.0.0.1'
PORT = 8099

def send_http_request(method, path, headers=None, body=None):
    """发送HTTP请求"""
    # 创建TCP套接字
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置超时
    s.settimeout(5)
    
    try:
        # 连接服务器
        s.connect((HOST, PORT))
        
        # 构建请求行
        request_line = f"{method} {path} HTTP/1.1\r\n"
        
        # 构建请求头
        request_headers = {
            'Host': f"{HOST}:{PORT}",
            'Connection': 'close',
        }
        
        # 添加自定义请求头
        if headers:
            request_headers.update(headers)
        
        # 构建请求体
        request_body = ''
        if body:
            request_body = json.dumps(body)
            request_headers['Content-Type'] = 'application/json'
            request_headers['Content-Length'] = str(len(request_body))
        
        # 拼接请求头字符串
        headers_str = '\r\n'.join([f"{k}: {v}" for k, v in request_headers.items()])
        
        # 拼接完整请求
        request = f"{request_line}{headers_str}\r\n\r\n{request_body}"
        
        # 发送请求
        s.sendall(request.encode('utf-8'))
        
        # 接收响应
        response = b''
        try:
            while True:
                data = s.recv(1024)
                if not data:
                    break
                response += data
        except socket.timeout:
            # 超时，可能响应已经接收完成
            pass
        
        # 解析响应
        if response:
            response_str = response.decode('utf-8')
            print(f"响应:\n{response_str}")
            return response_str
        else:
            print("没有收到响应")
            return None
    except socket.timeout:
        print("连接超时")
        return None
    except Exception as e:
        print(f"错误: {e}")
        return None
    finally:
        # 关闭套接字
        s.close()

# 测试设置密码功能
print("=== 测试设置密码功能 ===")
send_http_request(
    method='POST',
    path='/setPassWord',
    body={
        "oldPass": "12345678",
        "newPass": "12345678"
    }
)

# 测试远程开门功能
print("\n=== 测试远程开门功能 ===")
send_http_request(
    method='POST',
    path='/device/openDoorControl',
    body={
        "type": 1,
        "pass": "12345678"
    }
)