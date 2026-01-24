SELECT * FROM t_zz_power_device LIMIT 10;
SELECT * FROM t_zz_power_specialty LIMIT 10;
SELECT * FROM t_zz_site_property LIMIT 10;
SELECT * FROM t_zz_space_resources LIMIT 10;    	# 站点，机房
SELECT * from t_sync_field_config;						# 映射表


# 站点
SELECT * FROM t_zz_space_resources where space_type = 101 order by data_time desc  LIMIT 10;  # 站点
	SELECT * FROM t_zz_power_specialty where zh_label = '玉林北流市新圩镇新大新购物广场' LIMIT 10;
	
	SELECT * FROM t_zz_power_specialty where device_type_id = 0 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_specialty where device_type_id = 0 order by data_time desc LIMIT 1;
	
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config
	where es_index_name = 'ods_ftp_site_property' and sync_model = 1 and table_name is not null LIMIT 1;





# 机房
SELECT * FROM t_zz_space_resources where space_type = 102 order by data_time desc LIMIT 10;  # 机房
	SELECT * FROM t_zz_power_specialty where zh_label = '玉林北流市新圩镇新大新购物广场' LIMIT 10;
	
	SELECT * FROM t_zz_power_specialty where device_type_id = 1020 order by data_time desc LIMIT 10;
	
	SELECT COUNT(*) FROM t_zz_power_specialty where device_type_id = 1020 AND data_time = '20251104' order by create_time desc LIMIT 10;
	
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_room_property' and sync_model = 1 and table_name is not null LIMIT 1;

	SELECT * FROM t_sync_field_config;



# 变压器
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_device_pe_transform' and sync_model = 1 and table_name is not null LIMIT 1;
	
	SELECT * FROM t_zz_power_specialty where device_type_id = 3 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 3 order by data_time desc LIMIT 1;

 	SELECT * FROM t_zz_power_device where device_type_id = 3 order by data_time desc LIMIT 10;
	
	SELECT * FROM t_sync_field_config;




# 变换设备
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_device_pe_transform' and sync_model = 1 and table_name is not null LIMIT 1;
	
	SELECT * FROM t_zz_power_specialty where device_type_id = 14 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 14 order by data_time desc LIMIT 1;

 	SELECT * FROM t_zz_power_device where device_type_id = 14 order by data_time desc LIMIT 10;
	
	SELECT * FROM t_sync_field_config;
	



# 高压配电系统
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_high_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
	
	SELECT * FROM t_zz_power_specialty where device_type_id = 204 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device_sys where device_type_id = 204 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device_sys where device_type_id = 204 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;




# 高压配电
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_high_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
	
	SELECT * FROM t_zz_power_specialty where device_type_id = 1 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 1 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 1 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	



# 高压直流电源系统
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_high_distribution' and sync_model = 205 and table_name is not null LIMIT 1;
	
	SELECT * FROM t_zz_power_specialty where device_type_id = 205 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device_sys where device_type_id = 205 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device_sys where device_type_id = 205 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	


# 高压直流电源
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_high_distribution' and sync_model = 87 and table_name is not null LIMIT 1;
	
	SELECT * FROM t_zz_power_specialty where device_type_id = 87 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 87 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 87 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;








# 高压直流配电
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_high_distribution' and sync_model = 88 and table_name is not null LIMIT 1;
	
	SELECT * FROM t_zz_power_specialty where device_type_id = 88 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 88 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 88 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;






# 低压配电系统
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 206 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 206 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 206 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;





# 低压交流配电报表
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 2 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 2 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 2 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	




# 发电系统
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 207 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device_sys where device_type_id = 207 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device_sys where device_type_id = 207 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;






# 发电机组
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 5 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device_sys where device_type_id = 5 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device_sys where device_type_id = 5 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	
	
	

# 开关电源系统
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 202 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device_sys where device_type_id = 202 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device_sys where device_type_id = 202 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	



# 开关电源
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 6 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 6 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 6 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;







# 低压直流配电
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 4 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 4 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 4 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	
	



# UPS系统
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 201 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device_sys where device_type_id = 201 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device_sys where device_type_id = 201 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	
	
	


# UPS设备
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 8 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 8 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 8 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	



# 蓄电池（铅酸电池，锂电池）    仅需要展示铅酸电池
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 8 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 8 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 7 order by data_time desc LIMIT 1;
 	select * from t_zz_power_device where device_type_id = 7 order by data_time desc LIMIT 1;
 	
	select * from t_zz_power_device where device_type_id = 68 order by data_time desc LIMIT 1;
	SELECT MAX(id) FROM t_zz_power_device;
	INSERT INTO `t_zz_power_device` (`id`, `res_code`, `zh_label`, `data_time`, `device_id`, `device_type_id`, `device_type`, `device_code`, `related_site`, `related_room`, `lifecycle_status`, `rated_power`, `device_subclass`, `start_time`, `product_name`, `vendor_id`, `power_device_id`, `power_site_level`, `gx_power_site_level`, `estimated_retirement_time`, `sys_no_uuid`, `city_id`, `county_id`, `province_id`, `asset_code`, `device_brand`, `power_monitor_dev_name`, `power_room_type`, `serial_number`, `accept_date`, `factory_number`, `upper_device_name`, `upper_device_type`, `ralated_power_device`, `create_time`) 
	VALUES (49101828, '2a448cb59521408fb759c975c3711123', '光宇开关电源铅酸电池1/1', '20251022', '00771006000003161222', 68, '锂电池', '070200001000001', 'SITE-BC730F4003F42E7FE044000B5DE0921F', 'ROOM-77002089', '退网', NULL, '开关电源铅酸电池', '2005-12-30', 'GFM-500', NULL, NULL, NULL, NULL, '2011-12-30', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-10-23 07:42:58');

	
	SELECT * FROM t_sync_field_config;
	
	
	
	
	
	
	


# 空调（普通空调，机房专用空调    -- 查了两类了）  仅需要展示普通空调
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 11 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 11 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 11 order by data_time desc LIMIT 1;
 	select * from t_zz_power_device where device_type_id = 15 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	
	
	
	
	
# 节能设备
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 208 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 208 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 208 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	




# 动环监控
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 208 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 208 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 208 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	
	
	


# 智能电表
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 92 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 92 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 92 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	
	




# 动环专业内输出分路
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 203 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 203 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 203 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;
	
	
	




# 跨专业输出分路
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_net_pe_low_distribution' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 210 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 210 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 210 order by data_time desc LIMIT 1;
	
	SELECT * FROM t_sync_field_config;






# 其它设备
	select table_name tableName,device_type deviceType,device_type_id deviceTypeId 
		from t_sync_field_config 
	where es_index_name = 'ods_ftp_device_pe_other' and sync_model = 1 and table_name is not null LIMIT 1;
		
	SELECT * FROM t_zz_power_specialty where device_type_id = 209 order by data_time desc LIMIT 10;
	
	select data_time from t_zz_power_device where device_type_id = 209 order by data_time desc LIMIT 1;

 	select * from t_zz_power_device where device_type_id = 209 order by data_time desc LIMIT 1;
	SELECT MAX(id) FROM t_zz_power_device;
	INSERT INTO `t_zz_power_device` (`id`, `res_code`, `zh_label`, `data_time`, `device_id`, `device_type_id`, `device_type`, `device_code`, `related_site`, `related_room`, `lifecycle_status`, `rated_power`, `device_subclass`, `start_time`, `product_name`, `vendor_id`, `power_device_id`, `power_site_level`, `gx_power_site_level`, `estimated_retirement_time`, `sys_no_uuid`, `city_id`, `county_id`, `province_id`, `asset_code`, `device_brand`, `power_monitor_dev_name`, `power_room_type`, `serial_number`, `accept_date`, `factory_number`, `upper_device_name`, `upper_device_type`, `ralated_power_device`, `create_time`) 
	VALUES (49101828, '2a448cb59521408fb759c975c3442123', '光宇开关电源铅酸电池1/1', '20251022', '00771006000003161222', 209, '锂电池', '070200001000001', 'SITE-BC730F4003F42E7FE044000B5DE0921F', 'ROOM-77002089', '退网', NULL, '开关电源铅酸电池', '2005-12-30', 'GFM-500', NULL, NULL, NULL, NULL, '2011-12-30', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-10-23 07:42:58');
	
	SELECT * FROM t_sync_field_config;
	
	
	
	
	SELECT * FROM workflow_role_user LIMIT 10;