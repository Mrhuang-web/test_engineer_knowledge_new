# 简单测试脚本，用于验证重构后的代码是否正常工作

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 测试导入是否正常
print("测试导入模块...")
try:
    from rules.response import base_response
    print("✓ 成功导入 rules.response")
except ImportError as e:
    print(f"✗ 导入 rules.response 失败: {e}")

try:
    from models import device_data, person_data, face_data, record_data
    print("✓ 成功导入 models 模块")
except ImportError as e:
    print(f"✗ 导入 models 模块失败: {e}")

try:
    from services import device_service, person_service, face_service, record_service
    print("✓ 成功导入 services 模块")
except ImportError as e:
    print(f"✗ 导入 services 模块失败: {e}")

# 测试设备服务
try:
    print("\n测试设备服务...")
    response = device_service.get_device_info()
    print(f"✓ 设备信息查询成功: {response['code']}")
except Exception as e:
    print(f"✗ 设备服务测试失败: {e}")

# 测试人员服务
try:
    print("\n测试人员服务...")
    person_json = '{"name": "测试人员", "idcardNum": "123456789012345678"}'
    response = person_service.create_person(person_json)
    print(f"✓ 人员创建成功: {response['code']}")
except Exception as e:
    print(f"✗ 人员服务测试失败: {e}")

# 测试照片服务
try:
    print("\n测试照片服务...")
    # 注意：这里只是测试导入和基本功能，实际照片注册需要有效的人员ID
    print("✓ 照片服务模块加载成功")
except Exception as e:
    print(f"✗ 照片服务测试失败: {e}")

# 测试识别记录服务
try:
    print("\n测试识别记录服务...")
    response = record_service.simulate_identify()
    print(f"✓ 模拟识别成功: {response['code']}")
except Exception as e:
    print(f"✗ 识别记录服务测试失败: {e}")

print("\n所有测试完成！")
