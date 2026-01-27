#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动环平台双向认证 Token 生成脚本（针对指定 body）
"""
import hashlib
import hmac
import json
import base64


def base16_encode(data: bytes) -> str:
    return data.hex().upper()


def build_token(app_key: str, body: str = '') -> str:
    """
    根据文档实现的 token 生成算法
    token = Base16(HMAC-SHA-256(appkey, SignBytes))
    SignBytes = Content-MD5-Str
    Content-MD5-Str 为消息体所有内容 MD5
    对于GET请求（无消息体），可不参与TOKEN计算
    """
    # 如果是GET请求（无消息体），不参与TOKEN计算
    if not body:
        return ''
    
    # 步骤 1: 计算消息体的 MD5 散列值
    md5_hash = hashlib.md5(body.encode('utf-8')).digest()
    print(f"MD5 散列值 (前 10 字节): {md5_hash[:10]}")
    
    # 步骤 2: 使用 HMAC-SHA-256 对 MD5 散列值进行加密
    # 直接使用 app_key 的 UTF-8 编码作为密钥
    app_key_bytes = app_key.encode('utf-8')
    print(f"AppKey 长度: {len(app_key_bytes)}")
    
    hmac_result = hmac.new(app_key_bytes, md5_hash, hashlib.sha256).digest()
    print(f"HMAC 结果 (前 10 字节): {hmac_result[:10]}")
    
    # 步骤 3: 使用 Base16 对 HMAC 结果进行转换
    token = base16_encode(hmac_result)
    return token


def build_auth_header(app_id: str, app_key: str, body: str = '') -> dict:
    token = build_token(app_key, body)
    return {'Authorization': f'appid="{app_id}",token="{token}"'}


if __name__ == '__main__':
    # ==================== 配置区 ====================

    # 请求路径（根据实际接口修改）
    request_path = "/xxxGroup/xxx?V=1.1"
    
    # 请求方法
    request_method = "POST"

    # 请求体数据
    payload = {
        "data": {
            "workOrdNum": "123",
            "name": "test001",
            "account": "1233",
            "phone": "142523",
            "city": "咸阳市",
            "site": ["安康白河庆华化工厂站点"],
            "room": ["咸阳秦都应急楼一楼综合机房"],
            "deviceIdList": ["ad8c7a55-362e-4b58-8644-b6e9169e1439"],
            "picture": "123",
            "startDate": "2026-01-26"
        }
    }

    # json.dumps 确保与请求 body 完全一致（注意分隔符和中文编码）
    # 使用文档推荐的格式：无额外空格，UTF-8编码
    body_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)

    # 替换为你自己的 app_id & app_key
    app_id = 'lbVGV48llz7EEa2RbWqcbAUtAX37mB'

    # 注意：app_key 直接使用字符串格式
    app_key = 'gKF16OwACS2wSohu2KV2SqG4mrJ5eYOueWB793542rQai'

    # ==================== 执行 ====================
    try:
        # 生成 token 和认证头
        auth_header = build_auth_header(app_id, app_key, body_str)
        # 从认证头中提取token（如果需要单独使用）
        token = auth_header["Authorization"].split('token="')[1].rstrip('"')

        # 打印完整的请求信息
        print('=' * 80)
        print('完整请求信息:')
        print('=' * 80)
        print(f'{request_method} {request_path} HTTP/1.1')
        print('Accept: application/json')
        print('Content-Type: application/json; charset=UTF-8')
        print('Host: example.com:80')  # 根据实际主机修改
        print(f'Authorization: {auth_header["Authorization"]}')
        print('')
        print('Body:')
        print(body_str)
        print('')
        print('=' * 80)
        print('Token 生成信息:')
        print('=' * 80)
        print(f'Token: {token}')
        print(f'Authorization: {auth_header["Authorization"]}')
        print('')
        print('提示:')
        print('1. 确保请求路径和方法正确')
        print('2. 确保所有HTTP头正确设置')
        print('3. 确保发送的body与计算token时使用的完全一致')
        print('4. 确保AppID和AppKey正确无误')
    except Exception as e:
        print(f'错误: {e}')