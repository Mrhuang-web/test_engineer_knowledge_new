# index_builder.py
from elasticsearch import Elasticsearch
from config import ESConfig


class IndexBuilder:
    def __init__(self, index_type, index_suffix):
        self.es = Elasticsearch(ESConfig.ES_URL)
        self.index_type = index_type
        self.index_suffix = index_suffix

    def create_index(self):
        index_name = self._generate_index_name()
        if self.es.indices.exists(index=index_name):
            print(f"索引 {index_name} 已存在，跳过创建。")
            return

        print(f"创建索引: {index_name}")
        self.es.indices.create(index=index_name, body=self._get_index_settings())
        print(f"索引 {index_name} 创建成功。")

    def _generate_index_name(self):
        prefix = ESConfig.INDEX_PREFIX_MAP.get(self.index_type)
        if not prefix:
            raise ValueError(f"未知的索引类型: {self.index_type}")

        suffix = self._get_suffix_from_batch()
        return f"{prefix}_{suffix}"

    def _get_suffix_from_batch(self):
        if self.index_suffix == 'YYYYMMm':
            return datetime.datetime.now().strftime('%Y%m') + 'm'
        elif self.index_suffix == 'YYYYy':
            return datetime.datetime.now().strftime('%Y') + 'y'
        elif self.index_suffix == 'YYYYMMDDd':
            return datetime.datetime.now().strftime('%Y%m%d') + 'd'
        else:
            raise ValueError(f"未知的索引后缀规则: {self.index_suffix}")

    def _get_index_settings(self):
        return ESConfig.INDEX_SETTINGS
