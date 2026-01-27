SELECT * FROM zz_data_sync_info;

SELECT * FROM topu_mete_display_config;
SELECT * FROM t_cfg_topology_v2_configuration WHERE up_precinct_id LIKE "01-08-08%" LIMIT 10;
SELECT * FROM t_cfg_topology_v2_configuration WHERE up_room = '广州从化青云四楼机房交换1';
SELECT * FROM t_cfg_topology_v2_configuration  LIMIT 1000;
SELECT * FROM zz_to_rm_rm_device LIMIT 10;

SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-01-11-02-01';

SELECT COUNT(1) FROM ods_zz_link_pe_out;
SELECT * FROM ods_zz_link_pe_out LIMIT 10;


# 站点机房设备查看
SELECT * FROM t_cfg_precinct WHERE precinct_id LIKE '01-08-08-01-11-02%';
SELECT * FROM t_cfg_precinct WHERE precinct_id LIKE '01-01-03-07-01-02%';



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


# 机房匹配(01-08-08-01-11-02-01   贵1数据中心楼2_综合机房)
ods_zz_irms_rom_map
ods_zz_room
ods_zz_room_property
01-08-09-03-01-11
SELECT * FROM ods_zz_irms_rom_map LIMIT 10;
INSERT INTO `ods_zz_irms_rom_map` (`stat_time`, `zg_id`, `address_code`, `batch_num`, `province_id`, `uuid`, `zg_name`, `pms_id`, `pms_name`, `dh_id`, `dh_name`, `statis_ymd`, `flow_time`) 
VALUES ('2026-01-26', '2026012602', '202601260201', '2026-01-26 16:11:18.477179', NULL, '5c07c1b3-c869-4bae-b57f-921231293d', '贵1数据中心楼2_综合机房', NULL, NULL, '01-08-08-01-11-02-01', '贵1数据中心楼2_综合机房', '20260126', '2026-01-13 15:41:13');

SELECT * FROM ods_zz_room LIMIT 10;
INSERT INTO `ods_zz_room` (`stat_time`, `int_id`, `tele_cmn_serv_pro_name`, `pms_design_code`, `plan_rack_num`, `loadable_rack_num`, `retire_time`, `zh_label`, `batch_num`, `collect_time`, `qualitor`, `room_area`, `floor_num`, `row_num`, `lifecycle_status`, `column_num`, `end_row`, `start_column`, `end_column`, `length`, `width`, `airconditioner_power`, `asset_address_code`, `equipment_power`, `qr_code_no`, `maintainor_method`, `uuid`, `equiproom_level`, `equiproom_type`, `province_id`, `city_id`, `county_id`, `address_code`, `project_code`, `height`, `project_name`, `row_direction`, `china_tower_operations_id`, `shared_unit`, `china_tower_station_code`, `china_tower_room_type`, `installed_rack_num`, `is_headquarters_used`, `start_row`, `related_site`, `if_village_pass_serv`, `village_pass_serv_name`, `village_pass_serv_code`, `alias_name`, `property_right`, `property_unit`, `cutin_date`, `irms_province_code`, `column_direction`, `if_tele_cmn_serv`, `tele_cmn_serv_pro_code`, `fifth_generation_flag`, `mainit_unit`, `pms_design_name`, `business_unit`, `flow_time`) 
VALUES ('2026-01-26', '2026012602', NULL, NULL, NULL, NULL, NULL, '贵1数据中心楼2_综合机房', '20260126', '2026-01-26 16:11:18', '许兵', '20', '1', NULL, '在网', NULL, NULL, NULL, NULL, NULL, NULL, '0.0', NULL, '0.0', '070524010010000595732', NULL, NULL, '接入', '无线机房', '520000', '520400', '520404', NULL, NULL, NULL, NULL, NULL, NULL, '无', NULL, NULL, NULL, '否', NULL, '2026012601', '否', NULL, NULL, '贵1数据中心楼2_综合机房', '租用', '中国移动', '2011-08-16', 'GZ', NULL, '否', NULL, '否', NULL, NULL, NULL, '2026-01-26 16:11:18');

SELECT * FROM ods_zz_room_property LIMIT 10;
INSERT INTO `ods_zz_room_property` (`stat_time`, `res_code`, `irms_province_code`, `power_related_site_name`, `power_monitor_conf`, `video_monitor_conf`, `batch_num`, `collect_time`, `province_id`, `city_id`, `county_id`, `zh_label`, `power_room_type`, `space_room_type`, `battery_backup_time`, `power_supply_mode`, `power_room_name`, `power_room_id`, `log_saved_time`, `power_supply_type`, `ac_terminal`, `ac_config`, `refrigeration_mode`, `refer_pue`, `flow_time`) 
VALUES ('2026-01-26', '202601260201', 'GZ', '-970402447', '无', '无', '20260126', '2026-01-26 16:11:18', '520000', '520400', '520404', '2026012602', '基站机房', '无线机房', '15', '单电源双回路供电', '新化县化溪白溪村无线机房', '121812', '1', '交流220V', '精密空调', '其他', '风冷', '1.1', '2026-01-26 16:11:18');



# 设备匹配
ods_zz_device_transform
ods_zz_device_high_distribution
ods_zz_device_low_ac_distribution

# ID:303121G00379232
SELECT * FROM ods_zz_device_transform LIMIT 10;
INSERT INTO `ods_zz_device_transform` (`stat_time`, `res_code`, `low_reted_current`, `backup_method`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `device_number`, `qr_code_no`, `power_device_id`, `power_device_name`, `assets_no`, `product_name`, `vendor_id`, `rated_power`, `input_rated_voltage`, `flow_time`) 
VALUES ('2026-01-26', '1059067601', NULL, 'N+1冷备', '2020-11-01', '2035-11-01', '工程', '李童', '黄月', '20260126', '2026-01-26 16:11:18', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '变压器', '干式变压器', '沈阳西瓦窑通信楼1层高低压配电动力机房-变压器-7643', '0301000059067643', NULL, '04240408004-105906764', '303121G00379232' , NULL, '303121G00379232', 'SCZB11-2000/10', '广州广高', '2000', '10KV', '2026-01-26 16:11:18');
SELECT * FROM ods_zz_device_transform WHERE res_code = '4276239001' LIMIT 10;
DELETE FROM ods_zz_device_transform WHERE res_code = '4276239001';

# 链路匹配
ods_zz_link_pe_out
ods_zz_link_pe_in

SELECT * FROM ods_zz_link_pe_out LIMIT 10;
INSERT INTO `ods_zz_link_pe_out` (`stat_time`, `res_code`, `related_device`, `branch_type`, `branch_type_abbreviation`, `branch_number`, `major_type`, `down_device_related_rack`, `rack_switch_name`, `down_device_power`, `qualitor`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `branch_active_standby`, `lifecycle_status`, `branch_name`, `down_device_ralated_room`, `down_device_type`, `branch_rated_capacity`, `down_device_name`, `down_device_related_rackpos`, `qr_code_no`, `related_site`, `related_room`, `related_device_type`, `flow_time`) 
VALUES ('2026-01-26', '1000389194', '1059067601', '微型断路器', 'KOUT', '38', NULL, NULL, NULL, '0', '刘硕', '20251224', '2025-12-24 16:29:12', 'GZ', '520000', '520400', '520404', '主用', '空闲', '贵州_鞍山移动铁西生产楼局四楼402IDC机房', '2026012602', NULL, '32', NULL, NULL, '04120208017-100038919', '2026012601', '2026012602', '低压交流配电', '2026-01-13 16:18:13');

SELECT * FROM ods_zz_link_pe_in LIMIT 10;
INSERT INTO `ods_zz_link_pe_in` (`stat_time`, `res_code`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `related_device_type`, `related_device`, `branch_type`, `branch_type_abbreviation`, `branch_number`, `branch_active_standby`, `branch_rated_capacity`, `lifecycle_status`, `branch_name`, `down_device_ralated_room`, `down_device_name`, `down_branch_name`, `down_device_type`, `down_branch_type`, `down_branch_type_abbreviation`, `down_branch_number`, `down_branch_rated_capacity`, `down_branch_active_standby`, `down_use_status`, `qr_code_no`, `qualitor`, `flow_time`) 
VALUES ('2026-01-26', '1000568100', '20260126', '2026-01-26 16:11:05', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '变压器', '1059067601', '刀闸开关', 'MOUT', '1', '主用', '250', '在用', '营口渤海局七层IDC动力机房-MOUT1-250-主用-在用488', '2026012602', '4276239001', '营口渤海局七层IDC动力机房-KIN36-32-主用-在用488', '低压交流配电', '塑壳断路器', 'KIN', '36', '32', '主用', '在用', '04170108016-100056848', '吴昊（营口）', '2026-01-26 16:11:18');

SELECT * FROM ods_zz_link_pe_in where res_code = '4276239001' LIMIT 10;


SELECT * FROM ods_zz_link_pe_in WHERE res_code = '1000568100' and irms_province_code = 'GZ' LIMIT 10;
DELETE FROM ods_zz_link_pe_in WHERE res_code = '1000568100' and irms_province_code = 'GZ' ;

SELECT * FROM ods_zz_link_pe_in WHERE related_device = '441000000000008089010115'


SELECT * FROM dws_zz_dh_room LIMIT 10;
SELECT COUNT(1) FROM dws_zz_dh_room LIMIT 10;

SELECT * FROM dws_zz_dh_site LIMIT 10;
SELECT * FROM dws_zz_dh_site  where precinct_id = '01-08-08-01-11-02' LIMIT 10;
SELECT * FROM dws_zz_dh_room LIMIT 10;
SELECT * FROM dws_zz_dh_room  where precinct_id = '01-08-08-01-11-02-01' LIMIT 10;
SELECT * FROM dws_zz_dh_device LIMIT 10;
SELECT * FROM dws_zz_dh_device  where precinct_id = '01-08-08-01-11-02-01' LIMIT 10;
DELETE FROM dws_zz_dh_device where precinct_id = '01-08-08-01-11-02-01' AND res_code = '4276239001'


SELECT * FROM dwd_zz_device_total LIMIT 10;
SELECT * FROM dwd_zz_device_total where related_room = '2026012602' LIMIT 10;
delete from dwd_zz_device_total where res_code = '4276239001';










4370623028     4276239312
4370623032     4276239315
4489114672     1147994757581615104

SELECT * FROM ods_zz_link_pe_in WHERE related_device_type = '变压器' and irms_province_code = 'GZ' LIMIT 10;



SELECT * FROM ods_zz_link_pe_in WHERE res_code = '1060385088059518976' and irms_province_code = 'GZ' LIMIT 10;
INSERT INTO `ods_zz_link_pe_in` (`stat_time`, `res_code`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `related_device_type`, `related_device`, `branch_type`, `branch_type_abbreviation`, `branch_number`, `branch_active_standby`, `branch_rated_capacity`, `lifecycle_status`, `branch_name`, `down_device_ralated_room`, `down_device_name`, `down_branch_name`, `down_device_type`, `down_branch_type`, `down_branch_type_abbreviation`, `down_branch_number`, `down_branch_rated_capacity`, `down_branch_active_standby`, `down_use_status`, `qr_code_no`, `qualitor`, `flow_time`) 
VALUES ('2026-01-26', '2026010101', '20260126', '2026-01-26 14:13:37', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '变压器', '1059067601', '母排', 'MOUT', '1', '主用', '2000', '在用', '花溪区花溪枢纽B栋一楼B间动力机房-MOUT01-2000-主用-在用', '2026012602', '4276239001', '4276239001', '低压交流配电', '框架断路器', 'KIN', NULL, '1250', '主用', '其他', NULL, '吴邦庆', '2025-12-31 11:23:09');

SELECT * FROM ods_zz_link_pe_in WHERE res_code = '2026010101'
DELETE FROM  ods_zz_link_pe_in  WHERE res_code = '2026010101'



INSERT INTO `ods_zz_link_pe_in` (`stat_time`, `res_code`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `related_device_type`, `related_device`, `branch_type`, `branch_type_abbreviation`, `branch_number`, `branch_active_standby`, `branch_rated_capacity`, `lifecycle_status`, `branch_name`, `down_device_ralated_room`, `down_device_name`, `down_branch_name`, `down_device_type`, `down_branch_type`, `down_branch_type_abbreviation`, `down_branch_number`, `down_branch_rated_capacity`, `down_branch_active_standby`, `down_use_status`, `qr_code_no`, `qualitor`, `flow_time`) 
VALUES ('2026-01-26', '2026010102', '20260126', '2026-01-26 14:13:37', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '变压器', '4370623032', '母排', 'MOUT', '01', '主用', '2000', '在用', '花溪区花溪枢纽B栋一楼B间动力机房-MOUT01-2000-主用-在用', '4343988767', '1056208924081524736', NULL, '低压交流配电', '框架断路器', 'KIN', NULL, '1250', '主用', '其他', NULL, '吴邦庆', '2025-12-31 11:23:09');
INSERT INTO `ods_zz_link_pe_in` (`stat_time`, `res_code`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `related_device_type`, `related_device`, `branch_type`, `branch_type_abbreviation`, `branch_number`, `branch_active_standby`, `branch_rated_capacity`, `lifecycle_status`, `branch_name`, `down_device_ralated_room`, `down_device_name`, `down_branch_name`, `down_device_type`, `down_branch_type`, `down_branch_type_abbreviation`, `down_branch_number`, `down_branch_rated_capacity`, `down_branch_active_standby`, `down_use_status`, `qr_code_no`, `qualitor`, `flow_time`) 
VALUES ('2026-01-26', '2026010103', '20260126', '2026-01-26 14:13:37', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '变压器', '4489114672', '母排', 'MOUT', '01', '主用', '2000', '在用', '花溪区花溪枢纽B栋二楼A间动力机房-MOUT01-2000-主用-在用', '4343990631', '1056219490879672320', NULL, '低压交流配电', '框架断路器', 'KIN', NULL, '1250', '主用', '其他', NULL, '吴邦庆', '2025-12-31 11:23:09');



INSERT INTO `ods_zz_device_transform` (`stat_time`, `res_code`, `low_reted_current`, `backup_method`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `device_number`, `qr_code_no`, `power_device_id`, `power_device_name`, `assets_no`, `product_name`, `vendor_id`, `rated_power`, `input_rated_voltage`, `flow_time`) 
VALUES ('2026-01-26', '4276239001', '2886', '1+1热备', '2019-10-01', '2034-10-01', '其他', '殷祖利-13639112286', '吴邦庆', '20260126', '2026-01-26 14:21:15', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '变压器', '干式变压器', '花溪区花溪枢纽B栋一楼A间动力机房-干式变压器-1', '03010001', '1', '235103080044276239312', '4276239001', NULL, NULL, 'SCB13-2000/10（T1-7）', '广州明珠', '2000', '10KV', '2026-01-13 15:13:18');




SELECT * FROM ods_zz_device_low_ac_distribution LIMIT 10;
SELECT * FROM ods_zz_device_low_ac_distribution where res_code IN ('4276239312','4276239315','1147994757581615104') 
LIMIT 10;
SELECT * FROM ods_zz_device_low_ac_distribution where res_code IN ('4276239001') 


SELECT * FROM ods_zz_device_transform where res_code IN ('4276239312','4276239315','1147994757581615104') 

LIMIT 10;






SELECT * FROM ods_zz_link_pe_in WHERE irms_province_code = 'GZ' LIMIT 10;
SELECT * FROM dws_zz_dh_room where zh_label = '4280128036'
SELECT * FROM ods_zz_room where int_id = '4280128036' LIMIT 10;