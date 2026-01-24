# 站点机房筛选(需要选择接入的设备)
	SELECT * FROM m_room WHERE siteid = '2028';

	SELECT * FROM t_cfg_precinct WHERE precinct_name LIKE "贵1%";
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-01-11-01-01';
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-01-11-01-04';

	# 获取用电关系(机柜和机柜列)
	SELECT * FROM energy_cabinet WHERE precinct_id = '01-08-08-01-11-01-04';
	SELECT * FROM energy_cabinet_column WHERE precinct_id = '01-08-08-01-11-01-04';
	SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id = '2c86a83392544c56919e0df9e257082d';
	SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id ='2589b780780d43419c0c4eac5af99d55';
	SELECT * FROM energy_cabinet_mete;


	# 获取mpp对应（机房的映射，设备的映射）
	SELECT precinct_id,precinct_name,dim_spatial_id FROM t_cfg_precinct WHERE precinct_id = '01-08-08-01-11-01-01';
	SELECT device_id,device_name,precinct_id,device_model,device_type,dim_device_id FROM t_cfg_device WHERE device_id = '00751006000005648551';	
	SELECT device_id,device_name,precinct_id,device_model,device_type,dim_device_id FROM t_cfg_device WHERE device_id = '00751006000005648487';

	
	# 获取mpp数据
	SELECT * FROM fact_dwd_signal_value WHERE device_id = '10017242'  AND left(signal_start_time,10) like '2025-11-24%'


	# 获取机柜下配置数据(电能/功率)
	SELECT * FROM fact_dwd_signal_value WHERE device_id = '10017281'  AND left(signal_start_time,10) IN ('2025-11-25') AND signal_meta_code IN ('092316','092334');
	SELECT * FROM fact_dwd_signal_value WHERE device_id = '10017281'  AND left(signal_start_time,10) IN ('2025-11-25') AND signal_meta_code IN ('092309','092330');

	
	# 获取机柜列下配置数据(电能/功率)
	SELECT * FROM fact_dwd_signal_value WHERE device_id = '10017242'  AND left(signal_start_time,10) IN ('2025-11-25') AND signal_meta_code IN ('001329','001328');
	SELECT * FROM fact_dwd_signal_value WHERE device_id = '10017242'  AND left(signal_start_time,10) IN ('2025-11-25') AND signal_meta_code IN ('001311','001312');	
	
	
	
	
	# 获取机房配置数据
		# 站点配置
		SELECT * FROM energy_formula_config WHERE precinct_id = '01-08-08-01-11';
		# 楼栋配置
		SELECT * FROM energy_formula_config WHERE precinct_id = '01-08-08-01-11-01';
		# 机房配置
		SELECT * FROM energy_formula_config WHERE precinct_id = '01-08-08-01-11-01-04';




	# 结果表
	SELECT * FROM energy_cabinet_daily_report WHERE cabinet_id = '2c86a83392544c56919e0df9e257082d';
	SELECT * FROM energy_cabinet_column_daily_report WHERE cabinet_column_id = '2589b780780d43419c0c4eac5af99d55';



	SELECT * FROM energy_day_audit_summary LIMIT 10;


	
	
	
	
	
	
	
	
	
	
	
	
	# 补充sql
		
		# 机房（用电关系-主要） 手工刷新
		SELECT 
			a.precinct_id AS precinctId,
			b.site_type AS siteType,
			a.precinct_kind AS precinctKind,
			c.time AS TIME,
			c.electric_sum AS electricSum,
			c.device_sum AS deviceSum,
			c.air_sum AS airSum,
			c.city_ele_sum AS cityEleSum,
			c.electric_sum_status AS electricSumStatus,
			c.pue AS pue,
			d.design_pue AS designPue,
			c.electricity_offset AS electricityOffset,
			c.engineering_status AS engineeringStatus,
			c.electric_sum_update_status AS electricSumUpdateStatus,
			c.device_sum_update_status AS deviceSumUpdateStatus,
			c.air_sum_update_status AS airSumUpdateStatus
		FROM t_cfg_precinct AS a
		JOIN t_cfg_site AS b ON b.site_id = a.precinct_id
			LEFT JOIN t_cfg_design_property AS d ON d.precinct_id = a.precinct_id
			LEFT JOIN (
				SELECT 
					t.precinct_id,
					'2025-11-25' AS TIME,
					a.capacity_estimates AS capacity_estimates, CONVERT(b.electric_sum, DECIMAL(18, 3)) AS electric_sum, CONVERT(b.device_sum, DECIMAL(18, 3)) AS device_sum, CONVERT(b.air_sum, DECIMAL(18, 3)) AS air_sum, CONVERT(c.municipal_electricity, DECIMAL(18, 3)) AS city_ele_sum, CASE WHEN b.electric_sum >= IFNULL(b.device_sum, 0) + IFNULL(b.air_sum, 0) - 0.000001 THEN 0 ELSE 1 END AS electric_sum_status, CONVERT(b.electric_sum / b.device_sum, DECIMAL(18, 3)) AS pue, CONVERT(
					(b.device_sum - IF(IFNULL(a.capacity_estimates, '') = '', NULL, IFNULL(a.capacity_estimates, ''))) 
					/ IF(IFNULL(a.capacity_estimates, '') = '', NULL, IFNULL(a.capacity_estimates, '')) * 100, DECIMAL(18, 3)
					) AS electricity_offset,
					b.is_del AS engineering_status,
					b.electric_sum_update_status AS electric_sum_update_status,
					b.device_sum_update_status AS device_sum_update_status,
					b.air_sum_update_status AS air_sum_update_status
				FROM t_cfg_precinct AS t
					LEFT JOIN energy_audit_estimates AS a ON a.audit_date = '2025-11-25' AND a.precinct_id = t.precinct_id
					LEFT JOIN energy_station_building_day AS b ON b.time = '2025-11-25' AND b.precinct_id = t.precinct_id
					LEFT JOIN energy_station_building_item_day AS c ON c.time = '2025-11-25' AND c.precinct_id = t.precinct_id
				WHERE t.isdel = '0' AND t.precinct_kind IN (2, 3)
				GROUP BY t.precinct_id
				) AS c ON c.precinct_id = a.precinct_id
			WHERE a.isdel = '0' AND a.precinct_kind IN (2, 3) AND a.precinct_id LIKE CONCAT('01-08-08-01', '%') AND a.precinct_id LIKE CONCAT('01-08-08-01-11', '%');






