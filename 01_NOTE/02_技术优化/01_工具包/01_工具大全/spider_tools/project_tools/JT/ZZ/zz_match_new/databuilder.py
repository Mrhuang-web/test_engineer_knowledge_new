class DataBuilder:
    """数据构建器 - 保留原始字段顺序和生成逻辑"""

    # 设备字段定义（保持原始顺序）
    DEVICE_FIELDS = {
        # 高压配电（综资）：1-高压配电（动环）
        'high_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                              'device_code', 'device_number', 'device_subclass', 'device_type',
                              'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                              'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                              'province_id', 'qr_code_no', 'qualitor', 'rated_cooling_capacity',
                              'rated_input_power', 'rated_operating_voltage', 'related_room',
                              'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 低压交流配电（综资）：2-低压交流配电（动环）、96-交流母线配电
        'low_ac_distribution': ['assets_no', 'backup_time', 'batch_num', 'cell_voltage_level',
                                'city_id', 'collect_time', 'county_id', 'device_code',
                                'device_number', 'device_subclass', 'device_type',
                                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                                'province_id', 'qr_code_no', 'qualitor', 'ralated_power_device',
                                'related_room', 'related_site', 'res_code', 'reted_capacity',
                                'start_time', 'total_monomers_number', 'vendor_id', 'zh_label'],
        # 变压器（）综资）：3-变压器（动环）
        'transform': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                      'device_code', 'device_number', 'device_subclass', 'device_type',
                      'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                      'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                      'province_id', 'qr_code_no', 'qualitor', 'rated_capacity',
                      'rated_output_voltage', 'related_room', 'related_site', 'related_system',
                      'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 低压直流配电（综资）：4-低压直流配电（动环）
        'low_dc_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                                'device_code', 'device_number', 'device_subclass', 'device_type',
                                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                                'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                                'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 发电机组（综资）：5-发电机组（动环）  -- 需要检测下
        'power_generation': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                             'device_code', 'device_number', 'device_subclass', 'device_type',
                             'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                             'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                             'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                             'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 开关电源（综资）：6-开关电源（动环）
        'switch_power': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                         'device_code', 'device_number', 'device_subclass', 'device_type',
                         'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                         'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                         'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                         'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 蓄电池（综资）：7-铅酸电池（动环）、68-锂电池（动环）
        'battery': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                    'device_code', 'device_number', 'device_subclass', 'device_type',
                    'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                    'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                    'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                    'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # ups设备（综资）：8-UPS设备（动环）
        'ups': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                'device_code', 'device_number', 'device_subclass', 'device_type',
                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 空调设备（综资）：11-机房专用空调（动环）、12-中央空调末端（动环）、13-中央空调主机（动环）、15-普通空调（已经可以了
        'air': ['rated_cooling_capacity', 'power_device_name', 'estimated_retirement_time', 'device_subclass',
                'device_type', 'assets_no', 'county_id', 'rated_operating_voltage',
                'maintainor', 'lifecycle_status', 'qualitor', 'related_room', 'rated_input_power', 'qr_code_no',
                'irms_province_code', 'related_site', 'power_device_id', 'batch_num', 'product_name', 'res_code',
                'zh_label', 'start_time', 'province_id', 'device_number', 'device_code', 'vendor_id', 'collect_time',
                'city_id'],
        # 变换设备（综资）：14-变换设备（动环）
        'transform_device': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                             'device_code', 'device_number', 'device_subclass', 'device_type',
                             'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                             'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                             'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                             'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 动环监控（综资）：17-机房环境（动环）、76-动环监控（动环）、93-智能门禁（动环）
        'power_monitor': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                          'device_code', 'device_number', 'device_subclass', 'device_type',
                          'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                          'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                          'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                          'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 节能设备（综资）：18-电池恒温箱（动环）、77-智能通风换热（动环）、78-风光设备（动环）、潜热过度（动环）
        'energy_save': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                        'device_code', 'device_number', 'device_subclass', 'device_type',
                        'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                        'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                        'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                        'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 高压直流电源（综资）：87-高压直流电源（动环）
        'high_power': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                       'device_code', 'device_number', 'device_subclass', 'device_type',
                       'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                       'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                       'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                       'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 高压直流配电（综资）：88-高压直流电源配电（动环）
        'high_dc_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                                 'device_code', 'device_number', 'device_subclass', 'device_type',
                                 'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                 'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                                 'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                                 'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 智能电表（综资）：92-智能电表（动环）
        'smart_meter': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                        'device_code', 'device_number', 'device_subclass', 'device_type',
                        'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                        'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                        'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                        'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        # 其他设备（综资）：16-极早期烟感（动环）、94-一体化能源柜（动环）、户外小型一体化电源（动环）、其他设备（动环）
        'other': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                  'device_code', 'device_number', 'device_subclass', 'device_type',
                  'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                  'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                  'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                  'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],

    }

    # 房间字段（保持原始顺序）
    ROOM_FIELDS = [
        'uuid', 'province_id', 'city_id', 'batch_num', 'collect_time',
        'equiproom_type', 'equiproom_level', 'room_area', 'installed_rack_num',
        'loadable_rack_num', 'lifecycle_status', 'zh_label', 'length',
        'width', 'height', 'cutin_date', 'address_code', 'airconditioner_power',
        # ... 保留所有原始字段
    ]

    @staticmethod
    def build_device_docs(device_type: str, count: int, context: Dict) -> List[Dict]:
        """构建设备文档 - 严格保持字段顺序"""
        fields = DataBuilder.DEVICE_FIELDS.get(device_type, [])
        if not fields:
            # 通用字段（保持原始逻辑）
            fields = ['assets_no', 'batch_num', 'city_id', 'collect_time',
                      'device_code', 'device_number', 'province_id', 'zh_label']
            print(f"设备类型 '{device_type}' 未预定义，使用通用字段")

        docs = []
        for i in range(count):
            doc = {}
            # 按字段定义顺序生成（关键！）
            for field in fields:
                doc[field] = DataBuilder._generate_field_value(field, context, device_type)
            docs.append(doc)
        return docs

    @staticmethod
    def _generate_field_value(field: str, context: Dict, device_type: str = None) -> Any:
        """生成字段值 - 保留原始全部逻辑"""
        # 业务参数字段
        if field == 'rated_cooling_capacity':
            return context.get('rated_cooling_capacity', f"{random.randint(1, 100)}")
        elif field == 'power_device_name':
            return context.get('power_device_name', f"")
        elif field == 'estimated_retirement_time':
            return context.get('estimated_retirement_time', f"{datetime.now().strftime('%Y-%m-%d')}")
        elif field == 'device_subclass':
            return context.get('device_subclass', f"{random.choice(['风冷专用空调'])}")
        elif field == 'device_type':
            return context.get('device_type', f"{random.choice(['机房专用空调'])}")
        elif field == 'assets_no':
            return context.get('assets_no', f"")
        elif field == 'county_id':
            return context.get('county_id', f"{random.choice(['440112'])}")
        elif field == 'rated_operating_voltage':
            return context.get('rated_operating_voltage', f"{random.randint(1, 100)}V")
        elif field == 'maintainor':
            return context.get('maintainor', f"test_{random.randint(1, 100)}")
        elif field == 'lifecycle_status':
            return context.get('lifecycle_status', f"{random.choice(['现网'])}")
        elif field == 'qualitor':
            return context.get('qualitor', f"test_{random.choice(['现网'])}")
        elif field == 'related_room':
            return context.get('related_room', f"room_{random.randint(1000, 9999)}")
        elif field == 'rated_input_power':
            return context.get('rated_input_power', f"{random.randint(1, 10)}")
        elif field == 'qr_code_no':
            return context.get('qr_code_no', f'')
        elif field == 'irms_province_code':
            return context.get('irms_province_code', f"{random.choice(['GZ'])}")
        elif field == 'related_site':
            return context.get('related_site', f"site_{random.randint(1000, 9999)}")
        elif field == 'power_device_id':
            return context.get('power_device_id', f"device_{random.randint(1000, 9999)}")
        elif field == 'batch_num':
            return context.get('batch_num', f"{datetime.now().strftime('%Y%m%d')}")
        elif field == 'product_name':
            return context.get('product_name', f"{random.choice(['test'])}")
        elif field == 'res_code':
            return context.get('res_code', f"res_code_{random.randint(1000, 9999)}")
        elif field == 'zh_label':
            return context.get('zh_label', f"zh_label_{random.randint(1000, 9999)}")
        elif field == 'start_time':
            return context.get('start_time', f"{datetime.now().strftime('%Y-%m-%d')}")
        elif field == 'province_id':
            return context.get('province_id', f"zh_label_{random.randint(300000, 900000)}")
        elif field == 'device_number':
            return context.get('device_number', f"{random.randint(1, 10)}")
        elif field == 'device_code':
            return context.get('device_code', f"{random.randint(1, 10)}")
        elif field == 'vendor_id':
            return context.get('vendor_id', f"{random.choice(['test'])}")
        elif field == 'collect_time':
            return context.get('collect_time', f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        elif field == 'city_id':
            return context.get('city_id', f"{random.randint(300000, 900000)}")
        return f"{random.randint(1, 100)}"