class SitePropertyWriter(BaseWriter):
    """站点属性写入器 - 保留与site_int_id关联逻辑"""

    def __init__(self, **kwargs):
        super().__init__(index_type='site_property', **kwargs)

    def generate_mock_data(self, count: int) -> List[Dict]:
        docs = []
        for i in range(count):
            doc = {
                'mains_nature': self.mains_nature,
                'cold_storage_time': f"",
                'property_unit': f"",
                'water_cooling_conf': f"",
                'county_id': self.county_id,
                'power_is_substations': f"{random.choice(['是', '否'])}",
                'mains_configuration_level': f"{random.choice(['1市电无油机'])}",
                'total_mains_number': f"{random.choice(['1', '0'])}",
                'tatal_tank_volume': f"",
                'is_attach_idc_room': f"{random.choice(['是', '否'])}",
                'power_site_level': self.power_site_level,
                'irms_province_code': self.irms_province_code,
                'is_cold_storage_install': f"",
                'batch_num': self.batch_num,
                'mains_voltage_level': f"{random.randint(1, 10)}V",
                'res_code': self.site_res_code,
                'zh_label': self.site_int_id,
                'mains_capacity': f"{random.randint(100, 1000)}KVA",
                'power_supply': f"{random.choice(['其他'])}",
                'province_id': self.province_id,
                'collect_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'design_pue': f"{random.uniform(1.2, 1.8):.2f}",
                'actual_pue': f"{random.uniform(1.3, 2.0):.2f}",
                'city_id': self.city_id,
            }

            # 填充其他字段
            # extra_fields = ['cold_storage_time', 'is_cold_storage_install',
            #                 'mains_backup_method', 'power_monitoring_site_id',
            #                 'power_monitoring_site_name', 'property_unit',
            #                 'tatal_tank_volume', 'total_tank_number', 'water_cooling_conf']
            # for field in extra_fields:
            #     if field not in doc:
            #         doc[field] = f"mock_{field}_{random.randint(1, 100)}"

            docs.append(doc)
        return docs