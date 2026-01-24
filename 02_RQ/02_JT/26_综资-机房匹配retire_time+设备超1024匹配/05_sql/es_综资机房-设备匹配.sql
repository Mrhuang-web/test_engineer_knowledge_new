SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
SELECT * FROM t_cfg_device WHERE precinct_id LIKE "01-08-08-01-02-01%" AND device_type = '3' AND power_device_id =
'1001001001001' ;

SELECT * FROM t_cfg_device WHERE precinct_id LIKE "01-08-08-01-02-01%";
update t_cfg_device SET power_device_id = '' WHERE precinct_id LIKE "01-08-08-01-02-01%" ;


20251231000000
SELECT * FROM zz_data_sync_info;

SELECT * FROM zz_to_rm_rm_area_site WHERE batch_num = '20200223';

SELECT * FROM zz_to_rm_rm_area_room WHERE batch_num = '20200223';

SELECT * FROM zz_to_rm_rm_area_room WHERE batch_num = '20250723';


SELECT * FROM zz_to_rm_rm_device WHERE power_device_id = "1001001001002";


SELECT * FROM zz_to_rm_rm_device WHERE precinct_id LIKE "01-08-08-01-02-01%" ;
DELETE FROM  zz_to_rm_rm_device WHERE precinct_id LIKE "01-08-08-01-02-01%" ;




SELECT * FROM access_control_device
SELECT * FROM t_cfg_device where device_id LIKE "%008000000%";
SELECT * FROM t_cfg_fsu WHERE  device_id LIKE "%008000000%";
00800000025
00800000026
124123131241
SELECT * FROM t_cfg_device WHERE device_name LIKE "%UDP%"
SELECT * FROM t_cfg_fsu 

24537e2c-d925-47a7-bcb3-5d232002c455   UDP-邦讯-旧版1门			20250125
250ecc4d-3772-49f8-b5e8-1250ca25a976   UDP-邦讯-旧版2门			20250126
b7ee98d5-ca4d-4ae2-8aa2-1d7ceafc8ab9   UDP-海能1门					20250119



INSERT INTO `t_cfg_device` (`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`, `brand`, `manufacturer`, `battery_single_number`, `battery_single_voltage`, `module_count`, `back_module_count`, `sigle_module_info`, `confirm_content`, `confirm_time`, `convert_efficiency`, `design_reserve_length`, `battery_number`, `max_discharge_efficiency`, `battery_type`, `protocol_convert_type`, `dev_describe`, `power_device_id`, `status`, `sys_no`) 
VALUES ('1', '00800000009', 'UDP-海能1门', '01-01-17-02-05-01', 1, NULL, 000, '000010080000000009', 13, NULL, 76, 1, NULL, '20250109', 1617, 1, NULL, NULL, NULL, '2026-01-06 09:41:19', NULL, NULL, NULL, NULL, '中兴力维', NULL, 'V1.0', NULL, NULL, NULL, NULL, NULL, 10107177, NULL, NULL, NULL, NULL, NULL, 0, 0, 101, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);


INSERT INTO `t_cfg_device` (`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`, `brand`, `manufacturer`, `battery_single_number`, `battery_single_voltage`, `module_count`, `back_module_count`, `sigle_module_info`, `confirm_content`, `confirm_time`, `convert_efficiency`, `design_reserve_length`, `battery_number`, `max_discharge_efficiency`, `battery_type`, `protocol_convert_type`, `dev_describe`, `power_device_id`, `status`, `sys_no`) 
VALUES ('1', '00800000025', 'UDP-邦讯-旧版1门', '01-01-17-02-05-01', 1, NULL, 000, '000010080000000025', 13, NULL, 76, 1, NULL, '20250126', 1617, 1, NULL, NULL, NULL, '2026-01-06 09:41:19', NULL, NULL, NULL, NULL, '中兴力维', NULL, 'V1.0', NULL, NULL, NULL, NULL, NULL, 10107177, NULL, NULL, NULL, NULL, NULL, 0, 0, 101, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);

INSERT INTO `t_cfg_device` (`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`, `brand`, `manufacturer`, `battery_single_number`, `battery_single_voltage`, `module_count`, `back_module_count`, `sigle_module_info`, `confirm_content`, `confirm_time`, `convert_efficiency`, `design_reserve_length`, `battery_number`, `max_discharge_efficiency`, `battery_type`, `protocol_convert_type`, `dev_describe`, `power_device_id`, `status`, `sys_no`) 
VALUES ('1', '00800000026', 'UDP-邦讯-旧版2门', '01-01-17-02-05-01', 1, NULL, 000, '000010080000000026', 13, NULL, 76, 1, NULL, '20250126', 1617, 1, NULL, NULL, NULL, '2026-01-06 09:41:19', NULL, NULL, NULL, NULL, '中兴力维', NULL, 'V1.0', NULL, NULL, NULL, NULL, NULL, 10107177, NULL, NULL, NULL, NULL, NULL, 0, 0, 101, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);






SELECT * FROM access_control_device
SELECT * FROM t_cfg_device WHERE device_name LIKE "%UDP%"
SELECT * FROM t_cfg_fsu 


