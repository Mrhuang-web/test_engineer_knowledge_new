hex_raw = """
7B 22 69 70 22 3A 22 31 30 2E 31 32 2E 35 2E 31 34 32 22 2C 22 70 6F 72 74 22 3A 31 30 31 
31 35 2C 22 72 65 71 75 65 73 74 22 3A 6E 75 6C 6C 2C 22 72 65 73 70 6F 6E 73 65 22 3A 22 
46 46 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 33 31 33 32 33 34 33 31 33 32 33 33 
33 31 33 33 33 31 33 32 33 34 33 31 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 31 
30 31 32 37 30 30 30 30 30 31 30 30 32 32 30 30 37 45 30 30 30 30 38 31 31 30 38 31 31 30 
30 37 30 38 30 33 30 35 31 34 30 38 32 32 30 30 30 30 30 30 30 30 30 30 46 44 30 30 46 44 
30 30 46 44 30 30 46 44 30 30 46 44 30 30 46 44 30 30 46 44 30 30 30 30 30 30 30 30 30 30 
30 30 45 46 30 30 30 44 35 33 46 45 22 2C 22 74 61 73 6B 49 64 22 3A 6E 75 6C 6C 2C 22 64 
65 76 69 63 65 49 64 22 3A 6E 75 6C 6C 2C 22 73 74 61 74 75 73 22 3A 22 32 30 30 22 2C 22 
72 65 71 75 65 73 74 54 79 70 65 22 3A 6E 75 6C 6C 2C 22 73 64 6B 54 79 70 65 22 3A 6E 75 
6C 6C 2C 22 72 65 71 75 65 73 74 42 6F 64 79 22 3A 6E 75 6C 6C 2C 22 63 6F 6E 6E 65 63 74 
54 79 70 65 22 3A 6E 75 6C 6C 2C 22 73 74 61 72 74 54 69 6D 65 22 3A 6E 75 6C 6C 2C 22 65 
6E 64 54 69 6D 65 22 3A 6E 75 6C 6C 7D
"""

# 2. 清洗 + 解码
import json
hex_clean = hex_raw.replace(" ", "").replace("\n", "")
json_obj = json.loads(bytes.fromhex(hex_clean).decode("utf-8"))

# 3. 打印结果（PyCharm 控制台直接看）
print(json.dumps(json_obj, indent=2, ensure_ascii=False))








# 1. 把你要发回 Kafka 的 JSON 粘到下面三引号里，随便换行/缩进都行
json_raw = """
{
  "fsuID": "00441006000000200120",
  "deviceList": [
    {
      "deviceID": "00441006000000200123",
      "signIDs": null
    }
  ],
  "focusRefresh": false
}
"""

# 2. 压缩成紧凑 JSON（去掉多余空白）
import json, textwrap
json_compact = json.dumps(json.loads(json_raw), separators=(',', ':'))

# 3. 转十六进制并大写显示
hex_str = json_compact.encode('utf-8').hex().upper()

# 4. 控制台输出：一整行 + 每 32 字节换行（方便复制）
print("One-line hex:")
print(hex_str)
print("\n32-byte wrap:")
print(textwrap.fill(hex_str, width=64))
