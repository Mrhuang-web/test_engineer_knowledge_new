# 人脸门禁一体机接口返回说明规则汇总
## 一、接口通用说明
### 1.1 接口规范
- 接口根地址：http://设备IP地址:8090/
- 接口形式：通过HTTP请求对外提供服务
- 接口安全：初次调用需设置设备密码（缺省密码12345678），后续调用需传入该密码作为校验密钥

### 1.2 接口返回通用格式
所有接口返回数据包含4个基本字段，业务数据通过`data`字段返回：
| 字段 | 描述 | 类型 | 必传 | 说明 |
| --- | --- | --- | --- | --- |
| result | 处理结果 | Int | Y | 1成功，0失败 |
| success | 操作结果 | Boolean | Y | true成功，false无效 |
| msg | 返回信息 | String | N | 通常为错误信息 |
| code | 返回码 | String | Y | 正常操作统一返回码，异常操作有单独返回码 |
| data | 返回数据 | Int/String/Object/List等 | Y | 业务相关数据 |

### 1.3 接口调用流程
1. 设备开机进入识别主界面，初始无密码
2. 设置设备密码（oldPass与newPass传入相同值）
3. 调用人员注册接口添加人员
4. 调用照片管理接口添加注册照
5. 设备识别成功后生成识别记录并存储，支持回调通知

### 1.4 注意事项
1. 同一设备接口不可同时被多个客户端调用
2. 若返回"参数异常"，需检查参数名称、参数值格式及Json语法
3. 若返回为空，需检查URL的IP、拼写及字段完整性
4. 若返回"Could not get any response"，需检查IP、端口及传参形式（POST参数放body，格式为x-www-urlencoded）

## 二、设备管理类接口
### 2.1 设置设备密码
#### 接口描述
用于初次设置或修改设备密码，新设备需将oldPass与newPass设为相同值，修改密码时需分别传入新旧密码。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/setPassWord
- Content-Type：application/x-www-form-urlencoded
- 必传参数：oldPass（旧密码）、newPass（新密码）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 参数异常 | LAN_EXP-2001 | oldPass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2002 | newPass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-2003 | 密码不允许为空或空格 | 初次设置时oldPass格式错误 |
| 参数不合法 | LAN_EXP-2004 | 新密码不允许为空或空格 | 修改密码时newPass格式错误 |
| 其他 | LAN_EXP-2005 | 旧密码错误 | 修改密码时oldPass与设备密码不一致 |
| 其他 | LAN_EXP-2006 | 初次设置密码时，请确保oldPass、newPass相同 | 初次设置时两参数值不相等 |
| 操作正确 | LAN_SUS-0 | 密码修改成功 | 设备使用新密码 |
| 操作正确 | LAN_SUS-0 | 密码设置成功 | 设备已完成初始密码设置 |

### 2.2 设备信息查询
#### 接口描述
查询设备的硬件信息、系统状态、人员统计等数据，需传入设备密码进行校验。
#### 请求信息
- Method：GET
- URL：http://设备IP:8090/device/information
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 操作正确 | LAN_SUS-0 | 查询成功 | 成功获取设备信息 |

### 2.3 设置设备时间
#### 接口描述
设置设备系统时间，支持公网时间校对（连网时每分钟校对一次），未连网时使用手动设置时间。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/setTime
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、timestamp（Unix毫秒级时间戳）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2049 | timestamp参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-2050 | timestamp时间格式错误 | timestamp包含非法字符 |
| 操作正确 | LAN_SUS-0 | 设置成功。若设备未连入公网，则此时间会生效；若设备连入公网，则会重新使用公网时间 | timestamp生效后局域网内按该时间增长 |

### 2.4 语言切换
#### 接口描述
切换设备操作界面语言，支持中文简体和英文，默认语言为中文，重置后恢复默认。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/device/setLanguage
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、languageType（语言类型：zh_CN/中文简体，en/英文）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2188 | languageType参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-2189 | 不支持的语言类型 | languageType传入非指定值 |
| 操作正确 | LAN_SUS-0 | 设置成功 | 语言设置生效 |
| 操作正确 | LAN_SUS-0 | 语言设置成功，设备即将重启 | 语言切换需重启生效 |

### 2.5 设置时区
#### 接口描述
设置设备时区，默认时区为中国标准时间（Asia/Shanghai），支持多种时区选择（详见附表2）。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/device/setTimeZone
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、timeZone（时区标识）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2201 | timezone参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-2200 | timezone参数不合法 | timezone传入非指定值 |
| 操作正确 | LAN_SUS-0 | 设置成功 | 时区设置生效 |

### 2.6 设备重启
#### 接口描述
远程触发设备重启，需传入设备密码验证权限。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/restartDevice
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 操作正确 | LAN_SUS-0 | 操作成功，设备即将重启 | pass验证正确，重启指令下发 |

### 2.7 识别回调
#### 接口描述
设置识别成功后的回调地址，设备识别成功后会向该地址POST识别数据，支持清空回调地址。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/setIdentifyCallBack
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、callbackUrl（回调地址，空值清空）
- 可选参数：base64Enable（现场照base64开关，1关/默认，2开）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2063 | callbackUrl参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-2099 | 请输入正确格式的callbackUrl地址 | callbackUrl不符合正则表达式 |
| 操作正确 | LAN_SUS-0 | 设置成功 | 回调地址设置生效 |

### 2.8 注册照片回调
#### 接口描述
设置照片注册/更新后的回调地址，设备完成照片注册或更新后会向该地址POST照片数据，支持清空回调地址。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/setImgRegCallBack
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、url（回调地址，空值清空）
- 可选参数：base64Enable（现场照base64开关，1关/默认，2开）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2061 | url参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-2064 | 请输入正确格式的url地址 | url不符合正则表达式 |
| 操作正确 | LAN_SUS-0 | 设置成功 | 回调地址设置生效 |

### 2.9 远程控制输出
#### 接口描述
远程控制设备输出信号（如开门），需传入设备密码验证权限。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/device/openDoorControl
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）
- 可选参数：type（设备交互类型，1为开门）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 操作正确 | LAN_SUS-0 | 开门成功 | 开门信号输出成功 |

### 2.10 信号输入设置
#### 接口描述
配置设备硬件信号输入接口（如门磁、开门按钮、火警输入），支持启用/禁用及类型设置。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/device/setSignalInput
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、config（Json格式配置集合）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2007 | config参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-2013 | config参数不能为空 | config传入空值 |
| 参数不合法 | LAN_EXP-2008 | config类json格式错误 | Json格式不正确 |
| 参数不合法 | LAN_EXP-2009 | config参数不合法 | 传入未定义的非法内容 |
| 参数不合法 | LAN_EXP-2208 | inputNo参数异常 | config中传入非法inputNo值 |
| 参数不合法 | LAN_EXP-2209 | inputNo参数不合法 | inputNo值越界或非法 |
| 参数不合法 | LAN_EXP-2210 | isEnable参数异常 | config中传入非法isEnable值 |
| 参数不合法 | LAN_EXP-2211 | isEnable参数不合法 | isEnable值非布尔类型 |
| 参数不合法 | LAN_EXP-2212 | type参数异常 | config中传入非法type值 |
| 参数不合法 | LAN_EXP-2213 | type参数不合法 | type值非指定类型（1-3） |
| 参数不合法 | LAN_EXP-2214 | name参数不合法 | name值非法 |
| 操作正确 | LAN_SUS-0 | 设置成功 | 配置参数生效 |

### 2.11 会议与关门告警设置
#### 接口描述
配置会议功能开关、空闲时间及关门告警开关、关门时间，支持会议签到和未关门告警。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/meetAndWarnSet
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）
- 可选参数：meetEnable（会议开关）、meetFreeTime（会议空闲时间）、doorWarnEnable（关门告警开关）、doorCloseTime（关门时间）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 操作正确 | LAN_SUS-0 | 设置成功 | 配置参数生效 |

### 2.12 卡片设置
#### 接口描述
配置卡片数据读取开关、读取扇区/块、偏移地址、密钥及韦根输出格式，支持多种韦根格式配置。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/cardInfoSet
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、readDataEnable（读取开关）、readSector（扇区）、readBlock（块）、readShift（偏移地址）、readKeyA（A密钥）、wgOutType（韦根格式）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 操作正确 | LAN_SUS-0 | 设置成功 | 配置参数生效 |

### 2.13 事件回调
#### 接口描述
设置设备警报事件的回调地址，设备产生火警、门磁、防拆等警报时会向该地址POST事件数据，支持清空回调地址。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/device/eventCallBack
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、url（回调地址，空值清空）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2061 | url参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-2064 | 请输入正确格式的url地址 | url不符合正则表达式 |
| 操作正确 | LAN_SUS-0 | 设置成功 | 回调地址设置生效 |

### 2.14 获取门磁状态
#### 接口描述
查询设备门磁当前状态（开启/闭合），需传入设备密码验证权限。
#### 请求信息
- Method：GET
- URL：http://设备IP:8090/getDoorSensor
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 操作正确 | LAN_SUS-0 | 获取成功 | 成功获取门磁状态 |

## 三、人员管理类接口
### 3.1 人员注册
#### 接口描述
添加人员信息到设备，包括姓名、卡号、身份证号及各类识别模式权限，支持系统自动生成人员ID。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/person/create
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、person（Json格式人员信息集合）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3001 | person参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3002 | person类json格式错误 | Json格式不正确或person为空 |
| 参数不合法 | LAN_EXP-3003 | 人员ID(id)只允许数字0~9和英文字母，且最大长度为255 | personId含有非法字符 |
| 参数不合法 | LAN_EXP-3004 | name参数不能为空 | name未传或为空 |
| 参数不合法 | LAN_EXP-3005 | 人员ID已存在，请调用人员删除或者更新接口 | 人员库中已存在该id |
| 其他 | LAN_EXP-3006 | 数据库异常，人员注册失败 | 数据库未知异常 |
| 其他 | LAN_EXP-3011 | facePermission参数不合法 | facePermission传入非1/2值 |
| 其他 | LAN_EXP-3012 | idCardPermission参数不合法 | idCardPermission传入非1/2值 |
| 其他 | LAN_EXP-3013 | faceAndCardPermission参数不合法 | faceAndCardPermission传入非1/2值 |
| 操作正确 | LAN_SUS-0 | 人员信息添加成功 | 人员信息写入数据库 |

### 3.2 人员删除
#### 接口描述
删除设备中的指定人员信息，支持批量删除（ID用英文逗号拼接）或删除所有人员（ID传入-1），同时删除关联的识别记录和照片。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/person/delete
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、id（人员ID）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3007 | id参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3008 | id参数不能为空 | id未传或为空 |
| 参数不合法 | LAN_EXP-3039 | 人员ID(id)只允许数字-1，0~9和英文字母，且最大长度为255 | id含有非法字符 |
| 其他 | LAN_EXP-3010 | 数据库异常，人员删除失败 | 数据库未知异常 |
| 操作正确 | LAN_SUS-0 | 删除成功 | 成功删除指定ID人员 |

### 3.3 人员更新
#### 接口描述
更新设备中已存在人员的信息，包括姓名、卡号、身份证号及各类识别模式权限，需指定人员ID。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/person/update
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、person（Json格式人员信息集合，含id）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3001 | person参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3002 | person类json格式错误 | Json格式不正确或person为空 |
| 参数不合法 | LAN_EXP-3003 | 人员ID(id)只允许数字0~9和英文字母，且最大长度为255 | id含有非法字符 |
| 参数不合法 | LAN_EXP-3008 | id参数不能为空 | id未传或为空 |
| 参数不合法 | LAN_EXP-3004 | name参数不能为空 | name未传或为空 |
| 参数不合法 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该id |
| 其他 | LAN_EXP-3006 | 数据库异常，人员注册失败 | 数据库未知异常 |
| 其他 | LAN_EXP-3011 | facePermission参数不合法 | facePermission传入非1/2值 |
| 其他 | LAN_EXP-3012 | idCardPermission参数不合法 | idCardPermission传入非1/2值 |
| 其他 | LAN_EXP-3013 | faceAndCardPermission参数不合法 | faceAndCardPermission传入非1/2值 |
| 操作正确 | LAN_SUS-0 | 人员信息更新成功 | 人员信息更新生效 |

### 3.4 人员查询
#### 接口描述
查询设备中指定人员或所有人员的信息（ID传入-1查询所有），需传入设备密码验证权限。
#### 请求信息
- Method：GET
- URL：http://设备IP:8090/person/find
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、id（人员ID，-1查询所有）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3007 | id参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3008 | id参数不能为空 | id未传或为空 |
| 参数不合法 | LAN_EXP-3039 | 人员id只允许数字-1，0~9和英文字母，且最大长度为255 | id含有非法字符 |
| 其他 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该id |
| 其他 | LAN_EXP-3040 | 设备人员数量过多，请使用分页查询 | 一次查询数量超过10000条 |
| 操作正确 | LAN_SUS-0 | 数据库人员数量为0 | 无符合条件的人员记录 |
| 操作正确 | LAN_SUS-0 | 查询成功 | 成功获取人员信息 |

### 3.5 人员分页查询
#### 接口描述
分页查询设备中指定人员或所有人员的信息，支持设置每页数量和页码，适用于人员数量较多的场景。
#### 请求信息
- Method：GET
- URL：http://设备IP:8090/person/findByPage
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、personId（人员ID，-1查询所有）
- 可选参数：length（每页最大数量，默认1000）、index（页码，从0开始）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3015 | personId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3016 | personId参数不能为空 | personId未传或为空 |
| 参数不合法 | LAN_EXP-3017 | 人员ID(personId)只允许数字-1，0~9和英文字母，且最大长度为255 | personId含有非法字符 |
| 参数不合法 | LAN_EXP-3018 | 每页显示数量length要求为(0,1000]的正整数 | length超出范围或非整数 |
| 参数不合法 | LAN_EXP-3019 | 页码index为从0开始计数的整数，必须小于总页码 | index超出总页码范围 |
| 其他 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该personId |
| 操作正确 | LAN_SUS-0 | 数据库人员数量为0 | 无符合条件的人员记录 |
| 操作正确 | LAN_SUS-0 | 查询成功 | 成功获取分页人员信息 |

## 四、照片管理类接口
### 4.1 照片注册
#### 接口描述
为已注册人员添加注册照片，支持宽松/严格质量检测模式，照片需满足像素、分辨率和大小要求。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/face/create
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、personId（人员ID）、faceId（照片ID）、imgBase64（照片base64编码）
- 可选参数：isEasyWay（质量检测模式，默认false/严格）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3015 | personId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-4002 | faceId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2024 | imgBase64参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3016 | personId参数不能为空 | personId未传或为空 |
| 参数不合法 | LAN_EXP-4005 | 人员ID(personId)只允许数字0~9和英文字母，且最大长度为255 | personId含有非法字符 |
| 参数不合法 | LAN_EXP-4006 | 照片ID(faceId)只允许数字0~9和英文字母，且最大长度为255 | faceId含有非法字符 |
| 参数不合法 | LAN_EXP-4007 | 照片ID已存在，请先调用删除或更新接口 | 照片库中已存在该faceId |
| 参数不合法 | LAN_EXP-4008 | imgBase64不能为空 | imgBase64未传或为空 |
| 参数不合法 | LAN_EXP-4009 | isEasyWay参数不合法 | isEasyWay传入非布尔值 |
| 图片异常 | LAN_EXP-4035 | 提供的图片文件不完整或格式不正确 | Base64码无法转换为图片 |
| 图片异常 | LAN_EXP-2218 | 图片格式不支持 | 图片格式非png/jpg/jpeg |
| 图片异常 | LAN_EXP-4011 | 图片解析异常 | 设备转换图片编码失败 |
| 图片异常 | LAN_EXP-2241 | 图片分辨率大于1080p | 图片分辨率超出限制 |
| 其他 | LAN_EXP-4012 | 注册照片已达到最大数量限定(3张) | 该personId已有3张注册照 |
| 其他 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该personId |
| 其他 | LAN_EXP-4030 | 设备存储空间已满 | 设备存储不足 |
| 其他 | LAN_EXP-4013 | 数据库异常，照片注册失败 | 数据库未知异常 |
| 算法报错 | LAN_EXP-8006 | 未检测到面部 | 照片中无面部 |
| 算法报错 | LAN_EXP-8007 | 检测到多个面部 | 照片中有多个面部 |
| 算法报错 | LAN_EXP-8010 | 人像过小 | 人像占比不足1/3 |
| 算法报错 | LAN_EXP-8013 | 面部过大或面部不完整 | 面部超出照片范围 |
| 算法报错 | LAN_EXP-8011 | FaceSDK无法从照片中提到特征 | 人像特征点提取不足 |
| 算法报错 | LAN_EXP-8012 | FaceSDK提取特征异常 | 人像特征点提取失败 |
| 算法报错 | LAN_EXP-8014 | 人像偏转角度过大 | 侧脸或偏头角度过大 |
| 算法报错 | LAN_EXP-8015 | 人像面部太暗或太亮 | 面部过曝或过暗 |
| 算法报错 | LAN_EXP-8016 | 人像清晰度过低 | 人像模糊 |
| 算法报错 | LAN_EXP-8017 | 人像面部光线不均匀 | 面部光照明暗不均 |
| 操作正确 | LAN_SUS-0 | 照片添加成功 | 照片信息写入数据库 |

### 4.2 照片删除
#### 接口描述
删除设备中指定照片ID对应的注册照片，删除后不可恢复，需传入设备密码验证权限。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/face/delete
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、faceId（照片ID）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-4002 | faceId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-4016 | faceId参数不能为空 | faceId未传或为空 |
| 参数不合法 | LAN_EXP-4006 | 照片ID(faceId)只允许数字0~9和英文字母，且最大长度为255 | faceId含有非法字符 |
| 其他 | LAN_EXP-4017 | 照片ID不存在，请先调用照片注册接口 | 无对应faceId的照片 |
| 其他 | LAN_EXP-4018 | 数据库异常，照片删除失败 | 数据库未知异常 |
| 操作正确 | LAN_SUS-0 | 照片删除成功 | 成功删除指定照片 |

### 4.3 照片更新
#### 接口描述
更新设备中指定照片ID的注册照片，照片需满足像素、分辨率和大小要求，支持宽松/严格质量检测模式。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/face/update
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、personId（人员ID）、faceId（照片ID）、imgBase64（照片base64编码）
- 可选参数：isEasyWay（质量检测模式，默认false/严格）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3015 | personId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-4002 | faceId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-2024 | imgBase64参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3016 | personId参数不能为空 | personId未传或为空 |
| 参数不合法 | LAN_EXP-4016 | faceId参数不能为空 | faceId未传或为空 |
| 参数不合法 | LAN_EXP-4005 | 人员ID(personId)只允许数字0~9和英文字母，且最大长度为255 | personId含有非法字符 |
| 参数不合法 | LAN_EXP-4006 | 照片ID(faceId)只允许数字0~9和英文字母，且最大长度为255 | faceId含有非法字符 |
| 参数不合法 | LAN_EXP-4031 | 该人员没有这个照片ID，请先调用照片注册接口 | 无对应personId和faceId的照片 |
| 参数不合法 | LAN_EXP-4008 | imgBase64不能为空 | imgBase64未传或为空 |
| 参数不合法 | LAN_EXP-4009 | isEasyWay参数不合法 | isEasyWay传入非布尔值 |
| 图片异常 | LAN_EXP-4010 | 提供的图片文件不完整或格式不正确 | Base64码无法转换为图片 |
| 图片异常 | LAN_EXP-4011 | 图片解析异常 | 设备转换图片编码失败 |
| 图片异常 | LAN_EXP-4032 | imgBase64不能为gif图 | 图片为gif格式 |
| 图片异常 | LAN_EXP-2241 | 图片分辨率大于1080p | 图片分辨率超出限制 |
| 其他 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该personId |
| 其他 | LAN_EXP-4020 | 数据库异常，照片更新失败 | 数据库未知异常 |
| 算法报错 | LAN_EXP-8006 | 未检测到面部 | 照片中无面部 |
| 算法报错 | LAN_EXP-8007 | 检测到多个面部 | 照片中有多个面部 |
| 算法报错 | LAN_EXP-8010 | 人像过小 | 人像占比不足1/3 |
| 算法报错 | LAN_EXP-8013 | 面部过大或面部不完整 | 面部超出照片范围 |
| 算法报错 | LAN_EXP-8011 | FaceSDK无法从照片中提到特征 | 人像特征点提取不足 |
| 算法报错 | LAN_EXP-8012 | FaceSDK提取特征异常 | 人像特征点提取失败 |
| 算法报错 | LAN_EXP-8014 | 人像偏转角度过大 | 侧脸或偏头角度过大 |
| 算法报错 | LAN_EXP-8015 | 人像面部太暗或太亮 | 面部过曝或过暗 |
| 算法报错 | LAN_EXP-8016 | 人像清晰度过低 | 人像模糊 |
| 算法报错 | LAN_EXP-8017 | 人像面部光线不均匀 | 面部光照明暗不均 |
| 操作正确 | LAN_SUS-0 | 照片更新成功 | 照片信息更新生效 |

### 4.4 照片查询
#### 接口描述
查询设备中指定人员ID对应的所有注册照片信息，包括照片路径、特征值等，需传入设备密码验证权限。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/face/find
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、personId（人员ID）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3015 | personId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3016 | personId参数不能为空 | personId未传或为空 |
| 参数不合法 | LAN_EXP-4005 | 人员ID(personId)只允许数字0~9和英文字母，且最大长度为255 | personId含有非法字符 |
| 其他 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该personId |
| 操作正确 | LAN_SUS-0 | 照片查询成功 | 成功获取该人员所有照片信息 |
| 操作正确 | LAN_SUS-0 | 该人员没有注册照片 | 该personId无注册照片 |

### 4.5 拍照注册
#### 接口描述
控制设备为已注册人员拍摄照片并自动完成注册，支持通过注册照片回调获取拍摄结果。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/face/takeImg
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、personId（人员ID）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3015 | personId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3016 | personId参数不能为空 | personId未传或为空 |
| 参数不合法 | LAN_EXP-4005 | 人员ID(personId)只允许数字0~9和英文字母，且最大长度为255 | personId含有非法字符 |
| 其他 | LAN_EXP-4012 | 注册照片已达到最大数量限定(3张) | 该personId已有3张注册照 |
| 其他 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该personId |
| 操作正确 | LAN_SUS-0 | 正在开启拍照注册模式，注册成功后可根据personId查询拍摄的照片。请根据引导完成注册 | 设备开始执行拍照指令 |

### 4.6 清空人员注册照片
#### 接口描述
删除设备中指定人员的所有注册照片，同步注销照片ID，需传入设备密码验证权限。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/face/deletePerson
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、personId（人员ID）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3015 | personId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3016 | personId参数不能为空 | personId未传或为空 |
| 参数不合法 | LAN_EXP-4005 | 人员ID(personId)只允许数字0~9和英文字母，且最大长度为255 | personId含有非法字符 |
| 其他 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该personId |
| 其他 | LAN_EXP-4025 | 数据库异常 | 照片清空失败 |
| 操作正确 | LAN_SUS-0 | 照片清空成功 | 成功删除该人员所有照片 |
| 操作正确 | LAN_SUS-0 | 该人员没有注册照片 | 该personId无注册照片 |

## 五、识别记录接口
### 5.1 识别记录查询
#### 接口描述
查询设备中的识别记录，支持按人员ID、时间范围、记录类型分页查询，可查询所有人员、陌生人或人证比对记录。
#### 请求信息
- Method：GET
- URL：http://设备IP:8090/newFindRecords
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、personId（人员ID）、startTime（开始时间）、endTime（结束时间）
- 可选参数：length（每页最大数量，默认1000）、model（记录类型，默认-1/所有）、order（排序方式，默认降序）、index（页码，从0开始）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3015 | personId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3031 | startTime参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3032 | endTime参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3033 | startTime时间格式错误 | startTime非0且不符合指定格式 |
| 参数不合法 | LAN_EXP-3034 | endTime时间格式错误 | endTime非0且不符合指定格式 |
| 参数不合法 | LAN_EXP-3035 | endTime应大于startTime | endTime早于startTime |
| 参数不合法 | LAN_EXP-5007 | model参数不合法 | model传入非指定范围值 |
| 参数不合法 | LAN_EXP-3016 | personId参数不能为空 | personId未传或为空 |
| 参数不合法 | LAN_EXP-3017 | 人员ID(personId)只允许数字-1，0~9和英文字母，且最大长度为255 | personId含有非法字符 |
| 参数不合法 | LAN_EXP-3018 | 每页显示数量length要求为(0,1000]的正整数 | length超出范围或非整数 |
| 参数不合法 | LAN_EXP-3019 | 页码index为从0开始计数的整数，必须小于总页码 | index超出总页码范围 |
| 其他 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该personId |
| 操作正确 | LAN_SUS-0 | 该查询条件对应的识别记录数量为0 | 无符合条件的识别记录 |
| 操作正确 | LAN_SUS-0 | 查询成功 | 成功获取识别记录 |

### 5.2 识别记录删除
#### 接口描述
删除设备中指定条件的识别记录及现场照，支持按人员ID、时间范围、记录类型删除，可删除所有人员、陌生人或人证比对记录。
#### 请求信息
- Method：POST
- URL：http://设备IP:8090/newDeleteRecords
- Content-Type：application/x-www-form-urlencoded
- 必传参数：pass（设备密码）、personId（人员ID）、startTime（开始时间）、endTime（结束时间）
- 可选参数：model（记录类型，默认-1/所有）
#### 返回说明
| 类型 | Code码 | msg | 触发原因 |
| --- | --- | --- | --- |
| 通用报错 | LAN_EXP-1006 | The XX method is not supported. | Method与url不匹配 |
| 通用报错 | LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 | 设备禁用中 |
| 通用报错 | LAN_EXP-1005 | 设备正忙，请稍后再试 | 设备正在升级或执行其他任务 |
| 通用报错 | LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 | 设备未设置密码 |
| 通用报错 | LAN_EXP-1001 | 密码错误，请检查密码正确性 | pass值与设备密码不一致 |
| 参数异常 | LAN_EXP-1002 | pass参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3015 | personId参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3031 | startTime参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数异常 | LAN_EXP-3032 | endTime参数异常 | 参数名错误、漏传、位置错误或值异常 |
| 参数不合法 | LAN_EXP-3033 | startTime时间格式错误 | startTime非0且不符合指定格式 |
| 参数不合法 | LAN_EXP-3034 | endTime时间格式错误 | endTime非0且不符合指定格式 |
| 参数不合法 | LAN_EXP-3035 | endTime应大于startTime | endTime早于startTime |
| 参数不合法 | LAN_EXP-5007 | model参数不合法 | model传入非指定范围值 |
| 参数不合法 | LAN_EXP-3016 | personId参数不能为空 | personId未传或为空 |
| 参数不合法 | LAN_EXP-3017 | 人员ID(personId)只允许数字-1，0~9和英文字母，且最大长度为255 | personId含有非法字符 |
| 其他 | LAN_EXP-3009 | 人员ID不存在，请先调用人员注册接口 | 人员库中无该personId |
| 其他 | LAN_EXP-5013 | 数据库异常，识别记录删除失败 | 数据库未知异常 |
| 操作正确 | LAN_SUS-0 | 删除成功 | 成功删除指定识别记录和现场照 |

## 六、附表
### 附表1 Code码总览
| Code码 | 说明 |
| --- | --- |
| LAN_SUS-0 | 接口调用成功，msg随接口不同而不同 |
| LAN_EXP-1000 | 未知异常 |
| LAN_EXP-1001 | 密码错误，请检查密码正确性 |
| LAN_EXP-1002 | pass参数异常 |
| LAN_EXP-1003 | 接口服务未设置密码，请先设置密码 |
| LAN_EXP-1004 | 设备已被禁用，请先启用再做其它操作 |
| LAN_EXP-1005 | 设备正忙，请稍后再试 |
| LAN_EXP-1006 | The XX method is not supported. |
| （其余Code码详见文档附表1完整列表） |

### 附表2 可用时区列表
| 时区标识 | 说明 |
| --- | --- |
| Asia/Shanghai | 中国标准时间 (北京) |
| Asia/Hong_Kong | 香港时间 (香港) |
| Asia/Taipei | 台北时间 (台北) |
| Asia/Seoul | 首尔 |
| Asia/Tokyo | 日本时间 (东京) |
| America/New_York | 美国东部时间 (纽约) |
| （其余时区详见文档附表2完整列表） |

要不要我帮你整理一份**完整Code码对照表（含所有异常码及说明）**？