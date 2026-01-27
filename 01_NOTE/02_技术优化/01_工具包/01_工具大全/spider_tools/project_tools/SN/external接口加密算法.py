import hashlib
import hmac
import json
import requests

def generate_token_ultimate(appkey: str, data: dict) -> tuple[str, str]:
    """
    终极版：完全按接口参数表生成请求体，逐字节对齐平台校验逻辑
    :param appkey: 平台分配的appkey
    :param data: 业务数据（data节点内容）
    :return: (原始JSON请求体字符串, 生成的token)
    """
    try:
        # 1. 构造请求体：根节点为data（严格匹配2.1.1接口参数表）
        request_body = {
            "data": data
        }

        # 2. 生成「无任何多余字符」的JSON字符串（关键中的关键）
        # ensure_ascii=False：不转义Base64和中文
        # separators=(',', ':')：去除所有逗号/冒号后的空格
        # indent=None：无缩进
        json_str = json.dumps(
            request_body,
            sort_keys=False,  # 不排序，保持你提供的字段顺序
            indent=None,
            ensure_ascii=False,
            separators=(',', ':')
        )

        # 3. 按文档3.1.3算法生成token
        # 步骤1：计算请求体的MD5字节数组（Content-MD5-Str）
        md5_obj = hashlib.md5()
        md5_obj.update(json_str.encode('utf-8'))  # 文档要求UTF-8编码
        sign_bytes = md5_obj.digest()

        # 步骤2：HMAC-SHA-256加密（appkey为密钥）
        appkey_bytes = appkey.encode('utf-8')
        hmac_obj = hmac.new(appkey_bytes, sign_bytes, hashlib.sha256)
        hmac_bytes = hmac_obj.digest()

        # 步骤3：Base16编码（大写16进制）
        token = hmac_bytes.hex().upper()

        # 输出关键信息（用于核对）
        print(f"=== 最终校验信息 ===")
        print(f"1. 实际发送的JSON请求体（无空格无缩进）：\n{json_str}")
        print(f"\n2. Content-MD5（16进制大写）：\n{md5_obj.hexdigest().upper()}")
        print(f"\n3. 生成的token：\n{token}")
        return json_str, token
    except Exception as e:
        raise Exception(f"token生成失败：{str(e)}")

# ------------------- 你的实际数据+请求逻辑（直接运行） -------------------
if __name__ == "__main__":
    # 你的业务数据（原样传入，无修改）
    business_data = {
        "workOrdNum": "123",
        "name": "test001",
        "account": "1233",
        "phone": "142523",
        "city": "咸阳市",
        "site": ["安康白河庆华化工厂站点"],
        "room": ["咸阳秦都应急楼一楼综合机房"],
        "deviceIdList": ["ad8c7a55-362e-4b58-8644-b6e9169e1439"],
        "picture": "X05baHXRzipDdXP368CxaPqjrcaffWOpLgZa1uElj/Na9w8FXVvYRxj/R1873xiv5q9I+I",
        "startDate": "2026-01-26",
        "endDate": "2026-12-31"
    }

    # 你的配置信息（必须替换为实际值）
    appkey = "gKF16OwACS2wSohu2KV2SqG4mrJ5eYOueWB793542rQai"
    appid = "lbVGV48llz7EEa2RbWqcbAUtAX37mB"  # 平台分配的appid（必填，不能错）
    server_root = "10.12.7.177:30506"  # 平台提供的服务器地址（如112.4.17.144:8080）
    url = f"http://{server_root}/v1/external/ywgl/addFace"

    # 生成JSON请求体和token
    json_str, token = generate_token_ultimate(appkey, business_data)

    # 构造请求头（完全按文档3.2.1要求）
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": f'appid="{appid}",token="{token}"'
    }

    # 发送请求（使用requests库，避免手动构造请求的格式错误）
    try:
        print(f"\n=== 发送请求 ===")
        print(f"URL：{url}")
        print(f"请求头：{headers}")
        response = requests.post(
            url=url,
            headers=headers,
            data=json_str.encode('utf-8'),  # 直接使用原始JSON字符串编码，不二次序列化
            verify=False  # 如果是http协议，关闭SSL验证（https需开启）
        )

        # 输出响应结果
        print(f"\n响应状态码：{response.status_code}")
        print(f"响应头：{dict(response.headers)}")
        print(f"响应体：{response.text}")
    except Exception as e:
        print(f"\n请求发送失败：{str(e)}")