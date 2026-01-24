class RoomWriter(BaseWriter):
    """房间写入器 - 保留原始逻辑和字段顺序"""

    def __init__(self, **kwargs):
        super().__init__(index_type='room', **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        room_types = ['数据中心', '接入网', '核心网', '基站']
        levels = ['A级', 'B级', 'C级']

        docs = []
        for i in range(count):
            doc = {
                'china_tower_station_code': f"",
                'asset_address_code': f"{random.randint(300000, 399999)}KH{random.randint(10000000, 99999999)}",
                'equipment_power': f"{random.uniform(0, 50):.1f}",
                'cutin_date': self.cutin_date,
                'china_tower_room_type': random.choice(['其他机房']),
                'row_num': f"{random.randint(1, 100)}",
                'end_row': f"{random.randint(1, 100)}",
                'retire_time': f"",
                'property_unit': random.choice(['中国移动']),
                'county_id': f"{random.randint(350000, 359999)}",
                'int_id': self.room_int_id,
                'qualitor': f"test{random.randint(1, 100)}",
                'lifecycle_status': random.choice(['在网', '退网', '工程', '预占']),
                'column_num': str(random.randint(1, 20)) if random.random() > 0.3 else "",
                'equiproom_level': random.choice(['核心（省内）']),
                'start_column': str(random.randint(1, 20)) if random.random() > 0.5 else "",
                'airconditioner_power': f"{random.uniform(0, 30):.1f}",
                'property_right': random.choice(['自有自建']),
                'floor_num': str(random.randint(1, 30)),
                'start_row': str(random.randint(1, 20)) if random.random() > 0.5 else "",
                'length': f"{random.randint(5, 50)}" if random.random() > 0.3 else "",
                'irms_province_code': self.irms_province_code,
                'room_area': f"{random.randint(10, 1000)}",
                'related_site': self.site_int_id,
                'batch_num': self.batch_num,
                'alias_name': f"机房别名_{random.randint(1000, 9999)}" if random.random() > 0.6 else "",
                'shared_unit': random.choice(['移动']),
                'zh_label': self.room_zh_label,
                'province_id': self.province_id,
                'equiproom_type': random.choice(['其他机房']),
                'width': f"{random.randint(10, 99)}",
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city_id': self.city_id,
                'end_column': f"{random.randint(10, 99)}",
            }

            # # 填充剩余字段（保持原始逻辑）
            # for field in DataBuilder.ROOM_FIELDS:
            #     if field not in doc:
            #         doc[field] = f"mock_{field}_{random.randint(1, 100)}"

            docs.append(doc)
        return docs

    def write(self, count: int = 100, **kwargs):
        """保持与原始一致的写入接口"""
        super().write(count=count, **kwargs)