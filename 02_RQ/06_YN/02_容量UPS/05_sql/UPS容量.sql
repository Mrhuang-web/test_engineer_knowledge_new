ups
	00531006000005759877
	01-32-01-02-01-03，四楼电力室1#艾默生(EMERSON UPS)(NXR)
	# 查找设备（可以直接在设备中查找已经有关联的）
	SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
	SELECT * FROM t_cfg_device WHERE device_name = '四楼电力室1#艾默生(EMERSON UPS)(NXR)';
	SELECT * FROM t_cfg_device WHERE device_id IN ('00531006000005759877','37261006000000079739');
	SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000010762';
	
	
	
	
	# 删除曾经已经产生的数据
	SELECT * FROM device_es_mete WHERE device_id IN ('00531006000005759877','37261006000000079739');
	DELETE FROM device_es_mete WHERE device_id IN ('00531006000005759877','37261006000000079739');
	
	
	# 建立关联设备并准备数据（三相输出电流计算逻辑）   ---- 设备与系统关联
	SELECT * FROM t_cfg_devicesys_detail WHERE sub_id IN ('00531006000005759877','37261006000000079739');
	SELECT * FROM t_cfg_devicesys_detail WHERE devicesys_id IN ('da8ed141-a97b-4b28-aa2b-0127ea952e5e');
	INSERT INTO  t_cfg_devicesys_detail (devicesys_id,sub_id,scc_index,cell_index,cell_num) VALUE ('da8ed141-a97b-4b28-aa2b-0127ea952e5e','37261006000000079739',NULL,NULL,NULL);
	
	# ups定义
	SELECT * FROM t_cfg_devicesys where devicesys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';	
	
	
	# 设备系统所属precinct_id要存在precinct表中
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01-03';
	SELECT * FROM t_cfg_precinct WHERE precinct_name = 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)';


	# 容量历史数据
	SELECT * from device_es_mete LIMIT 10;
	SELECT * from device_es_mete WHERE sys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';
	
	
	# 容量实时数据
	SELECT * from t_current_capacity;
	SELECT * from t_current_capacity WHERE sys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';
	




	# 组合查询现有的（已经关联的设备系统，设备）
	SELECT
		a.device_id,
		a.rated_power,
		a.load_power,
		a.device_type,
		c.devicesys_id,
		c.work_style,
		a.sub_device_type,
		a.rectifierModuleNumber,
		a.singleModuleRatedCurrent,
		c.ktRatio,
		c.up_id,
		d.precinct_name,
		c.devicesys_name,
		a.device_name,
		c.pe_entity_type,
		c.current_ele,
		d.precinct_id
	from t_cfg_device a
	LEFT JOIN t_cfg_devicesys_detail b ON b.sub_id=a.device_id
	LEFT JOIN t_cfg_devicesys c ON c.devicesys_id=b.devicesys_id
	LEFT JOIN t_cfg_precinct d ON d.precinct_id=a.precinct_id
	WHERE  a.isdel='0'
		and a.device_type = 8;



	
	
	
	SELECT province.precinct_name,city.precinct_name,county.precinct_name,site.precinct_name,building.precinct_name FROM t_cfg_precinct building
		JOIN  t_cfg_precinct site ON building.up_precinct_id = site.precinct_id
		JOIN t_cfg_precinct county ON site.up_precinct_id = county.precinct_id
		JOIN t_cfg_precinct city ON county.up_precinct_id = city.precinct_id
		JOIN t_cfg_precinct province ON county.up_precinct_id = province.precinct_id
			WHERE building.precinct_id = '01-32-01-02-01';
	
	
	
	
	
	
	
	
	
	
# 已用造数（一个系统，多个设备）
	
	# 查找设备（可以直接在设备中查找已经有关联的）
	SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
	SELECT * FROM t_cfg_device WHERE device_name = '四楼电力室1#艾默生(EMERSON UPS)(NXR)';
	SELECT * FROM t_cfg_device WHERE device_id IN ('00531006000005759877','37261006000000079739');
	SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000010762';
	# 删除曾经已经产生的数据
	SELECT * FROM device_es_mete WHERE device_id IN ('00531006000005759877','37261006000000079739');
	DELETE FROM device_es_mete WHERE device_id IN ('00531006000005759877','37261006000000079739');
	# 建立关联设备并准备数据（三相输出电流计算逻辑）   ---- 设备与系统关联
	SELECT * FROM t_cfg_devicesys_detail WHERE sub_id IN ('00531006000005759877','37261006000000079739');
	SELECT * FROM t_cfg_devicesys_detail WHERE devicesys_id IN ('da8ed141-a97b-4b28-aa2b-0127ea952e5e');
	INSERT INTO  t_cfg_devicesys_detail (devicesys_id,sub_id,scc_index,cell_index,cell_num) VALUE ('da8ed141-a97b-4b28-aa2b-0127ea952e5e','37261006000000079739',NULL,NULL,NULL);
	# ups定义
	SELECT * FROM t_cfg_devicesys where devicesys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';	
	# 设备系统所属precinct_id要存在precinct表中
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01-03';
	SELECT * FROM t_cfg_precinct WHERE precinct_name = 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)';


	# 容量历史数据
	SELECT * from device_es_mete LIMIT 10;
	SELECT * from device_es_mete WHERE sys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';
	
	
	# 容量实时数据
	SELECT * from t_current_capacity;
	SELECT * from t_current_capacity WHERE sys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	



# 日志
	SELECT * from early_alerts; 
	
	
	where 
		alert_create_time='2025-11-27' 
		and device_type in ('6','8', '87') 
		and precinct_id like CONCAT('01-02','%') and precinct_id like CONCAT('01-02','%');


	SELECT MAX(
		LEFT (m.es_date, 10)) data_time, c.devicesys_id AS sys_id, c.devicesys_name AS sys_name, d1.precinct_name AS province_name, d2.precinct_name AS city_name, IFNULL(d4.precinct_name,d3.precinct_name) AS floor_name, IFNULL(d4.precinct_id,d3.precinct_id) AS floor_id, MAX(m.load_per) AS load_per, c.devicesys_desc AS remark, a.device_type, IFNULL(s3.site_type,s.site_type) AS site_type, CONCAT(tcd.dict_note,'??') AS device_type_name, IFNULL(m.rate, a.rated_power) rate
	FROM t_cfg_device a
		LEFT JOIN device_es_mete m ON m.device_id = a.device_id AND m.is_valida = 'Y'
		JOIN t_cfg_devicesys_detail b ON b.sub_id = a.device_id
		JOIN t_cfg_devicesys c ON c.devicesys_id = b.devicesys_id
		LEFT JOIN t_cfg_precinct d ON d.precinct_id = a.precinct_id
		LEFT JOIN t_cfg_precinct AS d1 ON d1.precinct_id = LEFT (d.precinct_id, 5)
		LEFT JOIN t_cfg_precinct AS d2 ON d2.precinct_id = LEFT (d.precinct_id, 8)
		LEFT JOIN t_cfg_precinct AS d3 ON d3.precinct_id = d.up_precinct_id
		LEFT JOIN t_cfg_precinct AS d4 ON d4.precinct_id = d3.up_precinct_id AND d4.precinct_kind = 2
		LEFT JOIN t_cfg_site s ON s.site_id = d.up_precinct_id
		LEFT JOIN t_cfg_site s3 ON s3.site_id = d3.up_precinct_id
		LEFT JOIN t_cfg_dict tcd ON a.device_type = tcd.dict_code AND col_name = 'device_type'
	WHERE a.rated_power >= '0.000' AND a.device_type in (6,8) AND a.isdel='0'
		GROUP BY c.devicesys_id;
	
	
	
	
	SELECT MAX(
		LEFT (m.es_date, 10)) data_time, c.devicesys_id AS sys_id, c.devicesys_name AS sys_name, d1.precinct_name AS province_name, d2.precinct_name AS city_name, IFNULL(d4.precinct_name,d3.precinct_name) AS floor_name, IFNULL(d4.precinct_id,d3.precinct_id) AS floor_id, MAX(m.load_per) AS load_per, c.devicesys_desc AS remark, a.device_type, IFNULL(s3.site_type,s.site_type) AS site_type, CONCAT(tcd.dict_note,'??') AS device_type_name, IFNULL(m.rate, a.rated_power) rate
	FROM t_cfg_device a
		LEFT JOIN device_es_mete m ON m.device_id = a.device_id AND m.is_valida = 'Y'
		JOIN t_cfg_gyzlsys_detail g1 ON g1.sub_id = a.device_id AND g1.item_type = 2
		JOIN t_cfg_gyzlsys_detail g2 ON g2.sub_id = g1.devicesys_id AND g2.item_type = 1
		JOIN t_cfg_gyzlsys c ON c.devicesys_id = g2.devicesys_id
		LEFT JOIN t_cfg_precinct d ON d.precinct_id = a.precinct_id
		LEFT JOIN t_cfg_precinct AS d1 ON d1.precinct_id =
		LEFT (d.precinct_id, 5)
		LEFT JOIN t_cfg_precinct AS d2 ON d2.precinct_id =
		LEFT (d.precinct_id, 8)
		LEFT JOIN t_cfg_precinct AS d3 ON d3.precinct_id = d.up_precinct_id
		LEFT JOIN t_cfg_precinct AS d4 ON d4.precinct_id = d3.up_precinct_id AND d4.precinct_kind = 2
		LEFT JOIN t_cfg_site s ON s.site_id = d.up_precinct_id
		LEFT JOIN t_cfg_site s3 ON s3.site_id = d3.up_precinct_id
		LEFT JOIN t_cfg_dict tcd ON a.device_type = tcd.dict_code AND col_name = 'device_type'
	WHERE a.rated_power >= '0.000' AND a.device_type = 87 AND a.isdel='0'
		GROUP BY c.devicesys_id;
	
	
	SELECT * from t_current_capacity where device_type IN ( 6 , 8 , 87 );
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	SELECT * FROM t_cfg_device WHERE device_id IN ('00531006000003792726','00531006000003792725');
	SELECT * FROM t_cfg_device WHERE device_id = '00531006000005759877';
	
	
