class ZZMatchSpider:
    """综资匹配爬虫 - 完全保留原始逻辑"""
    """force_create - 最后传False,除非新建的日期是跟之前数据没有关联到,就可以强制删除"""

    def __init__(self, precinct_id: str, **kwargs):
        # 公共参数
        self.precinct_id = precinct_id
        self.batch_num = kwargs.get('batch_num', datetime.now().strftime('%Y%m%d'))
        self.zh_label = kwargs.get('zh_label', f'贵州贵通信枢纽楼')
        self.force_create = kwargs.get('force_create', False)
        self.irms_province_code = kwargs.get('irms_province_code', 'GZ')
        self.province = kwargs.get('province_id', '520000')
        self.city = kwargs.get('city_id', '520400')
        self.site_int_id = None
        # 汇聚机楼
        self.mains_nature = kwargs.get('mains_nature', '市电转供')
        self.power_site_level = kwargs.get('power_site_level', '传输节点')
        self.power_room_type = kwargs.get('power_room_type', '汇聚机房')
        self.power_supply_mode = kwargs.get('power_supply_mode', '双电源双回路供电')
        self.cutin_date = kwargs.get('cutin_date', datetime.now().strftime('%Y-%m-%d'))
        self.site_type = kwargs.get('site_type', random.choice(
            ['核心站点', '核心站点（配套）', '骨干站点', '汇聚站点', '接入站点', '用户站点', '其他站点']))
        self.power_related_site_name = kwargs.get('power_related_site_name', self.zh_label)
        self.county_id = kwargs.get('county_id', f'')

        # 校验列表
        self.site_names = []
        self.room_names = []

        # 数据库连接
        self.db = MysqlConnect(precinct_id=precinct_id, **kwargs)

    def name_match_site(self):
        """按名称匹配 - 按对应站点的匹配 -- > 对应match_mode = 0"""
        """目前从市开始匹配 - 可以修改selectForESlist.sql的第5块更改逻辑"""
        data = self.db.insert_esdata_device()
        for record in data:
            # 站点匹配
            if record[4]:
                site_name = record[4]  # 楼栋时走这条
                self.zh_label = site_name
            else:
                site_name = record[8]  # 非楼栋的站点时走这条
                self.zh_label = site_name
            if site_name not in getattr(self, 'site_names', []):
                self.site_names.append(site_name)
                self._create_site_and_property(site_name)
                print(f"站点已写入: {site_name}")

    def name_match_site_room(self):
        """按名称匹配 - 按对应机房或站点-实现综资动环-站点-机房-设备的匹配"""
        data = self.db.insert_esdata_device()
        number = 1
        for record in data:
            # 站点匹配
            if record[4]:
                site_name = record[4]  # 楼栋时走这条
                self.zh_label = site_name
            else:
                site_name = record[8]  # 非楼栋的站点时走这条
                self.zh_label = site_name
            if site_name not in getattr(self, 'site_names', []):
                self.site_names.append(site_name)
                self._create_site_and_property(site_name)
                print(f"站点已写入: {site_name}")
            # 机房匹配
            room_name = record[1]  # 机房名称在查询结果的第20列
            room_id = record[0]  # 机房ID在查询结果的第1列
            if room_name not in getattr(self, 'room_names', []):
                self.room_names.append(room_name)
                self._create_room_and_property_and_irm(room_name, room_id)
                print(f"机房已写入: {room_name}")

    def name_match_site_room_device(self):
        """按名称匹配 - 按对应机房或站点-实现综资动环-站点-机房-设备的匹配 -- > 对应match_mode = 2"""
        data = self.db.insert_esdata_device()
        for record in data:
            # 站点匹配
            site_name = record[-6]  # 站点名称在查询结果的倒数第6列
            self.zh_label = site_name
            if site_name not in getattr(self, 'site_names', []):
                self.site_names.append(site_name)
                self._create_site_and_property(site_name)
                print(f"站点已写入: {site_name}")
            # 机房匹配
            room_name = record[1]  # 机房名称在查询结果的第20列
            room_id = record[3]  # 机房ID在查询结果的第1列
            if room_name not in getattr(self, 'room_names', []):
                self.room_names.append(room_name)
                self._create_room_and_property_and_irm(room_name, room_id)
                print(f"机房已写入: {room_name}")
            # 设备匹配
            device_type_str = record[14]
            power_device_id = record[8]
            index_type = DeviceTypeMapper.get_index_type(str(device_type_str))
            self._create_device(index_type, device_type_str, power_device_id, record)

    def _create_site_and_property(self, site_name: str):
        """创建站点和属性 - 实际站点匹配的处理逻辑"""
        # 创建站点（修复后正确调用）
        site_writer = WriterFactory.create_writer(
            'site',
            batch_num=self.batch_num,
            zh_label=site_name,
            city_id=self.city,
            province_id=self.province,
            irms_province_code=self.irms_province_code,
            cutin_date=self.cutin_date,
            county_id=self.county_id,
            site_type=self.site_type
        )

        # 保存关键关联信息
        self.site_int_id = site_writer.site_int_id
        self.province = site_writer.province_id
        self.city = site_writer.city_id

        site_writer.write(count=1, force_create=self.force_create)

        # 创建站点属性（关键：通过 site_int_id 关联）
        prop_writer = WriterFactory.create_writer(
            'site_property',
            batch_num=self.batch_num,
            site_int_id=self.site_int_id,
            province_id=self.province,
            city_id=self.city,
            irms_province_code=self.irms_province_code,
            power_site_level=self.power_site_level,
            mains_nature=self.mains_nature,
            cutin_date=self.cutin_date,
            power_related_site_name=self.power_related_site_name,
            county_id=self.county_id,
            site_type=self.site_type
        )
        prop_writer.write(count=1, force_create=self.force_create)

        print(f"站点对创建成功: {site_name} (site_int_id: {self.site_int_id})")

    def _create_room_and_property_and_irm(self, room_name: str, room_id: str):
        """创建机房和属性 - 实际机房匹配的处理逻辑"""
        # 创建站点（修复后正确调用）
        room_writer = WriterFactory.create_writer(
            'room',
            batch_num=self.batch_num,
            room_zh_label=room_name,
            site_int_id=self.site_int_id,
            city_id=self.city,
            province_id=self.province,
            irms_province_code=self.irms_province_code,
            cutin_date=self.cutin_date,
            power_room_type=self.power_room_type,
            power_supply_mode=self.power_supply_mode,
            county_id=self.county_id
        )

        # 保存关键关联信息
        self.room_int_id = room_writer.room_int_id
        self.province = room_writer.province_id
        self.city = room_writer.city_id

        room_writer.write(count=1, force_create=self.force_create)

        # 创建站点属性（关键：通过 site_int_id 关联）
        prop_writer = WriterFactory.create_writer(
            'room_property',
            batch_num=self.batch_num,
            room_int_id=self.room_int_id,
            province_id=self.province,
            city_id=self.city,
            site_int_id=self.zh_label,
            irms_province_code=self.irms_province_code,
            cutin_date=self.cutin_date,
            power_room_type=self.power_room_type,
            power_supply_mode=self.power_supply_mode,
            county_id=self.county_id
        )
        prop_writer.write(count=1, force_create=self.force_create)

        # 创建IRMS映射关系
        irms = WriterFactory.create_writer(
            'irms_rom_map',
            batch_num=self.batch_num,
            room_dh_name=room_id,
            room_zg_name=self.room_int_id,
            city_id=self.city,
            province_id=self.province,
            county_id=self.county_id
        )
        irms.write(count=1, force_create=self.force_create)

        print(f"机房对创建成功: {room_name} (room_int_id: {self.room_int_id})")

    def _create_device(self, index_type: str, device_type_str: str, power_device_id: str, record: Tuple):
        """创建设备数据 - 实际设备匹配的处理逻辑"""
        try:
            writer = WriterFactory.create_writer(
                index_type,
                site_int_id=self.site_int_id,
                room_int_id=self.room_int_id,
                power_device_id=power_device_id,
                batch_num=self.batch_num,
                zh_label=f"{record[8]}",  # 用设备ID作为标识
                city_id=self.city,
                province_id=self.province
            )
            writer.write(count=1, force_create=self.force_create)
            print(f"设备写入成功: {device_type_str} -> {index_type}")
        except Exception as e:
            print(f"设备写入失败: {device_type_str} -> {index_type}, 错误: {e}")