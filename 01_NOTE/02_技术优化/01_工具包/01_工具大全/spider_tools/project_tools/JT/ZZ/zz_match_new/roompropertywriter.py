class RoomPropertyWriter(BaseWriter):
    """房间属性写入器"""

    def __init__(self, **kwargs):
        super().__init__(index_type='room_property', **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        docs = []
        for i in range(count):
            doc = {
                'refrigeration_mode': random.choice(['风冷']),
                'power_room_type': self.power_room_type,
                'power_related_site_name': self.site_int_id,  # 也需要与站点id一致
                'battery_backup_time': f"{random.randint(1, 24)}",
                'power_supply_mode': self.power_supply_mode,
                'space_room_type': f"{random.choice(['传输机房'])}",
                'power_room_name': self.room_zg_name,  # 需要确认有无作用
                'irms_province_code': self.irms_province_code,
                'batch_num': self.batch_num,
                'ac_config': random.choice(['其他']),
                'res_code': self.room_res_code,
                'power_room_id': f"{random.randint(1, 2)}",
                'zh_label': self.room_int_id,
                'county_id': self.city_id,
                'power_supply_type': f"交流{random.randint(10000, 99999)}V",
                'ac_terminal': random.choice(['精密空调', '普通空调']),
                'power_monitor_conf': f"{random.choice(['有', '无'])}",
                'province_id': self.province_id,
                'video_monitor_conf': f"{random.choice(['有', '无'])}",
                'refer_pue': f"{random.randint(1, 2)}",
                'log_saved_time': f"{random.randint(1, 2)}",
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'city_id': self.city_id,
            }

            # # 填充其他字段
            # extra_fields = ['ac_terminal', 'county_id', 'irms_province_code',
            #                 'log_saved_time', 'power_related_site_name', 'power_room_type',
            #                 'power_supply_type', 'refer_pue', 'refrigeration_mode',
            #                 'res_code', 'space_room_type', 'video_monitor_conf']
            # for field in extra_fields:
            #     if field not in doc:
            #         doc[field] = f"mock_{field}_{random.randint(1, 2)}"

            docs.append(doc)
        return docs