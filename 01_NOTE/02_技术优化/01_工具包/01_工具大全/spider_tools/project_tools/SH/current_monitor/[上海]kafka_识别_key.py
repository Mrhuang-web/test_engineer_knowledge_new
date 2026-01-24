# hex_tool.py
# 支持空格分隔的十六进制字符串，直接粘贴即可运行

def from_hex(hex_str: str) -> str:
    """十六进制（可含空格）→ 明文"""
    return bytes.fromhex(hex_str.replace(' ', '')).decode('utf-8')

def to_hex(plain_str: str) -> str:
    """明文 → 十六进制（无空格小写）"""
    return plain_str.encode('utf-8').hex()

# 你直接复制粘贴下面这一行即可测试
if __name__ == '__main__':
    # 示例：你复制进来的样子
    hex_with_spaces = "30 30 31 30 30 30 30 36 30 31 31 30 30 31 37 36 38 37 30 38"
    to_hexs = "00441006000000200120"
    print("你粘贴的原文：", hex_with_spaces)
    print("解码结果：   ", from_hex(hex_with_spaces))
    print("再编码回去： ", to_hex(from_hex(hex_with_spaces)))
    print("反编译：",to_hex(to_hexs))