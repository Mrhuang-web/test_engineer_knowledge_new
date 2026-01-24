# writers.py
from elasticsearch import helpers
from index_builder import IndexBuilder


class BaseWriter:
    def __init__(self, index_type, index_suffix, **kwargs):
        self.index_type = index_type
        self.index_suffix = index_suffix
        self.es = Elasticsearch()
        self.doc_type = "point_history_data"
        self._load_business_params(kwargs)
        self.index_builder = IndexBuilder(index_type, index_suffix)
        self.index_builder.create_index()

    def _load_business_params(self, kwargs):
        self.site_type = kwargs.get('site_type', '核心站点')
        self.irms_province_code = kwargs.get('irms_province_code', 'GZ')
        self.batch_num = kwargs.get('batch_num', datetime.datetime.now().strftime('%Y%m%d'))
        self.related_dc = kwargs.get('related_dc', "")
        self.zh_label = kwargs.get('zh_label', f"test_{datetime.datetime.now().strftime('%Y%m%d')}")
        self.power_device_id = kwargs.get('power_device_id', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.device_res_code = kwargs.get('device_res_code', str(random.randint(10 ** 17, 10 ** 18 - 1)))
        self.device_zh_label = kwargs.get('device_zh_label', f"device_{random.randint(1000, 9999)}")
        self.province_id = kwargs.get('province_id', '520000')
        self.city_id = kwargs.get('city_id', '520400')
        self.county_id = kwargs.get('county_id', '000000')

    def bulk_write(self, data_list):
        actions = [
            {"_index": self.index_builder._generate_index_name(), "_type": self.doc_type, "_source": data}
            for data in data_list
        ]
        helpers.bulk(self.es, actions)
        print(f"成功写入 {len(data_list)} 条数据。")


class DeviceWriter(BaseWriter):
    def __init__(self, index_type, index_suffix, **kwargs):
        super().__init__(index_type, index_suffix, **kwargs)

    def generate_mock_data(self, count):
        return DataGenerator.generate_device_data(self.index_type, count)
