import requests
import json

# 测试服务器地址
BASE_URL = "http://127.0.0.1:8094"

def test_set_password():
    """测试设置密码功能"""
    print("1. 测试设置密码功能...")
    url = f"{BASE_URL}/setPassWord"
    data = {
        "oldPass": "12345678",
        "newPass": "12345678"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        # 检查是否返回了JSON响应
        response_data = response.json()
        if response.status_code == 200:
            print("   ✅ 设置密码功能正常")
            return True
        else:
            print("   ❌ 设置密码功能失败")
            return False
    except json.JSONDecodeError:
        print("   ❌ 设置密码接口返回非JSON响应")
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False

def test_open_door():
    """测试远程开门功能"""
    print("\n2. 测试远程开门功能...")
    url = f"{BASE_URL}/device/openDoorControl"
    data = {
        "type": 1,
        "pass": "12345678"
    }
    
    try:
        response = requests.post(url, json=data, timeout=10)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        # 检查是否返回了JSON响应
        response_data = response.json()
        if response.status_code == 200:
            print("   ✅ 远程开门功能正常")
            return True
        else:
            print("   ❌ 远程开门功能失败")
            return False
    except json.JSONDecodeError:
        print("   ❌ 远程开门接口返回非JSON响应")
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False

def test_device_information():
    """测试设备信息查询功能"""
    print("\n3. 测试设备信息查询功能...")
    url = f"{BASE_URL}/device/information?pass=12345678"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.text}")
        # 检查是否返回了JSON响应
        response_data = response.json()
        if response.status_code == 200:
            print("   ✅ 设备信息查询功能正常")
            return True
        else:
            print("   ❌ 设备信息查询功能失败")
            return False
    except json.JSONDecodeError:
        print("   ❌ 设备信息查询接口返回非JSON响应")
        return False
    except Exception as e:
        print(f"   错误: {e}")
        return False

if __name__ == "__main__":
    print("=== 测试修复后的功能 ===")
    
    # 运行所有测试
    tests = [
        test_set_password,
        test_open_door,
        test_device_information
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
