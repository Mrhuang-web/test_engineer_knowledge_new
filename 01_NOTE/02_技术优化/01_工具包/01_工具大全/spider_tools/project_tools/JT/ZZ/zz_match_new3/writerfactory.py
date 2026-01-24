from typing import Any
from elasticsearch import Elasticsearch
from spider_tools.project_tools.JT.ZZ.zz_match_new2.esconfig import ESConfig
from spider_tools.project_tools.JT.ZZ.zz_match_new2.writer import DeviceWriter
from spider_tools.project_tools.JT.ZZ.zz_match_new2.writer import LinkWriter
from spider_tools.project_tools.JT.ZZ.zz_match_new2.writer import MapWriter
from spider_tools.project_tools.JT.ZZ.zz_match_new2.writer import MetaWriter
from spider_tools.project_tools.JT.ZZ.zz_match_new2.zzallinonewriter import ZZAllInOneWriter


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
