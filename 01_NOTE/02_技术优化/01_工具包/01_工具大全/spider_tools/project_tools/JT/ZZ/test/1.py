# mock_es_writer.py
"""
ES数据模拟写入工具 - 简化版
支持设备、房间、站点等多种索引类型
"""

import json
import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Callable
from elasticsearch import Elasticsearch, helpers


# ==================== 配置 ====================
@dataclass
class ESConfig:
    """ES配置"""
    url: str = "http://10.1.203.38:9200"
    index_prefix: str = "ods_zz"
    number_of_replicas: int = 0
    refresh_interval: str = "5s"

    # 索引后缀规则：类型 -> 生成函数
    INDEX_SUFFIX_RULES = {
        'YYYYMMm': lambda dt: f"{dt.strftime('%Y%m')}m",
        'YYYYy': lambda dt: f"{dt.strftime('%Y')}y",
        'YYYYMMDDd': lambda dt: f"{dt.strftime('%Y%m%d')}d",
    }


# ==================== 核心写入器 ====================
class ESWriter:
    """简化版ES写入器 - 职责单一"""

    def __init__(self, config: ESConfig, index_name: str):
        self.config = config
        self.index_name = index_name
        self.es = Elasticsearch(config.url)
        self.doc_type = "point_history_data"

    def create_index(self, mapping: Optional[Dict] = None, force: bool = False):
        """创建索引（安全模式）"""
        exists = self.es.indices.exists(index=self.index_name)

        if exists and not force:
            print(f"✓ 索引已存在: {self.index_name}")
            return

        if exists and force:
            print(f"⚠️  强制删除并重建: {self.index_name}")
            self.es.indices.delete(index=self.index_name, ignore=[400, 404])

        # 创建索引
        self.es.indices.create(
            index=self.index_name,
            body={
                "settings": {
                    "number_of_replicas": self.config.number_of_replicas,
                    "refresh_interval": self.config.refresh_interval
                }
            },
            ignore=[400]
        )

        # 添加mapping
        if mapping:
            self.es.indices.put_mapping(
                index=self.index_name,
                doc_type=self.doc_type,
                body={self.doc_type: mapping}
            )
        print(f"✓ 索引创建成功: {self.index_name}")

    def bulk_write(self, data: List[Dict]) -> dict:
        """批量写入数据"""
        if not data:
            return {"success": 0, "failed": 0}

        actions = [
            {"_index": self.index_name, "_type": self.doc_type, "_source": doc}
            for doc in data
        ]

        try:
            success, failed = helpers.bulk(self.es, actions, stats_only=True)
            self.es.indices.refresh(index=self.index_name)
            return {"success": success, "failed": failed, "total": len(data)}
        except Exception as e:
            print(f"❌ 写入失败: {e}")
            return {"success": 0, "failed": len(data), "error": str(e)}


# ==================== 数据生成器 ====================
class DataGenerator:
    """数据生成器 - 独立职责"""

    # 字段生成规则
    FIELD_GENERATORS = {
        lambda f: f.endswith(('_id', '_code')): lambda: f"CODE_{random.randint(1000, 9999)}",
        lambda f: f.endswith(('_time', '_date')): lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        lambda f: 'power' in f: lambda: random.randint(10, 500),
        lambda f: 'voltage' in f: lambda: f"{random.randint(220, 380)}V",
        lambda f: 'capacity' in f: lambda: f"{random.randint(50, 500)}AH",
        lambda f: f in ['lifecycle_status', 'maintainor', 'qualitor']:
            lambda: random.choice(['active', 'inactive', 'maintenance']),
    }

    @staticmethod
    def generate_doc(fields: List[str], overrides: Dict[str, Any] = None) -> Dict:
        """生成单条文档"""
        doc = overrides or {}

        for field in fields:
            if field in doc:
                continue

            # 匹配字段生成规则
            for matcher, generator in DataGenerator.FIELD_GENERATORS.items():
                if matcher(field):
                    doc[field] = generator()
                    break
            else:
                # 默认生成
                doc[field] = f"mock_{field}_{random.randint(1, 100)}"

        return doc


# ==================== 索引定义 ====================
class IndexDefinition:
    """索引定义 - 聚合元数据"""

    def __init__(self, name: str, suffix_type: str, fields: List[str]):
        self.name = name
        self.suffix_type = suffix_type
        self.fields = fields

    def get_index_name(self, config: ESConfig, batch_num: str = None) -> str:
        """生成完整索引名"""
        prefix = f"{config.index_prefix}_{self.name}"

        # 根据batch_num或当前时间生成后缀
        if batch_num and len(batch_num) >= 6:
            if self.suffix_type == 'YYYYMMm':
                suffix = batch_num[:6] + 'm'
            elif self.suffix_type == 'YYYYy':
                suffix = batch_num[:4] + 'y'
            elif self.suffix_type == 'YYYYMMDDd':
                suffix = batch_num + 'd' if len(batch_num) == 8 else batch_num[:8] + 'd'
        else:
            suffix = ESConfig.INDEX_SUFFIX_RULES[self.suffix_type](datetime.now())

        return f"{prefix}_{suffix}"


# 预定义索引
INDEX_DEFINITIONS = {
    # 设备类
    'air': IndexDefinition('device_air', 'YYYYMMm', [
        'assets_no', 'batch_num', 'city_id', 'collect_time', 'device_code',
        'device_number', 'device_subclass', 'device_type', 'rated_cooling_capacity',
        'rated_input_power', 'related_room', 'related_site', 'zh_label'
    ]),
    'battery': IndexDefinition('device_battery', 'YYYYMMm', [
        'assets_no', 'backup_time', 'batch_num', 'cell_voltage_level', 'device_code',
        'reted_capacity', 'total_monomers_number', 'vendor_id', 'zh_label'
    ]),
    'ups': IndexDefinition('device_ups', 'YYYYy', [
        'assets_no', 'batch_num', 'rated_capacity', 'rated_output_voltage',
        'related_system', 'vendor_id', 'zh_label'
    ]),

    # 房间类
    'room': IndexDefinition('room', 'YYYYMMDDd', [
        'uuid', 'province_id', 'equiproom_type', 'equiproom_level',
        'room_area', 'installed_rack_num', 'zh_label'
    ]),
    'room_property': IndexDefinition('room_property', 'YYYYMMm', [
        'power_room_id', 'power_room_name', 'power_supply_mode', 'battery_backup_time'
    ]),

    # 站点类
    'site': IndexDefinition('site', 'YYYYMMm', [
        'address', 'site_type', 'cutin_date', 'latitude', 'longitude',
        'int_id', 'zh_label', 'county_id'
    ]),
    'site_property': IndexDefinition('site_property', 'YYYYMMm', [
        'zh_label', 'mains_capacity', 'design_pue', 'actual_pue'
    ]),
}


# ==================== 主API ====================
class MockDataWriter:
    """主API类 - 简洁入口"""

    def __init__(self, config: ESConfig = None):
        self.config = config or ESConfig()

    def write(self, index_key: str, count: int = 100, **kwargs):
        """
        写入mock数据

        Args:
            index_key: 索引键名 (如 'air', 'room', 'site')
            count: 数据条数
            **kwargs: 覆盖字段值，如 province_id='520000', city_id='520400'
        """
        # 获取索引定义
        if index_key not in INDEX_DEFINITIONS:
            raise ValueError(f"不支持的索引类型: {index_key}. 可选: {list(INDEX_DEFINITIONS.keys())}")

        definition = INDEX_DEFINITIONS[index_key]

        # 生成索引名
        index_name = definition.get_index_name(self.config, kwargs.get('batch_num'))
        print(f"\n{'=' * 60}")
        print(f"写入数据: {index_name}")
        print(f"{'=' * 60}")

        # 创建写入器
        writer = ESWriter(self.config, index_name)
        writer.create_index(force=kwargs.get('force_create', False))

        # 生成数据
        data = []
        for i in range(count):
            doc = DataGenerator.generate_doc(definition.fields, kwargs)
            data.append(doc)

        # 写入
        result = writer.bulk_write(data)
        print(f"✓ 成功: {result['success']}, 失败: {result['failed']}")

        return result


# ==================== 使用示例 ====================
if __name__ == '__main__':
    writer = MockDataWriter()

    # 示例1: 写入空调设备
    writer.write('air', count=30, province_id='520000', city_id='520400')

    # 示例2: 写入UPS设备
    writer.write('ups', count=20, batch_num='202511')

    # 示例3: 写入房间数据
    writer.write('room', count=25, date='20251103')

    # 示例4: 强制重建索引
    writer.write('site', count=10, force_create=True, zh_label="测试站点")