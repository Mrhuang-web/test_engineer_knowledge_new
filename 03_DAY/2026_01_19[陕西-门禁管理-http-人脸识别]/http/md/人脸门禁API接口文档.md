# 人脸门禁API接口文档

## 1. 基本信息

### 1.1 接口规范
- 接口根地址：http://设备IP地址:8090/
- 接口形式：HTTP请求
- 接口安全：所有接口需传入pass参数校验（设备初始无密码，需先调用setPassWord接口设置密码）
- 请求头：Content-Type: application/x-www-form-urlencoded
- 参数传递：所有请求参数均需通过请求body传递，不支持查询参数（GET请求也需从body获取参数）

### 1.2 接口返回格式
所有接口返回包含5个基本字段，业务数据通过data字段返回：
```json
{
  "result": 1,
  "success": true,
  "msg": "操作成功",
  "code": "LAN_SUS-0",
  "data": "业务数据"
}
```

## 2. 设备管理类接口

### 2.1 设置设备密码
- **请求方式**：POST
- **请求URL**：/setPassWord
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | oldPass | String | Y | 旧密码 |
  | newPass | String | Y | 新密码 |
- **特殊说明**：
  - 设备初始无密码，首次设置时oldPass和newPass必须相同
  - 设备已有密码时，oldPass必须匹配当前密码才能修改
- **curl示例**：
  - 首次设置密码：
```bash
curl -X POST "http://127.0.0.1:8090/setPassWord" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "oldPass=test1234&newPass=test1234"
```
  - 修改密码：
```bash
curl -X POST "http://127.0.0.1:8090/setPassWord" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "oldPass=old1234&newPass=new1234"
```

### 2.2 设备信息查询
- **请求方式**：GET
- **请求URL**：/device/information
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
- **curl示例**：
```bash
curl -X GET "http://127.0.0.1:8090/device/information" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678"
```

### 2.3 设置设备时间
- **请求方式**：POST
- **请求URL**：/setTime
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | timestamp | String | Y | Unix毫秒级时间戳 |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/setTime" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&timestamp=1737273600000"
```

### 2.4 语言切换
- **请求方式**：POST
- **请求URL**：/device/setLanguage
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | languageType | String | Y | 语言类型（zh_CN：中文简体，en：英文） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/device/setLanguage" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&languageType=en"
```

### 2.5 设置时区
- **请求方式**：POST
- **请求URL**：/device/setTimeZone
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | timeZone | String | Y | 时区（默认：Asia/Shanghai） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/device/setTimeZone" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&timeZone=Asia/Shanghai"
```

### 2.6 设备重启
- **请求方式**：POST
- **请求URL**：/restartDevice
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/restartDevice" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678"
```

### 2.7 识别回调
- **请求方式**：POST
- **请求URL**：/setIdentifyCallBack
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | callbackUrl | String | Y | 回调地址 |
  | base64Enable | Int | N | 现场照base64开关（1关，2开，默认1） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/setIdentifyCallBack" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&callbackUrl=http://your-server/callback&base64Enable=1"
```

### 2.8 注册照片回调
- **请求方式**：POST
- **请求URL**：/setImgRegCallBack
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | url | String | Y | 回调地址 |
  | base64Enable | Int | N | 现场照base64开关（1关，2开，默认1） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/setImgRegCallBack" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&url=http://your-server/callback&base64Enable=1"
```

### 2.9 远程控制输出
- **请求方式**：POST
- **请求URL**：/device/openDoorControl
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | type | Int | N | 设备交互类型（1：开门，默认1） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/device/openDoorControl" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&type=1"
```

### 2.10 获取门磁状态
- **请求方式**：GET
- **请求URL**：/getDoorSensor
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
- **curl示例**：
```bash
curl -X GET "http://127.0.0.1:8090/getDoorSensor" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678"
```

### 2.11 事件回调
- **请求方式**：POST
- **请求URL**：/device/eventCallBack
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | url | String | Y | 回调地址 |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/device/eventCallBack" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&url=http://your-server/callback"
```

### 2.12 重置设备
- **请求方式**：POST
- **请求URL**：/resetDevice
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
- **功能说明**：重置设备到初始状态，包括清空密码、人员数据、照片数据和记录数据
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/resetDevice" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678"
```

### 2.13 获取设备状态
- **请求方式**：GET
- **请求URL**：/device/status
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
- **返回数据说明**：
  | 字段 | 类型 | 说明 |
  | --- | --- | --- |
  | is_first_setup | Boolean | 是否首次设置 |
  | reset_count | Int | 重置次数 |
  | last_reset_time | String | 最后重置时间 |
- **curl示例**：
```bash
curl -X GET "http://127.0.0.1:8090/device/status" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678"
```

## 3. 人员管理类接口

### 3.1 人员注册
- **请求方式**：POST
- **请求URL**：/person/create
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | person | String | Y | 人员信息JSON字符串 |
- **person参数格式**：
```json
{
  "name": "张三",
  "idcardNum": "123456789012345678"
}
```
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/person/create" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&person=%7B%22name%22%3A%22张三%22%2C%22idcardNum%22%3A%22123456789012345678%22%7D"
```

### 3.2 人员删除
- **请求方式**：POST
- **请求URL**：/person/delete
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | id | String | Y | 人员ID（-1删除所有） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/person/delete" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&id=PERSON_ID"
```

### 3.3 人员更新
- **请求方式**：POST
- **请求URL**：/person/update
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | person | String | Y | 人员信息JSON字符串（包含id和name） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/person/update" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&person=%7B%22id%22%3A%22PERSON_ID%22%2C%22name%22%3A%22张三更新%22%2C%22idcardNum%22%3A%22123456789012345678%22%7D"
```

### 3.4 人员查询
- **请求方式**：GET
- **请求URL**：/person/find
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | id | String | Y | 人员ID（-1查询所有） |
- **curl示例**：
```bash
curl -X GET "http://127.0.0.1:8090/person/find" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&id=-1"
```

### 3.5 人员分页查询
- **请求方式**：GET
- **请求URL**：/person/findByPage
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | personId | String | Y | 人员ID（-1查询所有） |
  | length | Int | N | 每页最大数量（默认1000） |
  | index | Int | N | 页码（从0开始） |
- **curl示例**：
```bash
curl -X GET "http://127.0.0.1:8090/person/findByPage" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&personId=-1&length=10&index=0"
```

## 4. 照片管理类接口

### 4.1 照片注册
- **请求方式**：POST
- **请求URL**：/face/create
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | personId | String | Y | 人员ID |
  | faceId | String | N | 照片ID（空值自动生成） |
  | imgBase64 | String | Y | 照片base64编码（不含头部） |
  | isEasyWay | Boolean | N | 检测方式（false严格，true宽松，默认false） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/create" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&personId=PERSON_ID&imgBase64=BASE64_IMAGE_DATA&isEasyWay=false"
```

### 4.2 照片删除
- **请求方式**：POST
- **请求URL**：/face/delete
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | faceId | String | Y | 照片ID |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/delete" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&faceId=FACE_ID"
```

### 4.3 照片查询
- **请求方式**：POST
- **请求URL**：/face/find
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | personId | String | Y | 人员ID |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/find" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&personId=PERSON_ID"
```

### 4.4 拍照注册
- **请求方式**：POST
- **请求URL**：/face/takeImg
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | personId | String | Y | 人员ID |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/takeImg" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&personId=PERSON_ID"
```

### 4.5 清空人员注册照片
- **请求方式**：POST
- **请求URL**：/face/deletePerson
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | personId | String | Y | 人员ID |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/deletePerson" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&personId=PERSON_ID"
```

## 5. 识别记录接口

### 5.1 识别记录查询
- **请求方式**：GET
- **请求URL**：/newFindRecords
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | personId | String | Y | 人员ID（-1查所有） |
  | startTime | String | Y | 开始时间（0不按时间） |
  | endTime | String | Y | 结束时间 |
  | length | Int | N | 每页最大数量（默认1000） |
  | model | Int | N | 记录类型（-1所有，默认-1） |
  | order | String | N | 排序方式（1升序，其他降序） |
  | index | Int | N | 页码（从0开始） |
- **curl示例**：
```bash
curl -X GET "http://127.0.0.1:8090/newFindRecords" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&personId=-1&startTime=0&endTime=9999-12-31%2023:59:59&length=10&index=0"
```

### 5.2 识别记录删除
- **请求方式**：POST
- **请求URL**：/newDeleteRecords
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | personId | String | Y | 人员ID（-1删所有） |
  | startTime | String | Y | 开始时间 |
  | endTime | String | Y | 结束时间 |
  | model | Int | N | 记录类型（-1所有，默认-1） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/newDeleteRecords" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&personId=-1&startTime=0&endTime=9999-12-31%2023:59:59&model=-1"
```

### 5.3 模拟识别
- **请求方式**：POST
- **请求URL**：/simulateIdentify
- **参数说明**：
  | 参数名 | 类型 | 必传 | 说明 |
  | --- | --- | --- | --- |
  | pass | String | Y | 设备密码 |
  | personId | String | N | 人员ID（留空模拟陌生人） |
- **curl示例**：
```bash
curl -X POST "http://127.0.0.1:8090/simulateIdentify" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678&personId=PERSON_ID"
```

## 3. 使用说明

1. 将curl命令复制到Apifox的导入功能中，即可快速创建接口
2. 接口默认密码：12345678，可通过setPassWord接口修改
3. 所有POST请求均使用application/x-www-form-urlencoded格式
4. JSON参数需进行URL编码
5. 照片base64编码需去掉头部（如data:image/jpeg;base64,）

## 4. 常见错误码

| 错误码 | 说明 |
| --- | --- |
| LAN_SUS-0 | 操作成功 |
| LAN_EXP-1001 | 密码错误 |
| LAN_EXP-1003 | 未设置设备密码 |
| LAN_EXP-1004 | 设备已禁用 |
| LAN_EXP-2001 | oldPass参数异常 |
| LAN_EXP-3004 | name参数不能为空 |
| LAN_EXP-4008 | imgBase64不能为空 |
| LAN_EXP-8006 | 未检测到面部 |
