#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ZZ 22 类索引一次性写入 ES（单文件完整版 + 工厂类 + 初始化字段支持）
"""

import random
import uuid
from datetime import datetime
from typing import List, Dict, Any
from elasticsearch import Elasticsearch, helpers

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
        'low_dc_distribution': 'ods_zz_device_low_dc_distribution', 'power_generation': 'ods_zz_device_power_generation',
        'power_monitor': 'ods_zz_device_power_monitor', 'other': 'ods_zz_device_other',
        'room': 'ods_zz_room', 'room_property': 'ods_zz_room_property',
        'site': 'ods_zz_site', 'site_property': 'ods_zz_site_property',
        'irms_dc_map': 'ods_zz_irms_dc_map', 'irms_rom_map': 'ods_zz_irms_rom_map', 'irms_site_map': 'ods_zz_irms_site_map',
    }
    INDEX_SUFFIX_RULES = {
        'YYYYMMm': ['air', 'battery', 'low_ac_distribution', 'switch_power', 'room_property', 'site', 'site_property', 'link_pe_in'],
        'YYYYy': ['energy_save', 'high_dc_distribution', 'high_distribution', 'high_power', 'smart_meter', 'transform', 'transform_device', 'ups',
                  'irms_dc_map', 'irms_rom_map', 'irms_site_map'],
        'YYYYMMDDd': ['room'],
    }
    INDEX_SETTINGS = {"index": {"number_of_replicas": "0", "refresh_interval": "5s"}}

# ============ 字段生成器（复用原逻辑） ============ #
class DataBuilder:
    DEVICE_FIELDS = {
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
                                   body={"settings": ESConfig.INDEX_SETTINGS, "mappings": {"point_history_data": mappings}})
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
        mappings = {"properties": {f: {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}}
                                   for f in ['batch_num', 'collect_time', 'zh_label']}}
        if 'room' in self.index_type:
            mappings['properties']['cutin_date'] = {"type": "date"}
        if 'site' in self.index_type:
            mappings['properties']['cutin_date'] = {"type": "date"}
        self._ensure_index(mappings)
        data = []
        for i in range(count):
            doc = {
                'batch_num': self.ctx.get('batch_num', '20250729'),
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'zh_label': f"{self.index_type}_{i}"
            }
            if 'room' in self.index_type or 'site' in self.index_type:
                doc['cutin_date'] = datetime.now().strftime('%Y-%m-%d')
            data.append(doc)
        self._bulk(data)

    def _ensure_index(self, mappings):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name,
                                   body={"settings": ESConfig.INDEX_SETTINGS, "mappings": {"point_history_data": mappings}})
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
        mappings = {"properties": {
            "batch_num": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "uuid": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "pms_id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "pms_name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "dh_id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "dh_name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "zg_id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "zg_name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "statis_ymd": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "province_id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
        }}
        self._ensure_index(mappings)
        data = []
        for i in range(count):
            doc = {
                "batch_num": self.ctx.get('batch_num', '20250729'),
                "uuid": str(uuid.uuid4()),
                "pms_id": f"PMS{random.randint(10000, 99999)}",
                "pms_name": f"PMS系统_{i}",
                "dh_id": f"DH{random.randint(10000, 99999)}",
                "dh_name": f"DH_{i}",
                "zg_id": f"ZG{random.randint(10000, 99999)}",
                "zg_name": f"ZG_{i}",
                "statis_ymd": self.ctx.get('batch_num', '20250729'),
                "province_id": self.ctx.get('province_id', '440000'),
            }
            data.append(doc)
        self._bulk(data)

    def _ensure_index(self, mappings):
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name,
                                   body={"settings": ESConfig.INDEX_SETTINGS, "mappings": {"point_history_data": mappings}})
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
            "branch_type_abbreviation": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "city_id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "collect_time": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "county_id": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_number": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_rated_capacity": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_type": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_branch_type_abbreviation": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_device_name": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
            "down_device_ralated_room": {"type": "text", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
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
                                   body={"settings": ESConfig.INDEX_SETTINGS, "mappings": {"point_history_data": mappings}})
            print(f"[ES] 创建索引 {self.index_name}")
        else:
            print(f"[ES] 索引已存在 {self.index_name}")

    def _bulk(self, data):
        actions = [{"_index": self.index_name, "_type": "point_history_data", "_source": d} for d in data]
        success, failed = helpers.bulk(self.es, actions, stats_only=True)
        print(f"[ES] 写入 {self.index_name} 成功 {success} 条，失败 {failed} 条")


# ================= 命令行入口 ================= #
if __name__ == '__main__':
    # 示例：完全沿用原来调用方式
    spider = ZZAllInOneWriter(precinct_id='01-01-11', batch_num='20240101', force_create=False,
                              mains_nature='用于电费分析', power_site_level='传输节点',
                              power_room_type='汇聚机房', power_supply_mode='双电源双回路供电',
                              cutin_date='2025-01-02', province_id='440000', city_id='440200',
                              match_mode=0, irms_province_code='GD', county_id='440511',
                              site_type='汇聚站点')
    spider.write_all(count=10)