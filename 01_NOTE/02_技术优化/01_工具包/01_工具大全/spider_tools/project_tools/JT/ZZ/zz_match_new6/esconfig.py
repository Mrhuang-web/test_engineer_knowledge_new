# ============ 配置区（100% 复用 common_zz_match.py） ============ #
class ESConfig:
    ES_URL = "http://10.1.203.38:9200"
    INDEX_PREFIX_MAP = {
        'air': 'ods_zz_device_air', 'battery': 'ods_zz_device_battery',
        'low_ac_distribution': 'ods_zz_device_low_ac_distribution',
        'switch_power': 'ods_zz_device_switch_power', 'link_pe_in': 'ods_zz_link_pe_in',
        'energy_save': 'ods_zz_device_energy_save', 'high_dc_distribution': 'ods_zz_device_high_dc_distribution',
        'high_distribution': 'ods_zz_device_high_distribution', 'high_power': 'ods_zz_device_high_power',
        'smart_meter': 'ods_zz_device_smart_meter', 'transform': 'ods_zz_device_transform',
        'transform_device': 'ods_zz_device_transform_device', 'ups': 'ods_zz_device_ups',
        'low_dc_distribution': 'ods_zz_device_low_dc_distribution',
        'power_generation': 'ods_zz_device_power_generation',
        'power_monitor': 'ods_zz_device_power_monitor', 'other': 'ods_zz_device_other',
        'room': 'ods_zz_room', 'room_property': 'ods_zz_room_property',
        'site': 'ods_zz_site', 'site_property': 'ods_zz_site_property',
        'irms_dc_map': 'ods_zz_irms_dc_map', 'irms_rom_map': 'ods_zz_irms_rom_map',
        'irms_site_map': 'ods_zz_irms_site_map',
    }
    INDEX_SUFFIX_RULES = {
        'YYYYMMm': ['air', 'battery', 'low_ac_distribution', 'switch_power', 'room_property', 'site', 'site_property',
                    'link_pe_in'],
        'YYYYy': ['energy_save', 'high_dc_distribution', 'high_distribution', 'high_power', 'smart_meter', 'transform',
                  'transform_device', 'ups',
                  'irms_dc_map', 'irms_rom_map', 'irms_site_map'],
        'YYYYMMDDd': ['room'],
    }
    INDEX_SETTINGS = {"index": {"number_of_replicas": "0", "refresh_interval": "5s"}}
