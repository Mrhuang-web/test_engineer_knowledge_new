# mock_es_writer_v3.py
"""
ES数据模拟写入工具 - 安全版本 + 精确索引命名规则
支持设备、房间、站点等多种索引类型，自动检查索引存在性
索引命名严格遵循业务规则
"""

import json
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from elasticsearch import Elasticsearch, helpers
from spider_tools.Conf.Config import Config
from urllib.parse import quote_plus as urlquote
from sqlalchemy import *


# ==================== 配置类 ====================
class ESConfig:
    """ES配置管理"""
    # ES_URL = "http://localhost:9200"  # 修改为实际ES地址
    ES_URL = "http://10.1.203.38:9200"  # 修改为实际ES地址
    INDEX_SETTINGS = {
        "index": {
            "number_of_replicas": "0",
            "refresh_interval": "5s"
        }
    }

    # 实际索引名格式
    INDEX_PREFIX_MAP = {
        # 设备类 - 年月+m
        'air': 'ods_zz_device_air',
        'battery': 'ods_zz_device_battery',
        'low_ac_distribution': 'ods_zz_device_low_ac_distribution',
        'switch_power': 'ods_zz_device_switch_power',
        'link_pe_in': 'ods_zz_link_pe_in',

        # 设备类 - 年+y
        'energy_save': 'ods_zz_device_energy_save',
        'high_dc_distribution': 'ods_zz_device_high_dc_distribution',
        'high_distribution': 'ods_zz_device_high_distribution',
        'high_power': 'ods_zz_device_high_power',
        'smart_meter': 'ods_zz_device_smart_meter',
        'transform': 'ods_zz_device_transform',
        'transform_device': 'ods_zz_device_transform_device',
        'ups': 'ods_zz_device_ups',

        # 映射类 - 年+y
        'irms_dc_map': 'ods_zz_irms_dc_map',
        'irms_rom_map': 'ods_zz_irms_rom_map',
        'irms_site_map': 'ods_zz_irms_site_map',

        # 房间类 - 年月日+d
        'room': 'ods_zz_room',

        # 房间属性类 - 年月+m
        'room_property': 'ods_zz_room_property',

        # 站点类 - 年月+m
        'site': 'ods_zz_site',
        'site_property': 'ods_zz_site_property',
    }

    # 索引后缀格式规则
    INDEX_SUFFIX_RULES = {
        # 年月+m
        'YYYYMMm': ['air', 'battery', 'low_ac_distribution', 'switch_power',
                    'room_property', 'site', 'site_property', 'link_pe_in'],
        # 年+y
        'YYYYy': ['energy_save', 'high_dc_distribution', 'high_distribution',
                  'high_power', 'smart_meter', 'transform', 'transform_device', 'ups',
                  'irms_dc_map', 'irms_rom_map', 'irms_site_map'],
        # 年月日+d
        'YYYYMMDDd': ['room'],
    }


# ==================== 基类 ====================
class BaseESWriter:
    """ES写入基类"""

    def __init__(self, index_type: str, env: str = 'release', **kwargs):
        self.index_type = index_type
        self.env = env

        # 默认插入当天批次 - 贵州 - 安顺市 - 通信枢纽楼
        self.site_type = kwargs.get('site_type', '核心站点')
        self.irms_province_code = kwargs.get('irms_province_code', 'GZ')
        self.batch_num = kwargs.get('batch_num', f"BATCH_{datetime.now().strftime('%Y%m%d')}")
        self.related_dc = kwargs.get('related_dc', f"")
        self.zh_label = kwargs.get('zh_label', f"test_zh_label_{datetime.now().strftime('%Y%m%d')}")
        self.county_id = kwargs.get('city_id', '000000')
        self.province_id = kwargs.get('province_id', '520000')
        self.city_id = kwargs.get('city_id', '520400')
        self.date = kwargs.get('date', datetime.now().strftime('%Y%m%d'))
        self.site_int_id = kwargs.get('site_int_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.site_res_code = kwargs.get('site_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))

        self.es = Elasticsearch(ESConfig.ES_URL)
        self.index_name = self._get_index_name()
        self.doc_type = "point_history_data"

        print(f"[{self.__class__.__name__}] 初始化完成")
        print(f"  - 索引类型: {self.index_type}")
        print(f"  - 索引名称: {self.index_name}")
        print(f"  - 环境: {self.env}")
        print(f"  - 批次号: {self.batch_num}")

    def _get_index_name(self) -> str:
        """生成符合业务规则索引名称"""
        prefix = ESConfig.INDEX_PREFIX_MAP.get(self.index_type)
        if not prefix:
            raise ValueError(f"未知的索引类型: {self.index_type}")

        # 根据规则生成后缀
        now = datetime.now()
        for suffix_format, types in ESConfig.INDEX_SUFFIX_RULES.items():
            if self.index_type in types:
                if suffix_format == 'YYYYMMm':
                    if self.batch_num and len(self.batch_num) >= 6:
                        suffix = self.batch_num[:6] + 'm'
                    else:
                        suffix = now.strftime('%Y%m') + 'm'
                elif suffix_format == 'YYYYy':
                    if self.batch_num and len(self.batch_num) >= 6:
                        suffix = self.batch_num[:4] + 'y'
                    else:
                        suffix = now.strftime('%Y') + 'y'
                elif suffix_format == 'YYYYMMDDd':
                    # 使用传入的date参数或当前日期
                    if self.batch_num and len(self.batch_num) >= 6:
                        suffix = self.batch_num + 'd'
                    else:
                        suffix = self.date + 'd'
                else:
                    suffix = self.date
                break
        else:
            # 默认使用日期
            suffix = self.date

        return f"{prefix}_{suffix}"

    def create_index_and_mapping(self, mapping: Optional[Dict] = None, force_create: bool = False):
        """创建索引和mapping（安全模式）"""
        try:
            index_exists = self.es.indices.exists(index=self.index_name)

            if index_exists:
                if force_create:
                    print(f"BaseESWriter_create_index_and_mapping:强制删除并重建索引: {self.index_name}")
                    print(f"该操作将删除索引中所有现有数据！")
                    self.es.indices.delete(index=self.index_name, ignore=[400, 404])
                else:
                    print(f"索引已存在，将追加数据: {self.index_name}")

                    # 获取当前索引文档数量
                    try:
                        stats = self.es.count(index=self.index_name)
                        print(f"当前文档数: {stats.get('count', 0):,} 条")
                    except:
                        pass

                    print(f"提示：如需强制重建，请设置 force_create=True")
                    return  # 直接返回，不创建索引

            # 索引不存在，或已删除准备重建
            print(f"创建索引: {self.index_name}")
            self.es.indices.create(index=self.index_name, ignore=[400])

            # 设置索引配置
            self.es.indices.put_settings(
                index=self.index_name,
                body=ESConfig.INDEX_SETTINGS
            )

            # 设置mapping
            if mapping:
                mapping_body = {self.doc_type: mapping}
                self.es.indices.put_mapping(
                    index=self.index_name,
                    doc_type=self.doc_type,
                    body=mapping_body
                )
                print(f"Mapping已创建")

            print(f"索引创建成功: {self.index_name}")

        except Exception as e:
            print(f"索引创建失败: {str(e)}")
            raise

    def bulk_write(self, data_list: List[Dict]):
        """批量写入数据"""
        if not data_list:
            print("  - 无数据需要写入")
            return
        print('self.index_name:', self.index_name)
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
            print(f"写入成功: {success}条, 失败: {failed}条")

            # 写入后显示总数
            try:
                stats = self.es.count(index=self.index_name)
                print(f"索引总文档数: {stats.get('count', 0):,} 条")
            except:
                pass

            self.es.indices.refresh(index=self.index_name)
        except Exception as e:
            print(f"批量写入失败: {str(e)}")

    def generate_mock_data(self, count: int = 100) -> List[Dict]:
        """生成模拟数据（子类必须实现）"""
        raise NotImplementedError("子类必须实现generate_mock_data方法")

    def write(self, count: int = 100, force_create: bool = False):
        """
        完整流程：生成数据并写入
        :param count: 生成数据条数
        :param force_create: 是否强制重建索引（危险操作）
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
    """设备数据写入器"""

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

        'smart_meter': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                        'device_code', 'device_number', 'device_subclass', 'device_type',
                        'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                        'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                        'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                        'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
    }

    def __init__(self, device_type: str = 'air', **kwargs):
        self.device_type = device_type
        super().__init__(index_type=device_type, **kwargs)

        self.fields = self.DEVICE_FIELDS.get(device_type, [])
        if not self.fields:
            # 如果设备类型不在预定义列表中，使用通用字段
            self.fields = ['assets_no', 'batch_num', 'city_id', 'collect_time',
                           'device_code', 'device_number', 'province_id', 'zh_label']
            print(f"  ⚠️  设备类型 '{device_type}' 未预定义字段，使用通用字段")

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


class RoomPropertyIndexer(BaseESWriter):
    """房间属性写入器"""

    def __init__(self, **kwargs):
        super().__init__(index_type='room_property', **kwargs)

    def generate_mock_data(self, count: int = 100) -> List[Dict]:
        data_list = []
        for i in range(count):
            doc = {
                'batch_num': self.batch_num,
                'province_id': self.province_id,
                'city_id': self.city_id,
                'collect_time': datetime.now().strftime('%Y%m%d%H%M%S'),
                'power_room_id': f"PR_{random.randint(10000, 99999)}",
                'power_room_name': f"电力室_{random.randint(1, 100)}",
                'power_supply_mode': random.choice(['单路', '双路', '三路']),
                'battery_backup_time': f"{random.randint(1, 24)}小时",
                'ac_config': random.choice(['中央空调', '精密空调', '普通空调']),
                'zh_label': f"ROOM_PROP_{random.randint(1000, 9999)}",
            }

            # 填充其他字段
            for field in ['ac_terminal', 'county_id', 'irms_province_code',
                          'log_saved_time', 'power_related_site_name', 'power_room_type',
                          'power_supply_type', 'refer_pue', 'refrigeration_mode',
                          'res_code', 'space_room_type', 'video_monitor_conf']:
                if field not in doc:
                    doc[field] = f"mock_{field}_{random.randint(1, 100)}"

            data_list.append(doc)

        return data_list


# ==================== 站点类 ====================
class SiteIndexer(BaseESWriter):
    """
        站点数据写入器
        名称匹配法：
            建立动环与综资的映射关系 - 为关联提供前置条件：
                (动环)precinct_name -> (site空间)zh_label
                (site空间)int_id -> (property)zh_label
        id匹配法：
            建立动环与综资的映射关系 - 关联动环综资站点的后置处理：
                (动环)site_int_id -> (site空间)int_id
                (site空间)int_id -> (property)zh_label
    """

    def __init__(self, **kwargs):
        super().__init__(index_type='site', **kwargs)

    def generate_mock_data(self, count: int = 100) -> List[Dict]:
        site_types = ['核心局站', '汇聚局站', '接入局站', '基站']
        business_types = ['电信', '联通', '移动', '铁塔']

        data_list = []
        for i in range(count):
            doc = {
                'china_tower_station_code': f"mock_{'china_tower_station_code'}_{random.randint(1, 100)}",
                'address': f"XX省XX市XX区XX路{random.randint(1, 999)}号",
                'site_type': self.site_type,
                'cutin_date': (datetime.now() - timedelta(days=random.randint(100, 3000))).strftime('%Y-%m-%d'),
                'latitude': f"{random.uniform(30, 45):.6f}",
                'irms_province_code': self.irms_province_code,
                'floor_number': f"{random.randint(1, 20)}",
                'batch_num': self.batch_num,
                'related_dc': self.related_dc,
                'alias_name': f"{self.zh_label}",
                'standardaddress': f"{random.randint(10000, 99999)}",
                'zh_label': self.zh_label,
                'county_id': f"{random.randint(100000, 500000)}",
                'province_id': self.province_id,
                'int_id': self.site_int_id,
                'qualitor': f"测试记录",
                'lifecycle_status': f"在网",
                'use_corp': f"中国移动",
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city_id': self.city_id,
                'longitude': f"{random.uniform(100, 125):.6f}",
            }

            # #填充其他字段
            # for field in ['alias_name', 'area_type', 'china_tower_station_code',
            #               'county_id', 'floor_number', 'int_id', 'irms_province_code',
            #               'is_headquarters_used', 'pms_address_code', 'project_code',
            #               'project_name', 'qualitor', 'related_dc', 'tele_cmn_serv_pro_code',
            #               'tele_cmn_serv_pro_name', 'use_corp', 'village_pass_serv_code',
            #               'village_pass_serv_name']:
            #     if field not in doc:
            #         doc[field] = f"mock_{field}_{random.randint(1, 100)}"

            data_list.append(doc)

        return data_list


class SitePropertyIndexer(BaseESWriter):
    """
        站点数据写入器
        建立动环与综资的映射关系 - 关联动环综资站点的后置处理：
            (动环)precinct_name -> (site空间)zh_label
            (site空间)int_id -> (property)zh_label
    """

    def __init__(self, **kwargs):
        super().__init__(index_type='site_property', **kwargs)

    def generate_mock_data(self, count: int = 100) -> List[Dict]:
        print("self.site_int_id3:", self.site_int_id)
        data_list = []
        for i in range(count):
            doc = {
                'mains_nature': f"市电直供",
                'cold_storage_time': f"",
                'property_unit': f"",
                'water_cooling_conf': f"",
                'county_id': f"{random.randint(100000, 999999)}",
                'power_is_substations': f"{random.choice(['是', '否'])}",
                'mains_configuration_level': f"{random.choice(['1市电无油机'])}",
                'total_mains_number': f"{random.choice(['1', '0'])}",
                'tatal_tank_volume': f"",
                'is_attach_idc_room': f"{random.choice(['是', '否'])}",
                'power_site_level': f"{random.choice(['通信基站', '核心站点'])}",
                'irms_province_code': self.irms_province_code,
                'is_cold_storage_install': f"",
                'batch_num': self.batch_num,
                'mains_voltage_level': f"{random.randint(1, 10)}V",
                'res_code': self.site_res_code,
                'zh_label': self.site_int_id,
                'mains_capacity': f"{random.randint(100, 1000)}KVA",
                'power_supply': f"{random.choice(['其他'])}",
                'province_id': self.province_id,
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'design_pue': f"{random.uniform(1.2, 1.8):.2f}",
                'actual_pue': f"{random.uniform(1.3, 2.0):.2f}",
                'city_id': self.city_id,
            }

            # #填充其他字段
            # for field in ['cold_storage_time', 'county_id', 'irms_province_code',
            #               'is_attach_idc_room', 'is_cold_storage_install', 'mains_backup_method',
            #               'mains_configuration_level', 'mains_nature', 'power_is_substations',
            #               'power_monitoring_site_id', 'power_monitoring_site_name', 'power_site_level',
            #               'power_supply', 'property_unit', 'res_code', 'tatal_tank_volume',
            #               'total_mains_number', 'total_tank_number', 'water_cooling_conf']:
            #     if field not in doc:
            #         doc[field] = f"mock_{field}_{random.randint(1, 100)}"

            data_list.append(doc)
        return data_list


# ==================== 映射类 ====================
class IrmsMapIndexer(BaseESWriter):
    """IRMS映射数据写入器"""

    def __init__(self, map_type: str = 'dc', **kwargs):
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


# ==================== 工厂类 ====================
class ESWriterFactory:
    """简单工厂类"""

    @staticmethod
    def create_writer(index_category: str, **kwargs) -> BaseESWriter:
        """
        创建写入器实例
        :param index_category: 索引类别字符串
        """
        # 映射表：索引类别 -> (创建器类型, 额外参数)
        category_map = {
            # 设备类 - 年月+m
            'air': ('device', {'device_type': 'air'}),
            'battery': ('device', {'device_type': 'battery'}),
            'low_ac_distribution': ('device', {'device_type': 'low_ac_distribution'}),
            'switch_power': ('device', {'device_type': 'switch_power'}),

            # 设备类 - 年+y
            'energy_save': ('device', {'device_type': 'energy_save'}),
            'high_dc_distribution': ('device', {'device_type': 'high_dc_distribution'}),
            'high_distribution': ('device', {'device_type': 'high_distribution'}),
            'high_power': ('device', {'device_type': 'high_power'}),
            'smart_meter': ('device', {'device_type': 'smart_meter'}),
            'transform': ('device', {'device_type': 'transform'}),
            'transform_device': ('device', {'device_type': 'transform_device'}),
            'ups': ('device', {'device_type': 'ups'}),

            # 映射类 - 年+y
            'irms_dc_map': ('irms_map', {'map_type': 'dc'}),
            'irms_rom_map': ('irms_map', {'map_type': 'rom'}),
            'irms_site_map': ('irms_map', {'map_type': 'site'}),

            # 连接类 - 年月+m
            'link_pe_in': ('link', {}),

            # 房间类 - 年月日+d
            'room': ('room', {}),

            # 房间属性类 - 年月+m
            'room_property': ('room_property', {}),

            # 站点类 - 年月+m
            'site': ('site', {}),
            'site_property': ('site_property', {}),
        }

        if index_category not in category_map:
            raise ValueError(f"❌ 不支持的索引类别: {index_category}")

        writer_type, extra_params = category_map[index_category]
        kwargs.update(extra_params)

        # 创建对应的写入器实例
        if writer_type == 'device':
            return DeviceIndexer(**kwargs)
        elif writer_type == 'room':
            return RoomIndexer(**kwargs)
        elif writer_type == 'room_property':
            return RoomPropertyIndexer(**kwargs)
        elif writer_type == 'site':
            return SiteIndexer(**kwargs)
        elif writer_type == 'site_property':
            return SitePropertyIndexer(**kwargs)
        elif writer_type == 'irms_map':
            return IrmsMapIndexer(**kwargs)
        elif writer_type == 'link':
            # 可以扩展LinkIndexer
            return BaseESWriter(index_type='link_pe_in', **kwargs)
        else:
            raise ValueError(f"未知的写入器类型: {writer_type}")


class ESZzMatchSpider:
    def __init__(self, precinct_id, mete_code='000000', MinVal=1, MaxVal=1, device_id='1', del_col='meteID',
                 del_clo_v='1', EsTime='T23:50:50', env='release'):
        self.esWrite = ESWriterFactory
        self.date = '20251103'
        self.batch_num = '20251103'
        self.is_test = True
        self.zh_label = '贵州贵通信枢纽楼22正常'
        self.site_int_id = None
        self.precinct_id = precinct_id
        self.mete_code = mete_code
        self.EsTime = EsTime
        self.MinVal = MinVal
        self.MaxVal = MaxVal
        self.device_id = device_id
        self.env = env
        self.mysql_connect = MysqlConnect(precinct_id=self.precinct_id)
        self.site_name = []
        self.site_int_id = None
        self.province = None
        self.city = None

    def name_match_site(self, Precinct_id=None):
        data = self.mysql_connect.insert_esdata_device()
        for iter in data:
            if iter[18] not in self.site_name:
                self.site_name.append(iter[18])
                siteIndexer = self.esWrite.create_writer('site', batch_num=self.batch_num,
                                                         zh_label=iter[18], )
                self.site_int_id = siteIndexer.site_int_id
                self.province = siteIndexer.province_id
                self.city = siteIndexer.city_id
                siteIndexer.write(count=1)
                sitePropertyIndexer = self.esWrite.create_writer('site_property', batch_num=self.batch_num,
                                                                 site_int_id=self.site_int_id,
                                                                 province_id=self.province,
                                                                 city=self.city)
                sitePropertyIndexer.write(count=1)
            else:
                print("站点已存在，无需重复写入:", iter[18])
                break


class MysqlConnect:
    import datetime
    def __init__(self, precinct_id,
                 mete_code='000000',
                 ImDate=datetime.datetime.now().strftime('%Y-%m-%d'), MinVal=1, MaxVal=1, device_id='1',
                 del_col='meteID', del_clo_v='1', EsTime='T23:50:50', env='release'):
        conf = Config()

        self.precinct_id = precinct_id
        self.mete_code = mete_code
        self.EsTime = EsTime
        self.MinVal = MinVal
        self.MaxVal = MaxVal
        self.device_id = device_id
        self.del_col = del_col
        self.del_col_v = del_clo_v
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        self.url = conf.get_conf(env, 'esurl')
        engines = "mysql+pymysql://" + urlquote(self.dbuser) + ":" + urlquote(self.dbpw) + \
                  "@" + self.dbip + ":" + self.dbport + "/" + urlquote(self.dbname) + "?charset=utf8"
        EnGine = create_engine(engines, max_overflow=5)
        self.conn = EnGine.connect()
        self.SqlFile = open(str(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) +
                                '\\Common\\SQL' + '\\selectForESList.sql'), encoding='utf-8')

    def insert_esdata_device(self, flush=True):
        # 生成特定区域的某个测点的数据:return:
        if self.device_id == '1' and self.mete_code == '000000':
            # 未传入设备就向该区域下所有设备下的该测点写入数据
            print("机房全量查询未传设备==========")
            r = self.get_provincedata(4)
        else:
            # 机房全量查询
            print("机房全量查询==========")
            r = self.get_provincedata(0)

        # if self.device_id == '1':
        #     # 未传入设备就向该区域下所有设备下的该测点写入数据
        #     r = self.get_provincedata(2)
        # else:
        #     # 已经传入设备
        #     r = self.get_provincedata(1)
        actions = []
        print("预计写入数据条数==========", len(r))
        for i in r:
            l = list(i)
            if not l:
                break
            print("l:", l)
        return r

    def get_sql_list(self):
        # 读取到预设sql

        f = self.SqlFile
        # print("sql文件位置--------------,",f)
        line = f.readline()
        sqlall = ''
        while line:
            sqlall = sqlall + line.strip("\n").strip("\t")
            line = f.readline()
        sqlalllist = sqlall.split(';')
        return sqlalllist

    def get_provincedata(self, SqlIndex):
        """
        获取数据库特定区域下的某个测点相关数据
        :return:
        """
        sqlalllist = self.get_sql_list()  # 获取预设sql
        if SqlIndex == 1:
            result = self.conn.execute(
                text(sqlalllist[SqlIndex]),
                {'precinct_id': self.precinct_id + '%', 'mete_code': self.mete_code, 'device_id': self.device_id})
        elif SqlIndex == 2:
            result = self.conn.execute(text(sqlalllist[SqlIndex]),
                                       {'precinct_id': self.precinct_id + '%', 'mete_code': self.mete_code})
        elif SqlIndex == 0:
            result = self.conn.execute(
                text(sqlalllist[SqlIndex]),
                {'precinct_id': self.precinct_id + '%'})
        elif SqlIndex == 4:
            result = self.conn.execute(
                text(sqlalllist[SqlIndex]),
                {'precinct_id': self.precinct_id + '%'})
        else:
            print("其他")
        row = result.fetchall()
        return row


# ==================== 使用示例 ====================
if __name__ == '__main__':
    print("=" * 80)
    print("ES数据模拟写入工具 - 精确命名规则版本")
    print("=" * 80)
    print("\n索引命名规则：")
    print("  - 年月+m: air, battery, low_ac_distribution, switch_power, link_pe_in")
    print("  - 年月+m: room_property, site, site_property")
    print("  - 年+y: energy_save, high_dc_distribution, high_distribution, high_power")
    print("  - 年+y: smart_meter, transform, transform_device, ups")
    print("  - 年+y: irms_dc_map, irms_rom_map, irms_site_map")
    print("  - 年月日+d: room")

    # 示例1：年月+m 格式设备
    print("\n" + "=" * 80)
    print("示例1: 空调设备 (ods_zz_device_air_202507m)")
    print("=" * 80)
    air_writer = DeviceIndexer(
        device_type='air',
        province_id='01',
        city_id='0101',
        batch_num='BATCH_AIR_001'
    )
    air_writer.write(count=30)

    # 示例2：年+y 格式设备
    print("\n" + "=" * 80)
    print("示例2: UPS设备 (ods_zz_device_ups_2025y)")
    print("=" * 80)
    ups_writer = DeviceIndexer(
        device_type='ups',
        province_id='02',
        city_id='0201',
        batch_num='BATCH_UPS_001'
    )
    ups_writer.write(count=20)

    # 示例3：年月日+d 格式房间
    print("\n" + "=" * 80)
    print("示例3: 房间数据 (ods_zz_room_20250723d)")
    print("=" * 80)
    room_writer = RoomIndexer(
        province_id='03',
        city_id='0301',
        date='20250723',
        batch_num='BATCH_ROOM_001'
    )
    room_writer.write(count=25)

    # 示例4：年月+m 格式房间属性
    print("\n" + "=" * 80)
    print("示例4: 房间属性 (ods_zz_room_property_202507m)")
    print("=" * 80)
    room_prop_writer = RoomPropertyIndexer(
        province_id='03',
        city_id='0301',
        batch_num='BATCH_RMPROP_001'
    )
    room_prop_writer.write(count=15)

    # 示例5：年月+m 格式站点
    print("\n" + "=" * 80)
    print("示例5: 站点数据 (ods_zz_site_202507m)")
    print("=" * 80)
    site_writer = SiteIndexer(
        province_id='04',
        city_id='0401',
        batch_num='BATCH_SITE_001'
    )
    site_writer.write(count=35)

    # 示例6：年+y 格式映射
    print("\n" + "=" * 80)
    print("示例6: IRMS站点映射 (ods_zz_irms_site_map_2025y)")
    print("=" * 80)
    site_map_writer = IrmsMapIndexer(
        map_type='site',
        province_id='05',
        batch_num='BATCH_SITEMAP_001'
    )
    site_map_writer.write(count=20)

    # 示例7：工厂模式批量创建
    print("\n" + "=" * 80)
    print("示例7: 工厂模式批量创建设备")
    print("=" * 80)

    device_list = [
        ('battery', '06', '0601'),
        ('smart_meter', '07', '0701'),
        ('transform', '08', '0801'),
    ]

    for dev_type, province, city in device_list:
        print(f"\n创建 {dev_type} 数据...")
        writer = ESWriterFactory.create_writer(
            dev_type,
            province_id=province,
            city_id=city,
            batch_num=f'BATCH_{dev_type.upper()}'
        )
        writer.write(count=15)

    print("\n" + "=" * 80)
    print("✅ 所有示例执行完成！")
    print("=" * 80)
