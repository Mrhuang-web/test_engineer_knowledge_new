# 人脸门禁一体机接口调用示例（curl）

## 一、基础说明
- 接口根地址：http://设备IP地址:8090/
- 所有POST请求使用`application/x-www-form-urlencoded`格式
- 除设置密码接口外，其他所有接口需传入`pass`参数进行密码验证
- 默认密码：12345678
- **自动生成ID**：人员注册和照片注册时，如果未提供ID，系统会自动生成唯一ID
- **数据存储**：所有数据以JSON格式持久化存储在`data`目录下
- **日志记录**：系统操作日志记录在`logs`目录下，便于问题排查

## 二、设备管理类接口

### 2.1 设置设备密码
```bash
curl -X POST "http://localhost:8090/setPassWord" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "oldPass=12345678" \
  -d "newPass=newpassword123"
```

### 2.2 设备信息查询
```bash
curl -X GET "http://localhost:8090/device/information?pass=12345678" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### 2.3 远程开门
```bash
curl -X POST "http://localhost:8090/device/openDoorControl" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "type=1"
```

### 2.4 获取门磁状态
```bash
curl -X GET "http://localhost:8090/getDoorSensor?pass=12345678" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### 2.5 设置识别回调
```bash
curl -X POST "http://localhost:8090/setIdentifyCallBack" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "callbackUrl=http://your-server.com/callback" \
  -d "base64Enable=1"
```

### 2.6 设备重启
```bash
curl -X POST "http://localhost:8090/restartDevice" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678"
```

## 三、人员管理类接口

### 3.1 人员注册

#### 示例1：指定人员ID
```bash
curl -X POST "http://localhost:8090/person/create" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "person={\"id\":\"person001\",\"name\":\"张三\",\"idcardNum\":\"110101199001011234\"}"
```

#### 示例2：自动生成人员ID
```bash
curl -X POST "http://localhost:8090/person/create" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "person={\"name\":\"李四\",\"idcardNum\":\"110101199001011235\"}"
```

### 3.2 人员删除
```bash
# 删除单个人员
curl -X POST "http://localhost:8090/person/delete" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "id=person001"

# 删除所有人员
curl -X POST "http://localhost:8090/person/delete" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "id=-1"
```

### 3.3 人员更新
```bash
curl -X POST "http://localhost:8090/person/update" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "person={\"id\":\"person001\",\"name\":\"李四\",\"idcardNum\":\"110101199001011234\"}"
```

### 3.4 人员查询
```bash
# 查询单个人员
curl -X GET "http://localhost:8090/person/find?pass=12345678&id=person001" \
  -H "Content-Type: application/x-www-form-urlencoded"

# 查询所有人员
curl -X GET "http://localhost:8090/person/find?pass=12345678&id=-1" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### 3.5 人员分页查询
```bash
curl -X GET "http://localhost:8090/person/findByPage?pass=12345678&personId=-1&length=10&index=0" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

## 四、照片管理类接口

### 4.1 照片注册

#### 示例1：指定照片ID
```bash
curl -X POST "http://localhost:8090/face/create" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "personId=person001" \
  -d "faceId=face001" \
  -d "imgBase64=SGVsbG8sIFdvcmxkIQ==" \
  -d "isEasyWay=false"
```

#### 示例2：自动生成照片ID
```bash
curl -X POST "http://localhost:8090/face/create" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "personId=person001" \
  -d "imgBase64=SGVsbG8sIFdvcmxkIQ==" \
  -d "isEasyWay=true"
```

### 4.2 照片删除
```bash
curl -X POST "http://localhost:8090/face/delete" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "faceId=face001"
```

### 4.3 照片更新
```bash
curl -X POST "http://localhost:8090/face/update" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "personId=person001" \
  -d "faceId=face001" \
  -d "imgBase64=V29ybGQh" \
  -d "isEasyWay=true"
```

### 4.4 照片查询
```bash
curl -X POST "http://localhost:8090/face/find" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "personId=person001"
```

### 4.5 拍照注册
```bash
curl -X POST "http://localhost:8090/face/takeImg" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "personId=person001"
```

### 4.6 清空人员注册照片
```bash
curl -X POST "http://localhost:8090/face/deletePerson" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "personId=person001"
```

## 五、识别记录类接口

### 5.1 识别记录查询
```bash
curl -X GET "http://localhost:8090/newFindRecords?pass=12345678&personId=-1&startTime=0&endTime=9999-12-31 23:59:59" \
  -H "Content-Type: application/x-www-form-urlencoded"
```

### 5.2 识别记录删除
```bash
curl -X POST "http://localhost:8090/newDeleteRecords" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "pass=12345678" \
  -d "personId=-1" \
  -d "startTime=2023-01-01 00:00:00" \
  -d "endTime=2023-12-31 23:59:59" \
  -d "model=-1"
```

## 六、返回格式说明

所有接口返回包含4个基本字段，业务数据通过data字段返回：

```json
{
  "result": 1,      // 1成功，0失败
  "success": true,  // true成功，false失败
  "msg": "操作成功", // 返回信息
  "code": "LAN_SUS-0", // 返回码
  "data": {}       // 业务数据
}
```

## 七、常见返回码

| 返回码 | 说明 |
| --- | --- |
| LAN_SUS-0 | 操作成功 |
| LAN_EXP-1001 | 密码错误 |
| LAN_EXP-1003 | 未设置设备密码 |
| LAN_EXP-2001 | oldPass参数异常 |
| LAN_EXP-3004 | name参数不能为空 |
| LAN_EXP-4008 | imgBase64不能为空 |
| LAN_EXP-8006 | 未检测到面部 |

## 八、使用说明

1. **启动Mock Server**：
   ```bash
   python mockserver.py
   ```
   默认监听端口：8090

2. **修改端口**：
   ```bash
   python mockserver.py 8080
   ```
   或修改代码中的`run_server(port=8090)`为所需端口

3. **部署到服务器**：
   - 将`mockserver.py`文件上传到服务器
   - 确保服务器已安装Python 3
   - 使用后台运行命令：
     ```bash
     nohup python3 mockserver.py > mockserver.log 2>&1 &
     ```

4. **查看日志**：
   ```bash
   tail -f mockserver.log
   ```

5. **停止服务**：
   ```bash
   ps aux | grep mockserver.py
   kill <进程ID>
   ```

## 九、注意事项

1. 所有POST请求参数必须放在body中，使用`application/x-www-form-urlencoded`格式
2. 除设置密码接口外，其他所有接口必须传入`pass`参数
3. 人员注册时，`person`参数为JSON格式字符串
4. 照片注册时，`imgBase64`参数为不含头部的base64编码
5. 同一设备接口不可同时被多个客户端调用
6. 设备重启接口仅返回成功消息，不会实际重启服务器
7. 拍照注册接口仅返回成功消息，不会实际调用摄像头

## 十、主要功能测试流程

### 测试远程开关功能
1. 使用设置密码接口修改默认密码
2. 使用远程开门接口测试开门功能
3. 使用获取门磁状态接口查看门磁状态

### 测试人员管理功能
1. 使用人员注册接口添加人员
2. 使用人员查询接口验证人员已添加
3. 使用人员更新接口修改人员信息
4. 使用人员查询接口验证信息已更新
5. 使用人员删除接口删除人员
6. 使用人员查询接口验证人员已删除

### 测试照片注册功能
1. 先添加一个人员
2. 使用照片注册接口添加照片
3. 使用照片查询接口验证照片已添加
4. 使用照片更新接口修改照片
5. 使用照片查询接口验证照片已更新
6. 使用照片删除接口删除照片
7. 使用照片查询接口验证照片已删除

## 十一、数据存储说明

Mock Server使用内存存储数据，重启服务后数据会丢失。主要存储以下数据：

- 设备密码
- 人员信息
- 照片信息
- 识别记录
- 回调地址
- 门磁状态

如需持久化存储，可自行修改`DataStore`类，添加文件或数据库存储功能。