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

要先注意数据的构造
writer模块下
def generate_mock_data(self, count: int) -> List[Dict]:
context = {key: getattr(self, key) for key in dir(self) if not key.startswith('_')}
return DataBuilder.build_device_docs(self.index_type, count, context)

    context = {key: getattr(self, key) for key in dir(self) if not key.startswith('_')}
    将BaseWriter实例的所有非下划线属性作为键值对放入context字典中
    也就是说，context中只能包含BaseWriter实例实际拥有的属性，而不是任意传入的参数

    # 站点相关
    self.zh_label = kwargs.get('zh_label', f"test_{datetime.now().strftime('%Y%m%d')}")
    # 机房相关
    self.room_zh_label = kwargs.get('room_zh_label', f"ROOM_{random.randint(1000, 9999)}")
    # 设备相关
    self.device_zh_label = kwargs.get('device_zh_label', f"device_{random.randint(1000, 9999)}")

    没有初始化 site_zh_label、site_pro_zh_label 或 room_pro_zh_label 这些属性！

    Databuilder.py中的键名不匹配
        databuilder.py 的 _generate_field_value 方法中，处理zh_label时使用了这些键：
        
        if field == 'zh_label':
            if device_type == 'room':
                return context.get('room_zh_label', ...)  # ✅ 存在
            if device_type == 'site':
                return context.get('site_zh_label', ...)  # ❌ 不存在！
            if device_type == 'site_property':
                return context.get('site_pro_zh_label', ...)  # ❌ 不存在！
            if device_type == 'room_property':
                return context.get('room_pro_zh_label', ...)  # ❌ 不存在！
            if device_type not in (...):
                return context.get('device_zh_label', ...)  # ✅ 存在

    问题根源
        当 device_type == 'site' 时，代码尝试获取 site_zh_label，但context中只有 zh_label
        当 device_type == 'site_property' 时，代码尝试获取 site_pro_zh_label，但context中只有 zh_label
        当 device_type == 'room_property' 时，代码尝试获取 room_pro_zh_label，但context中只有 zh_label
        因为context中不存在这些键，所以每次都返回了默认值。
        
        解决方案
        修改 databuilder.py 中的 _generate_field_value 方法，使用正确的键名



databuilder 则进行分割base初始化中的前缀

# 映射到最终写入 ES 的字段名

    _STRIP_PREFIX = {
        'room_': '',
        'site_': '',
        # 如果有更多前缀继续加
    }