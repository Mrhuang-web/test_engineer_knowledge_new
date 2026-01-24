# mock_es_writer_v2.py
"""
简约易用的ES数据模拟写入工具 - 安全版本
支持设备、房间、站点等多种索引类型，自动检查索引存在性，避免误删数据
"""

import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from elasticsearch import Elasticsearch, helpers


# ==================== 配置类 ====================
class ESConfig:
    """ES配置管理"""
    ES_URL = "http://localhost:9200"  # 修改为实际ES地址
    INDEX_SETTINGS = {
        "index": {
            "number_of_replicas": "0",
            "refresh_interval": "5s"
        }
    }

    # 根据JSON映射文件提取的索引前缀映射
    INDEX_PREFIX_MAP = {
        # 设备类
        'air': 'ods_zz_device_air',
        'battery': 'ods_zz_device_battery',
        'energy_save': 'ods_zz_device_energy_save',
        'high_dc_distribution': 'ods_zz_device_high_dc_distribution',
        'high_distribution': 'ods_zz_device_high_distribution',
        'high_power': 'ods_zz_device_high_power',
        'low_ac_distribution': 'ods_zz_device_low_ac_distribution',
        'low_dc_distribution': 'ods_zz_device_low_dc_distribution',
        'other': 'ods_zz_device_other',
        'power_generation': 'ods_zz_device_power_generation',
        'power_monitor': 'ods_zz_device_power_monitor',
        'switch_power': 'ods_zz_device_switch_power',
        'transform_device': 'ods_zz_device_transform_device',
        'transform': 'ods_zz_device_transform',
        'ups': 'ods_zz_device_ups',
        # 房间类
        'room': 'ods_zz_room',
        'room_property': 'ods_zz_room_property',
        # 站点类
        'site': 'ods_zz_site',
        'site_property': 'ods_zz_site_property',
        # 映射类
        'irms_dc_map': 'ods_zz_irms_dc_map',
        'irms_rom_map': 'ods_zz_irms_rom_map',
        # 连接类
        'link_pe_in': 'ods_zz_link_pe_in',
    }


# ==================== 基类 ====================
class BaseESWriter:
    """ES写入基类，封装通用功能"""

    def __init__(self, index_type: str, env: str = 'release', **kwargs):
        """
        初始化
        :param index_type: 索引类型，如 'air', 'room', 'site' 等
        :param env: 环境标识
        :param kwargs: 可选参数：province_id, city_id, date, batch_num
        """
        self.index_type = index_type
        self.env = env
        self.province_id = kwargs.get('province_id', '00')
        self.city_id = kwargs.get('city_id', '0000')
        self.date = kwargs.get('date', datetime.now().strftime('%Y%m%d'))
        self.batch_num = kwargs.get('batch_num', f"BATCH_{datetime.now().strftime('%Y%m%d%H%M%S')}")

        # ES客户端
        self.es = Elasticsearch(ESConfig.ES_URL)

        # 索引名称格式：{prefix}_{date_suffix}_{province}
        self.index_name = self._get_index_name()
        self.doc_type = "point_history_data"

        print(f"[{self.__class__.__name__}] 初始化完成")
        print(f"  - 索引类型: {self.index_type}")
        print(f"  - 索引名称: {self.index_name}")
        print(f"  - 环境: {self.env}")
        print(f"  - 批次号: {self.batch_num}")

    def _get_index_name(self) -> str:
        """生成索引名称"""
        prefix = ESConfig.INDEX_PREFIX_MAP.get(self.index_type)
        if not prefix:
            raise ValueError(f"未知的索引类型: {self.index_type}")

        # 根据业务规则添加日期后缀（月/年/日）
        if self.index_type in ['air', 'battery']:
            suffix = f"2025{datetime.now().strftime('%m')}m"  # 年月，如 202506m
        elif self.index_type in ['high_dc_distribution', 'high_distribution', 'high_power',
                                 'energy_save', 'other', 'power_generation', 'transform_device',
                                 'transform', 'ups']:
            suffix = "2025y"  # 年，如 2025y
        elif self.index_type in ['room', 'room_property', 'site', 'site_property',
                                 'irms_dc_map', 'irms_rom_map', 'link_pe_in']:
            # 房间和站点类有具体日期
            suffix = self.date + "d"
        else:
            suffix = self.date

        return f"{prefix}_{suffix}"

    def create_index_and_mapping(self, mapping: Optional[Dict] = None, force_create: bool = False):
        """
        创建索引和mapping
        :param mapping: mapping定义
        :param force_create: 是否强制删除重建（⚠️ 危险：会删除已有数据）
        """
        try:
            index_exists = self.es.indices.exists(index=self.index_name)

            if index_exists:
                if force_create:
                    print(f"  ⚠️  强制删除并重建索引: {self.index_name}")
                    print(f"     ⚠️  警告：该操作将删除索引中所有现有数据！")
                    self.es.indices.delete(index=self.index_name, ignore=[400, 404])
                else:
                    print(f"  ✅ 索引已存在，跳过创建: {self.index_name}")
                    print(f"     提示：如需强制重建，请设置 force_create=True")
                    return  # 直接返回，不创建索引

            # 索引不存在，或已删除准备重建
            print(f"  📝 创建索引: {self.index_name}")
            self.es.indices.create(index=self.index_name, ignore=[400])

            # 设置索引配置
            self.es.indices.put_settings(
                index=self.index_name,
                body=ESConfig.INDEX_SETTINGS
            )

            # 如果提供了mapping，则设置
            if mapping:
                mapping_body = {self.doc_type: mapping}
                self.es.indices.put_mapping(
                    index=self.index_name,
                    doc_type=self.doc_type,
                    body=mapping_body
                )
                print(f"  ✅ Mapping已创建")

            print(f"✅ 索引创建成功: {self.index_name}")

        except Exception as e:
            print(f"❌ 索引创建失败: {str(e)}")
            raise

    def bulk_write(self, data_list: List[Dict]):
        """批量写入数据"""
        if not data_list:
            print("  - 无数据需要写入")
            return

        actions = [
            {
                "_index": self.index_name,
                "_type": self.doc_type,
                "_source": data
            }
            for data in data_list
        ]

        try:
            success, failed = helpers.bulk(self.es, actions, stats_only=True)
            print(f"✅ 写入成功: {success}条, 失败: {failed}条")
            self.es.indices.refresh(index=self.index_name)
        except Exception as e:
            print(f"❌ 批量写入失败: {str(e)}")

    def generate_mock_data(self, count: int = 100) -> List[Dict]:
        """生成模拟数据（子类必须实现）"""
        raise NotImplementedError("子类必须实现generate_mock_data方法")

    def write(self, count: int = 100, force_create: bool = False):
        """
        完整流程：生成数据并写入
        :param count: 生成数据条数
        :param force_create: 是否强制重建索引（⚠️ 危险操作）
        """
        print(f"\n[{self.index_type}] 开始写入流程...")
        print(f"  - 准备生成 {count} 条数据")

        # 检查索引存在性并创建（安全模式）
        self.create_index_and_mapping(force_create=force_create)

        # 生成数据
        print(f"  - 生成模拟数据中...")
        data_list = self.generate_mock_data(count)
        print(f"  - 数据生成完成")

        # 写入ES
        self.bulk_write(data_list)

        print(f"[{self.index_type}] 写入流程完成\n")


# ==================== 设备类 ====================
class DeviceIndexer(BaseESWriter):
    """设备数据写入器，支持多种设备类型"""

    # 设备类型字段映射（从JSON映射文件中提取）
    DEVICE_FIELDS = {
        'air': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                'device_code', 'device_number', 'device_subclass', 'device_type',
                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                'province_id', 'qr_code_no', 'qualitor', 'rated_cooling_capacity',
                'rated_input_power', 'rated_operating_voltage', 'related_room',
                'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],

        'battery': ['assets_no', 'backup_time', 'batch_num', 'cell_voltage_level',
                    'city_id', 'collect_time', 'county_id', 'device_code',
                    'device_number', 'device_subclass', 'device_type',
                    'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                    'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                    'province_id', 'qr_code_no', 'qualitor', 'ralated_power_device',
                    'related_room', 'related_site', 'res_code', 'reted_capacity',
                    'start_time', 'total_monomers_number', 'vendor_id', 'zh_label'],

        'ups': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                'device_code', 'device_number', 'device_subclass', 'device_type',
                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                'province_id', 'qr_code_no', 'qualitor', 'rated_capacity',
                'rated_output_voltage', 'related_room', 'related_site', 'related_system',
                'res_code', 'start_time', 'vendor_id', 'zh_label'],
    }

    def __init__(self, device_type: str = 'air', **kwargs):
        """
        初始化设备写入器
        :param device_type: 设备类型：air/battery/ups/...
        """
        self.device_type = device_type
        super().__init__(index_type=device_type, **kwargs)

        # 根据设备类型获取字段列表
        self.fields = self.DEVICE_FIELDS.get(device_type, [])
        if not self.fields:
            raise ValueError(f"不支持的设备类型: {device_type}")

        print(f"  - 设备类型: {device_type}")
        print(f"  - 字段数量: {len(self.fields)}")

    def _generate_field_value(self, field: str) -> Any:
        """根据字段名生成合适的模拟值"""
        if field.endswith('_id') or field.endswith('_code'):
            return f"{field.upper()}_{random.randint(1000, 9999)}"
        elif field.endswith('_time') or field.endswith('_date'):
            return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif field.endswith('_number') or field.endswith('_num'):
            return str(random.randint(1, 100))
        elif 'power' in field:
            return str(random.randint(10, 500))
        elif 'voltage' in field:
            return f"{random.randint(220, 380)}V"
        elif 'capacity' in field:
            return f"{random.randint(50, 500)}AH"
        elif field in ['lifecycle_status', 'maintainor', 'qualitor']:
            return random.choice(['active', 'inactive', 'maintenance'])
        elif field == 'province_id':
            return self.province_id
        elif field == 'city_id':
            return self.city_id
        elif field == 'batch_num':
            return self.batch_num
        elif field == 'collect_time':
            return datetime.now().strftime('%Y%m%d%H%M%S')
        elif field == 'zh_label':
            return f"{self.device_type}_{random.randint(1000, 9999)}"
        else:
            return f"mock_{field}_{random.randint(1, 100)}"

    def generate_mock_data(self, count: int = 100) -> List[Dict]:
        """生成设备模拟数据"""
        data_list = []

        for i in range(count):
            doc = {}
            for field in self.fields:
                doc[field] = self._generate_field_value(field)

            # 特殊字段修正
            if 'estimated_retirement_time' in doc:
                doc['estimated_retirement_time'] = (
                            datetime.now() + timedelta(days=random.randint(1000, 5000))).strftime('%Y-%m-%d')
            if 'start_time' in doc:
                doc['start_time'] = (datetime.now() - timedelta(days=random.randint(100, 1000))).strftime('%Y-%m-%d')

            data_list.append(doc)

        return data_list


# ==================== 房间类 ====================
class RoomIndexer(BaseESWriter):
    """房间数据写入器"""

    ROOM_FIELDS = [
        'address_code', 'airconditioner_power', 'alias_name', 'asset_address_code',
        'batch_num', 'business_unit', 'china_tower_operations_id', 'china_tower_room_type',
        'china_tower_station_code', 'city_id', 'collect_time', 'column_direction',
        'column_num', 'county_id', 'cutin_date', 'end_column', 'end_row',
        'equipment_power', 'equiproom_level', 'equiproom_type', 'fifth_generation_flag',
        'floor_num', 'height', 'if_tele_cmn_serv', 'if_village_pass_serv',
        'installed_rack_num', 'int_id', 'irms_province_code', 'is_headquarters_used',
        'length', 'lifecycle_status', 'loadable_rack_num', 'mainit_unit',
        'maintainor_method', 'plan_rack_num', 'pms_design_code', 'pms_design_name',
        'project_code', 'project_name', 'property_right', 'property_unit',
        'province_id', 'qr_code_no', 'qualitor', 'related_site', 'retire_time',
        'room_area', 'row_direction', 'row_num', 'shared_unit', 'start_column',
        'start_row', 'tele_cmn_serv_pro_code', 'tele_cmn_serv_pro_name', 'uuid',
        'village_pass_serv_code', 'village_pass_serv_name', 'width', 'zh_label'
    ]

    def __init__(self, **kwargs):
        super().__init__(index_type='room', **kwargs)

    def generate_mock_data(self, count: int = 100) -> List[Dict]:
        room_types = ['数据中心', '接入网', '核心网', '基站']
        levels = ['A级', 'B级', 'C级']

        data_list = []
        for i in range(count):
            doc = {
                'uuid': f"ROOM_{self.batch_num}_{random.randint(10000, 99999)}",
                'province_id': self.province_id,
                'city_id': self.city_id,
                'batch_num': self.batch_num,
                'collect_time': datetime.now().strftime('%Y%m%d%H%M%S'),
                'equiproom_type': random.choice(room_types),
                'equiproom_level': random.choice(levels),
                'room_area': f"{random.randint(50, 500)}㎡",
                'installed_rack_num': str(random.randint(10, 200)),
                'loadable_rack_num': str(random.randint(5, 150)),
                'lifecycle_status': random.choice(['active', 'inactive']),
                'zh_label': f"ROOM_{random.randint(1000, 9999)}",
                'length': f"{random.randint(10, 30)}m",
                'width': f"{random.randint(8, 20)}m",
                'height': f"{random.randint(3, 6)}m",
                'cutin_date': (datetime.now() - timedelta(days=random.randint(100, 2000))).strftime('%Y-%m-%d'),
            }

            # 填充其他字段
            for field in self.ROOM_FIELDS:
                if field not in doc:
                    doc[field] = f"mock_{field}_{random.randint(1, 100)}"

            data_list.append(doc)

        return data_list


# ==================== 站点类 ====================
class SiteIndexer(BaseESWriter):
    """站点数据写入器"""

    def __init__(self, **kwargs):
        super().__init__(index_type='site', **kwargs)

    def generate_mock_data(self, count: int = 100) -> List[Dict]:
        site_types = ['核心局站', '汇聚局站', '接入局站', '基站']
        business_types = ['电信', '联通', '移动', '铁塔']

        data_list = []
        for i in range(count):
            doc = {
                'uuid': f"SITE_{self.batch_num}_{random.randint(10000, 99999)}",
                'province_id': self.province_id,
                'city_id': self.city_id,
                'batch_num': self.batch_num,
                'collect_time': datetime.now().strftime('%Y%m%d%H%M%S'),
                'site_type': random.choice(site_types),
                'business_type': random.choice(business_types),
                'latitude': f"{random.uniform(30, 45):.6f}",
                'longitude': f"{random.uniform(100, 125):.6f}",
                'lifecycle_status': random.choice(['active', 'inactive']),
                'zh_label': f"SITE_{random.randint(1000, 9999)}",
                'address': f"XX省XX市XX区XX路{random.randint(1, 999)}号",
                'standardaddress': f"STD_ADDR_{random.randint(10000, 99999)}",
                'cutin_date': (datetime.now() - timedelta(days=random.randint(100, 3000))).strftime('%Y-%m-%d'),
            }

            # 填充其他字段
            for field in ['alias_name', 'area_type', 'china_tower_station_code',
                          'county_id', 'floor_number', 'int_id', 'irms_province_code',
                          'is_headquarters_used', 'pms_address_code', 'project_code',
                          'project_name', 'qualitor', 'related_dc', 'tele_cmn_serv_pro_code',
                          'tele_cmn_serv_pro_name', 'use_corp', 'village_pass_serv_code',
                          'village_pass_serv_name']:
                if field not in doc:
                    doc[field] = f"mock_{field}_{random.randint(1, 100)}"

            data_list.append(doc)

        return data_list


# ==================== 映射类 ====================
class IrmsMapIndexer(BaseESWriter):
    """IRMS映射数据写入器"""

    def __init__(self, map_type: str = 'dc', **kwargs):
        """
        :param map_type: 'dc' 或 'rom'
        """
        self.map_type = map_type
        super().__init__(index_type=f'irms_{map_type}_map', **kwargs)

    def generate_mock_data(self, count: int = 50) -> List[Dict]:
        data_list = []
        for i in range(count):
            doc = {
                'batch_num': self.batch_num,
                'province_id': self.province_id,
                'dh_id': f"DH{random.randint(10000, 99999)}",
                'dh_name': f"动环_{random.randint(1, 100)}",
                'pms_id': f"PMS{random.randint(10000, 99999)}",
                'pms_name': f"PMS系统_{random.randint(1, 100)}",
                'zg_id': f"ZG{random.randint(10000, 99999)}",
                'zg_name': f"资管系统_{random.randint(1, 100)}",
                'statis_ymd': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y%m%d'),
                'uuid': f"MAP_{self.batch_num}_{random.randint(10000, 99999)}",
            }

            if self.map_type == 'rom':
                doc['address_code'] = f"ADDR_{random.randint(10000, 99999)}"

            data_list.append(doc)

        return data_list


# ==================== 实用工具类 ====================
class ESWriterFactory:
    """简单工厂类，用于创建不同类型的写入器"""

    @staticmethod
    def create_writer(index_category: str, **kwargs) -> BaseESWriter:
        """
        创建写入器实例
        :param index_category: 索引类别，如 'air', 'battery', 'room', 'site', 'irms_dc_map', 'irms_rom_map'
        """
        category_map = {
            # 设备类
            'air': ('device', {'device_type': 'air'}),
            'battery': ('device', {'device_type': 'battery'}),
            'energy_save': ('device', {'device_type': 'energy_save'}),
            'high_dc_distribution': ('device', {'device_type': 'high_dc_distribution'}),
            'high_distribution': ('device', {'device_type': 'high_distribution'}),
            'high_power': ('device', {'device_type': 'high_power'}),
            'low_ac_distribution': ('device', {'device_type': 'low_ac_distribution'}),
            'low_dc_distribution': ('device', {'device_type': 'low_dc_distribution'}),
            'other': ('device', {'device_type': 'other'}),
            'power_generation': ('device', {'device_type': 'power_generation'}),
            'power_monitor': ('device', {'device_type': 'power_monitor'}),
            'switch_power': ('device', {'device_type': 'switch_power'}),
            'transform_device': ('device', {'device_type': 'transform_device'}),
            'transform': ('device', {'device_type': 'transform'}),
            'ups': ('device', {'device_type': 'ups'}),
            # 房间类
            'room': ('room', {}),
            'room_property': ('room_property', {}),
            # 站点类
            'site': ('site', {}),
            'site_property': ('site_property', {}),
            # 映射类
            'irms_dc_map': ('irms_map', {'map_type': 'dc'}),
            'irms_rom_map': ('irms_map', {'map_type': 'rom'}),
            # 连接类
            'link_pe_in': ('link', {}),
        }

        if index_category not in category_map:
            raise ValueError(f"不支持的索引类别: {index_category}")

        writer_type, extra_params = category_map[index_category]
        kwargs.update(extra_params)

        if writer_type == 'device':
            return DeviceIndexer(**kwargs)
        elif writer_type == 'room':
            return RoomIndexer(**kwargs)
        elif writer_type == 'room_property':
            # 可以扩展RoomPropertyIndexer
            return RoomIndexer(**kwargs)
        elif writer_type == 'site':
            return SiteIndexer(**kwargs)
        elif writer_type == 'site_property':
            # 可以扩展SitePropertyIndexer
            return SiteIndexer(**kwargs)
        elif writer_type == 'irms_map':
            return IrmsMapIndexer(**kwargs)
        elif writer_type == 'link':
            # 可以扩展LinkIndexer
            return BaseESWriter(index_type='link_pe_in', **kwargs)
        else:
            raise ValueError(f"未知的写入器类型: {writer_type}")


# ==================== 使用示例 ====================
if __name__ == '__main__':
    """
    使用示例：
    1. 直接实例化具体类（安全模式，默认不覆盖）
    2. 使用工厂类创建（安全模式，默认不覆盖）
    3. 强制重建模式（谨慎使用）
    """

    print("=" * 80)
    print("示例1: 安全写入 - 索引不存在时创建，存在时追加数据")
    print("=" * 80)

    # 首次运行：索引不存在，会自动创建
    air_writer = DeviceIndexer(
        device_type='air',
        province_id='01',
        city_id='0101',
        date='20250723',
        batch_num='BATCH_001'
    )
    air_writer.write(count=50)

    # 第二次运行：索引已存在，直接追加数据
    print("\n第二次运行：索引已存在，追加数据...")
    air_writer.write(count=30)

    print("=" * 80)
    print("示例2: 使用工厂创建 - 追加模式")
    print("=" * 80)

    room_writer = ESWriterFactory.create_writer(
        'room',
        province_id='03',
        city_id='0301',
        date='20250723',
        batch_num='BATCH_003'
    )
    room_writer.write(count=40)

    print("=" * 80)
    print("示例3: 危险操作 - 强制重建索引（⚠️ 会删除已有数据）")
    print("=" * 80)

    # 警告：这将删除索引并重建，所有现有数据会丢失！
    ups_writer = DeviceIndexer(
        device_type='ups',
        province_id='02',
        city_id='0201',
        date='20250723',
        batch_num='BATCH_002'
    )
    # 第一次：正常创建
    ups_writer.write(count=20)

    # 第二次：强制重建（删除后重建）
    print("\n强制重建索引（删除已有数据）...")
    ups_writer.write(count=10, force_create=True)

    print("=" * 80)
    print("示例4: 批量创建多种设备（安全模式）")
    print("=" * 80)

    device_types = ['battery', 'switch_power', 'transform']
    for dev_type in device_types:
        writer = ESWriterFactory.create_writer(
            dev_type,
            province_id='05',
            city_id='0501',
            date='20250723',
            batch_num=f'BATCH_{dev_type.upper()}'
        )
        writer.write(count=25)
        print(f"  ✅ {dev_type} 数据写入完成\n")

    print("=" * 80)
    print("示例5: 写入IRMS映射数据")
    print("=" * 80)

    dc_map_writer = IrmsMapIndexer(
        map_type='dc',
        province_id='06',
        batch_num='BATCH_DC_MAP'
    )
    dc_map_writer.write(count=30)

    rom_map_writer = IrmsMapIndexer(
        map_type='rom',
        province_id='06',
        batch_num='BATCH_ROM_MAP'
    )
    rom_map_writer.write(count=30)

    print("=" * 80)
    print("所有示例执行完成！")
    print("=" * 80)
    print("\n总结：")
    print("  ✅ 默认模式：索引不存在时创建，存在时追加数据（安全）")
    print("  ⚠️  force_create=True：强制删除重建（会丢失数据）")
    print("  💡 建议：生产环境务必使用默认模式，仅在测试环境使用强制重建")