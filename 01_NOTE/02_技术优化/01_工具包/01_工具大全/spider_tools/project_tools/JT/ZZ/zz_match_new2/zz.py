# -*- coding: utf-8 -*-
"""
ZZ 22 类索引一次性写入 ES（单文件完整版 + 工厂类 + 初始化字段支持）
"""

import random
import uuid
from datetime import datetime
from typing import List, Dict, Any
from elasticsearch import Elasticsearch, helpers
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus as urlquote
from spider_tools.Conf.Config import Config  # 你的原始配置入口


# ============ 配置区（100% 复用 common_zz_match.py） ============ #
class ESConfig:
    ES_URL = "http://10.1.203.38:9200"
    INDEX_PREFIX_MAP = {
        'air': 'ods_zz_device_air', 'battery': 'ods_zz_device_battery',
        'low_ac_distribution': 'ods_zz_device_low_ac_distribution',
        'switch_power': 'ods_zz_device_switch_power', 'link_pe_in': 'ods_zz_link_pe_in',
        'energy_save': 'ods_zz_device_energy_save', 'high_dc_distribution': 'ods_zz_device_high_dc_distribution',
        'high_distribution': 'ods_zz_device_high_distribution', 'high_power': 'ods_zz_device_high_power',
        'smart_meter': 'ods_zz_device_smart_meter', 'transform': 'ods_zz_device_transform',
        'transform_device': 'ods_zz_device_transform_device', 'ups': 'ods_zz_device_ups',
        'low_dc_distribution': 'ods_zz_device_low_dc_distribution',
        'power_generation': 'ods_zz_device_power_generation',
        'power_monitor': 'ods_zz_device_power_monitor', 'other': 'ods_zz_device_other',
        'room': 'ods_zz_room', 'room_property': 'ods_zz_room_property',
        'site': 'ods_zz_site', 'site_property': 'ods_zz_site_property',
        'irms_dc_map': 'ods_zz_irms_dc_map', 'irms_rom_map': 'ods_zz_irms_rom_map',
        'irms_site_map': 'ods_zz_irms_site_map',
    }
    INDEX_SUFFIX_RULES = {
        'YYYYMMm': ['air', 'battery', 'low_ac_distribution', 'switch_power', 'room_property', 'site', 'site_property',
                    'link_pe_in'],
        'YYYYy': ['energy_save', 'high_dc_distribution', 'high_distribution', 'high_power', 'smart_meter', 'transform',
                  'transform_device', 'ups',
                  'irms_dc_map', 'irms_rom_map', 'irms_site_map'],
        'YYYYMMDDd': ['room'],
    }
    INDEX_SETTINGS = {"index": {"number_of_replicas": "0", "refresh_interval": "5s"}}


# ============ 字段生成器（复用原逻辑） ============ #
class DataBuilder:
    DEVICE_FIELDS = {
        'room': [
            'batch_num', 'collect_time', 'zh_label', 'cutin_date', 'province_id', 'city_id',
            'county_id', 'site_int_id', 'room_int_id', 'power_room_type', 'power_supply_mode'
        ],
        'room_property': [
            'batch_num', 'room_int_id', 'province_id', 'city_id', 'site_int_id', 'irms_province_code',
            'cutin_date', 'power_room_type', 'power_supply_mode', 'county_id'
        ],
        'site': [
            'batch_num', 'zh_label', 'city_id', 'province_id', 'irms_province_code', 'cutin_date',
            'county_id', 'site_type'
        ],
        'site_property': [
            'batch_num', 'site_int_id', 'province_id', 'city_id', 'irms_province_code', 'cutin_date',
            'power_site_level', 'mains_nature', 'county_id', 'site_type'
        ],
        'irms_dc_map': [
            'batch_num', 'uuid', 'pms_id', 'pms_name', 'dh_id', 'dh_name', 'zg_id', 'zg_name',
            'statis_ymd', 'province_id'
        ],
        'irms_rom_map': [
            'batch_num', 'uuid', 'pms_id', 'pms_name', 'dh_id', 'dh_name', 'zg_id', 'zg_name',
            'statis_ymd', 'province_id'
        ],
        'irms_site_map': [
            'batch_num', 'uuid', 'pms_id', 'pms_name', 'dh_id', 'dh_name', 'zg_id', 'zg_name',
            'statis_ymd', 'province_id'
        ],
        'high_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                              'device_code', 'device_number', 'device_subclass', 'device_type',
                              'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                              'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                              'province_id', 'qr_code_no', 'qualitor', 'rated_cooling_capacity',
                              'rated_input_power', 'rated_operating_voltage', 'related_room',
                              'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'low_ac_distribution': ['assets_no', 'backup_time', 'batch_num', 'cell_voltage_level',
                                'city_id', 'collect_time', 'county_id', 'device_code',
                                'device_number', 'device_subclass', 'device_type',
                                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                                'province_id', 'qr_code_no', 'qualitor', 'ralated_power_device',
                                'related_room', 'related_site', 'res_code', 'reted_capacity',
                                'start_time', 'total_monomers_number', 'vendor_id', 'zh_label'],
        'transform': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                      'device_code', 'device_number', 'device_subclass', 'device_type',
                      'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                      'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                      'province_id', 'qr_code_no', 'qualitor', 'rated_capacity',
                      'rated_output_voltage', 'related_room', 'related_site', 'related_system',
                      'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'low_dc_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                                'device_code', 'device_number', 'device_subclass', 'device_type',
                                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                                'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                                'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'power_generation': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                             'device_code', 'device_number', 'device_subclass', 'device_type',
                             'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                             'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                             'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                             'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'switch_power': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                         'device_code', 'device_number', 'device_subclass', 'device_type',
                         'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                         'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                         'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                         'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'battery': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                    'device_code', 'device_number', 'device_subclass', 'device_type',
                    'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                    'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                    'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                    'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'ups': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                'device_code', 'device_number', 'device_subclass', 'device_type',
                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'air': ['rated_cooling_capacity', 'power_device_name', 'estimated_retirement_time', 'device_subclass',
                'device_type', 'assets_no', 'county_id', 'rated_operating_voltage',
                'maintainor', 'lifecycle_status', 'qualitor', 'related_room', 'rated_input_power', 'qr_code_no',
                'irms_province_code', 'related_site', 'power_device_id', 'batch_num', 'product_name', 'res_code',
                'zh_label', 'start_time', 'province_id', 'device_number', 'device_code', 'vendor_id', 'collect_time',
                'city_id'],
        'transform_device': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                             'device_code', 'device_number', 'device_subclass', 'device_type',
                             'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                             'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                             'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                             'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'power_monitor': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                          'device_code', 'device_number', 'device_subclass', 'device_type',
                          'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                          'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                          'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                          'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'energy_save': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                        'device_code', 'device_number', 'device_subclass', 'device_type',
                        'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                        'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                        'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                        'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'high_power': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                       'device_code', 'device_number', 'device_subclass', 'device_type',
                       'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                       'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                       'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                       'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'high_dc_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                                 'device_code', 'device_number', 'device_subclass', 'device_type',
                                 'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                 'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                                 'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                                 'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'smart_meter': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                        'device_code', 'device_number', 'device_subclass', 'device_type',
                        'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                        'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                        'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                        'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'other': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                  'device_code', 'device_number', 'device_subclass', 'device_type',
                  'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                  'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                  'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                  'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
    }

    @staticmethod
    def build_device_docs(device_type: str, count: int, context: Dict) -> List[Dict]:
        fields = DataBuilder.DEVICE_FIELDS.get(device_type, [])
        docs = []
        for _ in range(count):
            doc = {field: DataBuilder._generate_field_value(field, context, device_type) for field in fields}
            docs.append(doc)
        return docs

    @staticmethod
    def _generate_field_value(field: str, context: Dict, device_type: str = None) -> Any:
        # 与原 common_zz_match.py 逻辑完全一致，仅做极简裁剪
        if field == 'batch_num':
            return context.get('batch_num', datetime.now().strftime('%Y%m%d'))
        if field == 'collect_time':
            return context.get('collect_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if field == 'estimated_retirement_time':
            return context.get('estimated_retirement_time', datetime.now().strftime('%Y-%m-%d'))
        if field == 'start_time':
            return context.get('start_time', datetime.now().strftime('%Y-%m-%d'))
        if field in ('lifecycle_status', 'qualitor'):
            return '现网'
        if field == 'device_type':
            return device_type
        if field == 'related_site':
            return context.get('related_site', f"site_{random.randint(1000, 9999)}")
        if field == 'related_room':
            return context.get('related_room', f"room_{random.randint(1000, 9999)}")
        if field == 'power_device_id':
            return context.get('power_device_id', f"device_{random.randint(1000, 9999)}")
        if field == 'res_code':
            return context.get('res_code', f"res_{random.randint(1000, 9999)}")
        if field == 'zh_label':
            return context.get('zh_label', f"设备_{random.randint(1000, 9999)}")
        if field == 'province_id':
            return context.get('province_id', f"{random.randint(300000, 900000)}")
        if field == 'city_id':
            return context.get('city_id', f"{random.randint(300000, 900000)}")
        if field == 'county_id':
            return context.get('county_id', '440101')
        if field == 'irms_province_code':
            return context.get('irms_province_code', 'GZ')
        if field == 'device_code':
            return str(random.randint(1, 10))
        if field == 'device_number':
            return str(random.randint(1, 10))
        if field == 'vendor_id':
            return 'test'
        if field == 'product_name':
            return 'test'
        if field == 'assets_no':
            return ''
        if field == 'maintainor':
            return 'test'
        if field == 'qr_code_no':
            return ''
        if field == 'rated_cooling_capacity':
            return str(random.randint(1, 100))
        if field == 'rated_input_power':
            return str(random.randint(1, 10))
        if field == 'rated_operating_voltage':
            return f"{random.randint(1, 100)}V"
        if field == 'backup_time':
            return str(random.randint(1, 24))
        if field == 'cell_voltage_level':
            return str(random.randint(1, 10))
        if field == 'ralated_power_device':
            return ''
        if field == 'reted_capacity':
            return str(random.randint(100, 1000))
        if field == 'total_monomers_number':
            return str(random.randint(1, 10))
        if field == 'rated_capacity':
            return str(random.randint(100, 1000))
        if field == 'rated_output_voltage':
            return f"{random.randint(1, 100)}V"
        if field == 'related_system':
            return f"sys_{random.randint(1, 100)}"
        if field == 'meter_circuit_number':
            return str(random.randint(1, 10))
        if field == 'cutin_date':
            return context.get('cutin_date', datetime.now().strftime('%Y-%m-%d'))
        if field == 'site_int_id':
            return context.get('site_int_id', f"site_{random.randint(1000, 9999)}")
        if field == 'room_int_id':
            return context.get('room_int_id', f"room_{random.randint(1000, 9999)}")
        if field == 'power_room_type':
            return context.get('power_room_type', '汇聚机房')
        if field == 'power_supply_mode':
            return context.get('power_supply_mode', '双电源双回路供电')
        if field == 'site_type':
            return context.get('site_type', random.choice(
                ['核心站点', '核心站点（配套）', '骨干站点', '汇聚站点', '接入站点', '用户站点', '其他站点']
            ))
        if field == 'power_site_level':
            return context.get('power_site_level', '传输节点')
        if field == 'mains_nature':
            return context.get('mains_nature', '市电转供')
        if field == 'uuid':
            return str(uuid.uuid4())
        if field == 'pms_id':
            return f"PMS{random.randint(10000, 99999)}"
        if field == 'pms_name':
            return f"PMS系统_{random.randint(1000, 9999)}"
        if field == 'dh_id':
            return f"DH{random.randint(10000, 99999)}"
        if field == 'dh_name':
            return f"DH_{random.randint(1000, 9999)}"
        if field == 'zg_id':
            return f"ZG{random.randint(10000, 99999)}"
        if field == 'zg_name':
            return f"ZG_{random.randint(1000, 9999)}"
        if field == 'statis_ymd':
            return context.get('statis_ymd', datetime.now().strftime('%Y%m%d'))
        return f"{random.randint(1, 100)}"


# ============ 统一写入器 ============ #
class ZZAllInOneWriter:
    def __init__(self, **kwargs):
        self.es_url = kwargs.pop('es_url', ESConfig.ES_URL)
        self.es = Elasticsearch(self.es_url)
        self.kwargs = kwargs  # 全局默认参数
        self._registry = self._build_registry()

    def _build_registry(self):
        reg = {}
        device_types = ['air', 'battery', 'low_ac_distribution', 'switch_power',
                        'energy_save', 'high_dc_distribution', 'high_distribution',
                        'high_power', 'smart_meter', 'transform', 'transform_device', 'ups',
                        'low_dc_distribution', 'power_generation', 'power_monitor', 'other']
        for t in device_types:
            reg[t] = {'category': 'device', 'cls': DeviceWriter, 'index_type': t}
        for t in ['room', 'room_property', 'site', 'site_property']:
            reg[t] = {'category': 'meta', 'cls': MetaWriter, 'index_type': t}
        for t in ['irms_dc_map', 'irms_rom_map', 'irms_site_map']:
            reg[t] = {'category': 'map', 'cls': MapWriter, 'index_type': t}
        reg['link_pe_in'] = {'category': 'link', 'cls': LinkWriter, 'index_type': 'link_pe_in'}
        return reg

    def _make_index_name(self, index_type: str) -> str:
        prefix = ESConfig.INDEX_PREFIX_MAP[index_type]
        for rule, types in ESConfig.INDEX_SUFFIX_RULES.items():
            if index_type in types:
                if rule == 'YYYYMMm':
                    suffix = self.kwargs.get('batch_num', datetime.now().strftime('%Y%m')) + 'm'
                elif rule == 'YYYYy':
                    suffix = self.kwargs.get('batch_num', datetime.now().strftime('%Y')) + 'y'
                elif rule == 'YYYYMMDDd':
                    suffix = self.kwargs.get('batch_num', datetime.now().strftime('%Y%m%d')) + 'd'
                else:
                    suffix = self.kwargs.get('batch_num', datetime.now().strftime('%Y%m%d'))
                break
        else:
            suffix = self.kwargs.get('batch_num', datetime.now().strftime('%Y%m%d'))
        return f"{prefix}_{suffix}"

    # ---------------- 对外 API ---------------- #
    def write_all(self, count=10):
        for idx_type in self._registry:
            self.write_indices([idx_type], count=count)

    def write_indices(self, indices: List[str], count=10):
        for idx_type in indices:
            if idx_type not in self._registry:
                print(f"[WARN] 未知索引类型 {idx_type}，已跳过")
                continue
            meta = self._registry[idx_type]
            index_name = self._make_index_name(idx_type)
            writer = meta['cls'](index_name=index_name, es=self.es, index_type=idx_type, **self.kwargs)
            writer.write(count=count)
            print(f"[OK] {index_name} 写入完成")


# --------------------------------------------------------------------------- #
# 四种内部 Writer
# --------------------------------------------------------------------------- #
class DeviceWriter:
    def __init__(self, *, index_name, es, index_type, **ctx):
        self.index_name = index_name
        self.es = es
        self.index_type = index_type
        self.ctx = ctx

    def write(self, count=10):
        mappings = {"properties": self._device_mapping()}
        self._ensure_index(mappings)
        data = DataBuilder.build_device_docs(self.index_type, count, self.ctx)
        self._bulk(data)

    def _device_mapping(self):
        date_fields = {'estimated_retirement_time', 'start_time'}
        fields = DataBuilder.DEVICE_FIELDS[self.index_type]
        return {f: {"type": "date"} if f in date_fields else
        {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}}
                for f in fields}

    def _ensure_index(self, mappings):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name,
                                   body={"settings": ESConfig.INDEX_SETTINGS,
                                         "mappings": {"point_history_data": mappings}})
            print(f"[ES] 创建索引 {self.index_name}")
        else:
            print(f"[ES] 索引已存在 {self.index_name}")

    def _bulk(self, data):
        actions = [{"_index": self.index_name, "_type": "point_history_data", "_source": d} for d in data]
        success, failed = helpers.bulk(self.es, actions, stats_only=True)
        print(f"[ES] 写入 {self.index_name} 成功 {success} 条，失败 {failed} 条")


class MetaWriter:
    """room / room_property / site / site_property"""

    def __init__(self, *, index_name, es, index_type, **ctx):
        self.index_name = index_name
        self.es = es
        self.index_type = index_type
        self.ctx = ctx

    def write(self, count=10):
        mappings = {"properties": self._get_mappings()}
        self._ensure_index(mappings)
        data = DataBuilder.build_device_docs(self.index_type, count, self.ctx)
        self._bulk(data)

    def _get_mappings(self):
        fields = DataBuilder.DEVICE_FIELDS[self.index_type]
        return {field: {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}}
                for field in fields}

    def _ensure_index(self, mappings):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name,
                                   body={"settings": ESConfig.INDEX_SETTINGS,
                                         "mappings": {"point_history_data": mappings}})
            print(f"[ES] 创建索引 {self.index_name}")
        else:
            print(f"[ES] 索引已存在 {self.index_name}")

    def _bulk(self, data):
        actions = [{"_index": self.index_name, "_type": "point_history_data", "_source": d} for d in data]
        success, failed = helpers.bulk(self.es, actions, stats_only=True)
        print(f"[ES] 写入 {self.index_name} 成功 {success} 条，失败 {failed} 条")


class MapWriter:
    """irms_*_map"""

    def __init__(self, *, index_name, es, index_type, **ctx):
        self.index_name = index_name
        self.es = es
        self.index_type = index_type
        self.ctx = ctx

    def write(self, count=10):
        mappings = {"properties": self._get_mappings()}
        self._ensure_index(mappings)
        data = DataBuilder.build_device_docs(self.index_type, count, self.ctx)
        self._bulk(data)

    def _get_mappings(self):
        fields = DataBuilder.DEVICE_FIELDS[self.index_type]
        return {field: {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}}
                for field in fields}

    def _ensure_index(self, mappings):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name,
                                   body={"settings": ESConfig.INDEX_SETTINGS,
                                         "mappings": {"point_history_data": mappings}})
            print(f"[ES] 创建索引 {self.index_name}")
        else:
            print(f"[ES] 索引已存在 {self.index_name}")

    def _bulk(self, data):
        actions = [{"_index": self.index_name, "_type": "point_history_data", "_source": d} for d in data]
        success, failed = helpers.bulk(self.es, actions, stats_only=True)
        print(f"[ES] 写入 {self.index_name} 成功 {success} 条，失败 {failed} 条")


class LinkWriter:
    """link_pe_in"""

    def __init__(self, *, index_name, es, index_type, **ctx):
        self.index_name = index_name
        self.es = es
        self.index_type = index_type
        self.ctx = ctx

    def write(self, count=10):
        mappings = {"properties": {
            "batch_num": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "branch_name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "branch_number": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "branch_rated_capacity": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "branch_type": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "branch_type_abbreviation": {"type": "text",
                                         "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "city_id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "collect_time": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "county_id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_number": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_rated_capacity": {"type": "text",
                                           "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_type": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_type_abbreviation": {"type": "text",
                                              "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_device_name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_device_ralated_room": {"type": "text",
                                         "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_device_type": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_use_status": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "irms_province_code": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "lifecycle_status": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "province_id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "qr_code_no": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "qualitor": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "related_device": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "related_device_type": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "related_room": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "related_site": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "res_code": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
        }}
        self._ensure_index(mappings)
        data = []
        for i in range(count):
            doc = {
                "batch_num": self.ctx.get('batch_num', '20250729'),
                "branch_name": f"分支_{i}",
                "branch_number": str(i),
                "branch_rated_capacity": f"{random.randint(10, 500)}A",
                "branch_type": "普通",
                "branch_type_abbreviation": "PT",
                "city_id": self.ctx.get('city_id', '440100'),
                "collect_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "county_id": self.ctx.get('county_id', '440101'),
                "down_branch_name": f"下级分支_{i}",
                "down_branch_number": f"d{i}",
                "down_branch_rated_capacity": f"{random.randint(10, 500)}A",
                "down_branch_type": "普通",
                "down_branch_type_abbreviation": "PT",
                "down_device_name": f"下级设备_{i}",
                "down_device_ralated_room": f"room_{i}",
                "down_device_type": "switch_power",
                "down_use_status": "在用",
                "irms_province_code": self.ctx.get('irms_province_code', 'GZ'),
                "lifecycle_status": "在网",
                "province_id": self.ctx.get('province_id', '440000'),
                "qr_code_no": '',
                "qualitor": 'test',
                "related_device": f"device_{i}",
                "related_device_type": "switch_power",
                "related_room": f"room_{i}",
                "related_site": f"site_{i}",
                "res_code": f"res_{i}",
            }
            data.append(doc)
        self._bulk(data)

    def _ensure_index(self, mappings):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name,
                                   body={"settings": ESConfig.INDEX_SETTINGS,
                                         "mappings": {"point_history_data": mappings}})
            print(f"[ES] 创建索引 {self.index_name}")
        else:
            print(f"[ES] 索引已存在 {self.index_name}")

    def _bulk(self, data):
        actions = [{"_index": self.index_name, "_type": "point_history_data", "_source": d} for d in data]
        success, failed = helpers.bulk(self.es, actions, stats_only=True)
        print(f"[ES] 写入 {self.index_name} 成功 {success} 条，失败 {failed} 条")


# ============ 工厂类 ============ #
class WriterFactory:
    @staticmethod
    def create_writer(index_category: str, *, es_url: str = ESConfig.ES_URL, **kwargs) -> Any:
        es = Elasticsearch(es_url)
        if index_category in ['air', 'battery', 'low_ac_distribution', 'switch_power',
                              'energy_save', 'high_dc_distribution', 'high_distribution',
                              'high_power', 'smart_meter', 'transform', 'transform_device', 'ups',
                              'low_dc_distribution', 'power_generation', 'power_monitor', 'other']:
            index_name = ZZAllInOneWriter(es_url=es_url, **kwargs)._make_index_name(index_category)
            return DeviceWriter(index_name=index_name, es=es, index_type=index_category, **kwargs)
        if index_category in ['room', 'room_property', 'site', 'site_property']:
            index_name = ZZAllInOneWriter(es_url=es_url, **kwargs)._make_index_name(index_category)
            return MetaWriter(index_name=index_name, es=es, index_type=index_category, **kwargs)
        if index_category in ['irms_dc_map', 'irms_rom_map', 'irms_site_map']:
            index_name = ZZAllInOneWriter(es_url=es_url, **kwargs)._make_index_name(index_category)
            return MapWriter(index_name=index_name, es=es, index_type=index_category, **kwargs)
        if index_category == 'link_pe_in':
            index_name = ZZAllInOneWriter(es_url=es_url, **kwargs)._make_index_name(index_category)
            return LinkWriter(index_name=index_name, es=es, index_type=index_category, **kwargs)
        raise ValueError(f"不支持的索引类别: {index_category}")


# ============ MySQL 连接 ============ #
class MysqlConnect:
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

        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        self.url = conf.get_conf(env, 'esurl')

        engines = f"mysql+pymysql://{urlquote(self.dbuser)}:{urlquote(self.dbpw)}@{self.dbip}:{self.dbport}/{urlquote(self.dbname)}?charset=utf8"
        self.engine = create_engine(engines, max_overflow=5)
        self.conn = self.engine.connect()

        sql_path = 'your_path/selectForESList.sql'  # 换成你真实路径
        self.sql_file = open(sql_path, encoding='utf-8')

    def get_sql_list(self) -> List[str]:
        content = self.sql_file.read()
        return [sql.strip() for sql in content.split(';') if sql.strip()]

    def get_provincedata(self, sql_index: int) -> List[Any]:
        sql_list = self.get_sql_list()
        if sql_index >= len(sql_list):
            return []
        sql = sql_list[sql_index]
        params = {'precinct_id': self.precinct_id + '%'}
        if sql_index == 1:
            params.update({'mete_code': self.mete_code, 'device_id': self.device_id})
        elif sql_index == 2:
            params.update({'mete_code': self.mete_code})
        result = self.conn.execute(text(sql), params)
        return result.fetchall()

    def insert_esdata_device(self) -> List[Any]:
        if self.match_mode == 0:
            sql_index = 5
        elif self.match_mode == 1:
            sql_index = 6
        elif self.match_mode == 2:
            if self.device_id == '1' and self.mete_code == '000000':
                sql_index = 4
            else:
                sql_index = 0
        data = self.get_provincedata(sql_index)
        print(f"预计写入数据条数========== {len(data)}")
        return data


# ============ ZZMatchSpider ============ #
class ZZMatchSpider:
    def __init__(self, precinct_id: str, **kwargs):
        self.precinct_id = precinct_id
        self.batch_num = kwargs.get('batch_num', datetime.now().strftime('%Y%m%d'))
        self.zh_label = kwargs.get('zh_label', f'贵州贵通信枢纽楼')
        self.force_create = kwargs.get('force_create', False)
        self.irms_province_code = kwargs.get('irms_province_code', 'GZ')
        self.province = kwargs.get('province_id', '520000')
        self.city = kwargs.get('city_id', '520400')
        self.site_int_id = None
        self.mains_nature = kwargs.get('mains_nature', '市电转供')
        self.power_site_level = kwargs.get('power_site_level', '传输节点')
        self.power_room_type = kwargs.get('power_room_type', '汇聚机房')
        self.power_supply_mode = kwargs.get('power_supply_mode', '双电源双回路供电')
        self.cutin_date = kwargs.get('cutin_date', datetime.now().strftime('%Y-%m-%d'))
        self.site_type = kwargs.get('site_type', random.choice(
            ['核心站点', '核心站点（配套）', '骨干站点', '汇聚站点', '接入站点', '用户站点', '其他站点']
        ))
        self.county_id = kwargs.get('county_id', '')
        self.site_names = []
        self.room_names = []
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

    def name_match_site_room(self):
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
            room_name = record[1]
            room_id = record[0]
            if room_name not in getattr(self, 'room_names', []):
                self.room_names.append(room_name)
                self._create_room_and_property_and_irm(room_name, room_id)
                print(f"机房已写入: {room_name}")

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
        site_writer = WriterFactory.create_writer(
            'site', batch_num=self.batch_num, zh_label=site_name,
            city_id=self.city, province_id=self.province,
            irms_province_code=self.irms_province_code, cutin_date=self.cutin_date,
            county_id=self.county_id, site_type=self.site_type
        )
        self.site_int_id = site_writer.site_int_id
        self.province = site_writer.province_id
        self.city = site_writer.city_id
        site_writer.write(count=1, force_create=self.force_create)

        prop_writer = WriterFactory.create_writer(
            'site_property', batch_num=self.batch_num, site_int_id=self.site_int_id,
            province_id=self.province, city_id=self.city, irms_province_code=self.irms_province_code,
            power_site_level=self.power_site_level, mains_nature=self.mains_nature,
            cutin_date=self.cutin_date, power_related_site_name=self.power_related_site_name,
            county_id=self.county_id, site_type=self.site_type
        )
        prop_writer.write(count=1, force_create=self.force_create)
        print(f"站点对创建成功: {site_name} (site_int_id: {self.site_int_id})")

    def _create_room_and_property_and_irm(self, room_name: str, room_id: str):
        room_writer = WriterFactory.create_writer(
            'room', batch_num=self.batch_num, room_zh_label=room_name,
            site_int_id=self.site_int_id, city_id=self.city, province_id=self.province,
            irms_province_code=self.irms_province_code, cutin_date=self.cutin_date,
            power_room_type=self.power_room_type, power_supply_mode=self.power_supply_mode,
            county_id=self.county_id
        )
        self.room_int_id = room_writer.room_int_id
        self.province = room_writer.province_id
        self.city = room_writer.city_id
        room_writer.write(count=1, force_create=self.force_create)

        prop_writer = WriterFactory.create_writer(
            'room_property', batch_num=self.batch_num, room_int_id=self.room_int_id,
            province_id=self.province, city_id=self.city, site_int_id=self.site_int_id,
            irms_province_code=self.irms_province_code, cutin_date=self.cutin_date,
            power_room_type=self.power_room_type, power_supply_mode=self.power_supply_mode,
            county_id=self.county_id
        )
        prop_writer.write(count=1, force_create=self.force_create)

        irms = WriterFactory.create_writer(
            'irms_rom_map', batch_num=self.batch_num, room_dh_name=room_id,
            room_zg_name=self.room_int_id, city_id=self.city, province_id=self.province,
            county_id=self.county_id
        )
        irms.write(count=1, force_create=self.force_create)
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


# ============ 命令行入口 ================= #
if __name__ == '__main__':
    # 示例：完全沿用原来调用方式
    spider = ZZMatchSpider(precinct_id='01-01-11', batch_num='20240101', force_create=False,
                           mains_nature='用于电费分析', power_site_level='传输节点',
                           power_room_type='汇聚机房', power_supply_mode='双电源双回路供电',
                           cutin_date='2025-01-02', province_id='440000', city_id='440200',
                           match_mode=0, irms_province_code='GD', county_id='440511',
                           site_type='汇聚站点')
    spider.name_match_site()
    # spider.name_match_site_room()
    # spider.name_match_site_room_device()
