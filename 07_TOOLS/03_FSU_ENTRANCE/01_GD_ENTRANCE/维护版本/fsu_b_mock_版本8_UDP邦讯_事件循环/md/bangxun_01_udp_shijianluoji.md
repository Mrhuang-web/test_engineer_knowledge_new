## 邦讯108D事件时间转换完整流程

### 1. 时间格式说明

邦讯108D指令使用**压缩时间格式**来编码事件发生时间，总共32位（4字节），按**小端序（Little-Endian）**排列。

#### 1.1 时间字段结构

| 字节位置 | 长度 | 含义 | 位分布 |
|---------|------|------|--------|
| 0 | 1字节 | 年月日低位 | 年月日的低8位 |
| 1 | 1字节 | 年月日高位 | 年月日的高8位 |
| 2 | 1字节 | 时分秒低位 | 时分秒的低8位 |
| 3 | 1字节 | 时分秒高位 | 时分秒的高8位 |

#### 1.2 编码规则

- **年月日（16位）**：
  - Year: 7位 (0-119，相对于2000年)
  - Month: 4位 (1-12)
  - Day: 5位 (1-31)
  - 计算公式：`ymd = (year << 9) | (month << 5) | day`

- **时分秒（16位）**：
  - Hours: 5位 (0-23)
  - Minutes: 6位 (0-59)
  - Seconds: 5位 (0-29，以2秒为增量)
  - 计算公式：`hms = (hour << 11) | (minute << 5) | (second // 2)`

### 2. 编码流程（设备端）

#### 2.1 时间获取

1. 获取当前系统时间
2. 提取年、月、日、时、分、秒
3. 计算相对年份：`year = 当前年份 - 2000`

#### 2.2 时间编码

1. **编码年月日**：
   ```python
   ymd = (year << 9) | (month << 5) | day
   ```

2. **编码时分秒**：
   ```python
   hms = (hour << 11) | (minute << 5) | (second // 2)
   ```

3. **转换为小端序字节**：
   ```python
   # 年月日：低位字节在前
   ymd_low = ymd & 0xFF
   ymd_high = (ymd >> 8) & 0xFF
   # 时分秒：低位字节在前
   hms_low = hms & 0xFF
   hms_high = (hms >> 8) & 0xFF
   # 构建时间戳字节
   time_bytes = bytes([ymd_low, ymd_high, hms_low, hms_high])
   ```

#### 2.3 数据组装

1. 108D响应结构：
   - data_frame_type(2字节) + card_id(2字节) + vendor_id(1字节) + status(1字节) + 时间戳(4字节) + 填充

2. 时间戳位置：第6-9字节（从0开始计数）

### 3. 解码流程（服务端）

#### 3.1 数据提取

1. 从108D响应数据包中提取时间戳字段（4字节）
2. 按照小端序读取字节

#### 3.2 时间解码

1. **提取年月日和时分秒**：
   ```python
   # 假设时间戳字节为：[ymd_low, ymd_high, hms_low, hms_high]
   ymd = (ymd_high << 8) | ymd_low
   hms = (hms_high << 8) | hms_low
   ```

2. **解码年月日**：
   ```python
   year = (ymd >> 9) & 0x7F  # 7位
   month = (ymd >> 5) & 0x0F  # 4位
   day = ymd & 0x1F  # 5位
   actual_year = year + 2000  # 转换为实际年份
   ```

3. **解码时分秒**：
   ```python
   hour = (hms >> 11) & 0x1F  # 5位
   minute = (hms >> 5) & 0x3F  # 6位
   second = (hms & 0x1F) * 2  # 5位，转换为实际秒数
   ```

#### 3.3 时间格式化

将解码后的时间转换为标准格式：
```python
formatted_time = f"{actual_year}-{month:02d}-{day:02d} {hour:02d}:{minute:02d}:{second:02d}"
```

### 4. 配置说明

#### 4.1 配置文件修改

在 `config/bangsun_old/bangsun_old.json` 文件中，108D指令的响应配置需要设置为：

```json
{
    "name": "timestamp",
    "length": 4,
    "endian": "big",
    "type": "hex",
    "value": ""
}
```

**注意**：endian必须设置为"big"，否则解码时会得到错误的字节顺序。

#### 4.2 编码逻辑位置

时间编码逻辑位于 `codec/through_data_codec.py` 文件中的 `encode` 方法，针对108D指令的特殊处理部分。

### 5. 示例

#### 5.1 编码示例

假设当前时间为：2026-02-01 02:27:43

1. 计算相对年份：2026 - 2000 = 26
2. 编码年月日：
   ```python
   ymd = (26 << 9) | (2 << 5) | 1 = 0x3441
   ```
3. 编码时分秒：
   ```python
   hms = (2 << 11) | (27 << 5) | (43 // 2) = 0x1375
   ```
4. 转换为小端序字节：
   ```python
   time_bytes = bytes([0x41, 0x34, 0x75, 0x13])  # 41 34 75 13
   ```

#### 5.2 解码示例

假设收到的时间戳字节为：41 34 75 13

1. 提取年月日和时分秒：
   ```python
   ymd = (0x34 << 8) | 0x41 = 0x3441
   hms = (0x13 << 8) | 0x75 = 0x1375
   ```
2. 解码年月日：
   ```python
   year = (0x3441 >> 9) & 0x7F = 26
   month = (0x3441 >> 5) & 0x0F = 2
   day = 0x3441 & 0x1F = 1
   actual_year = 26 + 2000 = 2026
   ```
3. 解码时分秒：
   ```python
   hour = (0x1375 >> 11) & 0x1F = 2
   minute = (0x1375 >> 5) & 0x3F = 27
   second = (0x1375 & 0x1F) * 2 = 43
   ```
4. 格式化时间：2026-02-01 02:27:43

### 6. 常见问题及解决方案

#### 6.1 时间解析错误

**问题**：服务端解析时间为2000-09-06 02:33:03

**原因**：
1. 时间戳字段的endian设置错误
2. 编码逻辑不符合协议规范

**解决方案**：
1. 确保配置文件中timestamp字段的endian设置为"big"
2. 按照协议规范实现编码逻辑

#### 6.2 时间戳字节顺序问题

**问题**：时间戳字节顺序不正确

**原因**：小端序理解错误

**解决方案**：
- 编码时：年月日和时分秒都要按照低位字节在前的顺序
- 解码时：需要正确组合高低字节

### 7. 代码实现参考

#### 7.1 编码实现

```python
# 编码年月日（16位）：Year(7 bits) + Month(4 bits) + Day(5 bits)
ymd = (year << 9) | (month << 5) | day
# 编码时分秒（16位）：Hours(5 bits) + Minutes(6 bits) + 2-second increments(5 bits)
hms = (hour << 11) | (minute << 5) | (second // 2)

# 转换为4字节，低位在前（小端序）
ymd_low = ymd & 0xFF
ymd_high = (ymd >> 8) & 0xFF
hms_low = hms & 0xFF
hms_high = (hms >> 8) & 0xFF

# 构建时间戳字节：[ymd_low, ymd_high, hms_low, hms_high]
time_bytes = bytes([ymd_low, ymd_high, hms_low, hms_high])
```

#### 7.2 解码实现

```python
# 假设time_bytes为4字节的时间戳
ymd_low, ymd_high, hms_low, hms_high = time_bytes

# 组合年月日和时分秒
ymd = (ymd_high << 8) | ymd_low
hms = (hms_high << 8) | hms_low

# 解码年月日
year = (ymd >> 9) & 0x7F
month = (ymd >> 5) & 0x0F
day = ymd & 0x1F
actual_year = year + 2000

# 解码时分秒
hour = (hms >> 11) & 0x1F
minute = (hms >> 5) & 0x3F
second = (hms & 0x1F) * 2
```

### 8. 总结

邦讯108D事件时间转换采用了压缩时间格式，通过位运算实现了高效的时间存储。正确理解和实现这一格式对于确保设备和服务端之间的时间同步至关重要。

**关键点**：
- 小端序字节排列
- 压缩时间格式的位分布
- 正确的编码和解码逻辑
- 配置文件的正确设置

通过本文档的指导，开发者应该能够正确实现邦讯108D事件的时间转换功能。