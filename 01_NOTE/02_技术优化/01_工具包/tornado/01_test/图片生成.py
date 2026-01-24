from PIL import Image
import os

# 1. 创建一个新图像（纯色）
width, height = 5000, 5000  # 大分辨率
image = Image.new('RGB', (width, height), color='red')  # 创建纯红色图片

# 2. 或者打开一个现有图像
# image = Image.open("input.jpg")

# target_size_kb = 1024  # 目标文件大小：1024 KB (1MB)
target_size_kb = 521000  # 目标文件大小：1024 KB (1MB)
quality = 1000  # 初始质量

# 循环调整质量直到文件大小接近目标
while True:
    # 保存为JPEG，并设置质量
    image.save("output.jpg", "JPEG", quality=quality)

    # 获取当前文件大小（字节）
    current_size = os.path.getsize("output.jpg")
    current_size_kb = current_size / 1024

    print(f"质量: {quality}%, 大小: {current_size_kb:.2f} KB")

    # 判断是否达到目标
    if current_size_kb > target_size_kb:
        quality -= 5  # 如果太大，降低质量
    else:
        break  # 达到目标，退出循环

    if quality < 5:  # 防止质量过低
        break

print(f"完成！最终质量: {quality}%， 最终大小: {current_size_kb:.2f} KB")