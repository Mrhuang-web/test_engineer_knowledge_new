# 映射关系
	SELECT * FROM zz_data_sync_info;
	SELECT * FROM zz_to_rm_rm_area_dc;
	SELECT * FROM zz_to_rm_rm_area_site;
	SELECT * FROM zz_to_rm_rm_area_room;
	SELECT * FROM zz_to_rm_rm_device;


# 检查已有的power_id数量
	SELECT * FROM t_cfg_device WHERE power_device_id IS NOT NULL;
	

# 查看已经建立的站点（和未建立站点的）
	SELECT * FROM zz_to_rm_rm_area_site;
	
	# 检测其他站点未关联的
	SELECT device.device_type,device.device_name,device.precinct_id FROM t_cfg_device device 
		JOIN t_cfg_precinct  room ON device.precinct_id = room.precinct_id
		JOIN t_cfg_precinct  site ON room.up_precinct_id = site.precinct_id AND  site.precinct_id NOT IN (SELECT precinct_id FROM zz_to_rm_rm_area_site)
	WHERE
		device.power_device_id IS NULL  LIMIT 100;



	# 检测楼栋未关联的
	SELECT device.device_type,device.device_name,device.precinct_id FROM t_cfg_device device 
		left JOIN t_cfg_precinct  room ON device.precinct_id = room.precinct_id
		left JOIN t_cfg_precinct  building ON room.precinct_id = building.precinct_id
		left JOIN t_cfg_precinct  site ON building.up_precinct_id = site.precinct_id AND  site.precinct_id NOT IN (SELECT precinct_id FROM zz_to_rm_rm_area_site)
	WHERE
		device.power_device_id IS NULL	LIMIT 100;



	# 检测其他站点关联的，是否有存在的power_device_id
	SELECT device.device_type,device.device_name,device.precinct_id FROM t_cfg_device device 
		JOIN t_cfg_precinct  room ON device.precinct_id = room.precinct_id
		JOIN t_cfg_precinct  site ON room.up_precinct_id = site.precinct_id AND  site.precinct_id IN (SELECT precinct_id FROM zz_to_rm_rm_area_site)
		WHERE
			device.power_device_id IS NOT NULL;
		
	
	# 检测站点关联的，是否有存在的power_device_id
	SELECT building.precinct_id,device.device_type,device.device_name,device.precinct_id FROM t_cfg_device device 
		JOIN t_cfg_precinct  room ON device.precinct_id = room.precinct_id
		JOIN t_cfg_precinct  building ON room.up_precinct_id = building.precinct_id AND building.precinct_id IN (SELECT precinct_id FROM zz_to_rm_rm_area_site)
		WHERE
			device.power_device_id IS NULL
			GROUP BY device.precinct_id LIMIT 100;
	
	
	# 检测楼栋是否有匹配的设备，站点是关联的
	SELECT * FROM zz_to_rm_rm_device WHERE precinct_id NOT IN (
		SELECT device.precinct_id FROM t_cfg_device device 
			left JOIN t_cfg_precinct  room ON device.precinct_id = room.precinct_id
			left JOIN t_cfg_precinct  building ON room.precinct_id = building.precinct_id
			left JOIN t_cfg_precinct  site ON building.up_precinct_id = site.precinct_id AND  site.precinct_id IN (SELECT precinct_id FROM zz_to_rm_rm_area_site)
			WHERE
				device.power_device_id IS NULL
				GROUP BY device.precinct_id
	);
	
	
	


# 随机找几个未关联的站点下的设备，进行匹配（类型要对应下）
	
	SELECT * FROM t_cfg_dict WHERE col_name = 'device_kind';
	SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
	
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-38-12-10-01-01';
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-38-12-10-01-01' and device_type = '1';			# 站点未绑定的




	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-17-06-11-01-01';
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-17-06-11-01-01' and device_type = '1';			# 站点绑定的	
	
	
	SELECT * FROM t_cfg_site WHERE precinct_id = '01-17-06-11-01';
	SELECT * FROM t_cfg_site WHERE site_id = '01-17-06-11-01';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-17-06-11-01-01';
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-17-06-11-01-01' and device_type = '2';			# 站点绑定的  低压交流配电
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-17-06-11-01-01' and device_type = '1';			# 站点绑定的  高压配电
	
	
	
	
	
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-05-03-01-19';
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-01-05-03-01-19' and device_type = '3';			# 站点绑定的  变压器
	
	
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-38';													# 210000
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-38-10';												# 210500
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-38-10-05-01-03';
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-38-10-05-01-03' and device_type = '2';			# 站点绑定的  低压交流配电
	
	
	
	SELECT * FROM t_cfg_device WHERE device_id = '00531006000004590958';
	SELECT * FROM t_cfg_device WHERE device_id = '00531006000004587996';
	SELECT * FROM building_area;
	
	
	# 以这个为例，都没匹配上，怎么回事
	SELECT * FROM zz_to_rm_rm_area_site WHERE precinct_id = '01-17-06-11-01';	
	
	SELECT * FROM zz_to_rm_rm_area_site WHERE precinct_id = '01-38-10-05-01';
	SELECT * FROM zz_to_rm_rm_area_site WHERE precinct_id = '01-32-05-05-01';	
	
	
	SELECT * FROM zz_to_rm_rm_area_site WHERE precinct_id = '01-32-05-05-01';	
	
	
	
	
	# 举例说明:
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-17-06-11-01-01' and device_type = '2';			# 站点绑定的  低压交流配电
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-17-06-11-01-01' and device_type = '1';			# 站点绑定的  高压配电
	SELECT * FROM zz_to_rm_rm_area_site WHERE precinct_id = '01-17-06-11-01';
	