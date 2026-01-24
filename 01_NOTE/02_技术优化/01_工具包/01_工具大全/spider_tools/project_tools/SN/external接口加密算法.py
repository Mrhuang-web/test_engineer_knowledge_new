# -*- coding: utf-8 -*-
# Copyright (c) 2025 HuangJiaJie
# 许可证：xxx

import hashlib
import hmac
import binascii

# ---------- 1. 计算 Content-MD5-Str ----------
def content_md5(body: bytes) -> bytes:
    """
    对请求体做 MD5，返回 16 字节的摘要（byte[]，带不可见字符）。
    GET 请求无 body 时，可把 b'' 传进来，得到的是 MD5(b'') 的结果。
    """
    return hashlib.md5(body).digest()          # 注意是 digest() 不是 hexdigest()

# ---------- 2. HMAC-SHA-256 ----------
def hmac_sha256(key: bytes, msg: bytes) -> bytes:
    """
    用 appkey 做 key，对 MD5 结果再做 HMAC-SHA-256，返回 32 字节 byte[]。
    """
    return hmac.new(key, msg, hashlib.sha256).digest()

# ---------- 3. Base16 编码 ----------
def base16_encode(data: bytes) -> str:
    """
    把不可见字节流转成可见 16 进制字符串，字母大写，无分隔符。
    这就是最终要放到 HTTP 头里的 oken。
    """
    return binascii.b2a_hex(data).decode('ascii').upper()

# ---------- 4. 一条龙封装 ----------
def calc_token(appkey: str, body: bytes = b'') -> str:
    """
    给定 appkey 和请求体，返回最终 token。
    GET 请求直接不给 body 即可。
    """
    sign_bytes = content_md5(body)             # 步骤1
    hmac_bytes = hmac_sha256(appkey.encode('utf-8'), sign_bytes)  # 步骤2
    token      = base16_encode(hmac_bytes)     # 步骤3
    return token

# ---------- 5. 演示 ----------
if __name__ == '__main__':
    json_raw = """
        {
         "data":{
            "workOrdNum": "JF-20251222-0313",
            "name": "唐建峰",
            "account": "tangjianfeng",
            "phone": "13800001111",
            "city": "咸阳市",
            "site": ["安康白河庆华化工厂站点"],
            "room": ["咸阳秦都应急楼一楼综合机房"],
            "deviceId": ["20231201996901"],
            "picture": "单张图片的base64字符串",
            "startDate": "2025-12-26",
        }
        }    
    """
    post_body = json_raw.encode('utf-8')
    appkey = 'gKF16OwACS2wSohu2KV2SqG4mrJ5eYOueWB793542rQai'

    # 把每一步都打印出来，方便对照
    md5_val  = content_md5(post_body)
    hmac_val = hmac_sha256(appkey.encode(), md5_val)
    token    = base16_encode(hmac_val)

    print('1. 请求体 bytes        :', post_body)
    print('2. MD5 结果(16 字节)   :', md5_val)
    print('3. MD16 可见形式       :', md5_val.hex().upper())
    print('4. HMAC-SHA256 结果    :', hmac_val)
    print('5. Base16 最终 token   :', token)

    # 一行函数直接算
    print('6. 一条龙结果          :', calc_token(appkey, post_body))