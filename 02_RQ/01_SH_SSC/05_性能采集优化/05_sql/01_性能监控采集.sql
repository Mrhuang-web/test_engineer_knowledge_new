
SELECT *   from t_scheduled_task;

SELECT * FROM his_data_collect_device_metecodes hisd;
SELECT hisd.collect_tag,hisd.device_id,hisd.uuid,hisd.* FROM his_data_collect_device hisd LIMIT 10;

# 接入fsu和设备（接入6个fsu，共1200个设备）
	SELECT * FROM t_cfg_precinct where precinct_name LIKE "上海性能测试%" LIMIT 10
	SELECT * FROM t_cfg_precinct WHERE precinct_id  = '01-01-08-04-03';
	SELECT * FROM t_cfg_site WHERE site_id  = '01-01-08-04-16';
	
	INSERT INTO `t_cfg_precinct` (`precinct_id`, `lsc_id`, `precinct_name`, `up_precinct_id`, `precinct_kind`, `isdel`, `update_time`, `access_time`, `area_code`, `access_type`, `description`, `building_type`, `room_kind`, `air_type`, `refrigeration_mode`, `resource_code`, `leader`, `leader_name`, `leader_phone`, `address`, `resource_origin`, `resource_name`, `scene`, `imp_remark`, `room_business_type`, `room_status`) 
	VALUES ('01-01-07-01-02', '441', '本地调试站点', '01-01-07-01', 2, 000, '2023-02-24 00:33:53', '2024-05-17 11:37:08', '', 0, '', 1, NULL, NULL, '3', '4411', '', '', '', '汕头市濠江区滨海街道达南路南山湾产业园B02单元', NULL, NULL, NULL, NULL, NULL, NULL);
	
	INSERT INTO `t_cfg_site` (`site_id`, `site_type`, `x`, `y`, `isdel`, `manager`, `managerName`, `managerPhone`, `countFloor`, `countPowerRoom`, `property`, `transformer1`, `transformer2`, `capacity`, `int_id`, `province_code`, `prefecture_code`, `county_code`, `point_name`, `import_level`, `backup_method`, `is_from_differ_trans_site`, `es_voltage_level`, `es_nature`, `pe_monitor_site_name`, `pe_monitor_site_code`, `es_sum_ways`, `es_capacity`, `oil_num`, `es_oil_machine_level`, `electricity_property`, `transformer_station4`, `transformer_station3`, `rittal`, `server`, `system`, `Is_belongIDC`, `dc_class`, `is_having_netroom`, `site_describe`, `is_business`, `other_name`, `stop_oilengine_process`, `start_oilengine_process`, `design_load`, `design_pue`, `refrigeration_mode`, `design_approval_value`, `site_converge_type`) VALUES ('01-01-07-01-02', 1, NULL, NULL, 000, NULL, NULL, NULL, 10, 72, '0', NULL, NULL, NULL, NULL, '1', NULL, NULL, NULL, 3, 2, 1, 2, 2, NULL, NULL, '2', '40096', 027, 3, '0', NULL, NULL, 3611, '832', '832', 1, 3, 0, NULL, 0, NULL, 2, 3, NULL, '1.4', '3', '1.4', NULL);
	
	# G_B_INF_WSDL = "http://10.12.7.87:30814/services/LSCService?wsdl"

	SELECT b.service_addr,b.service_port,b.private_service_addr,b.rtsp_port,a.* FROM t_cfg_device a INNER JOIN t_cfg_nmsdevice b ON a.device_id=b.device_id limit 100;
	
	SELECT 
		servers.service_addr,
		servers.service_port,
		servers.private_service_addr,
		servers.rtsp_port,
		device.device_name,
		device.device_id ,
		fsu.ftp_proxy,
		fsu.http_proxy_url
	FROM t_cfg_device device 
		JOIN t_cfg_nmsdevice servers ON device.device_id=servers.device_id 
		JOIN t_cfg_fsu fsu ON fsu.device_id = servers.device_id
	limit 100;
		
		
	
	
	# private_service_addr:10.1.203.121
	# http_port:8086
	SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00001006000001531542';
	SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000001531542';
	UPDATE t_cfg_nmsdevice SET http_port = NULL WHERE  device_id = '00001006000001531542';
	UPDATE t_cfg_nmsdevice SET private_service_addr = NULL WHERE  device_id = '00001006000001531542';
	
	
	# 测试B接口-1
	SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00001006000001531541';
	SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000001531541';
	SELECT * FROM t_cfg_device WHERE device_id = '00001006000001531541';
	
	
	# 随机插入一个改 127.0.0.1  3304，并且删除fsu
	INSERT INTO `t_cfg_nmsdevice` (`device_id`, `service_addr`, `service_port`, `up_server_id`, `web_page`, `login_state`, `sip_port`, `private_service_addr`, `subnetmask`, `gateway`, `rtsp_port`, `http_port`, `icpu_summit`, `imem_summit`, `isend_summit`, `irecv_summit`, `nms_type`) 
	VALUES ('00001006023141531541', '10.12.8.211', 30814, NULL, NULL, NULL, NULL, '', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, 101);

	INSERT INTO `t_cfg_device` (`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`, `brand`, `manufacturer`, `battery_single_number`, `battery_single_voltage`, `module_count`, `back_module_count`, `sigle_module_info`, `confirm_content`, `confirm_time`, `convert_efficiency`, `design_reserve_length`, `battery_number`, `max_discharge_efficiency`, `battery_type`, `protocol_convert_type`, `dev_describe`, `power_device_id`, `status`, `sys_no`) 
	VALUES ('1', '00001006023141531541', '性能采集B接口-1', '01', NULL, NULL, 000, NULL, 13, NULL, 76, 2, NULL, NULL, 1617, 0, NULL, NULL, NULL, '2024-09-26 15:49:27', NULL, NULL, NULL, NULL, '中兴力维', NULL, NULL, NULL, NULL, NULL, NULL, NULL, 8527166, NULL, NULL, NULL, NULL, NULL, 0, 0, 0, NULL, 1, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
	
	SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00001006023141531541';
	SELECT * FROM t_cfg_device WHERE device_id = '00001006023141531541';
	
	
	
	# 有数据的fsu  00101006000000158346   20251105000
	SELECT * FROM t_cfg_fsu WHERE device_id = '00101006000000158346';
	SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00101006000000158346';
	SELECT * FROM t_cfg_device WHERE device_id = '00101006000000158346';
	
	
	# fsu1  性能采集fsu1
	SELECT * FROM t_cfg_nmsdevice;
	SELECT * FROM t_cfg_fsu WHERE device_id = '00441006000000200001';
	SELECT * FROM t_cfg_device WHERE device_id = '00441006000000200001';
	
	
	# fsu2   2025120202  00441006000000200002
	SELECT * FROM t_cfg_nmsdevice;
	SELECT * FROM t_cfg_fsu WHERE device_id = '00441006000000200005';
	SELECT * FROM t_cfg_device WHERE device_id = '00441006000000200005';
	
	
	# fsu3   2025120203  00441006000000200043
	SELECT * FROM t_cfg_nmsdevice;
	SELECT * FROM t_cfg_fsu WHERE device_id = '00441006000000200043';
	SELECT * FROM t_cfg_device WHERE device_id = '00441006000000200043';
	
	
	# fsu4   2025120204  00441006000000200119
	SELECT * FROM t_cfg_nmsdevice;
	SELECT * FROM t_cfg_fsu WHERE device_id = '00441006000000200119';
	SELECT * FROM t_cfg_device WHERE device_id = '00441006000000200119';
	
	
	
	# fsu5   2025120205  00441006000000200119
	SELECT * FROM t_cfg_nmsdevice;
	SELECT * FROM t_cfg_fsu WHERE device_id = '00441006000000200120';
	SELECT * FROM t_cfg_device WHERE device_id = '00441006000000200120';
		
	
		
	# fsu6   2025120206  00441006000000200158
	SELECT * FROM t_cfg_nmsdevice;
	SELECT * FROM t_cfg_fsu WHERE device_id = '00441006000000200158';
	SELECT * FROM t_cfg_device WHERE device_id = '00441006000000200158';		
	
	
	
	
	
	# fsu8   2025120208  00441006000000200388
	SELECT * FROM t_cfg_nmsdevice;
	SELECT * FROM t_cfg_fsu WHERE device_id = '00441006000000200388';
	SELECT * FROM t_cfg_device WHERE device_id = '00441006000000200388';		
		
		
		
		
		
		# 查看对应设备
		SELECT device_id,device_name,precinct_name FROM t_cfg_device device
			JOIN t_cfg_precinct room ON device.precinct_id = room.precinct_id
			WHERE device.precinct_id = '01-01-08-04-16-01-06'   and device.device_name like '低压直流配电%';		
	
		
		
		
		
		
		
		
		
# 快设备
	#  性能采集机房10_200快1
	SELECT * FROM t_cfg_precinct WHERE precinct_name = '性能采集机房10_200快1';
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-01-08-04-16-01-12';
		
		# 查看对应设备
		SELECT device_id,device_name,precinct_name FROM t_cfg_device device
		JOIN t_cfg_precinct room ON device.precinct_id = room.precinct_id
		WHERE device.precinct_id = '01-01-08-04-16-01-12'   and device.device_name like '低压直流配电%';
		
			# 指定某个fsu下的
			SELECT device.device_id,device.device_name,precinct_name FROM t_cfg_device device
			JOIN t_cfg_precinct room ON device.precinct_id = room.precinct_id
			JOIN t_cfg_monitordevice fsu ON fsu.device_id = device.device_id AND fsu.fsu_device_id IN ('00441006000000200638','00441006000000200639','00441006000000200640','00441006000000200641','00441006000000200642')
			WHERE device.precinct_id = '01-01-08-04-16-01-12'   and device.device_name LIKE '低压直流配电%' LIMIT 1000;
				
	
		# fsu1 性能采集机房10_200快1(2025120501  -  2025120505)	
	
		SELECT * FROM t_cfg_nmsdevice;
		SELECT * FROM t_cfg_fsu 
			WHERE device_id 
			IN( '00441006000000200638','00441006000000200639','00441006000000200640','00441006000000200641','00441006000000200642');
		SELECT * FROM t_cfg_device 
			WHERE device_id 
			IN( '00441006000000200638','00441006000000200639','00441006000000200640','00441006000000200641','00441006000000200642');
	
		
		
		
		
		# fsu1 性能采集测试机房1_非压测  (2025120901)	
		SELECT * FROM t_cfg_nmsdevice;
		SELECT * FROM t_cfg_fsu 
			WHERE device_id 
			IN( '00441006000000201788');
		SELECT * FROM t_cfg_device 
			WHERE device_id 
			IN( '00441006000000201788');
	
		
		
		
		
		SELECT * from t_cfg_monitordevice where device_id='00441006000000200644'
		SELECT * FROM t_cfg_precinct WHERE precinct_id LIKE "01-01-08-04-16-02%"
		SELECT * FROM t_cfg_precinct WHERE precinct_id LIKE "01-01-08-04-16-01%"
		INSERT INTO `t_cfg_precinct` (`precinct_id`, `lsc_id`, `precinct_name`, `up_precinct_id`, `precinct_kind`, `isdel`, `update_time`, `access_time`, `area_code`, `access_type`, `description`, `building_type`, `room_kind`, `air_type`, `refrigeration_mode`, `resource_code`, `leader`, `leader_name`, `leader_phone`, `address`, `resource_origin`, `resource_name`, `scene`, `imp_remark`, `room_business_type`, `room_status`) 
		VALUES ('01-01-08-04-16-02-01', '441', '性能采集测试机房1_非压测', '01-01-08-04-16-02', 5, 000, '2025-12-02 00:31:21', NULL, NULL, 0, NULL, 1, 001, 1, '0', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '0');
	
				
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
	
	SELECT * FROM fsu WHERE fsuid = '2025120206';
	SELECT * FROM device where fsuid = '2025120206' LIMIT 10;
	SELECT * FROM signals where fsuid = '2025120206';
	
	DELETE FROM fsu WHERE fsuid = '2025120208';
	DELETE FROM device where fsuid = '2025120208';
	DELETE FROM signals where fsuid = '2025120208';	
	
	SELECT * FROM t_cfg_fsu where fsu_origin_code = '2025120205' LIMIT 10;
	SELECT * FROM t_cfg_fsu where fsu_origin_code = '20251100706' LIMIT 10;
	SELECT * FROM t_cfg_device where device_id = '0081300600018392';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-17-07-03-03-0706';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-17-07-03-03';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-17-07-03';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-17-07';
	
	
	SELECT * from t_cfg_monitordevice LIMIT 10;
	
	
	
	
	
	
	
	
	
	
	SELECT * from t_cfg_monitordevice where device_id='00001006000000201777'  
	SELECT * FROM t_cfg_device WHERE device_id IN( '00001006000000201763');
	
			SELECT * FROM t_cfg_nmsdevice;
		SELECT * FROM t_cfg_fsu 
			WHERE device_id 
			IN( '00001006000000201763');
		SELECT * FROM t_cfg_device 
			WHERE device_id 
			IN( '00001006000000201763');
	
	SELECT * FROM fsu WHERE fsuid = '20251206';
	SELECT * FROM device where fsuid = '20251206' LIMIT 10;
	SELECT * FROM signals where fsuid = '20251206';
	