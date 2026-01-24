# spider.py
from writers import DeviceWriter


class ZZMatchSpider:
    def __init__(self, precinct_id, **kwargs):
        self.precinct_id = precinct_id
        self.batch_num = kwargs.get('batch_num', datetime.datetime.now().strftime('%Y%m%d'))
        self.index_suffix = kwargs.get('index_suffix', 'YYYYMMm')
        self.site_type = kwargs.get('site_type', '核心站点')
        self.irms_province_code = kwargs.get('irms_province_code', 'GZ')
        self.province_id = kwargs.get('province_id', '520000')
        self.city_id = kwargs.get('city_id', '520400')
        self.county_id = kwargs.get('county_id', '000000')

    def name_match_site(self):
        writer = DeviceWriter('air', self.index_suffix, batch_num=self.batch_num, site_type=self.site_type,
                              irms_province_code=self.irms_province_code, province_id=self.province_id,
                              city_id=self.city_id, county_id=self.county_id)
        data = writer.generate_mock_data(10)
        writer.bulk_write(data)
        print("站点匹配完成。")
