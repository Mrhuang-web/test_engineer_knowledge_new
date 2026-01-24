import random
from datetime import datetime
from elasticsearch import helpers
from spider_tools.project_tools.JT.ZZ.zz_match_new2.databuilder import DataBuilder
from spider_tools.project_tools.JT.ZZ.zz_match_new2.esconfig import ESConfig


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
