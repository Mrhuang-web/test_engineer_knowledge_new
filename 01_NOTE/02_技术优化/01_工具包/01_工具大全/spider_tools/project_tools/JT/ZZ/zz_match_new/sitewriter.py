class SiteWriter(BaseWriter):
    """站点写入器 - 保留原始字段和逻辑"""

    def __init__(self, **kwargs):
        super().__init__(index_type='site', **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        site_types = ['核心局站', '汇聚局站', '接入局站', '基站']

        docs = []
        for i in range(count):
            doc = {
                'china_tower_station_code': f"mock_{random.randint(1, 100)}",
                'address': f"XX省XX市XX区XX路{random.randint(1, 999)}号",
                'site_type': self.site_type,
                'cutin_date': self.cutin_date,
                'latitude': f"{random.uniform(30, 45):.6f}",
                'irms_province_code': self.irms_province_code,
                'floor_number': f"{random.randint(1, 20)}",
                'batch_num': self.batch_num,
                'related_dc': self.related_dc,
                'alias_name': self.zh_label,
                'standardaddress': f"{random.randint(10000, 99999)}",
                'zh_label': self.zh_label,
                'county_id': self.county_id,
                'province_id': self.province_id,
                'int_id': self.site_int_id,
                'qualitor': "测试记录",
                'lifecycle_status': "在网",
                'use_corp': "中国移动",
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city_id': self.city_id,
                'longitude': f"{random.uniform(100, 125):.6f}",
            }
            docs.append(doc)
        return docs