import requests
import json

base_url = "http://127.0.0.1:8090"
password = "12345678"

print("=== 测试完整流程 ===")

# 1. 先设置密码
print("\n1. 设置设备密码")
set_pass_url = f"{base_url}/setPassWord"
data = {
    "oldPass": password,
    "newPass": password
}
try:
    response = requests.post(set_pass_url, data=data)
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 密码设置成功")
    else:
        print(f"   ❌ 密码设置失败: {response.json()['msg']}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 2. 模拟生成一些测试记录
print("\n2. 模拟生成测试记录")
simulate_url = f"{base_url}/simulateIdentify"
data = {"pass": password}
for i in range(3):
    try:
        response = requests.post(simulate_url, data=data)
        if response.json()["success"]:
            print(f"   ✅ 生成记录 {i+1} 成功")
        else:
            print(f"   ❌ 生成记录 {i+1} 失败: {response.json()['msg']}")
    except Exception as e:
        print(f"   ❌ 生成记录 {i+1} 错误: {e}")

# 3. 查询识别记录，确认有记录存在
print("\n3. 查询识别记录")
find_records_url = f"{base_url}/newFindRecords?pass={password}&personId=-1&startTime=0&endTime=0"
try:
    response = requests.get(find_records_url)
    print(f"   状态码: {response.status_code}")
    response_data = response.json()
    print(f"   响应: {response_data}")
    if response_data["success"]:
        if "data" in response_data and isinstance(response_data["data"], dict) and "records" in response_data["data"]:
            record_count = len(response_data["data"]["records"])
            print(f"   ✅ 查询成功，共有 {record_count} 条记录")
        else:
            print("   ✅ 查询成功，没有记录")
    else:
        print(f"   ❌ 查询失败: {response_data['msg']}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 4. 测试识别记录删除功能
print("\n4. 测试识别记录删除功能")
delete_records_url = f"{base_url}/newDeleteRecords"
data = {
    "pass": password,
    "personId": "-1",
    "startTime": "0",
    "endTime": "9999-12-31 23:59:59",
    "model": "-1"
}
try:
    response = requests.post(delete_records_url, data=data)
    print(f"   状态码: {response.status_code}")
    response_data = response.json()
    print(f"   响应: {response_data}")
    if response_data["success"]:
        print("   ✅ 删除记录成功")
    else:
        print(f"   ❌ 删除记录失败: {response_data['msg']}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 5. 再次查询识别记录，确认记录已删除
print("\n5. 再次查询识别记录，确认记录已删除")
try:
    response = requests.get(find_records_url)
    print(f"   状态码: {response.status_code}")
    response_data = response.json()
    print(f"   响应: {response_data}")
    if response_data["success"]:
        if "data" in response_data and isinstance(response_data["data"], dict) and "records" in response_data["data"]:
            record_count = len(response_data["data"]["records"])
            print(f"   ✅ 查询成功，共有 {record_count} 条记录")
        else:
            print("   ✅ 查询成功，没有记录")
    else:
        print(f"   ❌ 查询失败: {response_data['msg']}")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n=== 测试完成 ===")
