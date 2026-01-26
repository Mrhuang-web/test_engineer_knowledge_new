SELECT * FROM zz_data_sync_info;

SELECT * FROM topu_mete_display_config;
SELECT * FROM t_cfg_topology_v2_configuration LIMIT 10;
SELECT * FROM zz_to_rm_rm_device LIMIT 10;

SELECT COUNT(1) FROM ods_zz_link_pe_out;
SELECT * FROM ods_zz_link_pe_out LIMIT 10;

# 关联
SELECT * FROM zz_data_sync_info;

# 站点匹配
ods_zz_irms_site_map
ods_zz_site
ods_zz_site_property

SELECT * FROM ods_zz_irms_site_map LIMIT 10;
INSERT INTO `ods_zz_irms_site_map` (`stat_time`, `zg_id`, `uuid`, `zg_name`, `pms_id`, `dh_id`, `dh_name`, `batch_num`, `province_id`, `pms_name`, `statis_ymd`, `flow_time`) 
VALUES ('2026-01-26', '2026012601', 'c6ac174b-5d4b-40c6-abf2-c0dc2231ew1', '贵1数据中心_液冷2', 'JF-LN-SCDD-9001', '01-08-08-01-11-02', '贵1数据中心_液冷2', '2026-01-26 08:30:24.415865', NULL, NULL, '20260126', '2026-01-26 10:56:10');

SELECT * FROM ods_zz_site LIMIT 10;
INSERT INTO `ods_zz_site` (`stat_time`, `int_id`, `project_code`, `uuid`, `tele_cmn_serv_pro_name`, `pms_address_code`, `project_name`, `business_type`, `area_type`, `cutin_date`, `batch_num`, `collect_time`, `irms_province_code`, `related_dc`, `lifecycle_status`, `qualitor`, `floor_number`, `use_corp`, `standardaddress`, `village_pass_serv_code`, `if_village_pass_serv`, `village_pass_serv_name`, `alias_name`, `china_tower_station_code`, `latitude`, `province_id`, `city_id`, `county_id`, `longitude`, `if_tele_cmn_serv`, `tele_cmn_serv_pro_code`, `is_headquarters_used`, `zh_label`, `site_type`, `address`, `flow_time`) 
VALUES ('2026-01-26', '2026012601', NULL, NULL, NULL, NULL, NULL, '家客集客', NULL, '2018-06-25', '20260126', '2026-01-26 14:10:56', 'GZ', NULL, '在网', NULL, NULL, '其他', NULL, NULL, NULL, NULL, NULL, NULL, '26.5651492', '520000', '520400', '520404', '106.7182', '否', NULL, '否', '贵1数据中心_液冷2', '用户站点', '贵阳市南明区桃园路95号（原电厂旧址）保利凤凰湾售楼部', '2026-01-26 11:24:16');

SELECT * FROM ods_zz_site_property LIMIT 10;
INSERT INTO `ods_zz_site_property` (`stat_time`, `res_code`, `mains_voltage_level`, `mains_nature`, `total_mains_number`, `mains_capacity`, `mains_configuration_level`, `total_tank_number`, `tatal_tank_volume`, `batch_num`, `collect_time`, `irms_province_code`, `power_is_substations`, `cold_storage_time`, `power_supply`, `actual_pue`, `water_cooling_conf`, `is_cold_storage_install`, `province_id`, `city_id`, `county_id`, `zh_label`, `power_site_level`, `design_pue`, `property_unit`, `power_monitoring_site_name`, `power_monitoring_site_id`, `mains_backup_method`, `is_attach_idc_room`, `flow_time`) 
VALUES ('2026-01-26', '202601260101', '10KV', '市电直供', '1', '225', '1市电无油机', NULL, NULL, '20260126', '2026-01-26 16:11:18', 'GZ', '否', '1', '单变电站双母线引入；', NULL, '无', '否', '520000', '520400', '520404', '2026012601', '通信基站', NULL, NULL, '贵1数据中心_液冷2', NULL, '单路引入', '否', '2026-01-26 10:45:06');


# 机房匹配
ods_zz_irms_rom_map
ods_zz_room
ods_zz_room_property

SELECT * FROM ods_zz_irms_rom_map LIMIT 10;
INSERT INTO `ods_zz_irms_rom_map` (`stat_time`, `zg_id`, `address_code`, `batch_num`, `province_id`, `uuid`, `zg_name`, `pms_id`, `pms_name`, `dh_id`, `dh_name`, `statis_ymd`, `flow_time`) 
VALUES ('2026-01-26', '2026012602', '202601260201', '2025-12-02 08:31:07.477179', NULL, '5c07c1b3-c869-4bae-b57f-92112fw1393d', '都匀市3G机楼四楼动力机房1号机房', NULL, NULL, '01-08-09-03-01-11', '都匀市3G机楼_都匀市3G机楼四楼动力机房2#', '20251203', '2026-01-13 15:41:13');

SELECT * FROM ods_zz_room LIMIT 10;
INSERT INTO `ods_zz_room` (`stat_time`, `int_id`, `tele_cmn_serv_pro_name`, `pms_design_code`, `plan_rack_num`, `loadable_rack_num`, `retire_time`, `zh_label`, `batch_num`, `collect_time`, `qualitor`, `room_area`, `floor_num`, `row_num`, `lifecycle_status`, `column_num`, `end_row`, `start_column`, `end_column`, `length`, `width`, `airconditioner_power`, `asset_address_code`, `equipment_power`, `qr_code_no`, `maintainor_method`, `uuid`, `equiproom_level`, `equiproom_type`, `province_id`, `city_id`, `county_id`, `address_code`, `project_code`, `height`, `project_name`, `row_direction`, `china_tower_operations_id`, `shared_unit`, `china_tower_station_code`, `china_tower_room_type`, `installed_rack_num`, `is_headquarters_used`, `start_row`, `related_site`, `if_village_pass_serv`, `village_pass_serv_name`, `village_pass_serv_code`, `alias_name`, `property_right`, `property_unit`, `cutin_date`, `irms_province_code`, `column_direction`, `if_tele_cmn_serv`, `tele_cmn_serv_pro_code`, `fifth_generation_flag`, `mainit_unit`, `pms_design_name`, `business_unit`, `flow_time`) 
VALUES ('2026-01-26', '000102053100000000595732', NULL, NULL, NULL, NULL, NULL, '泰州迎春路住宅区41号院01F', '20250723', '2025-07-23 17:05:04', '许兵', '20', '1', NULL, '在网', NULL, NULL, NULL, NULL, NULL, NULL, '0.0', NULL, '0.0', '070524010010000595732', NULL, NULL, '接入', '无线机房', '320000', '321200', '321202', NULL, NULL, NULL, NULL, NULL, NULL, '无', NULL, NULL, NULL, '否', NULL, '000102013100000000579692', '否', NULL, NULL, '泰州迎春路住宅区41号院01F', '租用', '中国移动', '2011-08-16', 'JS', NULL, '否', NULL, '否', NULL, NULL, NULL, '2025-12-31 11:00:28');

SELECT * FROM ods_zz_room_property LIMIT 10;
INSERT INTO `ods_zz_room_property` (`stat_time`, `res_code`, `irms_province_code`, `power_related_site_name`, `power_monitor_conf`, `video_monitor_conf`, `batch_num`, `collect_time`, `province_id`, `city_id`, `county_id`, `zh_label`, `power_room_type`, `space_room_type`, `battery_backup_time`, `power_supply_mode`, `power_room_name`, `power_room_id`, `log_saved_time`, `power_supply_type`, `ac_terminal`, `ac_config`, `refrigeration_mode`, `refer_pue`, `flow_time`) 
VALUES ('2026-01-26', '-1000733344', 'HN', '-970402447', '无', '无', '20250723', '2025-07-23 16:11:17', '430000', '431300', '431322', '-970402677', '基站机房', '无线机房', '15', '单电源双回路供电', '新化县化溪白溪村无线机房', '121812', '1', '交流220V', '精密空调', '其他', '风冷', '1.1', '2025-12-31 10:45:26');



# 设备匹配
ods_zz_device_transform
ods_zz_device_transform_device

# 链路匹配