from spider_tools.project_tools.JT.ZZ.zz_match_new2.esconfig import ESConfig
from spider_tools.project_tools.JT.ZZ.zz_match_new2.writer import DeviceWriter
from spider_tools.project_tools.JT.ZZ.zz_match_new2.writer import LinkWriter
from spider_tools.project_tools.JT.ZZ.zz_match_new2.writer import MapWriter
from spider_tools.project_tools.JT.ZZ.zz_match_new2.writer import MetaWriter
from datetime import datetime
from typing import List
from elasticsearch import Elasticsearch


# ============ 统一写入器 ============ #
class ZZAllInOneWriter:
    def __init__(self, **kwargs):
        self.es_url = kwargs.pop('es_url', ESConfig.ES_URL)
        self.es = Elasticsearch(self.es_url)
        self.kwargs = kwargs  # 全局默认参数
        self._registry = self._build_registry()

    def _build_registry(self):
        reg = {}
        device_types = [
            'air', 'battery', 'low_ac_distribution', 'switch_power',
            'energy_save', 'high_dc_distribution', 'high_distribution',
            'high_power', 'smart_meter', 'transform', 'transform_device', 'ups',
            'low_dc_distribution', 'power_generation', 'power_monitor', 'other',
            'room', 'room_property', 'site', 'site_property',
            'irms_dc_map', 'irms_rom_map', 'irms_site_map'
        ]
        for t in device_types:
            if t in ['room', 'room_property', 'site', 'site_property']:
                reg[t] = {'category': 'meta', 'cls': MetaWriter, 'index_type': t}
            elif t in ['irms_dc_map', 'irms_rom_map', 'irms_site_map']:
                reg[t] = {'category': 'map', 'cls': MapWriter, 'index_type': t}
            else:
                reg[t] = {'category': 'device', 'cls': DeviceWriter, 'index_type': t}
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
