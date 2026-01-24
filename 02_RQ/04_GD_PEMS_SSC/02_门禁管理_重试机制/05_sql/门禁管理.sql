# 已接入fsu门禁设备
SELECT 
	*
FROM t_cfg_device
	WHERE device_id IN (
	SELECT device_id
	FROM t_cfg_fsu
	WHERE device_code IS NOT NULL AND address = '10.12.5.142');
	
SELECT *
	FROM t_cfg_fsu
	WHERE address = '10.12.5.142'
	
	
SELECT *
	FROM t_cfg_fsu
	WHERE address = '10.1.203.120'

00001006000000015344
00001006000000015322
INSERT INTO `t_cfg_fsu` (`device_id`, `access_device_id`, `address`, `listen_port`, `up_fsu_id`, `up_link_port`, `net_type`, `net_info`, `fsu_state`, `register_server`, `udp_port`, `new_version`, `user_name`, `pass_word`, `ftp_port`, `ftp_proxy`, `http_proxy_url`, `fsu_origin_code`) 
VALUES ('00001006000000015322', '00001006000001531522', '10.1.203.120', 9999, NULL, NULL, 0, NULL, 0, NULL, NULL, 0, NULL, '', NULL, 0, NULL, NULL);
SELECT * FROM t_cfg_device WHERE device_id = '00001006000000015345';

INSERT INTO `t_cfg_device` (`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`, `brand`, `manufacturer`, `battery_single_number`, `battery_single_voltage`, `module_count`, `back_module_count`, `sigle_module_info`, `confirm_content`, `confirm_time`, `convert_efficiency`, `design_reserve_length`, `battery_number`, `max_discharge_efficiency`, `battery_type`, `protocol_convert_type`, `dev_describe`, `power_device_id`, `status`, `sys_no`) 
VALUES ('1', '00001006000000015322', 'FSU-门禁测试', '01', NULL, NULL, 000, NULL, 13, NULL, 76, 2, NULL, '01201712010123', 1617, 0, NULL, NULL, NULL, '2025-11-21 19:36:30', NULL, NULL, NULL, NULL, '中兴力维', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 10144403, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);


	
SELECT * FROM entrance_card_auth_task ORDER BY UPDATE_time DESC;
SELECT * FROM access_control_device ORDER BY time DESC;
