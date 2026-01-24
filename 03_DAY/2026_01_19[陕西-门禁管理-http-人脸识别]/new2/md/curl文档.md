# 人脸门禁系统API接口curl调用文档

## 一、设备管理类接口

### 1. 设置设备密码
**接口描述**：设置或修改设备密码
**请求URL**：`http://设备IP:8090/setPassWord`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| oldPass | String | Y | 旧密码，初次设置时与newPass相同 |
| newPass | String | Y | 新密码 |

**curl命令示例**：
```bash
# 初次设置密码
curl -X POST "http://127.0.0.1:8090/setPassWord" \
  -d "oldPass=12345678" \
  -d "newPass=12345678"

# 修改密码
curl -X POST "http://127.0.0.1:8090/setPassWord" \
  -d "oldPass=12345678" \
  -d "newPass=87654321"
```

### 2. 获取设备信息
**接口描述**：查询设备的硬件信息、系统状态等
**请求URL**：`http://设备IP:8090/device/information`
**请求方式**：GET
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |

**curl命令示例**：
```bash
curl -X GET "http://127.0.0.1:8090/device/information" \
  -d "pass=12345678"
```

### 3. 远程控制开门
**接口描述**：远程控制设备开门
**请求URL**：`http://设备IP:8090/device/openDoorControl`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| type | Int | N | 设备交互类型，1为开门 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/device/openDoorControl" \
  -d "pass=12345678" \
  -d "type=1"
```

### 4. 获取门磁状态
**接口描述**：查询门磁当前状态
**请求URL**：`http://设备IP:8090/getDoorSensor`
**请求方式**：GET
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |

**curl命令示例**：
```bash
curl -X GET "http://127.0.0.1:8090/getDoorSensor" \
  -d "pass=12345678"
```

### 5. 设置设备时间
**接口描述**：设置设备的系统时间
**请求URL**：`http://设备IP:8090/setTime`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| timestamp | String | Y | 时间戳，格式：年-月-日 时:分:秒 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/setTime" \
  -d "pass=12345678" \
  -d "timestamp=2023-12-31 23:59:59"
```

### 6. 设置设备语言
**接口描述**：设置设备的显示语言
**请求URL**：`http://设备IP:8090/device/setLanguage`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| languageType | String | Y | 语言类型，如"ch"中文，"en"英文 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/device/setLanguage" \
  -d "pass=12345678" \
  -d "languageType=ch"
```

### 7. 设置设备时区
**接口描述**：设置设备的时区
**请求URL**：`http://设备IP:8090/device/setTimeZone`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| timeZone | String | Y | 时区，如"Asia/Shanghai" |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/device/setTimeZone" \
  -d "pass=12345678" \
  -d "timeZone=Asia/Shanghai"
```

### 8. 重启设备
**接口描述**：远程控制设备重启
**请求URL**：`http://设备IP:8090/restartDevice`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/restartDevice" \
  -d "pass=12345678"
```

### 9. 设置识别回调
**接口描述**：设置识别结果的回调URL
**请求URL**：`http://设备IP:8090/setIdentifyCallBack`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| callbackUrl | String | Y | 回调URL地址 |
| base64Enable | Int | N | 是否启用base64编码，0不启用，1启用 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/setIdentifyCallBack" \
  -d "pass=12345678" \
  -d "callbackUrl=http://example.com/callback" \
  -d "base64Enable=1"
```

### 10. 设置图片注册回调
**接口描述**：设置图片注册结果的回调URL
**请求URL**：`http://设备IP:8090/setImgRegCallBack`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| url | String | Y | 回调URL地址 |
| base64Enable | Int | N | 是否启用base64编码，0不启用，1启用 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/setImgRegCallBack" \
  -d "pass=12345678" \
  -d "url=http://example.com/imgcallback" \
  -d "base64Enable=0"
```

### 11. 设置信号输入
**接口描述**：设置设备的信号输入配置
**请求URL**：`http://设备IP:8090/device/setSignalInput`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| config | JSON | Y | 信号输入配置 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/device/setSignalInput" \
  -d "pass=12345678" \
  -d "config={\"signal1\":1,\"signal2\":0}"
```

### 12. 设置会议预警
**接口描述**：设置会议和门磁预警功能
**请求URL**：`http://设备IP:8090/meetAndWarnSet`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| meetEnable | Boolean | N | 会议模式启用，true启用，false禁用 |
| meetFreeTime | Int | N | 会议空闲时间，单位秒 |
| doorWarnEnable | Boolean | N | 门磁预警启用，true启用，false禁用 |
| doorCloseTime | Int | N | 门关闭时间，单位秒 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/meetAndWarnSet" \
  -d "pass=12345678" \
  -d "meetEnable=true" \
  -d "meetFreeTime=300" \
  -d "doorWarnEnable=true" \
  -d "doorCloseTime=60"
```

### 13. 设置卡片信息
**接口描述**：设置卡片读取和输出配置
**请求URL**：`http://设备IP:8090/cardInfoSet`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| readDataEnable | Boolean | Y | 是否启用数据读取 |
| readSector | Int | Y | 读取扇区 |
| readBlock | Int | Y | 读取块 |
| readShift | Int | Y | 读取偏移 |
| readKeyA | String | Y | 读取密钥A |
| wgOutType | Int | Y | WG输出类型 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/cardInfoSet" \
  -d "pass=12345678" \
  -d "readDataEnable=true" \
  -d "readSector=1" \
  -d "readBlock=2" \
  -d "readShift=0" \
  -d "readKeyA=FFFFFFFFFFFF" \
  -d "wgOutType=1"
```

### 14. 设置事件回调
**接口描述**：设置设备事件的回调URL
**请求URL**：`http://设备IP:8090/device/eventCallBack`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| url | String | Y | 回调URL地址 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/device/eventCallBack" \
  -d "pass=12345678" \
  -d "url=http://example.com/eventcallback"```

## 二、人员管理类接口

### 1. 人员注册
**接口描述**：添加人员信息到设备
**请求URL**：`http://设备IP:8090/person/create`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| person | JSON | Y | 人员信息集合 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/person/create" \
  -d "pass=12345678" \
  -d "person={\"id\":\"1001\",\"name\":\"张三\",\"idcardNum\":\"110101199001011234\"}"
```

### 2. 人员删除
**接口描述**：删除设备中的指定人员信息
**请求URL**：`http://设备IP:8090/person/delete`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| id | String | Y | 人员ID，-1删除所有人员 |

**curl命令示例**：
```bash
# 删除单个人员
curl -X POST "http://127.0.0.1:8090/person/delete" \
  -d "pass=12345678" \
  -d "id=1001"

# 删除所有人员
curl -X POST "http://127.0.0.1:8090/person/delete" \
  -d "pass=12345678" \
  -d "id=-1"
```

### 3. 人员更新
**接口描述**：更新设备中已存在人员的信息
**请求URL**：`http://设备IP:8090/person/update`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| person | JSON | Y | 人员信息集合，含id |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/person/update" \
  -d "pass=12345678" \
  -d "person={\"id\":\"1001\",\"name\":\"李四\",\"idcardNum\":\"110101199001011234\"}"
```

### 4. 人员查询
**接口描述**：查询设备中指定人员或所有人员的信息
**请求URL**：`http://设备IP:8090/person/find`
**请求方式**：GET
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| id | String | Y | 人员ID，-1查询所有 |

**curl命令示例**：
```bash
# 查询单个人员
curl -X GET "http://127.0.0.1:8090/person/find" \
  -d "pass=12345678" \
  -d "id=1001"

# 查询所有人员
curl -X GET "http://127.0.0.1:8090/person/find" \
  -d "pass=12345678" \
  -d "id=-1"
```

### 5. 人员分页查询
**接口描述**：分页查询设备中指定人员或所有人员的信息
**请求URL**：`http://设备IP:8090/person/findByPage`
**请求方式**：GET
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| personId | String | Y | 人员ID，-1查询所有 |
| length | Int | N | 每页最大数量，默认1000 |
| index | Int | N | 页码，从0开始 |

**curl命令示例**：
```bash
curl -X GET "http://127.0.0.1:8090/person/findByPage" \
  -d "pass=12345678" \
  -d "personId=-1" \
  -d "length=10" \
  -d "index=0"
```

## 三、照片管理类接口

### 1. 照片注册
**接口描述**：为已注册人员添加注册照片
**请求URL**：`http://设备IP:8090/face/create`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| personId | String | Y | 人员ID，需先注册人员 |
| faceId | String | Y | 照片ID，空值自动生成32位ID |
| imgBase64 | String | Y | 照片base64编码，不含头部 |
| isEasyWay | Boolean | N | 检测方式，false严格（默认），true宽松 |

**curl命令示例**：
```bash
# 示例中使用简化的base64编码，实际使用时需替换为真实的图片base64编码
curl -X POST "http://127.0.0.1:8090/face/create" \
  -d "pass=12345678" \
  -d "personId=1001" \
  -d "faceId=face001" \
  -d "imgBase64=iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==" \
  -d "isEasyWay=false"
```

### 2. 照片删除
**接口描述**：删除设备中指定照片ID对应的注册照片
**请求URL**：`http://设备IP:8090/face/delete`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| faceId | String | Y | 照片ID |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/delete" \
  -d "pass=12345678" \
  -d "faceId=face001"
```

### 3. 照片更新
**接口描述**：更新设备中指定照片ID的注册照片
**请求URL**：`http://设备IP:8090/face/update`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| personId | String | Y | 人员ID |
| faceId | String | Y | 照片ID |
| imgBase64 | String | Y | 照片base64编码，不含头部 |
| isEasyWay | Boolean | N | 检测方式，false严格（默认），true宽松 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/update" \
  -d "pass=12345678" \
  -d "personId=1001" \
  -d "faceId=face001" \
  -d "imgBase64=iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==" \
  -d "isEasyWay=true"
```

### 4. 照片查询
**接口描述**：查询设备中指定人员的所有注册照片
**请求URL**：`http://设备IP:8090/face/find`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| personId | String | Y | 人员ID |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/find" \
  -d "pass=12345678" \
  -d "personId=1001"
```

### 5. 拍照注册
**接口描述**：控制设备为已注册人员拍摄照片并自动完成注册
**请求URL**：`http://设备IP:8090/face/takeImg`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| personId | String | Y | 人员ID，需已存在 |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/takeImg" \
  -d "pass=12345678" \
  -d "personId=1001"
```

### 6. 清空人员注册照片
**接口描述**：删除设备中指定人员的所有注册照片
**请求URL**：`http://设备IP:8090/face/deletePerson`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| personId | String | Y | 人员ID |

**curl命令示例**：
```bash
curl -X POST "http://127.0.0.1:8090/face/deletePerson" \
  -d "pass=12345678" \
  -d "personId=1001"
```

## 四、识别记录接口

### 1. 识别记录查询
**接口描述**：查询设备中的识别记录
**请求URL**：`http://设备IP:8090/newFindRecords`
**请求方式**：GET
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| personId | String | Y | 人员ID，-1查所有，STRANGERBABY查陌生人 |
| startTime | String | Y | 开始时间，0不按时间，格式：年-月-日 时:分:秒 |
| endTime | String | Y | 结束时间，0不按时间，格式：年-月-日 时:分:秒 |
| length | Int | N | 每页最大数量，默认1000 |
| model | Int | N | 记录类型，-1所有类型（默认），0刷脸等 |
| order | String | N | 排序方式，1升序，其他降序（默认） |
| index | Int | N | 页码，从0开始 |

**curl命令示例**：
```bash
# 查询所有人员的所有记录
curl -X GET "http://127.0.0.1:8090/newFindRecords" \
  -d "pass=12345678" \
  -d "personId=-1" \
  -d "startTime=0" \
  -d "endTime=0"

# 查询指定人员的记录
curl -X GET "http://127.0.0.1:8090/newFindRecords" \
  -d "pass=12345678" \
  -d "personId=1001" \
  -d "startTime=2023-01-01 00:00:00" \
  -d "endTime=2023-12-31 23:59:59"
```

### 2. 识别记录删除
**接口描述**：删除设备中指定条件的识别记录及现场照
**请求URL**：`http://设备IP:8090/newDeleteRecords`
**请求方式**：POST
**参数说明**：
| 参数名 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- |
| pass | String | Y | 设备密码 |
| personId | String | Y | 人员ID，-1删所有，STRANGERBABY删陌生人记录 |
| startTime | String | Y | 开始时间，格式同查询接口 |
| endTime | String | Y | 结束时间，格式同查询接口 |
| model | Int | N | 记录类型，-1所有类型（默认） |

**curl命令示例**：
```bash
# 删除所有记录
curl -X POST "http://127.0.0.1:8090/newDeleteRecords" \
  -d "pass=12345678" \
  -d "personId=-1" \
  -d "startTime=0" \
  -d "endTime=0"

# 删除指定时间范围内的记录
curl -X POST "http://127.0.0.1:8090/newDeleteRecords" \
  -d "pass=12345678" \
  -d "personId=1001" \
  -d "startTime=2023-01-01%2000:00:00" \
  -d "endTime=2023-12-31%2023:59:59"
```

## 五、使用说明

1. **启动服务器**：
   ```bash
   python mockserver.py
   ```

2. **访问地址**：
   - 服务器默认运行在 `http://0.0.0.0:8090`
   - 可通过修改 `config/url_config.py` 中的 `server_config` 配置项来修改端口和绑定地址

3. **接口调用流程**：
   1. 首先调用 `setPassWord` 设置设备密码
   2. 调用 `person/create` 注册人员
   3. 调用 `face/create` 为人员添加照片
   4. 调用 `device/openDoorControl` 进行远程开门
   5. 调用 `newFindRecords` 查询识别记录

4. **注意事项**：
   - 所有接口的参数都需要放在请求体中，使用 `application/x-www-form-urlencoded` 格式，**无论GET还是POST请求**
   - JSON格式的参数需要正确转义
   - 照片注册接口的 `imgBase64` 参数需要是真实的图片base64编码，不含 `data:image/png;base64,` 头部
   - 设备密码是所有接口（除 `setPassWord` 外）的必填参数
   - GET请求不再支持URL查询字符串参数，所有参数必须通过请求体传递

## 六、常见问题

1. **密码错误**：
   - 错误码：`LAN_EXP-1001`
   - 解决方案：检查设备密码是否正确，确保已使用 `setPassWord` 设置密码

2. **参数异常**：
   - 错误码：`LAN_EXP-1002`
   - 解决方案：检查参数名称、类型是否正确，必填参数是否完整

3. **人员不存在**：
   - 错误码：`LAN_EXP-3009`
   - 解决方案：先调用 `person/create` 注册人员，再进行后续操作

4. **照片ID已存在**：
   - 错误码：`LAN_EXP-4007`
   - 解决方案：使用新的照片ID，或先删除已存在的照片

5. **照片数量超过限制**：
   - 错误码：`LAN_EXP-4012`
   - 解决方案：每个人员最多只能有3张注册照片，删除旧照片后再添加新照片

6. **未检测到面部**：
   - 错误码：`LAN_EXP-8006`
   - 解决方案：确保照片中包含清晰的人脸，调整 `isEasyWay` 参数为 `true` 尝试宽松检测

## 七、响应格式说明

所有接口返回包含5个基本字段，业务数据通过 `data` 字段返回，字段顺序为：code, data, msg, result, success：

```json
{
  "code": "LAN_SUS-0",    // 返回码，正常操作统一返回码，异常操作单独返回码
  "data": {},             // 业务数据，数值、字符串、对象或集合等
  "msg": "操作成功",       // 返回信息，通常为错误信息
  "result": 1,           // 处理结果，1成功，0失败
  "success": true        // 操作结果，true成功，false无效
}
```

## 八、返回码说明

| 返回码 | 说明 |
| --- | --- |
| LAN_SUS-0 | 操作成功 |
| LAN_EXP-1001 | 密码错误，请检查密码正确性 |
| LAN_EXP-1002 | pass参数异常 |
| LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 |
| LAN_EXP-3004 | name参数不能为空 |
| LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 |
| LAN_EXP-4007 | 照片ID已存在，请先调用删除或更新接口 |
| LAN_EXP-4008 | imgBase64不能为空 |
| LAN_EXP-4012 | 注册照片已达到最大数量限定(3张) |
| LAN_EXP-8006 | 未检测到面部 |
| LAN_EXP-8007 | 检测到多个面部 |