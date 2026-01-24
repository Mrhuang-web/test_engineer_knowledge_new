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
    print("开始测试设备API参数异常处理")
    
    # 1. 测试切换语言 - 缺少languageType参数
    test_api("/device/setLanguage", data={"pass": "123456"})
    
    # 2. 测试切换语言 - 无效的languageType值
    test_api("/device/setLanguage", data={"pass": "123456", "languageType": "invalid_lang"})
    
    # 3. 测试设置时区 - 缺少timeZone参数
    test_api("/device/setTimeZone", data={"pass": "123456"})
    
    # 4. 测试设置时区 - 无效的timeZone值
    test_api("/device/setTimeZone", data={"pass": "123456", "timeZone": ""})
    
    print("\n=== 测试完成 ===")