# mock_es_writer_optimized.py
"""
ES数据模拟写入工具 - 优化版
保留所有业务逻辑，消除重复代码，提升可维护性
"""

import json
import os
import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from elasticsearch import Elasticsearch, helpers
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus as urlquote
from spider_tools.Conf.Config import Config


# ==================== 配置管理 ====================
class ESConfig:
    """ES配置集中管理"""
    ES_URL = "http://10.1.203.38:9200"

    # 索引前缀映射（保留原始全部）
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

    # 索引后缀规则（保留原始全部）
    INDEX_SUFFIX_RULES = {
        'YYYYMMm': ['air', 'battery', 'low_ac_distribution', 'switch_power',
                    'room_property', 'site', 'site_property', 'link_pe_in'],
        'YYYYy': ['energy_save', 'high_dc_distribution', 'high_distribution',
                  'high_power', 'smart_meter', 'transform', 'transform_device', 'ups',
                  'irms_dc_map', 'irms_rom_map', 'irms_site_map'],
        'YYYYMMDDd': ['room'],
    }

    INDEX_SETTINGS = {
        "index": {
            "number_of_replicas": "0",
            "refresh_interval": "5s"
        }
    }


# ==================== 设备类型映射器（用于匹配动环设备与索引映射） ====================
class DeviceTypeMapper:
    """设备类型到索引类型的映射器"""

    # 用户提供的映射关系
    DEVICE_TYPE_MAP = {
        # 高压配电
        '1': 'high_distribution',
        # 低压交流配电
        '2': 'low_ac_distribution',
        '96': 'low_ac_distribution',
        # 变压器
        '3': 'transform',
        # 低压直流配电
        '4': 'low_dc_distribution',  # 原配置中未包含，需补充
        # 发电机组
        '5': 'power_generation',  # 注意：原配置中未包含，需补充
        # 开关电源
        '6': 'switch_power',
        # 蓄电池
        '68': 'battery',
        '7': 'battery',
        # ups设备
        '8': 'ups',
        # 空调设备
        '11': 'air',
        '12': 'air',
        '13': 'air',
        '15': 'air',
        # 变换设备
        '14': 'transform_device',
        # 动环监控
        '17': 'power_monitor',  # 原配置中未包含，需补充
        '76': 'power_monitor',  # 原配置中未包含，需补充
        '93': 'power_monitor',  # 原配置中未包含，需补充
        # 节能设备
        '18': 'energy_save',
        '77': 'energy_save',
        '78': 'energy_save',
        # 高压直流电源
        '87': 'high_power',
        # 高压直流配电
        '88': 'high_dc_distribution',
        # 智能电表
        '92': 'smart_meter',
        # 其他设备
        '16': 'other',  # 原配置中未包含，需补充
        '94': 'other',  # 原配置中未包含，需补充
    }

    @staticmethod
    def get_index_type(device_type_str: str) -> str:
        """
        根据设备类型字符串返回对应的索引类型
        :param device_type_str: 如 'CDU', '空调', 'UPS设备'
        :return: 如 'air', 'ups', 'battery'
        """
        # 先尝试直接匹配
        index_type = DeviceTypeMapper.DEVICE_TYPE_MAP.get(device_type_str)
        if index_type:
            return index_type
        # 默认返回 other
        print(f"未找到设备类型 '{device_type_str}' 的映射，使用默认索引类型 'other'")
        return 'other'


# ==================== 基础写入器 ====================
class BaseWriter:
    """统一的基础写入器 - 合并原始BaseESWriter功能"""

    def __init__(self, index_type: str, **kwargs):
        self.index_type = index_type
        self.es = Elasticsearch(ESConfig.ES_URL)
        self.doc_type = "point_history_data"
        # 保留所有原始业务参数
        self._load_business_params(kwargs)

        # 生成索引名
        self.index_name = self._generate_index_name()

        print(f"[{self.__class__.__name__}] 初始化完成")
        print(f"  - 索引类型: {self.index_type}")
        print(f"  - 索引名称: {self.index_name}")

    def _load_business_params(self, kwargs: Dict[str, Any]):
        """加载业务参数 - 保留原始全部参数"""

        # 站点相关
        self.site_type = kwargs.get('site_type', '核心站点')
        self.irms_province_code = kwargs.get('irms_province_code', 'GZ')
        self.batch_num = kwargs.get('batch_num', f"BATCH_{datetime.now().strftime('%Y%m%d')}")
        self.related_dc = kwargs.get('related_dc', "")
        self.zh_label = kwargs.get('zh_label', f"test_{datetime.now().strftime('%Y%m%d')}")

        # 地域相关
        self.county_id = kwargs.get('county_id', '000000')
        self.province_id = kwargs.get('province_id', '520000')
        self.city_id = kwargs.get('city_id', '520400')

        # 时间相关
        self.date = kwargs.get('date', datetime.now().strftime('%Y%m%d'))

        # ID相关
        self.site_int_id = kwargs.get('site_int_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.room_int_id = kwargs.get('room_int_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.site_res_code = kwargs.get('site_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.room_res_code = kwargs.get('room_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.site_zg_id = kwargs.get('site_zg_id', f"ZG_{random.randint(1000, 9999)}")
        self.site_dh_id = kwargs.get('site_dh_id', f"DH_{random.randint(1000, 9999)}")

        # 机房相关
        self.room_zh_label = kwargs.get('room_zh_label', f"ROOM_{random.randint(1000, 9999)}")
        self.room_dh_name = kwargs.get('room_dh_name', f"DH_{random.randint(1000, 9999)}")
        self.room_zg_name = kwargs.get('room_zg_name', f"ZG_{random.randint(1000, 9999)}")

        # 设备相关
        self.power_device_id = kwargs.get('power_device_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.device_res_code = kwargs.get('device_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.device_zh_label = kwargs.get('device_zh_label', f"device_{random.randint(1000, 9999)}")

        # 扩充 - 其他业务参数可继续添加（汇聚机房）
        self.cutin_date = kwargs.get('cutin_date', datetime.now().strftime('%Y-%m-%d'))
        self.mains_nature = kwargs.get('mains_nature', random.choice(['市电转供', '市电直供', '其他']))
        self.power_site_level = kwargs.get('power_site_level',
                                           random.choice(['通信机楼', '数据中心', '传输节点', '通信基站']))
        self.power_room_type = kwargs.get('power_room_type',
                                          random.choice(['传输机房', '交换机房', '数据机房', '汇聚机房']))
        self.power_supply_mode = kwargs.get('power_supply_mode',
                                            random.choice(['双电源双回路供电', '单电源双回路供电', '其他']))
        self.site_type = kwargs.get('site_type', random.choice(
            ['核心站点', '核心站点（配套）', '骨干站点', '汇聚站点', '接入站点', '用户站点', '其他站点']))
        self.power_related_site_name = kwargs.get('power_related_site_name', f"site_{random.randint(1000, 9999)}")

    def _generate_index_name(self) -> str:
        """生成索引名 - 保留原始复杂逻辑"""
        prefix = ESConfig.INDEX_PREFIX_MAP.get(self.index_type)
        if not prefix:
            raise ValueError(f"未知的索引类型: {self.index_type}")

        # 根据业务规则生成后缀
        for suffix_format, types in ESConfig.INDEX_SUFFIX_RULES.items():
            if self.index_type in types:
                if suffix_format == 'YYYYMMm':
                    suffix = self._get_suffix_from_batch(6) + 'm'
                elif suffix_format == 'YYYYy':
                    suffix = self._get_suffix_from_batch(4) + 'y'
                elif suffix_format == 'YYYYMMDDd':
                    suffix = self._get_suffix_from_date() + 'd'
                else:
                    suffix = self.date
                break
        else:
            suffix = self.date

        return f"{prefix}_{suffix}"

    def _get_suffix_from_batch(self, length: int) -> str:
        """从batch_num提取后缀"""
        if self.batch_num and len(self.batch_num) >= length:
            return self.batch_num[:length]
        return datetime.now().strftime('%Y%m' if length == 6 else '%Y')

    def _get_suffix_from_date(self) -> str:
        """从date提取后缀"""
        if self.batch_num and len(self.batch_num) == 8:
            return self.batch_num
        return self.date

    def create_index(self, mapping: Optional[Dict] = None, force_create: bool = False):
        """创建索引 - 保留原始安全逻辑"""
        exists = self.es.indices.exists(index=self.index_name)

        if exists and not force_create:
            print(f"索引已存在，将追加数据: {self.index_name}")
            self._show_index_stats()
            return

        if exists and force_create:
            print(f"强制删除并重建索引: {self.index_name}")
            self.es.indices.delete(index=self.index_name, ignore=[400, 404])

        print(f"创建索引: {self.index_name}")
        self.es.indices.create(index=self.index_name, ignore=[400])

        # 设置配置和mapping
        self._apply_settings_and_mapping(mapping)
        print(f"索引创建成功")

    def _apply_settings_and_mapping(self, mapping: Optional[Dict]):
        """应用设置和mapping"""
        self.es.indices.put_settings(
            index=self.index_name,
            body=ESConfig.INDEX_SETTINGS
        )

        if mapping:
            self.es.indices.put_mapping(
                index=self.index_name,
                doc_type=self.doc_type,
                body={self.doc_type: mapping}
            )
            print(f"  - Mapping已创建")

    def _show_index_stats(self):
        """显示索引统计"""
        try:
            stats = self.es.count(index=self.index_name)
            print(f"  - 当前文档数: {stats.get('count', 0):,} 条")
        except:
            pass
        print(f"提示：如需强制重建，请设置 force_create=True")

    def bulk_write(self, data_list: List[Dict]):
        """批量写入 - 保留原始反馈逻辑"""
        if not data_list:
            print("  - 无数据需要写入")
            return

        actions = [
            {"_index": self.index_name, "_type": self.doc_type, "_source": data}
            for data in data_list
        ]

        try:
            success, failed = helpers.bulk(self.es, actions, stats_only=True)
            print(f"写入成功: {success}条, 失败: {failed}条")

            # 显示总数
            self._show_index_stats()
            self.es.indices.refresh(index=self.index_name)
        except Exception as e:
            print(f"❌ 批量写入失败: {e}")

    # ====== 新增：统一的 write 方法 ======
    def write(self, count: int = 100, force_create: bool = False):
        """
        完整流程：生成数据并写入 - 原为BaseESWriter的核心方法
        :param count: 生成数据条数
        :param force_create: 是否强制重建索引（危险操作）
        """
        print(f"\n[{self.index_type}] 开始写入流程...")
        print(f"  - 准备生成 {count} 条数据")

        # 检查索引存在性并创建（安全模式）
        self.create_index(force_create=force_create)

        # 生成数据（子类必须实现 generate_mock_data）
        print(f"  - 生成模拟数据中...")
        data_list = self.generate_mock_data(count)
        print(f"  - 数据生成完成")

        # 写入ES
        self.bulk_write(data_list)

        print(f"[{self.index_type}] 写入流程完成\n")

    def generate_mock_data(self, count: int) -> List[Dict]:
        """
        生成模拟数据 - 抽象方法，子类必须实现
        这是原始 BaseESWriter 的要求，必须保留
        """
        raise NotImplementedError(f"子类 {self.__class__.__name__} 必须实现 generate_mock_data 方法")


# ==================== 数据生成器 ====================
class DataBuilder:
    """数据构建器 - 保留原始字段顺序和生成逻辑"""

    # 设备字段定义（保持原始顺序）
    DEVICE_FIELDS = {
        # 高压配电（综资）：1-高压配电（动环）
        'high_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                              'device_code', 'device_number', 'device_subclass', 'device_type',
                              'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                              'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                              'province_id', 'qr_code_no', 'qualitor', 'rated_cooling_capacity',
                              'rated_input_power', 'rated_operating_voltage', 'related_room',
                              'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 低压交流配电（综资）：2-低压交流配电（动环）、96-交流母线配电
        'low_ac_distribution': ['assets_no', 'backup_time', 'batch_num', 'cell_voltage_level',
                                'city_id', 'collect_time', 'county_id', 'device_code',
                                'device_number', 'device_subclass', 'device_type',
                                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                                'province_id', 'qr_code_no', 'qualitor', 'ralated_power_device',
                                'related_room', 'related_site', 'res_code', 'reted_capacity',
                                'start_time', 'total_monomers_number', 'vendor_id', 'zh_label'],
        # 变压器（）综资）：3-变压器（动环）
        'transform': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                      'device_code', 'device_number', 'device_subclass', 'device_type',
                      'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                      'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                      'province_id', 'qr_code_no', 'qualitor', 'rated_capacity',
                      'rated_output_voltage', 'related_room', 'related_site', 'related_system',
                      'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 低压直流配电（综资）：4-低压直流配电（动环）
        'low_dc_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                                'device_code', 'device_number', 'device_subclass', 'device_type',
                                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                                'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                                'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 发电机组（综资）：5-发电机组（动环）  -- 需要检测下
        'power_generation': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                             'device_code', 'device_number', 'device_subclass', 'device_type',
                             'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                             'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                             'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                             'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 开关电源（综资）：6-开关电源（动环）
        'switch_power': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                         'device_code', 'device_number', 'device_subclass', 'device_type',
                         'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                         'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                         'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                         'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 蓄电池（综资）：7-铅酸电池（动环）、68-锂电池（动环）
        'battery': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                    'device_code', 'device_number', 'device_subclass', 'device_type',
                    'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                    'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                    'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                    'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # ups设备（综资）：8-UPS设备（动环）
        'ups': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                'device_code', 'device_number', 'device_subclass', 'device_type',
                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 空调设备（综资）：11-机房专用空调（动环）、12-中央空调末端（动环）、13-中央空调主机（动环）、15-普通空调（已经可以了
        'air': ['rated_cooling_capacity', 'power_device_name', 'estimated_retirement_time', 'device_subclass',
                'device_type', 'assets_no', 'county_id', 'rated_operating_voltage',
                'maintainor', 'lifecycle_status', 'qualitor', 'related_room', 'rated_input_power', 'qr_code_no',
                'irms_province_code', 'related_site', 'power_device_id', 'batch_num', 'product_name', 'res_code',
                'zh_label', 'start_time', 'province_id', 'device_number', 'device_code', 'vendor_id', 'collect_time',
                'city_id'],
        # 变换设备（综资）：14-变换设备（动环）
        'transform_device': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                             'device_code', 'device_number', 'device_subclass', 'device_type',
                             'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                             'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                             'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                             'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 动环监控（综资）：17-机房环境（动环）、76-动环监控（动环）、93-智能门禁（动环）
        'power_monitor': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                          'device_code', 'device_number', 'device_subclass', 'device_type',
                          'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                          'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                          'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                          'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 节能设备（综资）：18-电池恒温箱（动环）、77-智能通风换热（动环）、78-风光设备（动环）、潜热过度（动环）
        'energy_save': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                        'device_code', 'device_number', 'device_subclass', 'device_type',
                        'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                        'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                        'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                        'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 高压直流电源（综资）：87-高压直流电源（动环）
        'high_power': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                       'device_code', 'device_number', 'device_subclass', 'device_type',
                       'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                       'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                       'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                       'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 高压直流配电（综资）：88-高压直流电源配电（动环）
        'high_dc_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                                 'device_code', 'device_number', 'device_subclass', 'device_type',
                                 'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                 'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                                 'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                                 'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 智能电表（综资）：92-智能电表（动环）
        'smart_meter': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                        'device_code', 'device_number', 'device_subclass', 'device_type',
                        'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                        'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                        'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                        'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 其他设备（综资）：16-极早期烟感（动环）、94-一体化能源柜（动环）、户外小型一体化电源（动环）、其他设备（动环）
        'other': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                  'device_code', 'device_number', 'device_subclass', 'device_type',
                  'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                  'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                  'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                  'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],

    }

    # 房间字段（保持原始顺序）
    ROOM_FIELDS = [
        'uuid', 'province_id', 'city_id', 'batch_num', 'collect_time',
        'equiproom_type', 'equiproom_level', 'room_area', 'installed_rack_num',
        'loadable_rack_num', 'lifecycle_status', 'zh_label', 'length',
        'width', 'height', 'cutin_date', 'address_code', 'airconditioner_power',
        # ... 保留所有原始字段
    ]

    @staticmethod
    def build_device_docs(device_type: str, count: int, context: Dict) -> List[Dict]:
        """构建设备文档 - 严格保持字段顺序"""
        fields = DataBuilder.DEVICE_FIELDS.get(device_type, [])
        if not fields:
            # 通用字段（保持原始逻辑）
            fields = ['assets_no', 'batch_num', 'city_id', 'collect_time',
                      'device_code', 'device_number', 'province_id', 'zh_label']
            print(f"设备类型 '{device_type}' 未预定义，使用通用字段")

        docs = []
        for i in range(count):
            doc = {}
            # 按字段定义顺序生成（关键！）
            for field in fields:
                doc[field] = DataBuilder._generate_field_value(field, context, device_type)
            docs.append(doc)
        return docs

    @staticmethod
    def _generate_field_value(field: str, context: Dict, device_type: str = None) -> Any:
        """生成字段值 - 保留原始全部逻辑"""
        # 业务参数字段
        if field == 'rated_cooling_capacity':
            return context.get('rated_cooling_capacity', f"{random.randint(1, 100)}")
        elif field == 'power_device_name':
            return context.get('power_device_name', f"")
        elif field == 'estimated_retirement_time':
            return context.get('estimated_retirement_time', f"{datetime.now().strftime('%Y-%m-%d')}")
        elif field == 'device_subclass':
            return context.get('device_subclass', f"{random.choice(['风冷专用空调'])}")
        elif field == 'device_type':
            return context.get('device_type', f"{random.choice(['机房专用空调'])}")
        elif field == 'assets_no':
            return context.get('assets_no', f"")
        elif field == 'county_id':
            return context.get('county_id', f"{random.choice(['440112'])}")
        elif field == 'rated_operating_voltage':
            return context.get('rated_operating_voltage', f"{random.randint(1, 100)}V")
        elif field == 'maintainor':
            return context.get('maintainor', f"test_{random.randint(1, 100)}")
        elif field == 'lifecycle_status':
            return context.get('lifecycle_status', f"{random.choice(['现网'])}")
        elif field == 'qualitor':
            return context.get('qualitor', f"test_{random.choice(['现网'])}")
        elif field == 'related_room':
            return context.get('related_room', f"room_{random.randint(1000, 9999)}")
        elif field == 'rated_input_power':
            return context.get('rated_input_power', f"{random.randint(1, 10)}")
        elif field == 'qr_code_no':
            return context.get('qr_code_no', f'')
        elif field == 'irms_province_code':
            return context.get('irms_province_code', f"{random.choice(['GZ'])}")
        elif field == 'related_site':
            return context.get('related_site', f"site_{random.randint(1000, 9999)}")
        elif field == 'power_device_id':
            return context.get('power_device_id', f"device_{random.randint(1000, 9999)}")
        elif field == 'batch_num':
            return context.get('batch_num', f"{datetime.now().strftime('%Y%m%d')}")
        elif field == 'product_name':
            return context.get('product_name', f"{random.choice(['test'])}")
        elif field == 'res_code':
            return context.get('res_code', f"res_code_{random.randint(1000, 9999)}")
        elif field == 'zh_label':
            return context.get('zh_label', f"zh_label_{random.randint(1000, 9999)}")
        elif field == 'start_time':
            return context.get('start_time', f"{datetime.now().strftime('%Y-%m-%d')}")
        elif field == 'province_id':
            return context.get('province_id', f"zh_label_{random.randint(300000, 900000)}")
        elif field == 'device_number':
            return context.get('device_number', f"{random.randint(1, 10)}")
        elif field == 'device_code':
            return context.get('device_code', f"{random.randint(1, 10)}")
        elif field == 'vendor_id':
            return context.get('vendor_id', f"{random.choice(['test'])}")
        elif field == 'collect_time':
            return context.get('collect_time', f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        elif field == 'city_id':
            return context.get('city_id', f"{random.randint(300000, 900000)}")
        return f"{random.randint(1, 100)}"


# ==================== 业务写入器 ====================
class DeviceWriter(BaseWriter):
    """设备写入器"""

    def __init__(self, device_type: str, **kwargs):
        self.device_type = device_type
        super().__init__(index_type=device_type, **kwargs)
        print(f"  - 字段数量: {len(DataBuilder.DEVICE_FIELDS.get(device_type, []))}")

    def generate_mock_data(self, count: int) -> List[Dict]:
        """生成设备数据 - 保留原始逻辑"""
        context = {
            'related_site': self.site_int_id,
            'related_room': self.room_int_id,
            'irms_province_code': self.irms_province_code,
            'power_device_id': self.power_device_id,
            'batch_num': self.batch_num,
            'res_code': self.device_res_code,
            'zh_label': self.device_zh_label,
            'province_id': self.province_id,
            'city_id': self.city_id,
        }
        return DataBuilder.build_device_docs(self.device_type, count, context)

    def write(self, count: int = 100, force_create: bool = False):
        """完整写入流程 - 保留原始反馈"""
        print(f"\n[{self.device_type}] 开始写入流程...")
        print(f"  - 准备生成 {count} 条数据")

        self.create_index(force_create=force_create)

        print(f"  - 生成模拟数据中...")
        data = self.generate_mock_data(count)
        print(f"  - 数据生成完成")

        self.bulk_write(data)
        print(f"[{self.device_type}] 写入流程完成\n")


class RoomWriter(BaseWriter):
    """房间写入器 - 保留原始逻辑和字段顺序"""

    def __init__(self, **kwargs):
        super().__init__(index_type='room', **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        room_types = ['数据中心', '接入网', '核心网', '基站']
        levels = ['A级', 'B级', 'C级']

        docs = []
        for i in range(count):
            doc = {
                'china_tower_station_code': f"",
                'asset_address_code': f"{random.randint(300000, 399999)}KH{random.randint(10000000, 99999999)}",
                'equipment_power': f"{random.uniform(0, 50):.1f}",
                'cutin_date': self.cutin_date,
                'china_tower_room_type': random.choice(['其他机房']),
                'row_num': f"{random.randint(1, 100)}",
                'end_row': f"{random.randint(1, 100)}",
                'retire_time': f"",
                'property_unit': random.choice(['中国移动']),
                'county_id': f"{random.randint(350000, 359999)}",
                'int_id': self.room_int_id,
                'qualitor': f"test{random.randint(1, 100)}",
                'lifecycle_status': random.choice(['在网', '退网', '工程', '预占']),
                'column_num': str(random.randint(1, 20)) if random.random() > 0.3 else "",
                'equiproom_level': random.choice(['核心（省内）']),
                'start_column': str(random.randint(1, 20)) if random.random() > 0.5 else "",
                'airconditioner_power': f"{random.uniform(0, 30):.1f}",
                'property_right': random.choice(['自有自建']),
                'floor_num': str(random.randint(1, 30)),
                'start_row': str(random.randint(1, 20)) if random.random() > 0.5 else "",
                'length': f"{random.randint(5, 50)}" if random.random() > 0.3 else "",
                'irms_province_code': self.irms_province_code,
                'room_area': f"{random.randint(10, 1000)}",
                'related_site': self.site_int_id,
                'batch_num': self.batch_num,
                'alias_name': f"机房别名_{random.randint(1000, 9999)}" if random.random() > 0.6 else "",
                'shared_unit': random.choice(['移动']),
                'zh_label': self.room_zh_label,
                'province_id': self.province_id,
                'equiproom_type': random.choice(['其他机房']),
                'width': f"{random.randint(10, 99)}",
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city_id': self.city_id,
                'end_column': f"{random.randint(10, 99)}",
            }

            # # 填充剩余字段（保持原始逻辑）
            # for field in DataBuilder.ROOM_FIELDS:
            #     if field not in doc:
            #         doc[field] = f"mock_{field}_{random.randint(1, 100)}"

            docs.append(doc)
        return docs

    def write(self, count: int = 100, **kwargs):
        """保持与原始一致的写入接口"""
        super().write(count=count, **kwargs)


class RoomPropertyWriter(BaseWriter):
    """房间属性写入器"""

    def __init__(self, **kwargs):
        super().__init__(index_type='room_property', **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        docs = []
        for i in range(count):
            doc = {
                'refrigeration_mode': random.choice(['风冷']),
                'power_room_type': self.power_room_type,
                'power_related_site_name': self.site_int_id,  # 也需要与站点id一致
                'battery_backup_time': f"{random.randint(1, 24)}",
                'power_supply_mode': self.power_supply_mode,
                'space_room_type': f"{random.choice(['传输机房'])}",
                'power_room_name': self.room_zg_name,  # 需要确认有无作用
                'irms_province_code': self.irms_province_code,
                'batch_num': self.batch_num,
                'ac_config': random.choice(['其他']),
                'res_code': self.room_res_code,
                'power_room_id': f"{random.randint(1, 2)}",
                'zh_label': self.room_int_id,
                'county_id': self.city_id,
                'power_supply_type': f"交流{random.randint(10000, 99999)}V",
                'ac_terminal': random.choice(['精密空调', '普通空调']),
                'power_monitor_conf': f"{random.choice(['有', '无'])}",
                'province_id': self.province_id,
                'video_monitor_conf': f"{random.choice(['有', '无'])}",
                'refer_pue': f"{random.randint(1, 2)}",
                'log_saved_time': f"{random.randint(1, 2)}",
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city_id': self.city_id,
            }

            # # 填充其他字段
            # extra_fields = ['ac_terminal', 'county_id', 'irms_province_code',
            #                 'log_saved_time', 'power_related_site_name', 'power_room_type',
            #                 'power_supply_type', 'refer_pue', 'refrigeration_mode',
            #                 'res_code', 'space_room_type', 'video_monitor_conf']
            # for field in extra_fields:
            #     if field not in doc:
            #         doc[field] = f"mock_{field}_{random.randint(1, 2)}"

            docs.append(doc)
        return docs


class SiteWriter(BaseWriter):
    """站点写入器 - 保留原始字段和逻辑"""

    def __init__(self, **kwargs):
        super().__init__(index_type='site', **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        site_types = ['核心局站', '汇聚局站', '接入局站', '基站']

        docs = []
        for i in range(count):
            doc = {
                'china_tower_station_code': f"mock_{random.randint(1, 100)}",
                "village_pass_serv_code": "",
                'cutin_date': self.cutin_date,
                'site_type': self.site_type,
                'latitude': f"{random.uniform(30, 45):.6f}",
                'project_name': f"{random.uniform(30, 45):.6f}",
                'floor_number': f"{random.randint(1, 20)}",
                'related_dc': self.related_dc,
                'address': f"XX省XX市XX区XX路{random.randint(1, 999)}号",
                'uuid': f"{random.randint(1, 20)}",
                'county_id': self.county_id,
                'is_headquarters_used': f"{random.choice(['是','否'])}",
                'pms_address_code': f"{random.choice(['是', '否'])}",
                'irms_province_code': self.irms_province_code,
                'batch_num': self.batch_num,
                'alias_name': self.zh_label,
                'standardaddress': f"{random.randint(10000, 99999)}",
                'zh_label': self.zh_label,
                'province_id': self.province_id,
                'int_id': self.site_int_id,
                'qualitor': "测试记录",
                'lifecycle_status': "在网",
                'use_corp': "中国移动",
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city_id': self.city_id,
                'longitude': f"{random.uniform(100, 125):.6f}",
            }
            docs.append(doc)
        return docs


class SitePropertyWriter(BaseWriter):
    """站点属性写入器 - 保留与site_int_id关联逻辑"""

    def __init__(self, **kwargs):
        super().__init__(index_type='site_property', **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        docs = []
        for i in range(count):
            doc = {
                'mains_nature': self.mains_nature,
                'cold_storage_time': f"",
                'property_unit': f"",
                'water_cooling_conf': f"",
                'county_id': f"{random.randint(100000, 999999)}",
                'power_is_substations': f"{random.choice(['是', '否'])}",
                'mains_configuration_level': f"{random.choice(['1市电无油机'])}",
                'total_mains_number': f"{random.choice(['1', '0'])}",
                'tatal_tank_volume': f"",
                'is_attach_idc_room': f"{random.choice(['是', '否'])}",
                'power_site_level': self.power_site_level,
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

            # 填充其他字段
            # extra_fields = ['cold_storage_time', 'is_cold_storage_install',
            #                 'mains_backup_method', 'power_monitoring_site_id',
            #                 'power_monitoring_site_name', 'property_unit',
            #                 'tatal_tank_volume', 'total_tank_number', 'water_cooling_conf']
            # for field in extra_fields:
            #     if field not in doc:
            #         doc[field] = f"mock_{field}_{random.randint(1, 100)}"

            docs.append(doc)
        return docs


class IrmsMapWriter(BaseWriter):
    """IRMS映射写入器 - 保留原始逻辑"""

    def __init__(self, map_type: str, **kwargs):
        self.map_type = map_type
        super().__init__(index_type=f'irms_{map_type}_map', **kwargs)

    def generate_mock_data(self, count: int = 50) -> List[Dict]:
        docs = []
        for i in range(count):
            if self.map_type == 'rom':
                doc = {
                    'pms_id': f"PMS{random.randint(10000, 99999)}",
                    'address_code': f"",
                    'pms_name': f"",
                    'dh_name': self.room_dh_name,
                    'zg_name': self.room_zg_name,
                    'province_id': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'dh_id': f"",
                    'zg_id': self.province_id,
                    'batch_num': self.batch_num,
                    'statis_ymd': self.batch_num,
                    'uuid': uuid.uuid4(),
                }
            else:
                doc = {
                    'pms_id': f"PMS{random.randint(10000, 99999)}",
                    'pms_name': f"PMS系统_{random.randint(1, 100)}",
                    'dh_name': f"DH{random.randint(10000, 99999)}",
                    'zg_name': f"ZG{random.randint(10000, 99999)}",
                    'province_id': self.province_id,
                    'dh_id': self.site_dh_id,
                    'zg_id': self.site_zg_id,
                    'batch_num': self.batch_num,
                    'statis_ymd': self.batch_num,
                    'uuid': uuid.uuid4(),
                }

            docs.append(doc)
        return docs


# ==================== 工厂类 ====================
class WriterFactory:
    """写入器工厂"""

    @staticmethod
    def create_writer(index_category: str, **kwargs) -> BaseWriter:
        """
        创建写入器实例 - 保持原始接口不变
        :param index_category: 索引类别字符串
        """
        # 设备类 - 通过 device_type 参数传递
        if index_category in ['air', 'battery', 'low_ac_distribution', 'switch_power',
                              'energy_save', 'high_dc_distribution', 'high_distribution',
                              'high_power', 'smart_meter', 'transform', 'transform_device', 'ups']:
            return DeviceWriter(device_type=index_category, **kwargs)

        # 房间类
        elif index_category == 'room':
            return RoomWriter(**kwargs)
        elif index_category == 'room_property':
            return RoomPropertyWriter(**kwargs)

        # 站点类
        elif index_category == 'site':
            return SiteWriter(**kwargs)
        elif index_category == 'site_property':
            return SitePropertyWriter(**kwargs)

        # 映射类
        elif index_category.startswith('irms_') and index_category.endswith('_map'):
            # 提取映射类型，如 'dc', 'rom', 'site'
            map_type = index_category.split('_')[1]
            return IrmsMapWriter(map_type=map_type, **kwargs)

        # 连接类
        elif index_category == 'link_pe_in':
            return BaseWriter(index_type=index_category, **kwargs)

        else:
            raise ValueError(f"不支持的索引类别: {index_category}")


# ==================== 数据库连接 ====================
class MysqlConnect:
    """MySQL连接"""
    """match_mode - 为0站点匹配，为1机房匹配 - 为2走原逻辑（需要接入设备的机房才可以匹配）"""

    def __init__(self, precinct_id: str, env: str = 'release', **kwargs):
        self.precinct_id = precinct_id
        self.match_mode = kwargs.get('match_mode', 0)
        self.mete_code = kwargs.get('mete_code', '000000')
        self.EsTime = kwargs.get('EsTime', 'T23:50:50')
        self.MinVal = kwargs.get('MinVal', 1)
        self.MaxVal = kwargs.get('MaxVal', 1)
        self.device_id = kwargs.get('device_id', '1')
        self.del_col = kwargs.get('del_col', 'meteID')
        self.del_col_v = kwargs.get('del_clo_v', '1')

        # 数据库连接
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        self.url = conf.get_conf(env, 'esurl')

        # 创建引擎
        engines = f"mysql+pymysql://{urlquote(self.dbuser)}:{urlquote(self.dbpw)}@{self.dbip}:{self.dbport}/{urlquote(self.dbname)}?charset=utf8"
        self.engine = create_engine(engines, max_overflow=5)
        self.conn = self.engine.connect()

        # SQL文件路径
        sql_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'Common', 'SQL', 'selectForESList.sql'
        )
        self.sql_file = open(sql_path, encoding='utf-8')

    def get_sql_list(self) -> List[str]:
        """读取SQL文件 - 保留原始逻辑"""
        content = self.sql_file.read()
        return [sql.strip() for sql in content.split(';') if sql.strip()]

    def get_provincedata(self, sql_index: int) -> List[Tuple]:
        """执行查询 - 保留原始逻辑"""
        sql_list = self.get_sql_list()
        if sql_index >= len(sql_list):
            print(f"SQL索引 {sql_index} 超出范围")
            return []

        sql = sql_list[sql_index]
        params = {'precinct_id': self.precinct_id + '%'}

        if sql_index == 1:
            params.update({'mete_code': self.mete_code, 'device_id': self.device_id})
        elif sql_index == 2:
            params.update({'mete_code': self.mete_code})

        result = self.conn.execute(text(sql), params)
        return result.fetchall()

    def insert_esdata_device(self) -> List[Tuple]:
        """插入设备数据 - 保留原始逻辑"""
        # todo 待完善[目前展示只有0和else两种模式]
        if self.match_mode == 0:
            print("全量站点匹配==========")
            sql_index = 5
        elif self.match_mode == 1:
            print("全量机房匹配==========")
            sql_index = 6
        elif self.match_mode == 2:
            if self.device_id == '1' and self.mete_code == '000000':
                print("机房全量查询未传设备==========")
                sql_index = 4
            else:
                print("机房全量查询==========")
                sql_index = 0

        data = self.get_provincedata(sql_index)
        print(f"预计写入数据条数========== {len(data)}")
        return data


# ==================== 业务爬虫 ====================
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
        self.dh_id = kwargs.get('dh_id', '520400')
        self.zg_id = kwargs.get('zg_id', '520400')
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
        # 校验列表
        self.site_names = []
        self.room_names = []
        self.dh_ids = []

        # 数据库连接
        self.db = MysqlConnect(precinct_id=precinct_id, **kwargs)

    def id_match_site(self):
        """按名称匹配 - 按对应站点的匹配 -- > 对应match_mode = 0"""
        """目前从市开始匹配 - 可以修改selectForESlist.sql的第5块更改逻辑"""
        data = self.db.insert_esdata_device()
        for record in data:
            # 站点匹配
            if record[3]:
                dh_id = record[3]  # 楼栋时走这条
                self.dh_id = dh_id
            else:
                dh_id = record[7]  # 非楼栋的站点时走这条
                self.dh_id = dh_id
            if dh_id not in getattr(self, 'dh_ids', []):
                self.dh_ids.append(dh_id)
                self._id_create_site_and_property(dh_id)
                print(f"站点已写入: {dh_id}")

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

    def _id_create_site_and_property(self, dh_id: str):
        """ID模式实现动环综资站点关联 - 实际站点匹配的处理逻辑"""

        # 创建站点（修复后正确调用）
        site_writer = WriterFactory.create_writer(
            'site',
            batch_num=self.batch_num,
            zh_label=dh_id,
            city_id=self.city,
            dh_id=self.dh_id,
            zg_id=self.zg_id,
            province_id=self.province,
            irms_province_code=self.irms_province_code,
            cutin_date=self.cutin_date
        )
        site_writer.write(count=1, force_create=self.force_create)

        # 保存关键关联信息
        self.site_int_id = site_writer.site_int_id
        self.province = site_writer.province_id
        self.city = site_writer.city_id

        # 创建IRMS映射关系
        irms = WriterFactory.create_writer(
            'irms_site_map',
            batch_num=self.batch_num,
            site_dh_id=self.dh_id,
            site_zg_id=self.site_int_id,
            city_id=self.city,
            province_id=self.province,
        )
        irms.write(count=1, force_create=self.force_create)
        print(f"站点对创建成功: {dh_id} (site_int_id: {self.site_int_id})")

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
            power_related_site_name=self.power_related_site_name
        )
        prop_writer.write(count=1, force_create=self.force_create)
        print(f"站点对创建成功: {dh_id} (site_int_id: {self.site_int_id})")

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
            cutin_date=self.cutin_date
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
            power_related_site_name=self.power_related_site_name
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
            power_supply_mode=self.power_supply_mode
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
            power_supply_mode=self.power_supply_mode
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


# ==================== 使用示例 ====================
if __name__ == '__main__':
    # 示例2: 运行业务逻辑（保留原始调用方式）
    spider = ZZMatchSpider(precinct_id='01-01-08', batch_num='20250723', force_create=False,
                           mains_nature='市电转供', power_site_level='传输节点', power_room_type='汇聚机房',
                           power_supply_mode='双电源双回路供电', cutin_date='2024-11-01', province_id='440000',
                           city_id='440500', match_model=0, irms_province_code='GD')
    spider.id_match_site()
    # spider.name_match_site()
    # spider.name_match_site_room()

    # spider = ZZMatchSpider(precinct_id='01-08-08-04-03-01', batch_num='20250104', force_create=False, match_mode=2)
    # spider.name_match_site_room_device()

