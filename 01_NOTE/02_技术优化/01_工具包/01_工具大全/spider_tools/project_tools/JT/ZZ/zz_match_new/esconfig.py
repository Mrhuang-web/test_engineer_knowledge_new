class ESConfig:
    """ES配置集中管理"""
    ES_URL = "http://10.1.203.38:9200"

    # 索引前缀映射（保留原始全部）
    INDEX_PREFIX_MAP = {
        # 设备类 - 年月+m
        'air': 'ods_zz_device_air',
        'battery': 'ods_zz_device_battery',
        'low_ac_distribution': 'ods_zz_device_low_ac_distribution',
        'switch_power': 'ods_zz_device_switch_power',
        'link_pe_in': 'ods_zz_link_pe_in',

        # 设备类 - 年+y
        'energy_save': 'ods_zz_device_energy_save',
        'high_dc_distribution': 'ods_zz_device_high_dc_distribution',
        'high_distribution': 'ods_zz_device_high_distribution',
        'high_power': 'ods_zz_device_high_power',
        'smart_meter': 'ods_zz_device_smart_meter',
        'transform': 'ods_zz_device_transform',
        'transform_device': 'ods_zz_device_transform_device',
        'ups': 'ods_zz_device_ups',

        # 映射类 - 年+y
        'irms_dc_map': 'ods_zz_irms_dc_map',
        'irms_rom_map': 'ods_zz_irms_rom_map',
        'irms_site_map': 'ods_zz_irms_site_map',

        # 房间类 - 年月日+d
        'room': 'ods_zz_room',

        # 房间属性类 - 年月+m
        'room_property': 'ods_zz_room_property',

        # 站点类 - 年月+m
        'site': 'ods_zz_site',
        'site_property': 'ods_zz_site_property',
    }

    # 索引后缀规则（保留原始全部）
    INDEX_SUFFIX_RULES = {
        'YYYYMMm': ['air', 'battery', 'low_ac_distribution', 'switch_power',
                    'room_property', 'site', 'site_property', 'link_pe_in'],
        'YYYYy': ['energy_save', 'high_dc_distribution', 'high_distribution',
                  'high_power', 'smart_meter', 'transform', 'transform_device', 'ups',
                  'irms_dc_map', 'irms_rom_map', 'irms_site_map'],
        'YYYYMMDDd': ['room'],
    }

    INDEX_SETTINGS = {
        "index": {
            "number_of_replicas": "0",
            "refresh_interval": "5s"
        }
    }
