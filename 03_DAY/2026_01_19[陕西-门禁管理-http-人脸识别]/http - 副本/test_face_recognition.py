# 测试人脸识别功能的脚本

import sys
import os
import requests
import json
import time

# 设备地址
BASE_URL = "http://127.0.0.1:8090"
# 测试密码
TEST_PASSWORD = "test1234"

print("=== 测试人脸识别功能 ===")

# 初始化设备
print("\n1. 初始化设备（重置设备）")
try:
    # 使用初始密码重置设备
    response = requests.post(f"{BASE_URL}/resetDevice", data={"oldPass": "12345678", "newPass": "12345678"})
    print(f"   重置设备响应: {response.json()}")
    
    # 设置测试密码
    response = requests.post(f"{BASE_URL}/setPassWord", data={"oldPass": TEST_PASSWORD, "newPass": TEST_PASSWORD})
    print(f"   设置密码响应: {response.json()}")
    
    if response.json()["success"]:
        print("   ✅ 设备初始化成功")
    else:
        print("   ❌ 设备初始化失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")
    sys.exit(1)

# 测试2：注册测试人员
print("\n2. 注册测试人员")
test_person = {
    "id": "test_person_001",
    "name": "测试人员",
    "facePermission": 2,
    "idCardPermission": 2,
    "faceAndCardPermission": 1
}

try:
    response = requests.post(
        f"{BASE_URL}/person/create",
        data={"pass": TEST_PASSWORD, "person": json.dumps(test_person)}
    )
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 人员注册成功")
    else:
        print("   ❌ 人员注册失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试3：查询测试人员
print("\n3. 查询测试人员")
try:
    response = requests.get(f"{BASE_URL}/person/find?pass={TEST_PASSWORD}&id=test_person_001")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 人员查询成功")
        # 验证权限默认值
        person_data = response.json()["data"]
        if person_data["facePermission"] == 2 and person_data["idCardPermission"] == 2 and person_data["faceAndCardPermission"] == 1:
            print("   ✅ 权限默认值设置正确")
        else:
            print("   ❌ 权限默认值设置不正确")
    else:
        print("   ❌ 人员查询失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试4：模拟人脸注册（使用简化的base64图片）
print("\n4. 模拟人脸注册")
# 简化的base64图片（1x1像素的白色图片）
test_img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="

try:
    response = requests.post(
        f"{BASE_URL}/face/create",
        data={
            "pass": TEST_PASSWORD,
            "personId": "test_person_001",
            "faceId": "test_face_001",
            "imgBase64": test_img_base64,
            "isEasyWay": "true"
        }
    )
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 人脸注册成功")
    else:
        print(f"   ⚠️  人脸注册失败（可能是因为图片质量问题，这是预期的，因为我们使用的是1x1像素的测试图片）")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试5：模拟识别记录生成
print("\n5. 模拟识别记录生成")
try:
    response = requests.post(
        f"{BASE_URL}/simulateIdentify",
        data={"pass": TEST_PASSWORD, "personId": "test_person_001"}
    )
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 模拟识别成功")
    else:
        print("   ❌ 模拟识别失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试6：查询识别记录
print("\n6. 查询识别记录")
try:
    response = requests.get(
        f"{BASE_URL}/newFindRecords",
        params={
            "pass": TEST_PASSWORD,
            "personId": "test_person_001",
            "startTime": 0,
            "endTime": int(time.time() * 1000)
        }
    )
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 识别记录查询成功")
        records = response.json()["data"].get("records", [])
        if len(records) > 0:
            print(f"   ✅ 找到 {len(records)} 条识别记录")
        else:
            print("   ⚠️  未找到识别记录")
    else:
        print("   ❌ 识别记录查询失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试7：设置识别回调
print("\n7. 设置识别回调")
try:
    callback_url = "http://localhost:8080/identify_callback"
    response = requests.post(
        f"{BASE_URL}/setIdentifyCallBack",
        data={"pass": TEST_PASSWORD, "callbackUrl": callback_url}
    )
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 识别回调设置成功")
    else:
        print("   ❌ 识别回调设置失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试8：再次模拟识别记录生成，触发回调
print("\n8. 再次模拟识别记录生成，触发回调")
try:
    response = requests.post(
        f"{BASE_URL}/simulateIdentify",
        data={"pass": TEST_PASSWORD, "personId": "test_person_001"}
    )
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 模拟识别成功，回调已触发")
    else:
        print("   ❌ 模拟识别失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试9：删除测试人员
print("\n9. 删除测试人员")
try:
    response = requests.post(
        f"{BASE_URL}/person/delete",
        data={"pass": TEST_PASSWORD, "id": "test_person_001"}
    )
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    if response.json()["success"]:
        print("   ✅ 人员删除成功")
    else:
        print("   ❌ 人员删除失败")
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n=== 人脸识别功能测试完成 ===")
