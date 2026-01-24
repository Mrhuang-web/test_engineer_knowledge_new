class IrmsMapWriter(BaseWriter):
    """IRMS映射写入器 - 保留原始逻辑"""

    def __init__(self, map_type: str, **kwargs):
        self.map_type = map_type
        super().__init__(index_type=f'irms_{map_type}_map', **kwargs)

    def generate_mock_data(self, count: int = 50) -> List[Dict]:
        docs = []
        for i in range(count):
            if self.map_type == 'rom':
                doc = {
                    'pms_id': f"PMS{random.randint(10000, 99999)}",
                    'address_code': f"",
                    'pms_name': f"",
                    'dh_name': self.room_dh_name,
                    'zg_name': self.room_zg_name,
                    'province_id': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'dh_id': f"",
                    'zg_id': self.province_id,
                    'batch_num': self.batch_num,
                    'statis_ymd': self.batch_num,
                    'uuid': uuid.uuid4(),
                }
            else:
                doc = {
                    'pms_id': f"PMS{random.randint(10000, 99999)}",
                    'pms_name': f"PMS系统_{random.randint(1, 100)}",
                    'dh_name': self.room_dh_name,
                    'zg_name': self.room_zg_name,
                    'province_id': self.province_id,
                    'dh_id': f"DH{random.randint(10000, 99999)}",
                    'zg_id': f"ZG{random.randint(10000, 99999)}",
                    'batch_num': self.batch_num,
                    'statis_ymd': self.batch_num,
                    'uuid': uuid.uuid4(),
                }

            docs.append(doc)
        return docs