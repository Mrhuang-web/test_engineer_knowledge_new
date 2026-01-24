#!/usr/bin/env python3
# 测试动环接口客户端调用功能

from donghuan_client import get_donghuan_client

# 测试用例
print("=== 测试动环接口客户端调用功能 ===\n")

try:
    # 1. 初始化客户端（使用默认环境）
    print("1. 初始化动环客户端...")
    client = get_donghuan_client()
    print(f"   客户端初始化成功，环境: {client.env}，服务器: {client.server_root}")
    print(f"   密钥: {client.secret_key}")
    
    # 2. 构造测试数据
    print("\n2. 构造测试数据...")
    face_data = {
        "workOrdNum": "JF-20251222-0313",
        "name": "测试用户",
        "account": "testuser",
        "phone": "13800001111",
        "city": "咸阳市",
        "site": ["安康白河庆华化工厂站点"],
        "room": ["咸阳秦都应急楼一楼综合机房"],
        "deviceId": ["20231201996901"],
        "picture": "test_base64_string",
        "startDate": "2025-12-26"
    }
    print(f"   测试数据构造完成，工单号: {face_data['workOrdNum']}")
    print(f"   数据包含字段: {list(face_data.keys())}")
    
    # 3. 打印调用说明
    print("\n3. 调用说明...")
    print("   - 接口URL: {client.base_url}/v1/external/ywgl/addFace")
    print("   - 请求方法: POST")
    print("   - 请求格式: form-data")
    print("   - 鉴权方式: secret_key字段")
    print("   - 必填参数: workOrdNum, name, account, phone, city, site, room, deviceId, picture, startDate")
    
    # 4. 调用add_face接口
    print("\n4. 调用动环addFace接口...")
    print("   (注意: 实际调用会连接动环服务器，若服务器不可达会显示异常)")
    result = client.add_face(face_data)
    
    # 5. 打印结果
    print("\n5. 调用结果:")
    print(f"   响应码: {result['code']}")
    print(f"   响应描述: {result['desc']}")
    print(f"   响应数据: {result['data']}")
    
    # 6. 结果解析
    print("\n6. 结果解析...")
    if result['code'] == '00':
        print("   ✅ 调用成功")
    elif result['code'] == '22':
        print("   ❌ 安全校验不通过，请检查密钥是否正确")
    elif result['code'] == '23':
        print("   ❌ 请求参数错误，请检查必填参数是否完整")
    elif result['code'] == '21':
        print("   ⚠️  接口异常，可能是网络问题或服务器错误")
    else:
        print(f"   ⚠️  未知响应码: {result['code']}")
    
    print("\n" + "="*60)
    print("\n=== 测试完成 ===")
    
except Exception as e:
    print(f"\n测试失败: {e}")
    import traceback
    traceback.print_exc()
