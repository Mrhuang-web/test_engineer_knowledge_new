SELECT * FROM t_cfg_dict WHERE col_name = 'site_type';


1、综合监控-动环（综资）站点类型
	动环
	SELECT tc.precinct_id,tc.precinct_name,tcs.site_type,tcd.dict_note FROM t_cfg_precinct tc
		JOIN t_cfg_site tcs ON tc.precinct_id = tcs.site_id
		JOIN t_cfg_dict tcd ON tcd.dict_code = tcs.site_type
		WHERE 
			tcd.col_name = 'site_type' and
			tc.precinct_name = '百色测试数据to传输节点'
	综资（power_site_level 或 gx_power_site_level）
	SELECT * from t_zz_space_resources WHERE zh_label = '百色测试数据to传输节点';  




2、隐患统计
	SELECT * FROM t_zz_space_resources where zh_label = '百色测试数据to传输节点' LIMIT 10;

	SELECT * FROM t_high_voltage_device LIMIT 10;

	SELECT * FROM t_city_power_cut_line_info 

	SELECT * FROM t_external_power_supply_config

	SELECT * FROM t_gathering_config_device

	SELECT * FROM t_zz_field_mapping


	SELECT * FROM overdue_device_detail LIMIT 10;
	SELECT * FROM t_zz_power_device LIMIT 10;
	SELECT * FROM t_zz_power_specialty LIMIT 10;


	select count(*) from t_zz_power_device where device_type = '变压器' and lifecycle_status = '现网';
	select count(*) from t_zz_power_specialty where device_type = '变压器' and lifecycle_status = '现网';





	SELECT tc3.precinct_name,tc2.precinct_name,tc.precinct_name,ea.*  from energy_audit_estimates ea
		join t_cfg_precinct tc on ea.precinct_id = tc.precinct_id
		JOIN t_cfg_precinct tc2 ON tc.up_precinct_id = tc2.precinct_id
		JOIN t_cfg_precinct tc3 ON tc2.up_precinct_id = tc3.precinct_id
		WHERE ea.ups_estimates != 'NULL' OR hvdc_estimates != 'NULL' ;
		



		
	SELECT * FROM t_zz_space_resources where precinct_id != 'NULL' LIMIT 10;
	SELECT * FROM t_zz_space_resources where zh_label LIKE "%南宁%" AND space_type = 101 LIMIT 10;
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-10-06-A09'
	SELECT * FROM t_zz_power_device WHERE related_site = 'SITE-8a388e0a2f7ce03d012f8be943c719db'

	SELECT * FROM t_zz_power_device LIMIT 10


	SELECT * FROM t_cfg_site LIMIT 10;
	SELECT * FROM t_cfg_precinct WHERE precinct_name = '北海测试数据区解放路电信楼'
	SELECT * FROM t_cfg_site WHERE site_id = '01-07-07-01-88'

	SELECT * FROM t_cfg_device WHERE device_id = '00161006000000024794'



	SELECT b.device_id,b.device_code,b.device_name,a.device_type,a.mete_code,a.mete_name,
	        a.alarm_explain,b.precinct_id,c.precinct_name,c.resource_code,d.dict_note
	        FROM t_cfg_mete a,t_cfg_device b,t_cfg_precinct c,t_cfg_dict d
	        WHERE a.device_type = b.device_type AND b.precinct_id = c.precinct_id AND a.mete_code = 008333 
	        AND b.device_type = d.dict_code AND d.col_name = 'device_type'
	        AND c.precinct_name = '百色测试数据to传输节点机房1';
	        
	        
	SELECT * FROM t_cfg_precinct WHERE precinct_id = "01-07-07-01-01"




	select distinct device.device_id deviceId from hidden_danger_rule hidden 
	inner join hidden_danger_rule_scope a1 on a1.rule_id = hidden.id 
	inner join t_cfg_device device ON 
		IF(a1.scope_id like "01-07%", device.precinct_id like concat(a1.scope_id, '%'), device.device_id = a1.scope_id) 
		where hidden.id = 47
		
		
	SELECT * FROM t_cfg_device WHERE device_code != 'NULL' and device_name = '机房环境' LIMIT 10;
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-05-02-35-01';
	SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002827781';
	SELECT * FROM t_cfg_device WHERE device_id = '00771006000002944984'



	SELECT * FROM t_cfg_device WHERE device_id = '00771006000002944984'
	SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000685505';
	SELECT * FROM t_zz_power_device where device_id = '00771006000002944984' LIMIT 10;
	SELECT * FROM t_zz_power_specialty WHERE device_id = '00771006000002944984' LIMIT 10;
	SELECT * FROM t_zz_power_specialty WHERE device_type = '机房环境' LIMIT 10;



	SELECT tp.precinct_name,tc.* FROM t_cfg_device tc
		JOIN t_cfg_precinct tp ON tc.precinct_id = tp.precinct_id
		JOIN t_zz_power_specialty tz ON tz.device_id = tc.device_id
		WHERE tc.precinct_id IN (SELECT left(precinct_id,14) FROM t_zz_space_resources)
		LIMIT 10;
		

		
	SELECT * FROM t_zz_space_resources WHERE precinct_id != 'NULL' LIMIT 100;


	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-01-01-04'
	SELECT device_id FROM t_cfg_device WHERE left(precinct_id,14) = '01-07-01-01-04' 

	SELECT * FROM t_zz_power_specialty WHERE device_id IN 
		(SELECT device_id FROM t_cfg_device WHERE left(precinct_id,14) = '01-07-01-01-04' )
		
		
	SELECT * FROM t_zz_space_resources WHERE precinct_id = '01-07-05-01-13'
	SELECT * FROM t_zz_power_specialty WHERE device_id = '00781006000002949708'


	SELECT * FROM t_zz_power_specialty LIMIT 10

	INSERT INTO `t_zz_power_specialty` (`id`, `res_code`, `zh_label`, `data_time`, `device_id`, `device_type_id`, `device_type`, `device_code`, `related_site`, `related_room`, `ralated_power_device`, `cell_voltage_level`, `total_monomers_number`, `rated_capacity`, `signal_output_rated_capacity`, `total_rack_match_modules`, `lifecycle_status`, `rated_power`, `device_subclass`, `start_time`, `product_name`, `vendor_id`, `power_device_id`, `power_site_level`, `gx_power_site_level`, `create_time`) VALUES																																													 (null, NULL, '温度过低告警', NULL, '00781006000002949708', 17, '艾默生温度1', '017012', '温度过低告警', 'SITE-202510231450', NULL, '', '6', '2', '20', NULL,NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '2025-10-23 14:50:54');

	INSERT INTO `t_zz_power_specialty` (`id`, `res_code`, `zh_label`, `data_time`, `device_id`, `device_type_id`, `device_type`, `device_code`, `related_site`, `related_room`, `lifecycle_status`, `rated_power`, `device_subclass`, `start_time`, `product_name`, `vendor_id`, `power_device_id`, `power_site_level`, `gx_power_site_level`, `estimated_retirement_time`, `create_time`, `sys_no_uuid`, `city_id`, `county_id`, `province_id`, `asset_code`, `device_brand`, `power_monitor_dev_name`, `power_room_type`, `serial_number`, `accept_date`, `factory_number`, `upper_device_name`, `upper_device_type`, `ralated_power_device`) VALUES (NULL, NULL, '{cls.mete_name}', NULL, NULL, {cls.device_type}, '{cls.device_name}', '{cls.device_code}', 'SITE-2967', 'ROOM-2968', NULL, NULL, '市电交流配电箱', '2014-10-17', NULL, NULL, NULL, NULL, NULL, '2029-10-17', '2024-09-27 08:06:22', '54001', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);






	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-05-01-02'
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-05-01-02-01'
	SELECT * FROM t_cfg_device where device_id = '00771006000002944984' LIMIT 10;
	SELECT * FROM t_cfg_device where device_id = '00771006000002943062' LIMIT 10;
	SELECT * FROM t_cfg_mete WHERE mete_code = 017012

	SELECT * FROM t_zz_space_resources where int_id = 'SITE-77003944' LIMIT 10;  # 空precinct_id
	SELECT * FROM t_zz_power_specialty WHERE device_type = '机房环境' AND related_site = 'SITE-77003944' 
		AND res_code = 'T_PHY_ROOM_ENVIRONMENT-abfead2df98f49089b8af9118429e12f'
		LIMIT 10;  # SITE-77003944  id为空
		
		
	SELECT * FROM t_zz_power_specialty WHERE device_code = '170200000024118'




	SELECT b.device_id,b.device_code,b.device_name,a.device_type,a.mete_code,a.mete_name,
	        a.alarm_explain,b.precinct_id,c.precinct_name,c.resource_code,d.dict_note
	        FROM 
			  	   t_cfg_mete a,
					t_cfg_device b,
					t_cfg_precinct c,
					t_cfg_dict d
	        WHERE 
					a.device_type = b.device_type AND 
					b.precinct_id = c.precinct_id AND 
					a.mete_code = 017012 AND 
					b.device_type = d.dict_code AND 
					d.col_name = 'device_type'AND c.precinct_name = '百色测试数据县古障2基站无线机房';
	        


	SELECT * FROM t_cfg_device WHERE device_id = '00771006000002943062';
	SELECT * FROM t_zz_power_specialty WHERE device_id = '00771006000003193777';
	SELECT * FROM t_cfg_device WHERE left(precinct_id,11) = '01-07-10-02';




	SELECT * FROM t_zz_power_specialty WHERE device_code = '170200000024118';
	SELECT * FROM t_zz_space_resources WHERE int_id = 'SITE-151232bdeb24468e8cca57c1ce90e22e';
	SELECT * FROM t_cfg_precinct where precinct_id = '01-07-10-02-06' ;
	SELECT * FROM t_cfg_device WHERE left(precinct_id,14) = '01-07-10-02-06' LIMIT 10;
	SELECT * FROM t_cfg_device WHERE device_id = '00541006000000106478';
	SELECT * FROM t_cfg_precinct where precinct_id = '01-07-21-01-01-03' ;

	SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000894721'



	# 00541006000000106478
	SELECT b.device_id,b.device_code,b.device_name,a.device_type,a.mete_code,a.mete_name,
	        a.alarm_explain,b.precinct_id,c.precinct_name,c.resource_code,d.dict_note
	        FROM t_cfg_mete a,t_cfg_device b,t_cfg_precinct c,t_cfg_dict d
	        WHERE a.device_type = b.device_type AND b.precinct_id = c.precinct_id AND a.mete_code = '017012'
	        AND b.device_type = d.dict_code AND d.col_name = 'device_type'
			  AND b.device_id = '00541006000000106478'
			  LIMIT 100;

	SELECT * FROM `t_zz_space_resources` LIMIT 10;
	SELECT * FROM `t_zz_space_resources` WHERE precinct_id = '01-07-21-01-01-03';
	SELECT * FROM `t_zz_power_specialty` where device_type = '机房环境' LIMIT 10;
	SELECT * FROM `t_zz_power_specialty` WHERE device_id = '00161006000000023366';


	SELECT * FROM `t_zz_power_specialty` WHERE device_id IN 
		(SELECT b.device_id
	        FROM t_cfg_mete a,t_cfg_device b,t_cfg_precinct c,t_cfg_dict d
	        WHERE a.device_type = b.device_type AND b.precinct_id = c.precinct_id AND a.mete_code = '017012'
	        AND b.device_type = d.dict_code AND d.col_name = 'device_type')

