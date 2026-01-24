import random
from datetime import datetime
from spider_tools.project_tools.JT.ZZ.zz_match_new2.mysqlconnect import MysqlConnect
from spider_tools.project_tools.JT.ZZ.zz_match_new2.writerfactory import WriterFactory
from spider_tools.project_tools.JT.ZZ.zz_match_new2.devicetypemapper import DeviceTypeMapper


# ============ ZZMatchSpider ============ #
class ZZMatchSpider:
    def __init__(self, precinct_id: str, **kwargs):
        self.global_kwargs = kwargs.copy()
        # 公共参数
        self.precinct_id = kwargs.get('precinct_id', f'01-01-07')
        self.batch_num = kwargs.get('batch_num', datetime.now().strftime('%Y%m%d'))
        self.zh_label = kwargs.get('zh_label', f'贵州贵通信枢纽楼')
        self.force_create = kwargs.get('force_create', False)
        self.irms_province_code = kwargs.get('irms_province_code', 'GZ')
        self.province = kwargs.get('province_id', '520000')
        self.city = kwargs.get('city_id', '520400')
        self.site_int_id = kwargs.get('site_int_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.room_int_id = kwargs.get('room_int_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))

        # 汇聚机楼
        self.mains_nature = kwargs.get('mains_nature', '市电转供')
        self.power_site_level = kwargs.get('power_site_level', '传输节点')
        self.power_room_type = kwargs.get('power_room_type', '汇聚机房')
        self.power_supply_mode = kwargs.get('power_supply_mode', '双电源双回路供电')
        self.cutin_date = kwargs.get('cutin_date', datetime.now().strftime('%Y-%m-%d'))
        self.site_type = kwargs.get('site_type', random.choice(
            ['核心站点', '核心站点（配套）', '骨干站点', '汇聚站点', '接入站点', '用户站点', '其他站点']
        ))
        self.power_related_site_name = kwargs.get('power_related_site_name', '未知')
        self.county_id = kwargs.get('county_id', '')

        # 其他
        self.res_code = str(random.randint(10 ** 17, 10 ** 18 - 1))

        # 校验列表
        self.site_names = []
        self.room_names = []

        # 数据库连接
        self.db = MysqlConnect(precinct_id=precinct_id, **kwargs)

    def name_match_site(self):
        data = self.db.insert_esdata_device()
        for record in data:
            if record[4]:
                site_name = record[4]
                self.zh_label = site_name
            else:
                site_name = record[8]
                self.zh_label = site_name
            if site_name not in getattr(self, 'site_names', []):
                self.site_names.append(site_name)
                self._create_site_and_property(site_name)
                print(f"站点已写入: {site_name}")

            # 重置int_id避免重复
            self.site_int_id = str(random.randint(10 ** 17, 10 ** 18 - 1))

    def name_match_site_room(self):
        data = self.db.insert_esdata_device()
        for record in data:
            if record[4]:
                site_name = record[4]
                self.zh_label = site_name
                print(self.zh_label)
            else:
                site_name = record[8]
                self.zh_label = site_name
            if site_name not in getattr(self, 'site_names', []):
                self.site_names.append(site_name)
                self._create_site_and_property(site_name)
                print(f"站点已写入: {site_name}")
            room_name = record[1]
            room_id = record[0]
            if room_name not in getattr(self, 'room_names', []):
                self.room_names.append(room_name)
                self._create_room_and_property_and_irm(room_name, room_id, site_name)
                print(f"机房已写入: {room_name}")

            self.site_int_id = str(random.randint(10 ** 17, 10 ** 18 - 1))
            self.room_int_id = str(random.randint(10 ** 17, 10 ** 18 - 1))
            break

    def name_match_site_room_device(self):
        data = self.db.insert_esdata_device()
        for record in data:
            site_name = record[-6]
            self.zh_label = site_name
            if site_name not in getattr(self, 'site_names', []):
                self.site_names.append(site_name)
                self._create_site_and_property(site_name)
                print(f"站点已写入: {site_name}")
            room_name = record[1]
            room_id = record[3]
            if room_name not in getattr(self, 'room_names', []):
                self.room_names.append(room_name)
                self._create_room_and_property_and_irm(room_name, room_id)
                print(f"机房已写入: {room_name}")
            device_type_str = record[14]
            power_device_id = record[8]
            index_type = DeviceTypeMapper.get_index_type(str(device_type_str))
            self._create_device(index_type, device_type_str, power_device_id, record)

    def _create_site_and_property(self, site_name: str):
        self.global_kwargs.update({
            'batch_num': self.batch_num,
            'site_int_id': self.site_int_id,
            'site_zh_label': site_name,
            'province_id': self.province,
            'city_id': self.city,
            'county_id': self.county_id,
            'site_type': self.site_type,
            'cutin_date': self.cutin_date,
            'irms_province_code': self.irms_province_code,
            'site_res_code': self.res_code
        })
        site_writer = WriterFactory.create_writer('site', **self.global_kwargs)
        # site_writer.write(count=1, force_create=self.force_create)
        site_writer.write(count=1)

        self.global_kwargs.update({
            'batch_num': self.batch_num,
            'site_pro_zh_label': self.site_int_id,
            'province_id': self.province,
            'city_id': self.city,
            'power_related_site_name': self.power_related_site_name,
            'irms_province_code': self.irms_province_code,
            'mains_nature': self.mains_nature,
            'power_site_level': self.power_site_level,
            'cutin_date': self.cutin_date,
            'county_id': self.county_id,
            'site_type': self.site_type,
            'site_pro_res_code': self.res_code,
            'power_monitoring_site_name': site_name
        })
        prop_writer = WriterFactory.create_writer(
            'site_property', **self.global_kwargs)
        # prop_writer.write(count=1, force_create=self.force_create)
        prop_writer.write(count=1)
        print(f"站点对创建成功: {site_name} (site_int_id: {self.site_int_id})")

    def _create_room_and_property_and_irm(self, room_name: str, room_id: str, site_name: str):
        self.global_kwargs.update({
            'batch_num': self.batch_num,
            'room_zh_label': room_name,
            'room_int_id': self.room_int_id,
            'related_site': self.site_int_id,
            'city_id': self.city,
            'province_id': self.province,
            'county_id': self.county_id,
            'irms_province_code': self.irms_province_code,
            'cutin_date': self.cutin_date,
            'power_room_type': self.power_room_type,
            'power_supply_mode': self.power_supply_mode,
            'room_res_code': self.res_code
        })

        room_writer = WriterFactory.create_writer('room', **self.global_kwargs)
        room_writer.write(count=1)

        self.global_kwargs.update({
            'batch_num': self.batch_num,
            'room_pro_zh_label': self.room_int_id,
            'province_id': self.province,
            'city_id': self.city,
            'site_int_id': self.site_int_id,
            'irms_province_code': self.irms_province_code,
            'cutin_date': self.cutin_date,
            'power_room_type': self.power_room_type,
            'power_supply_mode': self.power_supply_mode,
            'county_id': self.county_id,
            'room_property_res_code': self.res_code,
            'power_monitoring_site_name': site_name
        })
        prop_writer = WriterFactory.create_writer(
            'room_property', **self.global_kwargs)
        prop_writer.write(count=1)

        self.global_kwargs.update({
            'batch_num': self.batch_num,
            'room_dh_name': room_name,
            'room_zg_name': room_name,
            'room_zg_id': self.room_int_id,
            'room_dh_id': room_id,
            'city_id': self.city,
            'province_id': self.province,
            'county_id': self.county_id,
        })
        irms = WriterFactory.create_writer(
            'irms_rom_map', **self.global_kwargs)
        irms.write(count=1)
        print(f"机房对创建成功: {room_name} (room_int_id: {self.room_int_id})")

    def _create_device(self, index_type: str, device_type_str: str, power_device_id: str, record):
        try:
            writer = WriterFactory.create_writer(
                index_type, site_int_id=self.site_int_id, room_int_id=self.room_int_id,
                power_device_id=power_device_id, batch_num=self.batch_num,
                zh_label=f"{record[8]}", city_id=self.city, province_id=self.province
            )
            writer.write(count=1, force_create=self.force_create)
            print(f"设备写入成功: {device_type_str} -> {index_type}")
        except Exception as e:
            print(f"设备写入失败: {device_type_str} -> {index_type}, 错误: {e}")
