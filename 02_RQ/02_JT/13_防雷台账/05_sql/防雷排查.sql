# 防雷安全台账
	SELECT * from lightning_manage_province;



# 查看全部
	SELECT * from lightning_manage_checkhd;
	SELECT * from lightning_manage_spotcheck;
	SELECT * from lightning_manage_thunderstatistics;

# 自查隐患
	SELECT * from lightning_manage_checkhd;
	SELECT * from lightning_manage_checkhd WHERE hd_detail = '11' AND telephone = '14523542331';
	DELETE FROM lightning_manage_checkhd;
	INSERT INTO `lightning_manage_checkhd` (`id`, `site_id`, `month`, `hd_detail`, `change_status`, `find_time`, `plan_finish_time`, `people1`, `people2`, `telephone`, `remark`, `update`, `is_system`) 
	VALUES ('01-02-08_mLHfJXiovSUWGNyI=2025-11=6512bd43d9caa6e02c990b0a82652dcc', '01-02-08_mLHfJXiovSUWGNyI', '2025-11', '11', 1, '2025-11', '2025-11', '11', '11', '14523542331', '', '2025-11-26 23:43:57', 2);
	
	UPDATE lightning_manage_checkhd SET 
	

# 检查机构抽查
	SELECT * from lightning_manage_spotcheck;
	SELECT * from lightning_manage_spotcheck WHERE hd_detail = '11';
	DELETE FROM lightning_manage_spotcheck;
	INSERT INTO `lightning_manage_spotcheck` (`id`, `site_id`, `month`, `hd_detail`, `change_status`, `find_time`, `plan_finish_time`, `people1`, `people2`, `telephone`, `mechanism_name`, `remark`, `update`, `is_system`) 
	VALUES ('01-02-08-01-01=2025-11=6512bd43d9caa6e02c990b0a82652dcb', '01-02-08-01-01', '2025-11', '11', 1, '2025-11', '2025-11', '123', '123', '13333444455', '123', '11', '2025-11-27 00:35:01', 1);

	
# 雷电灾害	
	SELECT * from lightning_manage_thunderstatistics;
	SELECT * from lightning_manage_thunderstatistics WHERE LEFT(`update`,4) = '2025';	
	DELETE FROM lightning_manage_thunderstatistics;
	INSERT INTO `lightning_manage_thunderstatistics` (`id`, `site_id`, `city_id`, `place_id`, `month`, `find_time`, `place`, `content`, `loss`, `money`, `reason`, `measures`, `is_change`, `finish_time`, `thunder_time`, `remark`, `update`, `is_system`) 
	VALUES ('01-01-03-01-01=2022-07-05', '01-01-03-01-01', '01-01-03', '', '2022-07-05', '2022-06-16', '福田区', '161616', '171717', 88.00, '191919', '101010', 1, '2022-07', 1, '备注备注', '2025-07-05 17:45:51', 1);


# 其余表
	SELECT * from lightning_manage_precinct;   								# 站点映射表
	SELECT * from lightning_manage_province_managesystem_list;
	SELECT * from lightning_manage_thunderreport;
	SELECT * from lightning_manage_thunderreport_detal;
