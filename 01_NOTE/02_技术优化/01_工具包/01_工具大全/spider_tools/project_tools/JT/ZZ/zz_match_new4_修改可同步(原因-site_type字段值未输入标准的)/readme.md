代码说明：
    DataBuilder：负责生成设备数据，支持自定义字段值或生成默认值。
    ZZAllInOneWriter：管理所有索引的写入逻辑，通过工厂类动态创建写入器。
    WriterFactory：根据索引类型动态创建对应的写入器实例。
    MysqlConnect：负责连接 MySQL 数据库并执行 SQL 查询。
    ZZMatchSpider：整合 MySQL 数据和 ES 写入逻辑，支持站点、机房和设备的匹配与写入。
如何运行：
    将上述代码保存为 zz_all_in_one_writer.py。
    确保 spider_tools.Conf.Config 和其他依赖项正确配置。
运行脚本：
    python zz_all_in_one_writer.py
初始化字段：
    在初始化 ZZMatchSpider 或 WriterFactory.create_writer 时，可以通过 **kwargs 传递任意字段值，这些值将覆盖默认值。


databuilder
    添加了site_,room_前缀，用于区分是否为站点的或是机房的字段（同名字段时）