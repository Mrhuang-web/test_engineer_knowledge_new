from typing import List, Dict
from spider_tools.project_tools.JT.ZZ.zz_match_new2.databuilder import DataBuilder
from spider_tools.project_tools.JT.ZZ.zz_match_new2.base_writer import BaseWriter


# --------------------------------------------------------------------------- #
# 四种内部 Writer
# --------------------------------------------------------------------------- #
class DeviceWriter(BaseWriter):
    def __init__(self, *, index_type, **kwargs):
        super().__init__(index_type=index_type, **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        context = {key: getattr(self, key) for key in dir(self) if not key.startswith('_')}
        return DataBuilder.build_device_docs(self.index_type, count, context)


class MetaWriter(BaseWriter):
    """room / room_property / site / site_property"""

    def __init__(self, *, index_type, **kwargs):
        super().__init__(index_type=index_type, **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        context = {key: getattr(self, key) for key in dir(self) if not key.startswith('_')}
        return DataBuilder.build_device_docs(self.index_type, count, context)


class MapWriter(BaseWriter):
    """irms_*_map"""

    def __init__(self, *, index_type, **kwargs):
        super().__init__(index_type=index_type, **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        context = {key: getattr(self, key) for key in dir(self) if not key.startswith('_')}
        return DataBuilder.build_device_docs(self.index_type, count, context)


class LinkWriter(BaseWriter):
    """link_pe_in"""

    def __init__(self, *, index_type, **kwargs):
        super().__init__(index_type=index_type, **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        context = {key: getattr(self, key) for key in dir(self) if not key.startswith('_')}
        return DataBuilder.build_device_docs(self.index_type, count, context)
