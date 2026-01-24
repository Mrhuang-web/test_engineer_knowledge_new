# 测试识别记录删除功能

import requests
import time

# 设备地址
BASE_URL = "http://127.0.0.1:8090"

print("=== 测试识别记录删除功能 ===")

# 测试1：使用正确的pass参数，删除所有记录
print("\n1. 测试使用正确的pass参数，删除所有记录")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "-1", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"] and response.json()["code"] == "LAN_SUS-0":
        print("   ✅ 预期：删除所有记录成功")
    else:
        print("   ❌ 预期：删除所有记录成功，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试2：模拟生成一些测试记录
print("\n2. 模拟生成一些测试记录")
try:
    # 生成3条不同类型的记录
    for i in range(3):
        person_id = "testperson" if i == 0 else "testperson2" if i == 1 else "STRANGERBABY"
        response = requests.post(f"{BASE_URL}/simulateIdentify", data={"pass": "12345678", "personId": person_id})
        if response.json()["success"]:
            print(f"   ✅ 生成记录 {i+1} 成功")
        else:
            print(f"   ❌ 生成记录 {i+1} 失败: {response.json()}")
        time.sleep(0.5)
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试3：使用正确的pass参数，删除指定personId的记录
print("\n3. 测试使用正确的pass参数，删除指定personId的记录")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "testperson", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"] and response.json()["code"] == "LAN_SUS-0":
        print("   ✅ 预期：删除指定personId的记录成功")
    else:
        print("   ❌ 预期：删除指定personId的记录成功，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试4：使用错误的pass参数
print("\n4. 测试使用错误的pass参数")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "wrongpass", "personId": "-1", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-1001":
        print("   ✅ 预期：删除记录失败，提示密码错误")
    else:
        print("   ❌ 预期：删除记录失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试5：使用不合法的personId参数
print("\n5. 测试使用不合法的personId参数")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "invalid@personid", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-3017":
        print("   ✅ 预期：删除记录失败，提示personId参数不合法")
    else:
        print("   ❌ 预期：删除记录失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试6：使用不合法的model参数
print("\n6. 测试使用不合法的model参数")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "-1", "model": "invalid", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-1002":
        print("   ✅ 预期：删除记录失败，提示参数异常")
    else:
        print("   ❌ 预期：删除记录失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试7：使用不合法的model值（超出范围）
print("\n7. 测试使用不合法的model值（超出范围）")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "-1", "model": "6", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-5007":
        print("   ✅ 预期：删除记录失败，提示model参数不合法")
    else:
        print("   ❌ 预期：删除记录失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试8：使用不合法的startTime格式
print("\n8. 测试使用不合法的startTime格式")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "-1", "startTime": "2024-13-32 25:61:61", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-3033":
        print("   ✅ 预期：删除记录失败，提示startTime时间格式错误")
    else:
        print("   ❌ 预期：删除记录失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试9：使用不合法的endTime格式
print("\n9. 测试使用不合法的endTime格式")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "-1", "startTime": "0", "endTime": "invalid_time"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-3034":
        print("   ✅ 预期：删除记录失败，提示endTime时间格式错误")
    else:
        print("   ❌ 预期：删除记录失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试10：endTime早于startTime
print("\n10. 测试endTime早于startTime")
try:
    current_time = int(time.time() * 1000)
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "-1", "startTime": str(current_time), "endTime": str(current_time - 1000)})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-3035":
        print("   ✅ 预期：删除记录失败，提示endTime应大于startTime")
    else:
        print("   ❌ 预期：删除记录失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试11：使用STRANGERBABY删除陌生人记录
print("\n11. 测试使用STRANGERBABY删除陌生人记录")
try:
    # 先生成一条陌生人记录
    response = requests.post(f"{BASE_URL}/simulateIdentify", data={"pass": "12345678", "personId": "STRANGERBABY"})
    if response.json()["success"]:
        print("   ✅ 生成陌生人记录成功")
        
        # 然后删除陌生人记录
        response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "STRANGERBABY", "startTime": "0", "endTime": "0"})
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")
        if response.json()["success"] and response.json()["code"] == "LAN_SUS-0":
            print("   ✅ 预期：删除陌生人记录成功")
        else:
            print("   ❌ 预期：删除陌生人记录成功，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试12：使用字符串格式的startTime和endTime
print("\n12. 测试使用字符串格式的startTime和endTime")
try:
    # 生成一条测试记录
    response = requests.post(f"{BASE_URL}/simulateIdentify", data={"pass": "12345678", "personId": "testperson"})
    if response.json()["success"]:
        print("   ✅ 生成测试记录成功")
        
        # 使用字符串格式的时间删除记录
        current_time = time.strftime("%Y-%m-%d %H:%M:%S")
        response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "-1", "startTime": "2024-01-01 00:00:00", "endTime": current_time})
        print(f"   状态码: {response.status_code}")
        print(f"   响应: {response.json()}")
        if response.json()["success"] and response.json()["code"] == "LAN_SUS-0":
            print("   ✅ 预期：使用字符串格式时间删除记录成功")
        else:
            print("   ❌ 预期：使用字符串格式时间删除记录成功，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试13：使用空的personId
print("\n13. 测试使用空的personId")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-3016":
        print("   ✅ 预期：删除记录失败，提示personId参数不能为空")
    else:
        print("   ❌ 预期：删除记录失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试14：使用不存在的personId
print("\n14. 测试使用不存在的personId")
try:
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "nonexistentperson", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if not response.json()["success"] and response.json()["code"] == "LAN_EXP-3009":
        print("   ✅ 预期：删除记录失败，提示人员ID不存在")
    else:
        print("   ❌ 预期：删除记录失败，但实际结果不符")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试15：检查返回的删除记录数量
print("\n15. 测试返回的删除记录数量")
try:
    # 生成3条测试记录
    for i in range(3):
        response = requests.post(f"{BASE_URL}/simulateIdentify", data={"pass": "12345678", "personId": "testperson2"})
        if response.json()["success"]:
            print(f"   ✅ 生成记录 {i+1} 成功")
        else:
            print(f"   ❌ 生成记录 {i+1} 失败")
        time.sleep(0.5)
    
    # 删除这些记录
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "testperson2", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"] and response.json()["code"] == "LAN_SUS-0" and "data" in response.json():
        print(f"   ✅ 预期：删除记录成功，返回删除数量: {response.json()['data']}")
    else:
        print("   ❌ 预期：删除记录成功并返回删除数量，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试16：使用model参数过滤删除记录
print("\n16. 测试使用model参数过滤删除记录")
try:
    # 生成不同model的记录
    for model in [0, 1, 2]:
        # 模拟不同model的记录（通过调用不同的模拟接口）
        response = requests.post(f"{BASE_URL}/simulateIdentify", data={"pass": "12345678", "personId": "testperson"})
        if response.json()["success"]:
            print(f"   ✅ 生成记录（model={model}）成功")
        else:
            print(f"   ❌ 生成记录（model={model}）失败")
        time.sleep(0.5)
    
    # 使用model=0删除刷脸识别记录
    response = requests.post(f"{BASE_URL}/newDeleteRecords", data={"pass": "12345678", "personId": "testperson", "model": "0", "startTime": "0", "endTime": "0"})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"] and response.json()["code"] == "LAN_SUS-0":
        print(f"   ✅ 预期：使用model=0删除刷脸识别记录成功")
    else:
        print(f"   ❌ 预期：使用model=0删除刷脸识别记录成功，但实际失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n=== 所有测试完成 ===")
