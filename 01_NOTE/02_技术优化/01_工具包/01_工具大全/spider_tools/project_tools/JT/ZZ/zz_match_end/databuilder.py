import random
import uuid
from datetime import datetime
from typing import List, Dict, Any
from spider_tools.project_tools.JT.ZZ.zz_match_new2.esconfig import ESConfig


# ============ 字段生成器（复用原逻辑） ============ #
class DataBuilder:
    DEVICE_FIELDS = {
        'room': [
            'batch_num', 'collect_time', 'zh_label', 'cutin_date', 'province_id', 'city_id',
            'county_id', 'site_int_id', 'room_int_id', 'power_room_type', 'power_supply_mode',
            'uuid', 'airconditioner_power', 'alias_name', 'asset_address_code', 'business_unit',
            'china_tower_operations_id', 'china_tower_room_type', 'china_tower_station_code',
            'floor_num', 'height', 'if_tele_cmn_serv', 'if_village_pass_serv', 'installed_rack_num',
            'int_id', 'irms_province_code', 'is_headquarters_used', 'length', 'lifecycle_status',
            'loadable_rack_num', 'mainit_unit', 'maintainor_method', 'plan_rack_num',
            'pms_design_code', 'pms_design_name', 'project_code', 'project_name', 'property_right',
            'property_unit', 'qr_code_no', 'qualitor', 'related_site', 'retire_time', 'room_area',
            'row_direction', 'row_num', 'shared_unit', 'start_column', 'start_row',
            'tele_cmn_serv_pro_code', 'tele_cmn_serv_pro_name', 'width'
        ],
        'room_property': [
            'batch_num', 'room_int_id', 'province_id', 'city_id', 'site_int_id', 'irms_province_code',
            'cutin_date', 'power_room_type', 'power_supply_mode', 'county_id',
            'uuid', 'ac_config', 'ac_terminal', 'battery_backup_time', 'collect_time',
            'county_id', 'irms_province_code', 'log_saved_time', 'power_monitor_conf',
            'power_related_site_name', 'power_room_id', 'power_room_name', 'power_room_type',
            'power_supply_mode', 'power_supply_type', 'province_id', 'refer_pue', 'refrigeration_mode',
            'res_code', 'space_room_type', 'video_monitor_conf', 'zh_label'
        ],
        'site': [
            'batch_num', 'zh_label', 'city_id', 'province_id', 'irms_province_code', 'cutin_date',
            'county_id', 'site_type',
            'uuid', 'address', 'alias_name', 'area_type', 'business_type', 'china_tower_station_code',
            'floor_number', 'if_tele_cmn_serv', 'if_village_pass_serv', 'int_id', 'latitude',
            'longitude', 'pms_address_code', 'project_code', 'project_name', 'related_dc',
            'site_type', 'standardaddress', 'tele_cmn_serv_pro_code', 'tele_cmn_serv_pro_name',
            'use_corp', 'village_pass_serv_code', 'village_pass_serv_name'
        ],
        'site_property': [
            'batch_num', 'site_int_id', 'province_id', 'city_id', 'irms_province_code', 'cutin_date',
            'power_site_level', 'mains_nature', 'county_id', 'site_type',
            'uuid', 'actual_pue', 'batch_num', 'city_id', 'cold_storage_time', 'collect_time',
            'county_id', 'design_pue', 'irms_province_code', 'is_attach_idc_room',
            'is_cold_storage_install', 'mains_backup_method', 'mains_capacity',
            'mains_configuration_level', 'mains_nature', 'mains_voltage_level',
            'power_is_substations', 'power_monitoring_site_id', 'power_monitoring_site_name',
            'power_site_level', 'power_supply', 'property_unit', 'province_id', 'res_code',
            'tatal_tank_volume', 'total_mains_number', 'total_tank_number', 'water_cooling_conf',
            'zh_label'
        ],
        'irms_dc_map': [
            'batch_num', 'uuid', 'pms_id', 'pms_name', 'dh_id', 'dh_name', 'zg_id', 'zg_name',
            'statis_ymd', 'province_id'
        ],
        'irms_rom_map': [
            'batch_num', 'uuid', 'pms_id', 'pms_name', 'dh_id', 'dh_name', 'zg_id', 'zg_name',
            'statis_ymd', 'province_id'
        ],
        'irms_site_map': [
            'batch_num', 'uuid', 'pms_id', 'pms_name', 'dh_id', 'dh_name', 'zg_id', 'zg_name',
            'statis_ymd', 'province_id'
        ],
        'high_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                              'device_code', 'device_number', 'device_subclass', 'device_type',
                              'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                              'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                              'province_id', 'qr_code_no', 'qualitor', 'rated_cooling_capacity',
                              'rated_input_power', 'rated_operating_voltage', 'related_room',
                              'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'low_ac_distribution': ['assets_no', 'backup_time', 'batch_num', 'cell_voltage_level',
                                'city_id', 'collect_time', 'county_id', 'device_code',
                                'device_number', 'device_subclass', 'device_type',
                                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                                'province_id', 'qr_code_no', 'qualitor', 'ralated_power_device',
                                'related_room', 'related_site', 'res_code', 'reted_capacity',
                                'start_time', 'total_monomers_number', 'vendor_id', 'zh_label'],
        'transform': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                      'device_code', 'device_number', 'device_subclass', 'device_type',
                      'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                      'maintainor', 'power_device_id', 'power_device_name', 'product_name',
                      'province_id', 'qr_code_no', 'qualitor', 'rated_capacity',
                      'rated_output_voltage', 'related_room', 'related_site', 'related_system',
                      'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'low_dc_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                                'device_code', 'device_number', 'device_subclass', 'device_type',
                                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                                'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                                'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'power_generation': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                             'device_code', 'device_number', 'device_subclass', 'device_type',
                             'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                             'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                             'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                             'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'switch_power': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                         'device_code', 'device_number', 'device_subclass', 'device_type',
                         'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                         'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                         'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                         'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'battery': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                    'device_code', 'device_number', 'device_subclass', 'device_type',
                    'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                    'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                    'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                    'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'ups': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                'device_code', 'device_number', 'device_subclass', 'device_type',
                'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'air': ['rated_cooling_capacity', 'power_device_name', 'estimated_retirement_time', 'device_subclass',
                'device_type', 'assets_no', 'county_id', 'rated_operating_voltage',
                'maintainor', 'lifecycle_status', 'qualitor', 'related_room', 'rated_input_power', 'qr_code_no',
                'irms_province_code', 'related_site', 'power_device_id', 'batch_num', 'product_name', 'res_code',
                'zh_label', 'start_time', 'province_id', 'device_number', 'device_code', 'vendor_id', 'collect_time',
                'city_id'],
        'transform_device': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                             'device_code', 'device_number', 'device_subclass', 'device_type',
                             'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                             'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                             'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                             'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'power_monitor': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                          'device_code', 'device_number', 'device_subclass', 'device_type',
                          'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                          'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                          'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                          'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'energy_save': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                        'device_code', 'device_number', 'device_subclass', 'device_type',
                        'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                        'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                        'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                        'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'high_power': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                       'device_code', 'device_number', 'device_subclass', 'device_type',
                       'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                       'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                       'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                       'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'high_dc_distribution': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                                 'device_code', 'device_number', 'device_subclass', 'device_type',
                                 'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                                 'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                                 'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                                 'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'smart_meter': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                        'device_code', 'device_number', 'device_subclass', 'device_type',
                        'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                        'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                        'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                        'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
        'other': ['assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id',
                  'device_code', 'device_number', 'device_subclass', 'device_type',
                  'estimated_retirement_time', 'irms_province_code', 'lifecycle_status',
                  'maintainor', 'meter_circuit_number', 'power_device_id', 'power_device_name',
                  'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_room',
                  'related_site', 'res_code', 'start_time', 'vendor_id', 'zh_label'],
    }

    @staticmethod
    def build_device_docs(device_type: str, count: int, context: Dict) -> List[Dict]:
        fields = DataBuilder.DEVICE_FIELDS.get(device_type, [])
        docs = []
        for _ in range(count):
            doc = {field: DataBuilder._generate_field_value(field, context, device_type) for field in fields}
            docs.append(doc)
        return docs

    @staticmethod
    def _generate_field_value(field: str, context: Dict, device_type: str = None) -> Any:
        if field == 'batch_num':
            return context.get('batch_num', datetime.now().strftime('%Y%m%d'))
        if field == 'collect_time':
            return context.get('collect_time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        if field == 'estimated_retirement_time':
            return context.get('estimated_retirement_time', datetime.now().strftime('%Y-%m-%d'))
        if field == 'start_time':
            return context.get('start_time', datetime.now().strftime('%Y-%m-%d'))
        if field in ('lifecycle_status', 'qualitor'):
            return '现网'
        if field == 'device_type':
            return device_type
        if field == 'related_site':
            return context.get('related_site', f"site_{random.randint(1000, 9999)}")
        if field == 'related_room':
            return context.get('related_room', f"room_{random.randint(1000, 9999)}")
        if field == 'power_device_id':
            return context.get('power_device_id', f"device_{random.randint(1000, 9999)}")
        if field == 'res_code':
            return context.get('res_code', f"res_{random.randint(1000, 9999)}")
        if field == 'zh_label':
            return context.get('zh_label', f"设备_{random.randint(1000, 9999)}")
        if field == 'province_id':
            return context.get('province_id', f"{random.randint(300000, 900000)}")
        if field == 'city_id':
            return context.get('city_id', f"{random.randint(300000, 900000)}")
        if field == 'county_id':
            return context.get('county_id', '440101')
        if field == 'irms_province_code':
            return context.get('irms_province_code', 'GZ')
        if field == 'device_code':
            return str(random.randint(1, 10))
        if field == 'device_number':
            return str(random.randint(1, 10))
        if field == 'vendor_id':
            return 'test'
        if field == 'product_name':
            return 'test'
        if field == 'assets_no':
            return ''
        if field == 'maintainor':
            return 'test'
        if field == 'qr_code_no':
            return ''
        if field == 'rated_cooling_capacity':
            return str(random.randint(1, 100))
        if field == 'rated_input_power':
            return str(random.randint(1, 10))
        if field == 'rated_operating_voltage':
            return f"{random.randint(1, 100)}V"
        if field == 'backup_time':
            return str(random.randint(1, 24))
        if field == 'cell_voltage_level':
            return str(random.randint(1, 10))
        if field == 'ralated_power_device':
            return ''
        if field == 'reted_capacity':
            return str(random.randint(100, 1000))
        if field == 'total_monomers_number':
            return str(random.randint(1, 10))
        if field == 'rated_capacity':
            return str(random.randint(100, 1000))
        if field == 'rated_output_voltage':
            return f"{random.randint(1, 100)}V"
        if field == 'related_system':
            return f"sys_{random.randint(1, 100)}"
        if field == 'meter_circuit_number':
            return str(random.randint(1, 10))
        if field == 'cutin_date':
            return context.get('cutin_date', datetime.now().strftime('%Y-%m-%d'))
        if field == 'site_int_id':
            return context.get('site_int_id', f"site_{random.randint(1000, 9999)}")
        if field == 'room_int_id':
            return context.get('room_int_id', f"room_{random.randint(1000, 9999)}")
        if field == 'power_room_type':
            return context.get('power_room_type', '汇聚机房')
        if field == 'power_supply_mode':
            return context.get('power_supply_mode', '双电源双回路供电')
        if field == 'site_type':
            return context.get('site_type', random.choice(
                ['核心站点', '核心站点（配套）', '骨干站点', '汇聚站点', '接入站点', '用户站点', '其他站点']
            ))
        if field == 'power_site_level':
            return context.get('power_site_level', '传输节点')
        if field == 'mains_nature':
            return context.get('mains_nature', '市电转供')
        if field == 'uuid':
            return str(uuid.uuid4())
        if field == 'pms_id':
            return f"PMS{random.randint(10000, 99999)}"
        if field == 'pms_name':
            return f"PMS系统_{random.randint(1000, 9999)}"
        if field == 'dh_id':
            return f"DH{random.randint(10000, 99999)}"
        if field == 'dh_name':
            return f"DH_{random.randint(1000, 9999)}"
        if field == 'zg_id':
            return f"ZG{random.randint(10000, 99999)}"
        if field == 'zg_name':
            return f"ZG_{random.randint(1000, 9999)}"
        if field == 'statis_ymd':
            return context.get('statis_ymd', datetime.now().strftime('%Y%m%d'))
        return f"{random.randint(1, 100)}"

    @staticmethod
    def generate_index_name(device_type: str, date_format: str) -> str:
        """
        根据设备类型和日期格式生成索引名称。
        :param device_type: 设备类型
        :param date_format: 日期格式（如 'YYYYMMm', 'YYYYy', 'YYYYMMDDd'）
        :return: 索引名称
        """
        now = datetime.now()
        if date_format == 'YYYYMMm':
            date_suffix = now.strftime('%Y%m')
        elif date_format == 'YYYYy':
            date_suffix = now.strftime('%Y')
        elif date_format == 'YYYYMMDDd':
            date_suffix = now.strftime('%Y%m%d')
        else:
            raise ValueError(f"Unsupported date format: {date_format}")

        return f"ods_zz_{device_type}_{date_suffix}"

    @staticmethod
    def get_index_suffix(device_type: str) -> str:
        """
        根据设备类型获取对应的日期格式。
        :param device_type: 设备类型
        :return: 日期格式
        """
        for date_format, types in ESConfig.INDEX_SUFFIX_RULES.items():
            if device_type in types:
                return date_format
        raise ValueError(f"Unsupported device type: {device_type}")

    @staticmethod
    def build_index_name(device_type: str) -> str:
        """
        根据设备类型生成完整的索引名称。
        :param device_type: 设备类型
        :return: 完整的索引名称
        """
        date_format = DataBuilder.get_index_suffix(device_type)
        return DataBuilder.generate_index_name(device_type, date_format)
