import requests
import json

# 测试函数
def test_api(endpoint, method="POST", data=None, headers=None):
    """通用API测试函数"""
    if headers is None:
        headers = {"Content-Type": "application/json"}
    
    url = f"http://localhost:8091{endpoint}"
    
    print(f"\n=== 测试 {method} {endpoint} ===")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False) if data else '无'}")
    print(f"请求头: {headers}")
    
    try:
        if method == "GET":
            response = requests.get(url, params=data)
        else:
            response = requests.post(url, headers=headers, json=data)
        
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
    print("开始测试信号输入设置API")
    
    # 测试数据：设置了密码的情况
    base_data = {"pass": "123456"}
    
    # 1. 测试信号输入设置 - 缺少config参数（预期失败）
    test_api("/device/setSignalInput", data=base_data)
    
    # 2. 测试信号输入设置 - config为空（预期失败）
    test_api("/device/setSignalInput", data={**base_data, "config": {}})
    
    # 3. 测试信号输入设置 - config为非JSON格式（预期失败）
    test_api("/device/setSignalInput", data={**base_data, "config": "not_json"}, headers={"Content-Type": "application/x-www-form-urlencoded"})
    
    # 4. 测试信号输入设置 - 缺少必填字段（预期失败）
    test_api("/device/setSignalInput", data={**base_data, "config": {"inputNo": 1, "isEnable": True}})
    
    # 5. 测试信号输入设置 - inputNo为字符串类型（预期失败）
    test_api("/device/setSignalInput", data={**base_data, "config": {"inputNo": "1", "isEnable": True, "type": 2}})
    
    # 6. 测试信号输入设置 - inputNo值越界（预期失败）
    test_api("/device/setSignalInput", data={**base_data, "config": {"inputNo": 3, "isEnable": True, "type": 2}})
    
    # 7. 测试信号输入设置 - isEnable为字符串类型（预期失败）
    test_api("/device/setSignalInput", data={**base_data, "config": {"inputNo": 1, "isEnable": "true", "type": 2}})
    
    # 8. 测试信号输入设置 - type为字符串类型（预期失败）
    test_api("/device/setSignalInput", data={**base_data, "config": {"inputNo": 1, "isEnable": True, "type": "2"}})
    
    # 9. 测试信号输入设置 - type值越界（预期失败）
    test_api("/device/setSignalInput", data={**base_data, "config": {"inputNo": 1, "isEnable": True, "type": 4}})
    
    # 10. 测试信号输入设置 - 所有参数正确（预期成功）
    test_api("/device/setSignalInput", data={**base_data, "config": {"inputNo": 1, "isEnable": True, "type": 2}})
    
    # 11. 测试信号输入设置 - 信号输入2（预期成功）
    test_api("/device/setSignalInput", data={**base_data, "config": {"inputNo": 2, "isEnable": False, "type": 3}})
    
    print("\n=== 测试完成 ===")