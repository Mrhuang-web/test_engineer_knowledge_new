ESConfig:
    配置综资es相关索引名命名规则（站点、机房、设备等）

BaseWriter：
    基础写入类，提供（站点、机房、设备等） --> 真正写入索引（生成索引名） --> 参数取值获取
    每次写入都会调基础类 -- > 进行参数获取
        _load_business_params(es字段映射关系)  # 业务参数加载 -- 主要就是初始化构建取值 [重点,维护后面所有综资上送]
        write(实现写入es)

WriterFactory
    实现（站点、机房、设备等）写入类的工厂类
        get_writer(writer_type)  # writer_type: 站点、机房、设备等
        自动判断索引类型

注意：
    站点匹配（必须是楼栋、其他类型站点、数据中心是对应到园区的-不能直接匹配进来，会导致机房匹配不上）
    维护时，每个索引的字段都要对齐，不能有缺失，否则会导致匹配不上

    设备索引映射前置了解：
        首先DeviceTypeMapper -> 把数据库中devcie_type转化为索引名
        先通过工厂类 - create_writer 进行过滤一次
            接着通过索引名到 -> DataBuilder -> 匹配索引和索引字段
        目前除了空调类型，其他类型都需要补充好key映射
            DataBuilder -> DEVICE_FIELDS

    省份-地市编码相关表：
        building_area

匹配之后需要触发对应curl（服务：spider-external）
    # 数据中心
    curl --location --request GET 'http://10.12.5.119:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000047'
    # 空间-站点（会去查看SSSP-20250110-000002：站点映射关系  -->  对应关系在总结中说明）
    curl --location --request GET 'http://10.12.5.123:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000010'
    # 空间-机房
    curl --location --request GET 'http://10.12.5.123:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000018'
    # 高压配电
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000025'
    # 低压交流配电
    curl --location --request GET 'http://10.12.5.123:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000031'
    # 变压器
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000022'
    # 低压直流配电
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000036'
    # 发电机组
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000032'
    # 开关电源
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000035'
    # 蓄电池
    curl --location --request GET 'http://10.12.5.123:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000039'
    # UPS设备
    curl --location --request GET 'http://10.12.5.123:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000038'
    # 空调
    curl --location --request GET 'http://10.12.5.123:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000040'
    # 变换设备
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000023'
    # 动环监控
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000042'
    # 节能设备
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000041'
    # 高压直流电源
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000027'
    # 高压直流配电
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000028'
    # 智能电表
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000043'
    # 其它设备
    curl --location --request GET 'http://10.1.202.2:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000044'