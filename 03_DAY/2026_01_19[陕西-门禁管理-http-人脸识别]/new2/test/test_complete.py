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
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, json=data)
        else:
            response = requests.post(url, headers=headers, json=data)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        # 检查响应格式
        try:
            response_json = response.json()
            print(f"响应格式检查: 成功")
            print(f"响应包含字段: {list(response_json.keys())}")
            
            # 检查data字段是否存在
            if "data" in response_json:
                print(f"data字段值: {response_json['data']}")
                if response_json['data'] is None:
                    print(f"警告: data字段值为null")
        except json.JSONDecodeError:
            print(f"响应格式检查: 失败，不是有效的JSON格式")
    
    except Exception as e:
        print(f"测试失败: {str(e)}")

# 主测试流程
if __name__ == "__main__":
    print("开始完整API测试流程")
    
    # 1. 初次设置密码
    test_api("/setPassWord", data={"oldPass": "123456", "newPass": "123456"})
    
    # 2. 测试获取设备信息
    test_api("/device/information", method="GET", data={"pass": "123456"})
    
    # 3. 测试设置时间
    test_api("/setTime", data={"pass": "123456", "timestamp": "1706077213605"})
    
    # 4. 测试切换语言
    test_api("/device/setLanguage", data={"pass": "123456", "languageType": "en"})
    
    # 5. 再次测试切换语言
    test_api("/device/setLanguage", data={"pass": "123456", "languageType": "zh_CN"})
    
    print("\n=== 测试完成 ===")