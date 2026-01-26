#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
动环平台双向认证 Token 生成脚本（针对指定 body）
"""
import hashlib
import hmac
import json

def base16_encode(data: bytes) -> str:
    return data.hex().upper()

def build_token(app_key: str, body: str = '') -> str:
    md5_hash = hashlib.md5(body.encode('utf-8')).digest()
    if isinstance(app_key, str):
        app_key_bytes = bytes.fromhex(app_key)
    else:
        app_key_bytes = app_key
    hmac_result = hmac.new(app_key_bytes, md5_hash, hashlib.sha256).digest()
    return base16_encode(hmac_result)

def build_auth_header(app_id: str, app_key: str, body: str = '') -> dict:
    token = build_token(app_key, body)
    return {'Authorization': f'appid="{app_id}",token="{token}"'}

if __name__ == '__main__':
    # 你的真实 body（注意保持空格/换行一致，建议直接 dumps 生成）
    payload = {
        "data": {
            "workOrdNum": "123",
            "name": "huangjiajie",
            "account": "huangjiajie",
            "phone": "13800001111",
            "city": "咸阳市",
            "site": ["安康白河庆华化工厂站点"],
            "room": ["咸阳秦都应急楼一楼综合机房"],
            "deviceIdList": ["ad8c7a55-362e-4b58-8644-b6e9169e1439"],
            "picture": "123",
            "startDate": "2025-12-26"
        }
    }
    body_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)

    # 替换为你自己的 app_id & app_key
    app_id  = '350000100020003'
    app_key = '0123456789ABCDEF0123456789ABCDEF'   # 64 字符示例

    token = build_token(app_key, body_str)
    auth  = build_auth_header(app_id, app_key, body_str)

    print('Token:', token)
    print('Authorization:', auth['Authorization'])