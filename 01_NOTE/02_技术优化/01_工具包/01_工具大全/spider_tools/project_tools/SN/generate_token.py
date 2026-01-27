import json
import hashlib
import hmac

# 定义两种数据结构
# 结构1：包含data字段的完整结构
full_data = {
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

# 结构2：只包含内部字段的结构
inner_data = {
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

# appkey
appkey = "gKF16OwACS2wSohu2KV2SqG4mrJ5eYOueWB793542rQai"

def generate_token(data, appkey):
    """生成token"""
    # 1. 将数据转换为JSON字符串（保持原始格式）
    json_str = json.dumps(data, ensure_ascii=False, separators=(',', ':'))
    print("请求报文:")
    print(json_str)
    
    # 2. 计算请求报文的MD5散列值（使用digest()获取字节数组）
    md5_hash = hashlib.md5(json_str.encode('utf-8')).digest()
    
    # 3. 以appkey作为密钥，对MD5散列值（字节数组）进行HMAC-SHA-256加密
    hmac_obj = hmac.new(appkey.encode('utf-8'), md5_hash, hashlib.sha256)
    hmac_result = hmac_obj.digest()
    
    # 4. 对加密结果（字节数组）进行Base16编码（大写）
    base16_str = hmac_result.hex().upper()
    
    return base16_str

if __name__ == "__main__":
    print("=== 使用完整结构（包含data字段）生成token ===")
    token_full = generate_token(full_data, appkey)
    print(f"最终生成的token: {token_full}")
    print(f"Authorization格式: appid=\"分配的appid\",token=\"{token_full}\"")
    
    print("\n=== 使用内部结构（不包含data字段）生成token ===")
    token_inner = generate_token(inner_data, appkey)
    print(f"最终生成的token: {token_inner}")
    print(f"Authorization格式: appid=\"分配的appid\",token=\"{token_inner}\"")
    
    print("\n=== 消息体选择说明 ===")
    print("消息体应选择与实际API请求中发送的JSON数据完全一致的结构")
    print("如果API要求发送包含data字段的完整结构，则使用full_data")
    print("如果API要求直接发送内部字段的结构，则使用inner_data")
    print("请根据API文档或实际请求格式选择正确的消息体结构")


