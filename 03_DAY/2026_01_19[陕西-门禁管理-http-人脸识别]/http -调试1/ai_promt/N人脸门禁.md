# 人脸门禁一体机接口协议配置与请求构建指南（V4.0.20）
## 一、接口基础说明
### 1.1 接口规范
- 接口根地址：http://设备IP地址:8090/
- 接口形式：HTTP请求
- 接口安全：初次需设置设备密码（缺省密码12345678），后续所有接口需传入pass参数校验

### 1.2 接口返回格式
所有接口返回包含4个基本字段，业务数据通过data字段返回：
| 字段 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| result | 处理结果 | Int | Y | 1成功，0失败 |
| success | 操作结果 | Boolean | Y | true成功，false无效 |
| msg | 返回信息 | String | N | 通常为错误信息 |
| code | 返回码 | String | Y | 正常操作统一返回码，异常操作单独返回码 |
| data | 业务数据 | 多类型 | Y | 数值、字符串、对象或集合等 |

### 1.3 接口调用流程
1. 设置设备密码（首次使用oldPass与newPass传入相同值）
2. 调用人员注册接口添加人员
3. 调用照片注册接口添加人员注册照
4. 设备识别成功后生成识别记录，支持回调通知

### 1.4 注意事项
- 同一设备接口不可多客户端同时调用
- 参数异常需检查名称拼写、值规范及JSON格式
- URL错误会导致返回为空，需核对IP、拼写及字段
- 无响应可能是IP/端口错误或POST参数格式问题（需用x-www-urlencoded）

## 二、设备管理类接口
### 2.1 设置设备密码
- 请求方式：POST
- 请求URL：http://设备IP:8090/setPassWord
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| oldPass | 旧密码 | String | Y | 初次设置与newPass相同 |
| newPass | 新密码 | String | Y | 不可为空或空格，无需传入pass |
- 成功返回示例：
```json
{
  "code": "LAN_SUS-0",
  "data": "password is : test1234",
  "msg": "密码设置成功",
  "result": 1,
  "success": true
}
```

### 2.2 设备信息查询
- 请求方式：GET
- 请求URL：http://设备IP:8090/device/information
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：pass（设备密码，必传）
- 成功返回包含SDK版本、CPU温度、设备序列号等信息

### 2.3 设置设备时间
- 请求方式：POST
- 请求URL：http://设备IP:8090/setTime
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| timestamp | Unix毫秒级时间戳 | String | Y | 公网设备会自动校对时间 |

### 2.4 语言切换
- 请求方式：POST
- 请求URL：http://设备IP:8090/device/setLanguage
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 密码 | String | Y | - |
| languageType | 语言类型 | String | Y | zh_CN（中文简体）、en（英文） |

### 2.5 设置时区
- 请求方式：POST
- 请求URL：http://设备IP:8090/device/setTimeZone
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| timeZone | 时区 | String | Y | 默认Asia/Shanghai，其他参考附表2 |

### 2.6 设备重启
- 请求方式：POST
- 请求URL：http://设备IP:8090/restartDevice
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：pass（设备密码，必传）

### 2.7 识别回调
- 请求方式：POST
- 请求URL：http://设备IP:8090/setIdentifyCallBack
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| callbackUrl | 回调地址 | String | Y | 符合HTTP/HTTPS/FTP正则，空值清空回调 |
| base64Enable | 现场照base64开关 | Int | N | 1关（默认），2开 |

### 2.8 注册照片回调
- 请求方式：POST
- 请求URL：http://设备IP:8090/setImgRegCallBack
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| url | 回调地址 | String | Y | 符合正则，空值清空回调 |
| base64Enable | 现场照base64开关 | Int | N | 1关（默认），2开 |

### 2.9 远程控制输出
- 请求方式：POST
- 请求URL：http://设备IP:8090/device/openDoorControl
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| type | 设备交互类型 | Int | N | 1：开门 |

### 2.10 信号输入设置
- 请求方式：POST
- 请求URL：http://设备IP:8090/device/setSignalInput
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| config | 硬件接口配置 | Json | Y | 包含inputNo、isEnable、type字段 |

### 2.11 会议与关门告警设置
- 请求方式：POST
- 请求URL：http://设备IP:8090/meetAndWarnSet
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| meetEnable | 会议功能开关 | Bool | N | 开启后显示签到状态 |
| meetFreeTime | 会议空闲时间 | Int | N | 单位毫秒，默认3分钟 |
| doorWarnEnable | 关门告警开关 | Bool | N | 开启后超时未关门生成记录 |
| doorCloseTime | 关门时间设定 | Int | N | 单位毫秒 |

### 2.12 卡片设置
- 请求方式：POST
- 请求URL：http://设备IP:8090/cardInfoSet
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| readDataEnable | 读取用户数据开关 | Bool | Y | true开，false关 |
| readSector | 读指定扇区 | Int | Y | - |
| readBlock | 读指定扇区内的块 | Int | Y | - |
| readShift | 读块数据偏移地址 | Int | Y | 0-12B，输出4B |
| readKeyA | A密钥 | String | Y | 6字节Hex格式，可为空 |
| wgOutType | 韦根输出格式 | Int | Y | 0不输出，支持26/34/50/66 |

### 2.13 事件回调
- 请求方式：POST
- 请求URL：http://设备IP:8090/device/eventCallBack
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| url | 回调地址 | String | Y | 符合正则，空值清空回调 |

### 2.14 获取门磁状态
- 请求方式：GET
- 请求URL：http://设备IP:8090/getDoorSensor
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：pass（设备密码，必传）
- 返回字段：status（2门磁开启，3门磁闭合）

## 三、人员管理类接口
### 3.1 人员注册
- 请求方式：POST
- 请求URL：http://设备IP:8090/person/create
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| person | 人员信息集合 | Json | Y | 包含id、name、idcardNum等字段 |

### 3.2 人员删除
- 请求方式：POST
- 请求URL：http://设备IP:8090/person/delete
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| id | 人员ID | String | Y | 多ID用逗号拼接，-1删除所有 |

### 3.3 人员更新
- 请求方式：POST
- 请求URL：http://设备IP:8090/person/update
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| person | 人员信息集合 | Json | Y | 包含id（必传）、name（必传）等字段 |

### 3.4 人员查询
- 请求方式：GET
- 请求URL：http://设备IP:8090/person/find
- Query参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| id | 人员ID | String | Y | -1查询所有人员 |

### 3.5 人员分页查询
- 请求方式：GET
- 请求URL：http://设备IP:8090/person/findByPage
- Query参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| personId | 人员ID | String | Y | -1查询所有人员 |
| length | 每页最大数量 | Int | N | 0<length≤1000，默认1000 |
| index | 页码 | Int | N | 从0开始 |

## 四、照片管理类接口
### 4.1 照片注册
- 注意：像素>112*112、分辨率<1080p、大小<2M
- 请求方式：POST
- 请求URL：http://设备IP:8090/face/create
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| personId | 人员ID | String | Y | 需先注册人员 |
| faceId | 照片ID | String | Y | 空值自动生成32位ID |
| imgBase64 | 照片base64编码 | String | Y | 不含头部，支持png/jpg/jpeg |
| isEasyWay | 检测方式 | Boolean | N | false严格（默认），true宽松 |

### 4.2 照片删除
- 请求方式：POST
- 请求URL：http://设备IP:8090/face/delete
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| faceId | 照片ID | String | Y | - |

### 4.3 照片更新
- 注意：同照片注册的图片要求
- 请求方式：POST
- 请求URL：http://设备IP:8090/face/update
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：同照片注册（personId、faceId必传）

### 4.4 照片查询
- 请求方式：POST
- 请求URL：http://设备IP:8090/face/find
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| personId | 人员ID | String | Y | 查询该人员所有照片 |

### 4.5 拍照注册
- 请求方式：POST
- 请求URL：http://设备IP:8090/face/takeImg
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| personId | 人员ID | String | Y | 需已存在 |

### 4.6 清空人员注册照片
- 请求方式：POST
- 请求URL：http://设备IP:8090/face/deletePerson
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| personId | 人员ID | String | Y | - |

## 五、识别记录接口
### 5.1 识别记录查询
- 请求方式：GET
- 请求URL：http://设备IP:8090/newFindRecords
- Query参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| personId | 人员ID | String | Y | -1查所有，STRANGERBABY查陌生人 |
| startTime | 开始时间 | String | Y | 0不按时间，格式：年-月-日 时:分:秒 |
| endTime | 结束时间 | String | Y | 同startTime格式 |
| length | 每页最大数量 | Int | N | 0<length≤1000，默认1000 |
| model | 记录类型 | Int | N | -1所有类型（默认），0刷脸等 |
| order | 排序方式 | String | N | 1升序，其他降序（默认） |
| index | 页码 | Int | N | 从0开始 |

### 5.2 识别记录删除
- 请求方式：POST
- 请求URL：http://设备IP:8090/newDeleteRecords
- Header：Content-Type: application/x-www-form-urlencoded
- Body参数：
| 参数名 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| pass | 设备密码 | String | Y | - |
| personId | 人员ID | String | Y | -1删所有，STRANGERBABY删陌生人记录 |
| startTime | 开始时间 | String | Y | 格式同查询接口 |
| endTime | 结束时间 | String | Y | 格式同查询接口 |
| model | 记录类型 | Int | N | -1所有类型（默认） |

## 六、附录
### 附表1 常用返回码说明
| 返回码 | 说明 |
| --- | --- |
| LAN_SUS-0 | 操作成功 |
| LAN_EXP-1001 | 密码错误 |
| LAN_EXP-1003 | 未设置设备密码 |
| LAN_EXP-1004 | 设备已禁用 |
| LAN_EXP-2001 | oldPass参数异常 |
| LAN_EXP-3004 | name参数不能为空 |
| LAN_EXP-4008 | imgBase64不能为空 |
| LAN_EXP-8006 | 未检测到面部 |

### 附表2 常用时区列表
| 时区标识 | 说明 |
| --- | --- |
| Asia/Shanghai | 中国标准时间（默认） |
| Asia/Hong_Kong | 香港时间 |
| Asia/Taipei | 台北时间 |
| America/New_York | 美国东部时间 |
| Europe/London | 格林尼治标准时间 |

要不要我帮你整理一份**接口请求示例代码集**（包含各核心接口的Postman配置导出和Python请求代码）？