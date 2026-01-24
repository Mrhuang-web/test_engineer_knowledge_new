import base64
import os


def image_to_base64_file(image_path, output_file):
    """
    将图片转换为base64并保存到文件
    :param image_path: 图片路径
    :param output_file: 输出文件路径
    """
    try:
        # 读取图片并转换为base64
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        # 保存到文件
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(encoded_string)

        print(f"✅ 转换成功！base64已保存到: {output_file}")
        print(f"📊 原始图片大小: {os.path.getsize(image_path)} 字节")
        print(f"📊 base64字符串长度: {len(encoded_string)} 字符")
        return encoded_string

    except Exception as e:
        print(f"❌ 转换失败: {str(e)}")
        return None


# 使用示例
if __name__ == "__main__":
    # 输入图片路径
    image_path = r"C:\Users\Administrator\Desktop\尾缀\test.jpg"  # 替换为你的图片路径

    # 输出文件路径
    output_file = "image_base64.txt"

    # 执行转换
    base64_string = image_to_base64_file(image_path, output_file)

    if base64_string:
        # 显示前100个字符作为预览
        print(f"🔍 base64预览: {base64_string[:100]}...")