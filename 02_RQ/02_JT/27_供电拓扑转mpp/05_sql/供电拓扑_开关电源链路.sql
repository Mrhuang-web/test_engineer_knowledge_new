SELECT * FROM zz_data_sync_info;
00123123
SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-01-11-02-01';
SELECT * FROM topu_mete_display_config;
SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';


SELECT * FROM ods_zz_link_pe_in WHERE related_device = '441000000000008089010115'
SELECT * FROM ods_zz_link_pe_in WHERE res_code = '441000000000008089010115'
SELECT * FROM ods_zz_link_pe_in WHERE res_code = '441100111000068928044111'

# 站点机房
'2026012601', '2026012602',



# 链路
SELECT * FROM ods_zz_link_pe_in where down_device_type = '低压交流配电' LIMIT 10;

INSERT INTO `ods_zz_link_pe_in` (`stat_time`, `res_code`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `related_device_type`, `related_device`, `branch_type`, `branch_type_abbreviation`, `branch_number`, `branch_active_standby`, `branch_rated_capacity`, `lifecycle_status`, `branch_name`, `down_device_ralated_room`, `down_device_name`, `down_branch_name`, `down_device_type`, `down_branch_type`, `down_branch_type_abbreviation`, `down_branch_number`, `down_branch_rated_capacity`, `down_branch_active_standby`, `down_use_status`, `qr_code_no`, `qualitor`, `flow_time`) 
VALUES ('2026-01-26', '441100111000068928044111', '20260126', '2026-01-26 15:25:44', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '开关电源', '44100000000000808901111', '设备', 'TOUT', '1', '主用', '2000', '在用', '广州从化青云四楼机房交换1-TOUT2-2000-主用-在用-REC-4F-6-1', '2026012602', '441000000000008088644213', '广州从化青云四楼机房动力3-REC/Q-4F-6-2--2000--', '低压直流配电', '微型断路器', 'KIN', NULL, NULL, '主用', '在用', NULL, '徐恒辉', '2026-01-13 15:32:14');

INSERT INTO `ods_zz_link_pe_in` (`stat_time`, `res_code`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `related_device_type`, `related_device`, `branch_type`, `branch_type_abbreviation`, `branch_number`, `branch_active_standby`, `branch_rated_capacity`, `lifecycle_status`, `branch_name`, `down_device_ralated_room`, `down_device_name`, `down_branch_name`, `down_device_type`, `down_branch_type`, `down_branch_type_abbreviation`, `down_branch_number`, `down_branch_rated_capacity`, `down_branch_active_standby`, `down_use_status`, `qr_code_no`, `qualitor`, `flow_time`) 
VALUES ('2026-01-26', '441100011100068928044111', '20260126', '2026-01-26 15:25:44', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '开关电源', '44100000000000808901111', '设备', 'TOUT', '1', '主用', '2000', '在用', '广州从化青云四楼机房交换1-TOUT1-2000-主用-在用-REC-4F-6-1', '2026012602', '441000000000008088441231', '广州从化青云四楼机房动力3-REC/Q-4F-6-1--2000--', '低压直流配电', '微型断路器', 'KIN', NULL, NULL, '主用', '在用', NULL, '徐恒辉', '2026-01-13 15:32:14');

INSERT INTO `ods_zz_link_pe_in` (`stat_time`, `res_code`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `related_device_type`, `related_device`, `branch_type`, `branch_type_abbreviation`, `branch_number`, `branch_active_standby`, `branch_rated_capacity`, `lifecycle_status`, `branch_name`, `down_device_ralated_room`, `down_device_name`, `down_branch_name`, `down_device_type`, `down_branch_type`, `down_branch_type_abbreviation`, `down_branch_number`, `down_branch_rated_capacity`, `down_branch_active_standby`, `down_use_status`, `qr_code_no`, `qualitor`, `flow_time`) 
VALUES ('2026-01-26', '441100011100068141244111', '20260126', '2026-01-26 15:25:44', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '开关电源', '44100000000000808901111', '设备', 'TOUT', '1', '主用', '2000', '在用', '广州从化青云四楼机房交换1-TOUT1-2000-主用-在用-REC-4F-6-1', '2026012602', '1000457941123', '广州从化青云四楼机房动力3-REC/Q-4F-6-1--2000--', '低压交流配电', '塑壳断路器', 'KIN', '1', '160', '主用', '空闲', '04139908016-100057253', '侯悦', '2025-12-31 10:56:19');


DELETE FROM ods_zz_link_pe_in WHERE res_code = '441100011100068928044111';
DELETE FROM ods_zz_link_pe_in WHERE res_code = '441100111000068928044111';







# 上游  开关电源
441000000000008089010115
ods_zz_device_switch_power

SELECT * FROM ods_zz_device_switch_power WHERE res_code IN ('441000000000008089010115');
SELECT * FROM ods_zz_device_switch_power WHERE res_code IN ('44100000000000808901111');
	# 插入综资
	INSERT INTO `ods_zz_device_switch_power` (`stat_time`, `res_code`, `qualitor`, `related_rackpos`, `qr_code_no`, `power_device_id`, `device_number`, `power_device_name`, `assets_no`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `related_system`, `rated_output_voltage`, `monitoring_module_model`, `total_rack_loading_modules`, `total_rack_match_modules`, `signal_output_rated_capacity`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `total_rack_loading_modules_number`, `total_rack_match_modules_number`, `flow_time`) 
	VALUES ('2026-01-26', '44100000000000808901111', 'admin', NULL, NULL, '00123123', '1', '开关电源[珠江电源](GZM42B7局)', '2121-A2515419,2121-01078588,2121-01078577,2121-01078578,2121-01078579,2121-01078580,2121-01078581,2121-01078582,2121-01078583,2121-01078584,2121-01078585,2121-01078586', '20260126', '2026-01-26 15:03:32', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '开关电源', '分立开关电源', '广州从化青云四楼机房交换1-分立开关电源-4F-6-1', '06010001', 'PRS6300', '珠江', '441000000000008732898964', '-48V', 'PRS6300', NULL, NULL, '100', '2011-11-21', '2023-11-21', '在网', 'liminyi5', '15', '10.0', '2026-01-13 15:17:10');









# 下游  低压直流配电
441000000000008088695324
441000000000008088695327
ods_zz_device_low_dc_distribution

SELECT * FROM ods_zz_device_low_dc_distribution WHERE res_code IN ('441000000000008088695324','441000000000008088695327');
SELECT * FROM ods_zz_device_low_dc_distribution WHERE res_code IN ('441000000000008088644213','441000000000008088441231');
	
	# 插入综资	
	INSERT INTO `ods_zz_device_low_dc_distribution` (`stat_time`, `res_code`, `power_device_name`, `assets_no`, `qr_code_no`, `device_number`, `batch_num`, `collect_time`, `irms_province_code`, `total_onput_port`, `start_time`, `estimated_retirement_time`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `related_system`, `reted_capacity`, `total_input_port`, `lifecycle_status`, `maintainor`, `qualitor`, `related_rackpos`, `power_device_id`, `flow_time`) 
	VALUES ('2026-01-26', '441000000000008088644213', NULL, '2121-A2515420', NULL, '56', '20260126', '2026-01-26 15:03:32', 'GZ', '108', '2011-11-21', '2026-11-21', '520000', '520400', '520404', '2026012601', '2026012602', '低压直流配电', '-48V直流配电柜', '贵州四楼机房动力3--48V直流配电柜-4F-6-1', '04020111', 'PRD2000DCH-6M', '珠江', '441000000000008732898964', '500', '2', '在网', '魏敏', 'liminyi5', '441100000000076957394977', '123456', '2026-01-13 15:16:59');
	
	INSERT INTO `ods_zz_device_low_dc_distribution` (`stat_time`, `res_code`, `power_device_name`, `assets_no`, `qr_code_no`, `device_number`, `batch_num`, `collect_time`, `irms_province_code`, `total_onput_port`, `start_time`, `estimated_retirement_time`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `related_system`, `reted_capacity`, `total_input_port`, `lifecycle_status`, `maintainor`, `qualitor`, `related_rackpos`, `power_device_id`, `flow_time`) 
	VALUES ('2026-01-26', '441000000000008088441231', NULL, '2121-A2515421', NULL, '56', '20260126', '2026-01-26 15:03:32', 'GZ', '144', '2011-11-21', '2026-11-21', '520000', '520400', '520404', '2026012601', '2026012602', '低压直流配电', '-48V直流配电柜', '贵州机房动力3--48V直流配电柜-4F-6-2', '04020111', 'PRD2000DCH-6S', '珠江', '441000000000008732898964', '500', '2', '在网', '魏敏', 'liminyi5', '441100000000076957394977', '1234567', '2026-01-13 15:16:59');

	DELETE FROM ods_zz_device_low_dc_distribution WHERE res_code = '441000000000008088441231';
	
	
	
	
# 下游  低压交流配电
ods_zz_device_low_ac_distribution
441000000000008088441231
SELECT * FROM ods_zz_device_low_ac_distribution LIMIT 10;
SELECT * FROM ods_zz_device_low_ac_distribution WHERE res_code = '1000457941123' LIMIT 10;

INSERT INTO `ods_zz_device_low_ac_distribution` (`stat_time`, `res_code`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `batch_num`, `collect_time`, `irms_province_code`, `device_number`, `qr_code_no`, `power_device_id`, `power_device_name`, `assets_no`, `related_room`, `product_name`, `vendor_id`, `related_system`, `reted_capacity`, `total_input_port`, `total_output_port`, `device_configuration_spd_brand`, `spd_max_rate`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `related_rackpos`, `province_id`, `city_id`, `county_id`, `related_site`, `flow_time`) 
VALUES ('2026-01-26', '1000457941123', '低压交流配电', 'UPS输出列头柜', '抚顺沈抚新城通信楼7层IDC机房-低压交流配电-7941', '0902000000457941', '20260126', '2026-01-26 16:11:05', 'GZ', NULL, '041308011-100045794', '1000457941123', NULL, NULL, '2026012602', 'HM1-O1C-Y', '广州敏思', '-267692123', '400', '2', '64', NULL, NULL, '2019-04-01', '2034-04-01', '现网', '经圣扬', '侯悦', NULL, '520000', '520400', '520404', '2026012601', '2025-12-31 10:45:51');





# 匹配情况
SELECT * FROM dws_zz_dh_site LIMIT 10;
SELECT * FROM dws_zz_dh_site  where precinct_id = '01-08-08-01-11-02' LIMIT 10;
SELECT * FROM dws_zz_dh_room LIMIT 10;
SELECT * FROM dws_zz_dh_room  where precinct_id = '01-08-08-01-11-02-01' LIMIT 10;
SELECT * FROM dws_zz_dh_device LIMIT 10;
SELECT * FROM dws_zz_dh_device  where precinct_id = '01-08-08-01-11-02-01' LIMIT 10;

SELECT * FROM dwd_zz_device_total LIMIT 10;
SELECT * FROM dwd_zz_device_total where related_room = '2026012602' LIMIT 10;