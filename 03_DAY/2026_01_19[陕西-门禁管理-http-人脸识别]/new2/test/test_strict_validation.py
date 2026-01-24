#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试严格参数验证
模拟apifox发送不同类型的参数，验证严格校验是否生效
"""

import http.client
import json

# 测试函数
def test_api(endpoint, method="POST", data=None, headers=None):
    """测试API，支持发送不同类型的参数"""
    if headers is None:
        headers = {"Content-Type": "application/json"}
    
    print(f"\n=== 测试 {method} {endpoint} ===")
    print(f"请求头: {headers}")
    print(f"请求数据: {json.dumps(data, ensure_ascii=False) if data else '无'}")
    
    try:
        conn = http.client.HTTPConnection("localhost", 8090)
        
        # 根据Content-Type处理请求数据
        if headers.get("Content-Type") == "application/json":
            body = json.dumps(data)
        else:  # application/x-www-form-urlencoded
            # 手动构建表单数据，避免引号问题
            body_parts = []
            for key, value in data.items():
                body_parts.append(f"{key}={value}")
            body = "&".join(body_parts)
            
        conn.request(method, endpoint, body=body, headers=headers)
        response = conn.getresponse()
        
        print(f"响应状态码: {response.status}")
        response_body = response.read().decode('utf-8')
        print(f"响应内容: {response_body}")
        
        # 检查响应格式
        try:
            response_json = json.loads(response_body)
            print(f"响应格式检查: 成功")
            print(f"响应code: {response_json['code']}")
            print(f"响应msg: {response_json['msg']}")
            return response_json
        except json.JSONDecodeError:
            print(f"响应格式检查: 失败，不是有效的JSON格式")
            return None
    
    except Exception as e:
        print(f"测试失败: {str(e)}")
        return None
    finally:
        conn.close()

def test_identify_callback():
    """测试识别回调设置，发送字符串类型的base64Enable"""
    print("\n开始测试识别回调设置")
    
    # 测试数据
    base_data = {"pass": "123456", "callbackUrl": "http://example.com/callback"}
    
    # 1. JSON格式 - base64Enable为字符串类型（预期失败）
    result = test_api("/setIdentifyCallBack", 
                    data={**base_data, "base64Enable": "0"}, 
                    headers={"Content-Type": "application/json"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    # 2. JSON格式 - base64Enable为int类型（预期成功）
    result = test_api("/setIdentifyCallBack", 
                    data={**base_data, "base64Enable": 0}, 
                    headers={"Content-Type": "application/json"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_SUS-0", f"预期LAN_SUS-0，实际{result['code']}"
    
    # 3. 表单格式 - base64Enable为字符串类型（预期失败）
    result = test_api("/setIdentifyCallBack", 
                    data={**base_data, "base64Enable": "1"}, 
                    headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    print("识别回调设置测试通过！")

def test_img_reg_callback():
    """测试注册照片回调设置，发送字符串类型的base64Enable"""
    print("\n开始测试注册照片回调设置")
    
    # 测试数据
    base_data = {"pass": "123456", "url": "http://example.com/callback"}
    
    # 1. JSON格式 - base64Enable为字符串类型（预期失败）
    result = test_api("/setImgRegCallBack", 
                    data={**base_data, "base64Enable": "0"}, 
                    headers={"Content-Type": "application/json"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    # 2. JSON格式 - base64Enable为int类型（预期成功）
    result = test_api("/setImgRegCallBack", 
                    data={**base_data, "base64Enable": 0}, 
                    headers={"Content-Type": "application/json"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_SUS-0", f"预期LAN_SUS-0，实际{result['code']}"
    
    # 3. 表单格式 - base64Enable为字符串类型（预期失败）
    result = test_api("/setImgRegCallBack", 
                    data={**base_data, "base64Enable": "1"}, 
                    headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    print("注册照片回调设置测试通过！")

def test_open_door_control():
    """测试远程控制输出，发送不同类型的type参数"""
    print("\n开始测试远程控制输出")
    
    # 测试数据
    base_data = {"pass": "123456"}
    
    # 1. JSON格式 - type为字符串类型（预期失败）
    result = test_api("/device/openDoorControl", 
                    data={**base_data, "type": "1"}, 
                    headers={"Content-Type": "application/json"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    # 2. JSON格式 - type为int类型但值为2（预期失败）
    result = test_api("/device/openDoorControl", 
                    data={**base_data, "type": 2}, 
                    headers={"Content-Type": "application/json"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    # 3. JSON格式 - type为int类型且值为1（预期成功）
    result = test_api("/device/openDoorControl", 
                    data={**base_data, "type": 1}, 
                    headers={"Content-Type": "application/json"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_SUS-0", f"预期LAN_SUS-0，实际{result['code']}"
    
    # 4. 表单格式 - type为字符串类型（预期失败）
    result = test_api("/device/openDoorControl", 
                    data={**base_data, "type": "1"}, 
                    headers={"Content-Type": "application/x-www-form-urlencoded"})
    assert result is not None, "响应为空"
    assert result["code"] == "LAN_EXP-1002", f"预期LAN_EXP-1002，实际{result['code']}"
    
    print("远程控制输出测试通过！")

if __name__ == "__main__":
    print("开始测试严格参数验证")
    
    try:
        # 确保设备已设置密码
        test_api("/setPassWord", 
                data={"oldPass": "123456", "newPass": "123456"}, 
                headers={"Content-Type": "application/json"})
        
        test_identify_callback()
        test_img_reg_callback()
        test_open_door_control()
        
        print("\n所有测试通过！严格参数验证生效。")
    except AssertionError as e:
        print(f"\n测试失败: {e}")
    except Exception as e:
        print(f"\n测试错误: {e}")
        import traceback
        traceback.print_exc()