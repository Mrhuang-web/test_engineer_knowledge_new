# 测试设备信息查询和设置设备时间的脚本

import sys
import os
import requests

# 设备地址
BASE_URL = "http://127.0.0.1:8090"

print("=== 测试设备信息查询和设置设备时间功能 ===")

# 测试1：设备信息查询
print("\n1. 测试设备信息查询")
try:
    response = requests.get(f"{BASE_URL}/device/information?oldPass=12345678&newPass=12345678")
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    # 检查返回字段是否符合要求
    expected_fields = ['SDKVersion', 'cpuTemperature', 'cpuUsageRate', 'deviceKey', 
                      'faceCount', 'fingerCount', 'freeDiskSpace', 'ip', 
                      'languageType', 'memoryUsageRate', 'personCount', 'time', 
                      'timeZone', 'version']
    
    data = response.json().get('data', {})
    missing_fields = [field for field in expected_fields if field not in data]
    
    if missing_fields:
        print(f"   ❌ 预期：返回包含所有必填字段，但缺少：{missing_fields}")
    else:
        print("   ✅ 预期：返回包含所有必填字段")
    
    if response.json().get('msg') == '查询成功':
        print("   ✅ 预期：返回消息为'查询成功'")
    else:
        print(f"   ❌ 预期：返回消息为'查询成功'，但实际返回：{response.json().get('msg')}")
        
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试2：设置设备时间
print("\n2. 测试设置设备时间")
try:
    timestamp = "1609459200000"  # 2021-01-01 00:00:00
    response = requests.post(f"{BASE_URL}/setTime", 
                          data={"oldPass": "12345678", "newPass": "12345678", "timestamp": timestamp})
    print(f"   状态码: {response.status_code}")
    print(f"   响应: {response.json()}")
    
    expected_msg = "设置成功。若设备未连入公网，则此时间会生效；若设备连入公网，则会重新使用公网时间"
    if response.json().get('msg') == expected_msg:
        print("   ✅ 预期：返回正确的设置时间消息")
    else:
        print(f"   ❌ 预期：返回消息为'{expected_msg}'，但实际返回：{response.json().get('msg')}")
        
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试3：设置设备时间后，再次查询设备信息，检查时间是否更新
print("\n3. 测试设置设备时间后，再次查询设备信息")
try:
    timestamp = "1609459200000"  # 2021-01-01 00:00:00
    # 先设置时间
    requests.post(f"{BASE_URL}/setTime", 
                data={"oldPass": "12345678", "newPass": "12345678", "timestamp": timestamp})
    
    # 再次查询设备信息
    response = requests.get(f"{BASE_URL}/device/information?oldPass=12345678&newPass=12345678")
    print(f"   状态码: {response.status_code}")
    data = response.json().get('data', {})
    print(f"   设备时间: {data.get('time')}")
    
    if data.get('time') == timestamp:
        print("   ✅ 预期：设备时间已更新为设置的时间")
    else:
        print(f"   ❌ 预期：设备时间应更新为{timestamp}，但实际为{data.get('time')}")
        
except Exception as e:
    print(f"   ❌ 错误: {e}")

# 测试4：模拟设备时间增长
print("\n4. 测试模拟设备时间增长")
try:
    timestamp = "1609459200000"  # 2021-01-01 00:00:00
    # 先设置时间
    requests.post(f"{BASE_URL}/setTime", 
                data={"oldPass": "12345678", "newPass": "12345678", "timestamp": timestamp})
    
    # 导入设备数据，模拟时间更新
    from models import device_data
    
    # 模拟时间更新（增加1分钟）
    device_data.update_time()
    
    # 再次查询设备信息
    response = requests.get(f"{BASE_URL}/device/information?oldPass=12345678&newPass=12345678")
    data = response.json().get('data', {})
    new_time = data.get('time')
    print(f"   设置的时间: {timestamp}")
    print(f"   更新后的时间: {new_time}")
    
    expected_time = str(int(timestamp) + 60 * 1000)  # 增加1分钟
    if new_time == expected_time:
        print("   ✅ 预期：设备时间已增长1分钟")
    else:
        print(f"   ❌ 预期：设备时间应增长1分钟至{expected_time}，但实际为{new_time}")
        
except Exception as e:
    print(f"   ❌ 错误: {e}")

print("\n=== 所有测试完成 ===")
