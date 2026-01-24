import random
import uuid
from datetime import datetime
from typing import List, Dict, Any
from spider_tools.project_tools.JT.ZZ.zz_match_new2.esconfig import ESConfig


# ============ 字段生成器（复用原逻辑） ============ #
class DataBuilder:
    DEVICE_FIELDS = {
        'site': [
            'china_tower_station_code', 'village_pass_serv_code', 'cutin_date', 'site_site_type', 'latitude', 'floor_number',
            'project_name', 'related_dc', 'uuid', 'county_id', 'is_headquarters_used', 'pms_address_code',
            'business_type', 'site_int_id', 'lifecycle_status', 'qualitor', 'if_village_pass_serv', 'longitude',
            'tele_cmn_serv_pro_code', 'address', 'village_pass_serv_name', 'irms_province_code', 'project_code',
            'area_type', 'batch_num', 'alias_name', 'standardaddress', 'if_tele_cmn_serv', 'zh_label', 'province_id',
            'tele_cmn_serv_pro_name', 'use_corp', 'collect_time', 'city_id',
        ],
        'site_property': [
            'mains_nature', 'power_monitoring_site_name', 'cold_storage_time', 'water_cooling_conf', 'property_unit',
            'county_id', 'power_is_substations', 'mains_configuration_level',
            'total_tank_number', 'tatal_tank_volume', 'is_attach_idc_room', 'total_mains_number', 'power_site_level',
            'irms_province_code', 'is_cold_storage_install', 'batch_num', 'mains_voltage_level', 'res_code',
            'power_monitoring_site_id', 'zh_label', 'mains_capacity', 'power_supply', 'province_id', 'collect_time',
            'design_pue', 'mains_backup_method', 'actual_pue', 'city_id'

        ],
        'room': [
            'address_code', 'airconditioner_power', 'alias_name', 'asset_address_code', 'batch_num',
            'business_unit', 'china_tower_operations_id', 'china_tower_room_type', 'china_tower_station_code',
            'city_id', 'collect_time', 'column_direction', 'column_num', 'county_id', 'cutin_date',
            'end_column', 'end_row', 'equipment_power', 'equiproom_level', 'equiproom_type',
            'fifth_generation_flag', 'floor_num', 'height', 'if_tele_cmn_serv', 'if_village_pass_serv',
            'installed_rack_num', 'int_id', 'irms_province_code', 'is_headquarters_used', 'length',
            'lifecycle_status', 'loadable_rack_num', 'mainit_unit', 'maintainor_method', 'plan_rack_num',
            'pms_design_code', 'pms_design_name', 'project_code', 'project_name', 'property_right',
            'property_unit', 'province_id', 'qr_code_no', 'qualitor', 'related_site', 'retire_time',
            'room_area', 'row_direction', 'row_num', 'shared_unit', 'start_column', 'start_row',
            'standardaddress', 'tele_cmn_serv_pro_code', 'tele_cmn_serv_pro_name', 'uuid', 'village_pass_serv_code',
            'village_pass_serv_name', 'width', 'zh_label'
        ],
        'room_property': [
            'ac_config', 'ac_terminal', 'batch_num', 'battery_backup_time', 'city_id', 'collect_time',
            'county_id', 'irms_province_code', 'log_saved_time', 'power_monitor_conf',
            'power_related_site_name', 'power_room_id', 'power_room_name', 'power_room_type',
            'power_supply_mode', 'power_supply_type', 'province_id', 'refer_pue', 'refrigeration_mode',
            'res_code', 'space_room_type', 'video_monitor_conf', 'zh_label'
        ],
        'irms_dc_map': [
            'batch_num', 'dh_id', 'dh_name', 'pms_id', 'pms_name', 'province_id', 'statis_ymd', 'uuid', 'zg_id',
            'zg_name'
        ],
        'irms_rom_map': [
            'address_code', 'batch_num', 'dh_id', 'dh_name', 'pms_id', 'pms_name', 'province_id', 'statis_ymd', 'uuid',
            'zg_id', 'zg_name'
        ],
        'irms_site_map': [
            'batch_num', 'dh_id', 'dh_name', 'zg_name', 'province_id', 'dh_id', 'zg_id', 'statis_ymd', 'uuid'
        ],
        'link_pe_in': [
            'batch_num', 'branch_active_standby', 'branch_name', 'branch_number', 'branch_rated_capacity',
            'branch_type', 'branch_type_abbreviation', 'city_id', 'collect_time', 'county_id',
            'down_branch_active_standby', 'down_branch_name', 'down_branch_number', 'down_branch_rated_capacity',
            'down_branch_type', 'down_branch_type_abbreviation', 'down_device_name', 'down_device_ralated_room',
            'down_device_type', 'down_use_status', 'irms_province_code', 'lifecycle_status', 'province_id',
            'qr_code_no', 'qualitor', 'related_device', 'related_device_type', 'related_room', 'related_site',
            'res_code'
        ],
        'transform': [
            'assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id', 'device_code', 'device_number',
            'device_subclass', 'device_type', 'estimated_retirement_time', 'irms_province_code',
            'lifecycle_status', 'maintainor', 'power_device_id', 'power_device_name', 'product_name',
            'province_id', 'qr_code_no', 'qualitor', 'related_room', 'related_site', 'res_code',
            'rated_input_voltage', 'rated_output_voltage', 'zh_label', 'start_time', 'vendor_id'
        ],
        'transform_device': [
            'assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id', 'device_code', 'device_number',
            'device_subclass', 'device_type', 'estimated_retirement_time', 'irms_province_code',
            'lifecycle_status', 'maintainor', 'power_device_id', 'power_device_name', 'product_name',
            'province_id', 'qr_code_no', 'qualitor', 'related_room', 'related_site', 'res_code',
            'rated_input_voltage', 'rated_output_voltage', 'zh_label', 'start_time', 'vendor_id'
        ],
        'ups': [
            'assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id', 'device_code', 'device_number',
            'device_subclass', 'device_type', 'estimated_retirement_time', 'irms_province_code',
            'lifecycle_status', 'maintainor', 'power_device_id', 'power_device_name', 'product_name',
            'province_id', 'qr_code_no', 'qualitor', 'related_room', 'related_site', 'res_code',
            'rated_output_voltage', 'zh_label', 'start_time', 'vendor_id'
        ],
        'air': [
            'rated_cooling_capacity', 'rated_input_power', 'estimated_retirement_time', 'device_subclass',
            'device_type', 'assets_no', 'county_id', 'rated_operating_voltage', 'maintainor',
            'lifecycle_status', 'qualitor', 'related_room', 'rated_input_power', 'qr_code_no',
            'irms_province_code', 'related_site', 'power_device_id', 'batch_num', 'product_name', 'res_code',
            'zh_label', 'start_time', 'province_id', 'device_number', 'device_code', 'vendor_id', 'collect_time',
            'city_id'
        ],
        'battery': [
            'reted_capacity', 'estimated_retirement_time', 'cell_voltage_level', 'irms_province_code',
            'related_site', 'device_subclass', 'device_type', 'batch_num', 'product_name', 'res_code',
            'zh_label', 'start_time', 'county_id', 'province_id', 'device_code', 'vendor_id', 'maintainor',
            'ralated_power_device', 'lifecycle_status', 'qualitor', 'collect_time', 'related_room', 'city_id'
        ],
        'energy_save': [
            'rated_cooling_capacity', 'fan_rated_power', 'estimated_retirement_time', 'device_subclass',
            'device_type', 'solar_modules_number', 'county_id', 'total_system_capacity', 'rated_operating_voltage',
            'maintainor', 'lifecycle_status', 'qualitor', 'related_room', 'solar_modules_brand',
            'rated_input_power', 'solar_modules_rated_capacity', 'fan_brand', 'system_output_voltage',
            'fan_form', 'irms_province_code', 'related_site', 'batch_num', 'power_device_id', 'power_device_name',
            'product_name', 'res_code', 'zh_label', 'start_time', 'province_id', 'device_code', 'vendor_id',
            'collect_time', 'total_fan_number', 'city_id'
        ],
        'high_dc_distribution': [
            'power_device_name', 'estimated_retirement_time', 'device_subclass', 'device_type', 'assets_no',
            'county_id', 'related_system', 'maintainor', 'lifecycle_status', 'qualitor', 'related_room',
            'reted_capacity', 'qr_code_no', 'total_input_port', 'total_onput_port', 'irms_province_code',
            'related_site', 'related_rackpos', 'power_device_id', 'batch_num', 'product_name', 'res_code',
            'zh_label', 'start_time', 'province_id', 'device_number', 'device_code', 'vendor_id', 'collect_time',
            'city_id'
        ],
        'high_distribution': [
            'power_device_name', 'estimated_retirement_time', 'device_subclass', 'device_type', 'assets_no',
            'county_id', 'related_system', 'maintainor', 'lifecycle_status', 'qualitor', 'related_room',
            'reted_capacity', 'qr_code_no', 'irms_province_code', 'related_site', 'power_device_id', 'batch_num',
            'product_name', 'res_code', 'zh_label', 'start_time', 'province_id', 'device_number', 'device_code',
            'vendor_id', 'collect_time', 'city_id'
        ],
        'high_power': [
            'power_device_name', 'estimated_retirement_time', 'monitoring_module_model', 'device_subclass',
            'device_type', 'assets_no', 'total_rack_loading_modules', 'county_id', 'related_system', 'maintainor',
            'lifecycle_status', 'qualitor', 'signal_output_rated_capacity', 'related_room',
            'total_rack_match_modules_number', 'irms_province_code', 'related_site', 'power_device_id', 'batch_num',
            'product_name', 'res_code', 'rated_output_voltage', 'zh_label', 'start_time', 'province_id',
            'device_number', 'device_code', 'vendor_id', 'total_rack_loading_modules_number', 'collect_time',
            'city_id'
        ],
        'low_ac_distribution': [
            'estimated_retirement_time', 'device_subclass', 'device_type', 'county_id', 'related_system',
            'maintainor', 'lifecycle_status', 'qualitor', 'related_room', 'reted_capacity',
            'device_configuration_spd_brand',
            'total_input_port', 'irms_province_code', 'related_site', 'related_rackpos', 'batch_num',
            'power_device_id', 'power_device_name', 'product_name', 'res_code', 'zh_label', 'spd_max_rate',
            'start_time', 'province_id', 'device_code', 'vendor_id', 'collect_time', 'city_id', 'total_output_port'
        ],
        'low_dc_distribution': [
            'estimated_retirement_time', 'device_subclass', 'device_type', 'county_id', 'related_system',
            'maintainor', 'lifecycle_status', 'qualitor', 'related_room', 'reted_capacity', 'total_input_port',
            'total_onput_port', 'irms_province_code', 'related_site', 'related_rackpos', 'batch_num',
            'power_device_id', 'power_device_name', 'product_name', 'res_code', 'zh_label', 'start_time',
            'province_id', 'device_code', 'vendor_id', 'collect_time', 'city_id'
        ],
        'other': [
            'power_device_name', 'estimated_retirement_time', 'device_subclass', 'device_type', 'assets_no',
            'county_id', 'related_system', 'maintainor', 'lifecycle_status', 'qualitor', 'related_room',
            'qr_code_no', 'irms_province_code', 'related_site', 'power_device_id', 'batch_num', 'product_name',
            'res_code', 'zh_label', 'start_time', 'province_id', 'device_number', 'device_code', 'vendor_id',
            'rated_capacity', 'collect_time', 'city_id'
        ],
        'power_generation': [
            'estimated_retirement_time', 'device_subclass', 'device_type', 'cooling_method', 'county_id',
            'related_system', 'self_start_function', 'maintainor', 'lifecycle_status', 'qualitor', 'related_room',
            'installation_method', 'rated_power', 'backup_method', 'irms_province_code', 'related_site',
            'batch_num', 'power_device_id', 'power_device_name', 'product_name', 'res_code', 'rated_output_voltage',
            'zh_label', 'start_time', 'province_id', 'device_code', 'vendor_id', 'collect_time', 'output_voltage_type',
            'city_id'
        ],
        'power_monitor': [
            'estimated_retirement_time', 'irms_province_code', 'related_site', 'device_subclass', 'device_type',
            'batch_num', 'power_device_id', 'power_device_name', 'product_name', 'res_code', 'zh_label',
            'start_time', 'county_id', 'province_id', 'device_code', 'vendor_id', 'maintainor', 'lifecycle_status',
            'qualitor', 'collect_time', 'related_room', 'city_id'
        ],
        'smart_meter': [
            'power_device_name', 'estimated_retirement_time', 'device_subclass', 'device_type', 'assets_no',
            'county_id', 'maintainor', 'lifecycle_status', 'qualitor', 'related_room', 'qr_code_no',
            'irms_province_code', 'related_site', 'power_device_id', 'batch_num', 'product_name', 'res_code',
            'zh_label', 'start_time', 'province_id', 'meter_circuit_number', 'device_number', 'device_code',
            'vendor_id', 'collect_time', 'city_id'
        ],
        'switch_power': [
            'assets_no', 'batch_num', 'city_id', 'collect_time', 'county_id', 'device_code', 'device_number',
            'device_subclass', 'device_type', 'estimated_retirement_time', 'irms_province_code',
            'lifecycle_status', 'maintainor', 'monitoring_module_model', 'power_device_id', 'power_device_name',
            'product_name', 'province_id', 'qr_code_no', 'qualitor', 'related_rackpos', 'related_room',
            'related_site', 'related_system', 'res_code', 'signal_output_rated_capacity', 'start_time',
            'total_rack_loading_modules', 'total_rack_loading_modules_number', 'total_rack_match_modules',
            'total_rack_match_modules_number', 'vendor_id', 'zh_label', 'rated_output_voltage', 'collect_time',
            'city_id'
        ]
    }

    # 映射到最终写入 ES 的字段名
    _STRIP_PREFIX = {
        'room_': '',
        'site_': '',
        # 如果有更多前缀继续加
    }

    @staticmethod
    def build_device_docs(device_type: str, count: int, context: Dict) -> List[Dict]:
        fields = DataBuilder.DEVICE_FIELDS.get(device_type, [])
        docs = []
        for _ in range(count):
            raw_doc = {
                f: DataBuilder._generate_field_value(f, context, device_type)
                for f in fields
            }
            # 把前缀去掉，得到真正写入 ES 的文档
            doc = {}
            for k, v in raw_doc.items():
                new_k = k
                for pre, repl in DataBuilder._STRIP_PREFIX.items():
                    if k.startswith(pre):
                        new_k = k.replace(pre, repl, 1)
                        break
                doc[new_k] = v
            docs.append(doc)
        return docs

    @staticmethod
    def _generate_field_value(field: str, context: Dict, device_type: str = None) -> Any:
        if field == 'use_corp':
            return context.get('use_corp', random.choice(['中国移动']))
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
        # site
        if field == 'china_tower_station_code':
            return context.get('china_tower_station_code', random.choice(['无']))
        if field == 'village_pass_serv_code':
            return context.get('village_pass_serv_code', random.choice(['']))
        if field == 'is_headquarters_used':
            return context.get('is_headquarters_used', random.choice(['否']))
        if field == 'pms_address_code':
            return context.get('pms_address_code', random.choice(['']))
        if field == 'business_type':
            return context.get('business_type', random.choice(['家客集客']))
        if field == 'area_type':
            return context.get('area_type', random.choice(['城区']))
        if field == 'power_monitoring_site_name':
            return context.get('power_monitoring_site_name', random.choice(['test']))
        if field == 'water_cooling_conf':
            return context.get('water_cooling_conf', random.choice(['其他']))
        if field == 'power_is_substations':
            return context.get('power_is_substations', random.choice(['否']))
        if field == 'is_attach_idc_room':
            return context.get('is_attach_idc_room', random.choice(['否']))
        if field == 'power_monitoring_site_id':
            return context.get('site_int_id', random.choice(['']))
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
