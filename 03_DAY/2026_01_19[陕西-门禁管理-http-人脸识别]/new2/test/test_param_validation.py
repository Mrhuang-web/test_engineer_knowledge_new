import requests
import json

# 测试函数
def test_api(endpoint, method="POST", data=None, headers=None):
    """通用API测试函数"""
    if headers is None:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    url = f"http://localhost:8091{endpoint}"
    
    print(f"\n=== 测试 {method} {endpoint} ===")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False) if data else '无'}")
    
    try:
        if method == "GET":
            response = requests.get(url, params=data)
        else:
            response = requests.post(url, headers=headers, data=data)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 检查响应格式
        try:
            response_json = response.json()
            print(f"响应格式检查: 成功")
            print(f"响应包含字段: {list(response_json.keys())}")
            print(f"响应code: {response_json['code']}")
            print(f"响应msg: {response_json['msg']}")
        except json.JSONDecodeError:
            print(f"响应格式检查: 失败，不是有效的JSON格式")
    
    except Exception as e:
        print(f"测试失败: {str(e)}")

# 主测试流程
if __name__ == "__main__":
    print("开始测试参数验证")
    
    # 测试数据：设置了密码的情况
    base_data = {"pass": "123456"}
    
    # 1. 测试识别回调 - base64Enable为字符串类型（应该失败）
    test_api("/setIdentifyCallBack", data={**base_data, "callbackUrl": "http://example.com/callback", "base64Enable": "0"})
    
    # 2. 测试识别回调 - base64Enable为int类型（应该成功）
    test_api("/setIdentifyCallBack", data={**base_data, "callbackUrl": "http://example.com/callback", "base64Enable": 0})
    
    # 3. 测试注册照片回调 - base64Enable为字符串类型（应该失败）
    test_api("/setImgRegCallBack", data={**base_data, "url": "http://example.com/callback", "base64Enable": "1"})
    
    # 4. 测试注册照片回调 - base64Enable为int类型（应该成功）
    test_api("/setImgRegCallBack", data={**base_data, "url": "http://example.com/callback", "base64Enable": 1})
    
    # 5. 测试远程控制输出 - type为字符串类型（应该失败）
    test_api("/device/openDoorControl", data={**base_data, "type": "1"})
    
    # 6. 测试远程控制输出 - type为int类型但值为2（应该失败）
    test_api("/device/openDoorControl", data={**base_data, "type": 2})
    
    # 7. 测试远程控制输出 - type为int类型且值为1（应该成功）
    test_api("/device/openDoorControl", data={**base_data, "type": 1})
    
    print("\n=== 测试完成 ===")