# config.py
import datetime


class ESConfig:
    ES_URL = "http://10.1.203.38:9200"
    INDEX_PREFIX_MAP = {
        'air': 'ods_zz_device_air',
        'battery': 'ods_zz_device_battery',
        'low_ac_distribution': 'ods_zz_device_low_ac_distribution',
        'high_dc_distribution': 'ods_zz_device_high_dc_distribution',
        'high_distribution': 'ods_zz_device_high_distribution',
        'high_power': 'ods_zz_device_high_power',
        'smart_meter': 'ods_zz_device_smart_meter',
        'transform': 'ods_zz_device_transform',
        'transform_device': 'ods_zz_device_transform_device',
        'ups': 'ods_zz_device_ups',
        'room': 'ods_zz_room',
        'room_property': 'ods_zz_room_property',
        'site': 'ods_zz_site',
        'site_property': 'ods_zz_site_property',
        'irms_dc_map': 'ods_zz_irms_dc_map',
        'irms_rom_map': 'ods_zz_irms_rom_map',
        'irms_site_map': 'ods_zz_irms_site_map',
        'link_pe_in': 'ods_zz_link_pe_in',
    }
    INDEX_SUFFIX_RULES = {
        'YYYYMMm': ['air', 'battery', 'low_ac_distribution', 'room_property', 'site', 'site_property', 'link_pe_in'],
        'YYYYy': ['high_dc_distribution', 'high_distribution', 'high_power', 'smart_meter', 'transform',
                  'transform_device', 'ups', 'irms_dc_map', 'irms_rom_map', 'irms_site_map'],
        'YYYYMMDDd': ['room'],
    }
    INDEX_SETTINGS = {
        "index": {
            "number_of_replicas": "0",
            "refresh_interval": "5s"
        }
    }
