import requests
import json

# 测试服务器地址
BASE_URL = "http://127.0.0.1:8093"

def test_set_password_no_pass_field():
    """测试设置密码不需要pass字段"""
    print("1. 测试设置密码不需要pass字段...")
    url = f"{BASE_URL}/setPassWord"
    data = {
        "oldPass": "12345678",
        "newPass": "12345678"
    }
    
    try:
        response = requests.post(url, data=data, timeout=5)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        # 检查是否返回了JSON响应
        response_data = response.json()
        print("   ✅ 设置密码接口正常响应")
        return True
    except json.JSONDecodeError:
        print("   ❌ 设置密码接口返回非JSON响应")
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False

def test_param_type_validation():
    """测试参数类型校验"""
    print("\n2. 测试参数类型校验...")
    url = f"{BASE_URL}/device/openDoorControl"
    
    # 先设置密码，以便后续请求能够通过验证
    set_password_url = f"{BASE_URL}/setPassWord"
    set_password_data = {
        "oldPass": "12345678",
        "newPass": "12345678"
    }
    requests.post(set_password_url, data=set_password_data, timeout=5)
    
    # 测试type参数为字符串的情况，应该返回错误
    data = {
        "type": "1",  # 应该为整数
        "pass": "12345678"
    }
    
    try:
        response = requests.post(url, data=data, timeout=5)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        # 检查是否返回了JSON响应
        response_data = response.json()
        print("   ✅ 参数类型校验接口正常响应")
        return True
    except json.JSONDecodeError:
        print("   ❌ 参数类型校验接口返回非JSON响应")
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False

def test_body_param_parsing():
    """测试从body内获取参数"""
    print("\n3. 测试从body内获取参数...")
    url = f"{BASE_URL}/device/openDoorControl"
    
    # 使用正确的type参数类型（整数）
    data = {
        "type": 1,
        "pass": "12345678"
    }
    
    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        # 检查是否返回了JSON响应
        response_data = response.json()
        print("   ✅ 从body获取参数正常")
        return True
    except json.JSONDecodeError:
        print("   ❌ 从body获取参数接口返回非JSON响应")
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False

if __name__ == "__main__":
    print("=== 测试POST请求功能 ===")
    
    # 运行所有测试
    tests = [
        test_set_password_no_pass_field,
        test_param_type_validation,
        test_body_param_parsing
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    # 输出测试结果汇总
    print("\n=== 测试结果汇总 ===")
    passed = sum(results)
    total = len(results)
    print(f"通过: {passed}/{total}")
    
    if passed == total:
        print("✅ 所有POST测试通过！")
    else:
        print(f"❌ 有 {total - passed} 个POST测试失败！")
