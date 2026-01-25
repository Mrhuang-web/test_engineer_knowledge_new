# 测试响应格式
from business_logic.device import device_service
from business_logic.person import person_service
from business_logic.face import face_service
from business_logic.record import record_service

print("=== 测试响应格式 ===")

# 测试设备服务响应
device_response = device_service._get_response('LAN_SUS-0', msg='测试成功', data={'key': 'value'})
print("设备服务响应:")
print(device_response)
print("响应字段顺序:", list(device_response.keys()))
print()

# 测试人员服务响应
person_response = person_service._get_response('LAN_SUS-0', data=[{'id': '1001', 'name': '测试人员'}])
print("人员服务响应:")
print(person_response)
print("响应字段顺序:", list(person_response.keys()))
print()

# 测试照片服务响应
face_response = face_service._get_response('LAN_EXP-4008')
print("照片服务响应:")
print(face_response)
print("响应字段顺序:", list(face_response.keys()))
print()

# 测试记录服务响应
record_response = record_service._get_response('LAN_SUS-0')
print("记录服务响应:")
print(record_response)
print("响应字段顺序:", list(record_response.keys()))
print()

print("=== 测试完成 ===")