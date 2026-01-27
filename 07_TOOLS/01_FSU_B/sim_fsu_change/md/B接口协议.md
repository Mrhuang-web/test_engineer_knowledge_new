# 5. B接口协议
## 5.1 报文原则
SC与FSU之间的接口基于WebService技术，消息协议采用XML格式。

## 5.2 WSDL定义
- SC提供的Webservice接口的WSDL定义见附件
- FSU接口的Webservice接口的WSDL定义见附件

## 5.3 基本定义
### 核心术语定义
|术语|说明|
| ---- | ---- |
|告警消息|监控对象及FSU上报的所有告警信息|
|FSUID|用于中国移动全网唯一标示FSU设备的编号，具体定义详见《中国移动动环命名及编码指导意见》|
|动环设备ID|即监控对象的编码，该编码在站点内唯一，可配置，后面简称“设备ID”，具体定义详见《中国移动动环命名及编码指导意见》|
|监控点ID|同类型设备唯一，可配置，每类信号的编码详见《中国移动动环告警及信号标准化字典表》中的信号编码ID|

### 数据类型的字节数定义
|类型|字节数|
| ---- | ---- |
|Long|4字节|
|Short|2字节|
|Char|1字节|
|Float|4字节|
|枚举类型|4字节|

### 工作过程定义
#### 连接建立流程
FSU和SC之间通过传送LOGIN、LOGIN_ACK报文进行注册，具体流程如下：
1. FSU向SC发送LOGIN报文，包含用户名和密码（由SC提供的合法信息）；
2. SC对用户名和密码进行认证；
3. 认证通过则注册成功，B接口通过该连接通讯；
4. 连接意外中断后，FSU需重新执行上述注册过程。

#### 常量定义
|常量名称|说明|长度|
| ---- | ---- | ---- |
|USER_LENGTH|用户名长度|20字节|
|PASSWORD_LEN|口令长度|20字节|
|DES_LENGTH|描述信息长度|120字节|
|VER_LENGTH|版本描述的长度|20字节|
|FSUID_LEN|FSU ID字符串长度|20字节|
|NMALARMID_LEN|网管告警编号|40字节|
|IP_LENGTH|IP串长度|15字节|
|DEVICEID_LEN|设备ID长度|26字节|
|ID_LENGTH|监控点/站点/机房ID长度|20字节|
|SERIALNO_LEN|告警序号长度|10字节|
|TIME_LEN|时间串长度|19字节|
|DEV_CONF_LEN|设备配置信息长度|6000字节|
|ALARMREMARK_LEN|告警预留字段|60字节|
|NAME_LENGTH|名字命名长度|80字节|
|FAILURE_CAUSE_LEN|失败原因描述信息长度|40字节|
|CONFREMARK_LEN|配置预留字段|40字节|

#### 枚举定义
|属性名称|属性描述|枚举类型|类型定义|
| ---- | ---- | ---- | ---- |
|EnumResult|报文返回结果|FAILURE＝0|失败|
|||SUCCESS＝1|成功|
|EnumType|监控系统数据的种类|DI＝4|数字输入量（包含多态数字输入量），遥信|
|||AI＝3|模拟输入量，遥测|
|||DO＝1|数字输出量，遥控|
|||AO＝2|模拟输出量，遥调|
|EnumState|信号值的状态|NOALARM＝0|正常数据|
|||INVALID＝1|无效数据|
|EnumLevel|告警等级|CRITICAL＝1|一级告警|
|||MAJOR＝2|二级告警|
|||MINOR＝3|三级告警|
|||HINT＝4|四级告警|
|EnumFlag|告警标志|BEGIN|开始|
|||END|结束|

#### 数据结构定义
|结构名称|结构描述|属性名称|属性数据类型|类型定义|
| ---- | ---- | ---- | ---- | ---- |
|TTime|时间的结构|Year|short|年|
|||Month|Char|月|
|||Day|Char|日|
|||Hour|Char|时|
|||Minute|Char|分|
|||Second|Char|秒|
|TSignalMeasurementId|设备采集点标识|ID|Char[ID_LENGTH]|监控点ID|
|||SignalNumber（注1）|short|同设备同类监控点顺序号|
|TSemaphore|信号量的值的结构|TSignalId|Sizeof(TSignalMeasurementId)|设备采集点标识|
|||Type|EnumType|数据类型|
|||MeasuredVal|Float|实测值。该字段对所有类型的信号数据均有效；当出现在SC->FSU操作中时，该字段置为“NULL”|
|||SetupVal|Float|设置值。该字段只适用于遥调和遥控信号，并且只在SC->FSU操作中有效，其余情况下置为“NULL”|
|||Status|EnumState|状态|
|||Time|Char[TIME_LEN]|时间，格式YYYY-MM-DD<SPACE键>hh:mm:ss（采用24小时的时间制式）|
|TThreshold|信号量的门限值的结构|TSignalId|Sizeof(TSignalMeasurementId)|设备采集点标识|
|||Type|EnumType|数据类型|
|||Threshold|Float|告警门限值|
|||AlarmLevel|EnumLevel|告警等级|
|||NMAlarmID|Char[NMALARMID_LEN]|网管告警编号（告警标准化编号），即《中国移动动环命名及编码指导意见》第五章定义的14位数字的告警ID|
|TStorageRule|信号数据存储规则的结构|TSignalId|Sizeof(TSignalMeasurementId)|设备采集点标识|
|||Type|EnumType|数据类型|
|||AbsoluteVal|Float|绝对阀值（注3）|
|||RelativeVal|Float|百分比阀值（注3）|
|||StorageInterval|long|存储时间间隔（单位：分钟）|
|||StorageRefTime|Char[TIME_LEN]|存储参考时间，格式YYYY-MM-DD<SPACE键>hh:mm:ss（采用24小时的时间制式）|
|TAlarm|告警消息的结构|SerialNo|Char[SERIALNO_LEN]|告警序号|
|||NMAlarmID|Char[NMALARMID_LEN]|网管告警编号（告警标准化编号），即《中国移动动环命名及编码指导意见》第五章定义的14位数字的告警ID|
|||DeviceID|Char[DEVICEID_LEN]|设备ID|
|||TSignalId|Sizeof(TSignalMeasurementId)|设备采集点标识。对于非监控点越限类告警，该参数涉及所有子参数取值为“NULL”|
|||AlarmTime|Char[TIME_LEN]|告警时间，YYYY-MM-DD<SPACE键>hh:mm:ss（采用24小时的时间制式）|
|||AlarmLevel|EnumLevel|告警级别|
|||AlarmFlag|EnumFlag|告警标志|
|||AlarmDesc|Char[DES_LENGTH]|告警的事件描述|
|||EventValue|Float|告警触发值。对于非监控点越限类告警，该字段置空|
|||AlarmRemark|Char[ALARMREMARK_LEN]|预留字段|
|TFSUStatus|FSU状态参数|CPUUsage|Float|CPU使用率|
|||MEMUsage|Float|内存使用率|
|||HardDiskUsage|Float|FSU硬盘占用率（含SD卡等存储介质）|
|TDevConf|监控对象配置信息|DeviceID|Char[DEVICEID_LEN]|设备ID|
|||DeviceName|Char[NAME_LENGTH]|设备名称[定义参考中国移动动环命名及编码指导意见]|
|||SiteID|Char[ID_LENGTH]|所属站点编码[定义参考中国移动动环命名及编码指导意见]|
|||RoomID|Char[n*ID_LENGTH]|FSU物理机房编码[定义参考中国移动动环命名及编码指导意见]|
|||SiteName|Char[NAME_LENGTH]|设备所在的站点名称[定义参考中国移动动环命名及编码指导意见1.1]|
|||RoomName|Char[NAME_LENGTH]|设备所在的机房名称[定义参考中国移动动环命名及编码指导意见1.2]|
|||DeviceType|EnumDeviceType|设备类型（按动环标准化定义）|
|||DeviceSubType|EnumDeviceSubType|设备子类型（按动环标准化定义）|
|||Model|Char[DES_LENGTH]|设备型号|
|||Brand|Char[DES_LENGTH]|设备品牌|
|||RatedCapacity|Float|额定容量|
|||Version|Char[VER_LENGTH]|版本|
|||BeginRunTime|Char[TIME_LEN]|启用时间|
|||DevDescribe|Char[DES_LENGTH]|设备描述信息（包含设备的安装位置）|
|||Signals|N*TSignal|一个或多个监控点信号配置信息（注2）|
|||ConfRemark|Char[CONFREMARK_LEN]|配置预留字段|

**注1**：必选字段。对于同一个设备上同一个监控点有多个采集点的场景（例如：信号ID为007303，信号名称为单体XXX电压，表示多个单体电压，当该字段取值为020时，则代表单体020电压），该字段取值范围为001-999，且同一个监控点下的顺序号是唯一的；对于同一个设备上同一个监控点只有一个采集点的场景，该字段取值固定为000。

**注2**：结构体TSignal定义如下：
|类型名称|描述|属性名称|属性数据类型|类型定义|
| ---- | ---- | ---- | ---- | ---- |
|TSignal|监控点信号配置信息|TSignalId|Sizeof(TSignalMeasurementId)|设备采集点标识|
|||SignalName|Char[NAME_LENGTH]|信号名称|
|||Type|EnumType|数据类型|
|||Threshold|Float|门限值|
|||AlarmLevel|EnumLevel|告警级别|
|||NMAlarmID|Char[NMALARMID_LEN]|网管告警编号（参照《中国移动动环命名及编码指导意见》）|

**注3**：绝对阀值和百分比阀值同时仅有一个字段生效，即当绝对阀值生效时，百分比阀值置空；反过来，当百分比阀值生效时，绝对阀值置空。

## 5.4 基本报文格式定义
|类型|一级节点|二级节点|定义|
| ---- | ---- | ---- | ---- |
|请求报文|Request|PK_Type|报文类型|
|||Info|报文内容|
|响应报文|Response|PK_Type|报文类型|
|||Info|报文内容|

完整的接口交互由请求报文和响应报文组成，每个请求报文必须有一个响应报文进行反馈。报文类型参见5.5报文类型定义，数据流方式和格式定义参见5.6数据流方式和格式定义。

## 5.5 报文类型定义
|报文类型|报文动作|数据流向|类型名称|
| ---- | ---- | ---- | ---- |
|FSU向SC注册|注册|SC<—FSU|LOGIN|
||注册响应|SC—>FSU|LOGIN_ACK|
|上报告警信息|实时告警发送|SC<—FSU|SEND_ALARM|
||实时告警发送确认|SC—>FSU|SEND_ALARM_ACK|
|请求监控点数据|监控点数据请求|SC—>FSU|GET_DATA|
||请求监控点数据响应|SC<—FSU|GET_DATA_ACK|
|写监控点设置值|写监控点设置值请求|SC—>FSU|SET_POINT|
||写监控点设置值响应|SC<—FSU|SET_POINT_ACK|
|请求监控点门限数据|监控点门限数据请求|SC—>FSU|GET_THRESHOLD|
||请求监控点门限数据响应|SC<—FSU|GET_THRESHOLD_ACK|
|写监控点门限数据|写监控点门限数据请求|SC—>FSU|SET_THRESHOLD|
||写监控点门限数据响应|SC<—FSU|SET_THRESHOLD_ACK|
|获取FSU注册信息|获取FSU注册信息请求|SC—>FSU|GET_LOGININFO|
||获取FSU注册信息响应|SC<—FSU|GET_LOGININFO_ACK|
|设置FSU注册信息|设置FSU注册信息请求|SC—>FSU|SET_LOGININFO|
||设置FSU注册信息响应|SC<—FSU|SET_LOGININFO_ACK|
|获取FSU的FTP信息|获取FSU的FTP信息请求|SC—>FSU|GET_FTP|
||获取FSU的FTP信息响应|SC<—FSU|GET_FTP_ACK|
|设置FSU的FTP信息|设置FSU的FTP信息请求|SC—>FSU|SET_FTP|
||设置FSU的FTP信息响应|SC<—FSU|SET_FTP_ACK|
|时间同步|时间同步请求|SC—>FSU|TIME_CHECK|
||时间同步响应|SC<—FSU|TIME_CHECK_ACK|
|获取FSU的状态信息（心跳机制）|获取FSU的状态参数请求|SC—>FSU|GET_FSUINFO|
||获取FSU的状态参数响应|SC<—FSU|GET_FSUINFO_ACK|
|更新FSU状态信息获取周期（心跳机制）|更新FSU状态信息获取周期请求|SC—>FSU|UPDATE_FSUINFO_INTERVAL|
||更新FSU状态信息获取周期响应|SC<—FSU|UPDATE_FSUINFO_INTERVAL_ACK|
|重启FSU|重启FSU请求|SC—>FSU|SET_FSUREBOOT|
||重启FSU响应|SC<—FSU|SET_FSUREBOOT_ACK|
|查询监控点存储规则|监控点存储规则查询请求|SC—>FSU|GET_STORAGERULE|
||监控点存储规则查询响应|SC<—FSU|GET_STORAGERULE_ACK|
|请求动环设备配置数据|动环配置数据请求|SC—>FSU|GET_DEV_CONF|
||动环配置数据确认|SC<—FSU|GET_DEV_CONF_ACK|
|上报动环设备配置数据|上报动环设备配置变更数据请求|SC<—FSU|SEND_DEV_CONF_DATA|
||上报动环设备配置变更数据响应|SC—>FSU|SEND_DEV_CONF_DATA_ACK|
|写动环设备配置数据|写动环设备配置数据请求|SC—>FSU|SET_DEV_CONF_DATA|
||写动环设备配置数据响应|SC<—FSU|SET_DEV_CONF_DATA_ACK|
|写监控点存储规则|写监控点存储规则请求|SC—>FSU|SET_STORAGERULE|
||写监控点存储规则响应|SC<—FSU|SET_STORAGERULE_ACK|

## 5.6 数据流方式和格式定义
### 5.6.1 FSU向SC注册
#### 数据流方式
FSU向SC传送FSUID、用户名、口令、内网IP、MAC地址和版本号，SC验证用户名和口令是否正确：
- 验证正确：返回注册成功报文；
- 验证失败：返回注册失败报文，并给出失败具体原因。

**注**：FSU上报给SC的账户信息均具备对FSU管理的最高权限（可读可写）。注册失败时FSU和SC要分别记录日志。

#### 数据流格式定义
##### 发起：FSU（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[LOGIN]|登录命令名|
|Info|UserName|Char[USER_LENGTH]|用户名|
||PassWord|Char[PASSWORD_LEN]|口令（采用MD5进行加密）|
||FSUID|Char[FSUID_LEN]|FSU ID号|
||FSUIP|Char[IP_LENGTH]|FSU的内网IP|
||FSUMAC|Char[MAC_LENGTH]|FSU的MAC地址|
||FSUVER|Char[VER_LENGTH]|FSU版本号|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>LOGIN</Name>
    </PK_Type>
    <Info>
        <UserName/>
        <PassWord/>
        <FSUID/>
        <FSUIP/>
        <FSUMAC/>
        <FSUVER/>
    </Info>
</Request>
```

##### 响应：SC（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[LOGIN_ACK]|登录命令响应|
|Info|Result|EnumResult|返回注册结果|
||FailureCause|Char[FAILURE_CAUSE_LEN]|上报告警失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>LOGIN_ACK</Name>
    </PK_Type>
    <Info>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.2 上报告警信息
#### 数据流方式
FSU根据设备产生告警或者根据遥测量判断有告警需上报时，向SC上报告警信息，SC返回确认信息：
- 网络中断导致上报失败：网络恢复后FSU重新上报；
- 服务未及时响应（请求超时默认30s）导致上报失败：最多尝试重新上报3次。

#### 数据流格式定义
##### 发起：FSU（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SEND_ALARM]|告警上报|
|Info|FSUID|Char[FSUID_LEN]|FSUID|
||Values|TAlarm|告警信息|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SEND_ALARM</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Values>
            <TAlarmList>
                <TAlarm>
                    <SerialNo/>
                    <ID/>
                    <DeviceID/>
                    <NMAlarmID/>
                    <AlarmTime/>
                    <AlarmLevel/>
                    <AlarmFlag/>
                    <AlarmDesc/>
                    <EventValue/>
                    <SignalNumber/>
                    <AlarmRemark/>
                </TAlarm>
                <TAlarm>
                    <SerialNo/>
                    <ID/>
                    <DeviceID/>
                    <NMAlarmID/>
                    <AlarmTime/>
                    <AlarmLevel/>
                    <AlarmFlag/>
                    <AlarmDesc/>
                    <EventValue/>
                    <SignalNumber/>
                    <AlarmRemark/>
                </TAlarm>
            </TAlarmList>
        </Values>
    </Info>
</Request>
```

##### 响应：SC（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SEND_ALARM_ACK]|告警信息响应|
|Info|Result|EnumResult|返回设置结果|
||FailureCause|Char[FAILURE_CAUSE_LEN]|上报告警失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>SEND_ALARM_ACK</Name>
    </PK_Type>
    <Info>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.3 请求监控点数据
#### 数据流方式
SC向FSU发送所需数据的标识，FSU向SC返回要求的监控点实时采集的数据信息。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_DATA]|监控点数据请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||DeviceID|Char[DEVICEID_LEN]|设备ID。当为空，则返回该FSU所监控的所有设备的监控点的值；这种情况下，忽略IDs参数（即监控点ID列表）|
||IDs|n*ID_LENGTH|相应的监控点ID号。当为空，则返回该设备的所有监控点的值|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>GET_DATA</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <DeviceList>
            <Device ID="000000000001">
                <ID/>
                <ID/>
                <ID/>
            </Device>
            <Device ID="000000000002">
                <ID/>
                <ID/>
                <ID/>
            </Device>
        </DeviceList>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_DATA_ACK]|监控点数据响应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||Result|EnumResult|请求数据成功与否的标志|
||Values|Sizeof(TSemaphore)|对应5.3中的TSemaphore的数据结构定义|
||FailureCause|Char[FAILURE_CAUSE_LEN]|请求监控点数据失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>GET_DATA_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <Values>
            <DeviceList>
                <Device ID="000000000001">
                    <TSemaphore Type="" ID="" SignalNumber="" MeasuredVal="" SetupVal="NULL" Status="" Time=""/>
                    <TSemaphore Type="" ID="" SignalNumber="" MeasuredVal="" SetupVal="NULL" Status="" Time=""/>
                </Device>
                <Device ID="000000000002">
                    <TSemaphore Type="" ID="" SignalNumber="" MeasuredVal="" SetupVal="NULL" Status="" Time=""/>
                    <TSemaphore Type="" ID="" SignalNumber="" MeasuredVal="" SetupVal="NULL" Status="" Time=""/>
                </Device>
            </DeviceList>
        </Values>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.4 写监控点设置值
#### 数据流方式
SC向FSU发送监控点的标识ID和新设置值，FSU设置监控点的新设置值并向SC返回设置结果。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_POINT]|写监控点的设置值请求|
|Info|FSUID|Char[FSUID_LEN]|单个FSU ID号|
||n*DeviceID|n*Char[DEVICEID_LEN]|n个设备ID的列表|
||m*Value|m*Sizeof(TSemaphore)|m个监控点的设置值，数据的值的类型由相应的数据结构决定|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SET_POINT</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Value>
            <DeviceList>
                <Device ID="000000000001">
                    <TSemaphore Type="" ID="" SignalNumber="" MeasuredVal="NULL" SetupVal="" Status="" Time=""/>
                    <TSemaphore Type="" ID="" SignalNumber="" MeasuredVal="NULL" SetupVal="" Status="" Time=""/>
                </Device>
                <Device ID="000000000002">
                    <TSemaphore Type="" ID="" SignalNumber="" MeasuredVal="NULL" SetupVal="" Status="" Time=""/>
                    <TSemaphore Type="" ID="" SignalNumber="" MeasuredVal="NULL" SetupVal="" Status="" Time=""/>
                </Device>
            </DeviceList>
        </Value>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_POINT_ACK]|写监控点的设置值回应|
|Info|FSUID|Char[FSUID_LEN]|单个FSU ID号|
||n*DeviceID|n*Char[DEVICEID_LEN]|n个设备ID的列表|
||m*TSignalMeasurementId|m*Sizeof(TSignalMeasurementId)|m个控制或调节成功的设备采集点的列表|
||t*TSignalMeasurementId|t*Sizeof(TSignalMeasurementId)|t个控制或调节失败的设备采集点的列表|
||Result|EnumResult|写成功/失败（即控制的结果）|
||FailureCause|Char[FAILURE_CAUSE_LEN]|写监控点设置值失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>SET_POINT_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <FailureCause/>
        <DeviceList>
            <Device ID="000000000001">
                <SuccessList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </SuccessList>
                <FailList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </FailList>
            </Device>
            <Device ID="000000000002">
                <SuccessList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </SuccessList>
                <FailList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </FailList>
            </Device>
        </DeviceList>
    </Info>
</Response>
```

### 5.6.5 请求监控点门限数据
#### 数据流方式
SC向FSU发送所需数据的标识，FSU向SC返回要求的监控点门限数据。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_THRESHOLD]|监控点门限数据请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||DeviceID|Char[DEVICEID_LEN]|设备ID。当为空，则返回该FSU所监控的所有设备的监控点门限数据，这种情况下，忽略IDs参数（即监控点ID列表）|
||IDs|n*ID_LENGTH|相应的监控点ID号。当为空，则返回该设备的所有监控点的门限数据|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>GET_THRESHOLD</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <DeviceList>
            <Device ID="000000000001">
                <ID/>
                <ID/>
                <ID/>
            </Device>
            <Device ID="000000000002">
                <ID/>
                <ID/>
                <ID/>
            </Device>
        </DeviceList>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_THRESHOLD_ACK]|监控点门限数据响应|
|Info|Result|EnumResult|请求数据成功与否的标志|
||FSUID|Char[FSUID_LEN]|FSU ID号|
||Values|Sizeof(TThreshold)|对应5.3中的TThreshold的数据结构定义|
||FailureCause|Char[FAILURE_CAUSE_LEN]|请求监控点门限失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>GET_THRESHOLD_ACK</Name>
    </PK_Type>
    <Info>
        <Result/>
        <FSUID/>
        <FailureCause/>
        <Values>
            <DeviceList>
                <Device ID="000000000001">
                    <TThreshold Type="" ID="" SignalNumber="" Threshold="" AlarmLevel="" NMAlarmID=""/>
                    <TThreshold Type="" ID="" SignalNumber="" Threshold="" AlarmLevel="" NMAlarmID=""/>
                </Device>
                <Device ID="000000000002">
                    <TThreshold Type="" ID="" SignalNumber="" Threshold="" AlarmLevel="" NMAlarmID=""/>
                    <TThreshold Type="" ID="" SignalNumber="" Threshold="" AlarmLevel="" NMAlarmID=""/>
                </Device>
            </DeviceList>
        </Values>
    </Info>
</Response>
```

### 5.6.6 写监控点门限数据
#### 数据流方式
SC向FSU发送监控点的标识ID和新门限数据，FSU设置监控点的新门限数据并向SC返回结果。若写失败，需自动重发一次。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_THRESHOLD]|写监控点门限数据请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||n*DeviceID|n*Char[DEVICEID_LEN]|n个设备ID的列表|
||m*Value|m*Sizeof(TThreshold)|m个监控点门限值，数据的值的类型由相应的数据结构决定|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SET_THRESHOLD</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Value>
            <DeviceList>
                <Device ID="000000000001">
                    <TThreshold Type="" ID="" SignalNumber="" Threshold="" AlarmLevel="" NMAlarmID=""/>
                    <TThreshold Type="" ID="" SignalNumber="" Threshold="" AlarmLevel="" NMAlarmID=""/>
                </Device>
                <Device ID="000000000002">
                    <TThreshold Type="" ID="" SignalNumber="" Threshold="" AlarmLevel="" NMAlarmID=""/>
                    <TThreshold Type="" ID="" SignalNumber="" Threshold="" AlarmLevel="" NMAlarmID=""/>
                </Device>
            </DeviceList>
        </Value>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_THRESHOLD_ACK]|写监控点门限数据请求回应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||n*DeviceID|n*Char[DEVICEID_LEN]|n个设备ID的列表|
||m*TSignalMeasurementId|m*Sizeof(TSignalMeasurementId)|m个写成功的设备采集点的列表|
||t*TSignalMeasurementId|t*Sizeof(TSignalMeasurementId)|t个写失败的设备采集点的列表|
||Result|EnumResult|写成功/失败（即控制的结果）|
||FailureCause|Char[FAILURE_CAUSE_LEN]|写监控点门限失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>SET_THRESHOLD_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <FailureCause/>
        <DeviceList>
            <Device ID="000000000001">
                <SuccessList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </SuccessList>
                <FailList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </FailList>
            </Device>
            <Device ID="000000000001">
                <SuccessList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </SuccessList>
                <FailList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </FailList>
            </Device>
        </DeviceList>
    </Info>
</Response>
```

### 5.6.7 获取FSU注册信息
#### 数据流方式
SC向FSU发送获取FSU注册信息的请求，FSU返回注册信息。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_LOGININFO]|获取注册信息请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>GET_LOGININFO</Name>
    </PK_Type>
    <Info>
        <FSUID/>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_LOGININFO_ACK]|获取注册信息响应|
|Info|UserName|Char[USER_LENGTH]|用户名|
||PassWord|Char[PASSWORD_LEN]|口令|
||FSUID|Char[FSUID_LEN]|FSU ID号|
||FSUIP|IP_LENGTH|FSU的内网IP|
||FSUMAC|Char[MAC_LENGTH]|FSU的MAC地址|
||FSUVER|Char[VER_LENGTH]|FSU版本号|
||SiteID|Char[ID_LENGTH]|所属站点编码|
||SiteName|Char[NAME_LENGTH]|设备所在的站点名称[定义参考中国移动动环命名及编码指导意见1.1]|
||RoomID|Char[n*ID_LENGTH]|FSU物理机房编码|
||RoomName|Char[NAME_LENGTH]|设备所在的机房名称[定义参考中国移动动环命名及编码指导意见1.2]|
||Result|EnumResult|成功/失败|
||FailureCause|Char[FAILURE_CAUSE_LEN]|获取FSU注册信息失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>GET_LOGININFO_ACK</Name>
    </PK_Type>
    <Info>
        <UserName>cmcc</UserName>
        <PassWord>cmcc</PassWord>
        <FSUID/>
        <FSUIP/>
        <FSUVER/>
        <SiteID/>
        <SiteName/>
        <RoomID/>
        <RoomName/>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.8 批量设置FSU注册信息
#### 数据流方式
SC向FSU发送设置注册信息的数据，FSU存储注册数据并返回设置结果：
- 设置成功：更新后的用户名和密码在SC下次访问FSU时生效；
- 设置失败：SC自动重发一次（“设置失败”包括FSU返回“Failure”消息以及FSU响应超时（5s未响应））。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_LOGININFO]|设置注册信息请求|
|Info|UserName|Char[USER_LENGTH]|用户名|
||PassWord|Char[PASSWORD_LEN]|口令|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SET_LOGININFO</Name>
    </PK_Type>
    <Info>
        <UserName>cmcc</UserName>
        <PassWord>cmcc</PassWord>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_LOGININFO_ACK]|设置注册信息响应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||Result|EnumResult|设置成功/失败|
||FailureCause|Char[FAILURE_CAUSE_LEN]|设置FSU注册信息失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>SET_LOGININFO_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.9 获取FSU的FTP信息
#### 数据流方式
SC向FSU发送获取FTP用户、密码信息的请求，FSU返回FTP信息。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_FTP]|获取FTP用户、密码请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>GET_FTP</Name>
    </PK_Type>
    <Info>
        <FSUID/>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_FTP_ACK]|获取FTP用户、密码响应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||UserName|Char[USER_LENGTH]|用户登录名|
||PassWord|Char[PASSWORD_LEN]|密码|
||Result|EnumResult|成功/失败|
||FailureCause|Char[FAILURE_CAUSE_LEN]|获取FSU的FTP信息失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>GET_FTP_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <UserName/>
        <PassWord/>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.10 设置FSU的FTP信息
#### 数据流方式
SC向FSU发送设置FTP用户、密码的信息，FSU存储和设置FTP信息，并返回设置结果。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_FTP]|设置FTP用户、密码请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||UserName|Char[USER_LENGTH]|用户登录名|
||PassWord|Char[PASSWORD_LEN]|密码|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SET_FTP</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <UserName/>
        <PassWord/>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_FTP_ACK]|设置FTP用户、密码响应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||Result|EnumResult|设置成功/失败|
||FailureCause|Char[FAILURE_CAUSE_LEN]|设置FSU的FTP信息失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>SET_FTP_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.11 时间同步
#### 数据流方式
SC向FSU发送标准时间信息（FSU注册成功后自动发送，也可手动发送），FSU按参数更新时间并返回对时结果。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[TIME_CHECK]|时间同步请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||Time|Sizeof(TTime)|本机时间|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>TIME_CHECK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Time>
            <Year/>
            <Month/>
            <Day/>
            <Hour/>
            <Minute/>
            <Second/>
        </Time>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[TIME_CHECK_ACK]|时间同步回应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||Result|EnumResult|同步成功/失败|
||FailureCause|Char[FAILURE_CAUSE_LEN]|时间同步失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>TIME_CHECK_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.12 获取FSU状态信息
#### 数据流方式
SC向FSU定期发送获取FSU状态信息的请求（时间间隔可设置，默认为10分钟），FSU返回当前FSU状态参数。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_FSUINFO]|获取FSU状态信息请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>GET_FSUINFO</Name>
    </PK_Type>
    <Info>
        <FSUID/>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_FSUINFO_ACK]|获取FSU状态信息响应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||TFSUStatus|Sizeof（TFSUStatus）|FSU状态|
||Result|EnumResult|成功/失败|
||FailureCause|Char[FAILURE_CAUSE_LEN]|获取FSU状态信息失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>GET_FSUINFO_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <TFSUStatus>
            <CPUUsage/>
            <MEMUsage/>
            <HardDiskUsage/>
        </TFSUStatus>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.13 更新FSU状态信息获取周期
#### 数据流方式
SC向FSU发送更新FSU状态获取周期的请求，FSU返回更新是否成功。触发场景：
- 场景一：某FSU向SC注册成功后，SC发送更新请求；
- 场景二：SC侧FSU状态获取周期变更后，SC向所有FSU发送更新请求。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[UPDATE_FSUINFO_INTERVAL]|更新FSU状态信息获取周期请求|
|Info|FSUID|Char[FSUID_LEN]|FSU设备的ID号。当SC需向所有FSU发送更新状态获取周期请求时，FSUID取值为“NULL”|
||Interval|short|FSU状态信息获取周期值，以秒（s）为单位|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>UPDATE_FSUINFO_INTERVAL</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Interval/>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[UPDATE_FSUINFO_INTERVAL_ACK]|更新FSU状态信息获取周期响应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||Result|EnumResult|成功/失败|
||FailureCause|Char[FAILURE_CAUSE_LEN]|更新FSU状态信息获取周期失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>UPDATE_FSUINFO_INTERVAL_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.14 重启FSU
#### 数据流方式
SC向FSU发送重启要求，FSU返回成功标志后重启（此报文用于FSU升级：SC先通过FTP将升级文件上传到FSU的/upgrade/目录，再发送此报文使FSU重启后自动升级）。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_FSUREBOOT]|重启FSU请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SET_FSUREBOOT</Name>
    </PK_Type>
    <Info>
        <FSUID/>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_FSUREBOOT_ACK]|重启FSU响应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||Result|EnumResult|成功/失败|
||FailureCause|Char[FAILURE_CAUSE_LEN]|重启FSU失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>SET_FSUREBOOT_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.15 请求动环设备配置数据
#### 数据流方式
SC向指定FSU发送所需配置数据的设备标识，FSU向SC返回请求的动环设备当前配置信息。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_DEV_CONF]|动环设备配置数据请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||DeviceID|Char[DEVICEID_LEN]|动环设备标识号，本操作只限于单个设备配置数据的查询|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>GET_DEV_CONF</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <DeviceID/>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_DEV_CONF_ACK]|动环设备配置数据确认信息|
|Info|Result|EnumResult|请求数据成功与否的标志|
||Values|Sizeof(TDevConf)|对应5.3中的TDevConf的数据结构定义|
||FailureCause|Char[FAILURE_CAUSE_LEN]|请求动环设备配置数据失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>GET_DEV_CONF_ACK</Name>
    </PK_Type>
    <Info>
        <Result/>
        <FailureCause/>
        <Values>
            <Device DeviceID="" DeviceName="" SiteID="" RoomID="" SiteName="" RoomName="" DeviceType="" DeviceSubType="" Model="" Brand="" RatedCapacity="" Version="" BeginRunTime="" DevDescribe="" ConfRemark="">
                <Signals Count="">
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                </Signals>
            </Device>
        </Values>
    </Info>
</Response>
```

### 5.6.16 上报动环设备的配置数据
#### 数据流方式
FSU上动环设备的配置信息发生变更或者FSU重启后，FSU向SC上报变化的配置信息，SC返回确认信息。

#### 数据流格式定义
##### 发起：FSU（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SEND_DEV_CONF_DATA]|上报动环设备配置数据请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||Values|Sizeof(TDevConf)|对应5.3中的TDevConf的数据结构定义|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SEND_DEV_CONF_DATA</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Values>
            <Device DeviceID="000000000001" DeviceName="" SiteID="" RoomID="" SiteName="" RoomName="" DeviceType="" DeviceSubType="" Model="" Brand="" RatedCapacity="" Version="" BeginRunTime="" DevDescribe="" ConfRemark="">
                <Signals Count="">
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                </Signals>
            </Device>
            <Device DeviceID="000000000002" DeviceName="" SiteID="" RoomID="" SiteName="" RoomName="" DeviceType="" DeviceSubType="" Model="" Brand="" RatedCapacity="" Version="" BeginRunTime="" DevDescribe="" ConfRemark="">
                <Signals Count="">
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                </Signals>
            </Device>
        </Values>
    </Info>
</Request>
```

##### 响应：SC（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SEND_DEV_CONF_DATA_ACK]|动环设备配置数据上报确认信息|
|Info|Result|EnumResult|返回设置结果|
||FailureCause|Char[FAILURE_CAUSE_LEN]|接收监控对象配置数据失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>SEND_DEV_CONF_DATA_ACK</Name>
    </PK_Type>
    <Info>
        <Result/>
        <FailureCause/>
    </Info>
</Response>
```

### 5.6.17 写动环设备的配置数据
#### 数据流方式
SC向FSU发送动环设备的配置数据设置请求信息，FSU设置新的配置信息并向SC返回成功与否。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_DEV_CONF_DATA]|写动环设备配置数据请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||Values|Sizeof(TDevConf)|需要修改的监控对象的配置信息|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SET_DEV_CONF_DATA</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Values>
            <Device DeviceID="000000000001" DeviceName="" SiteID="" RoomID="" SiteName="" RoomName="" DeviceType="" DeviceSubType="" Model="" Brand="" RatedCapacity="" Version="" BeginRunTime="" DevDescribe="" ConfRemark="">
                <Signals Count="">
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                </Signals>
            </Device>
            <Device DeviceID="000000000002" DeviceName="" SiteID="" RoomID="" SiteName="" RoomName="" DeviceType="" DeviceSubType="" Model="" Brand="" RatedCapacity="" Version="" BeginRunTime="" DevDescribe="" ConfRemark="">
                <Signals Count="">
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                    <Signal Type="" ID="" SignalName="" SignalNumber="" AlarmLevel="" Thresbhold="" NMAlarmID=""/>
                </Signals>
            </Device>
        </Values>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_DEV_CONF_DATA_ACK]|写动环设备配置数据回应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||SuccessList|n*Char[DEVICEID_LEN]|n个成功设备ID的列表|
||FailList|n*Char[DEVICEID_LEN]|n个失败设备ID的列表|
||Result|EnumResult|写成功/失败（即控制的结果）|
||FailureCause|Char[FAILURE_CAUSE_LEN]|设置监控对象配置数据失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>SET_DEV_CONF_DATA_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <FailureCause/>
        <SuccessList>
            <Device ID="000000000001"/>
        </SuccessList>
        <FailList>
            <Device ID="000000000002"/>
        </FailList>
    </Info>
</Response>
```

### 5.6.18 查询监控点存储规则
#### 数据流方式
SC向FSU发送存储规则相关的设备和监控点标识，FSU向SC返回所请求的监控点存储规则信息。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_STORAGERULE]|查询监控点存储规则请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||DeviceID|m*Char[DEVICEID_LEN]|设备ID。当为空，则返回该FSU所监控的所有设备的监控点存储规则，这种情况下，忽略IDs参数（即监控点ID列表）|
||TSignalId|n*Sizeof(TSignalMeasurementId)|相应的设备采集点标识。当为空，则返回该设备的所有监控点的存储规则|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>GET_STORAGERULE</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <DeviceList>
            <Device ID="000000000001">
                <TSignalMeasurementId ID="" SignalNumber=""/>
                <TSignalMeasurementId ID="" SignalNumber=""/>
            </Device>
            <Device ID="000000000002">
                <TSignalMeasurementId ID="" SignalNumber=""/>
                <TSignalMeasurementId ID="" SignalNumber=""/>
            </Device>
        </DeviceList>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[GET_STORAGERULE_ACK]|监控点存储规则响应|
|Info|Result|EnumResult|请求数据成功与否的标志|
||Values|Sizeof(TStorageRule)|对应5.3中的TStorageRule的数据结构定义|
||FailureCause|Char[FAILURE_CAUSE_LEN]|获取监控点存储规则失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>GET_STORAGERULE_ACK</Name>
    </PK_Type>
    <Info>
        <Result/>
        <FailureCause/>
        <Values>
            <DeviceList>
                <Device ID="000000000001">
                    <TStorageRule Type="" ID="" SignalNumber="" AbsoluteVal="" RelativeVal="" StorageInterval="" StorageRefTime=""/>
                    <TStorageRule Type="" ID="" SignalNumber="" AbsoluteVal="" RelativeVal="" StorageInterval="" StorageRefTime=""/>
                </Device>
                <Device ID="000000000002">
                    <TStorageRule Type="" ID="" SignalNumber="" AbsoluteVal="" RelativeVal="" StorageInterval="" StorageRefTime=""/>
                    <TStorageRule Type="" ID="" SignalNumber="" AbsoluteVal="" RelativeVal="" StorageInterval="" StorageRefTime=""/>
                </Device>
            </DeviceList>
        </Values>
    </Info>
</Response>
```

### 5.6.19 写监控点存储规则
#### 数据流方式
SC向FSU发送监控点的标识ID以及需要更新的存储规则，FSU按照下发的新监控点信号存储规则设置并向SC返回结果。若SC指令下发失败，需自动重发一次。

#### 数据流格式定义
##### 发起：SC（请求报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_STORAGERULE]|写监控点存储规则请求|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||n*DeviceID|n*Char[DEVICEID_LEN]|n个设备ID的列表|
||m*Value|m*Sizeof(TStorageRule)|m个监控点存储规则，数据的值的类型由相应的数据结构决定|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SET_STORAGERULE</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Value>
            <DeviceList>
                <Device ID="000000000001">
                    <TStorageRule Type="" ID="" SignalNumber="" AbsoluteVal="" RelativeVal="" StorageInterval="" StorageRefTime=""/>
                    <TStorageRule Type="" ID="" SignalNumber="" AbsoluteVal="" RelativeVal="" StorageInterval="" StorageRefTime=""/>
                </Device>
                <Device ID="000000000002">
                    <TStorageRule Type="" ID="" SignalNumber="" AbsoluteVal="" RelativeVal="" StorageInterval="" StorageRefTime=""/>
                    <TStorageRule Type="" ID="" SignalNumber="" AbsoluteVal="" RelativeVal="" StorageInterval="" StorageRefTime=""/>
                </Device>
            </DeviceList>
        </Value>
    </Info>
</Request>
```

##### 响应：FSU（应答报文）
|字段|变量名称/报文定义|长度及类型|描述|
| ---- | ---- | ---- | ---- |
|PK_Type|Name|Char[SET_STORAGERULE_ACK]|写监控点存储规则请求回应|
|Info|FSUID|Char[FSUID_LEN]|FSU ID号|
||n*DeviceID|n*Char[DEVICEID_LEN]|n个设备ID的列表|
||m*Id|m*Sizeof(Long)|m个写成功的设备采集点的列表|
||t*Id|t*Sizeof(Long)|t个写失败的设备采集点的列表|
||Result|EnumResult|写成功/失败（即控制的结果）|
||FailureCause|Char[FAILURE_CAUSE_LEN]|写监控点存储规则失败的原因（厂家自定义）。当Result取值为1时，FailureCause取值为“NULL”|

XML样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <PK_Type>
        <Name>SET_STORAGERULE_ACK</Name>
    </PK_Type>
    <Info>
        <FSUID/>
        <Result/>
        <FailureCause/>
        <DeviceList>
            <Device ID="000000000001">
                <SuccessList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </SuccessList>
                <FailList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </FailList>
            </Device>
            <Device ID="000000000002">
                <SuccessList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </SuccessList>
                <FailList>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                    <TSignalMeasurementId ID="" SignalNumber=""/>
                </FailList>
            </Device>
        </DeviceList>
    </Info>
</Response>
```

## 5.7 FTP接口能力
FSU应提供FTP接口，提供FTP存储文件能力至少8G。通过FSU提供的FTP服务，SC定期登录后取回或上传文件（FSU做服务端，SC是客户端）。

### 5.7.1 批量获取监控对象的配置数据
FSU将动环监控对象的配置数据以XML格式存储在一级子目录\Config\下并按需定期更新，文件名为devices_FSUID.xml。SC根据需要（例如：新FSU上线后等场景）通过FTP文件接口获取FSU下全部监控对象的配置数据，也可定期（例如：每天、每周指定天等方式）获取指定FSU的全部监控对象的配置数据。

配置文件样例：
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Devices Count="">
    <Device DeviceID="" DeviceName="" SiteID="" RoomID="" SiteName="" RoomName="" DeviceType="" DeviceSubType="" Model="" Brand="" RatedCapacity="" Version="" BeginRunTime="" DevDescribe="" ConfRemark="">