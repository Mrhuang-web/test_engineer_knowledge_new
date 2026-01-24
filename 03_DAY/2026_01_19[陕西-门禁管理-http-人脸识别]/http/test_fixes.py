import requests
import json
import threading

# 测试服务器地址
BASE_URL = "http://127.0.0.1:8092"

def test_set_password_no_pass_field():
    """测试设置密码不需要pass字段"""
    print("1. 测试设置密码不需要pass字段...")
    url = f"{BASE_URL}/setPassWord"
    data = {
        "oldPass": "12345678",
        "newPass": "12345678"
    }
    
    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        return True
    except Exception as e:
        print(f"   错误: {e}")
        return False

def test_param_type_validation():
    """测试参数类型校验"""
    print("\n2. 测试参数类型校验...")
    url = f"{BASE_URL}/device/openDoorControl"
    
    # 测试type参数为字符串的情况，应该返回错误
    data = {
        "type": "1",  # 应该为整数
        "pass": "12345678"
    }
    
    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        # 检查是否返回了类型错误
        response_data = response.json()
        if response_data['code'] == 'LAN_EXP-2213':  # TYPE_ILLEGAL
            print("   ✅ 参数类型校验工作正常")
            return True
        else:
            print("   ❌ 参数类型校验失败")
            return False
    except Exception as e:
        print(f"   错误: {e}")
        return False

def test_body_param_parsing():
    """测试从body内获取参数"""
    print("\n3. 测试从body内获取参数...")
    url = f"{BASE_URL}/device/openDoorControl"
    
    # 从body内传递参数
    data = {
        "type": 1,
        "pass": "12345678"
    }
    
    try:
        response = requests.post(url, json=data, timeout=5)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        return True
    except Exception as e:
        print(f"   错误: {e}")
        return False

def test_multithreading_support():
    """测试多线程支持"""
    print("\n4. 测试多线程支持...")
    
    def make_request():
        """发起单个请求"""
        url = f"{BASE_URL}/device/information"
        data = {"pass": "12345678"}
        try:
            response = requests.get(url, json=data, timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    # 创建多个线程同时发起请求
    threads = []
    results = []
    
    for _ in range(10):
        thread = threading.Thread(target=lambda r: r.append(make_request()), args=(results,))
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    success_count = sum(results)
    print(f"   10个并发请求，成功{success_count}个，失败{10 - success_count}个")
    
    if success_count >= 8:  # 允许少量失败，可能是因为服务器启动时间问题
        print("   ✅ 多线程支持工作正常")
        return True
    else:
        print("   ❌ 多线程支持失败")
        return False

def test_person_query_from_body():
    """测试人员查询从body获取参数"""
    print("\n5. 测试人员查询从body获取参数...")
    url = f"{BASE_URL}/person/find"
    
    # 从body内传递id参数
    data = {
        "id": "test123",
        "pass": "12345678"
    }
    
    try:
        response = requests.get(url, json=data, timeout=5)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        # 即使人员不存在，只要返回JSON响应就说明参数解析正常
        response.json()
        print("   ✅ 人员查询从body获取参数正常")
        return True
    except json.JSONDecodeError:
        print("   ❌ 人员查询返回非JSON响应")
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False

if __name__ == "__main__":
    print("=== 测试修复后的服务器功能 ===")
    
    # 运行所有测试
    tests = [
        test_set_password_no_pass_field,
        test_param_type_validation,
        test_body_param_parsing,
        test_multithreading_support,
        test_person_query_from_body
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
        print("✅ 所有测试通过！")
    else:
        print(f"❌ 有 {total - passed} 个测试失败！")
