SELECT res_code,COUNT(0) AS count_res
	FROM ods_zz_device_high_power t
	LEFT JOIN (
	SELECT int_id, zh_label
	FROM ods_zz_room t
	WHERE t.stat_time = '2025-07-23') r ON t.related_room = r.int_id
	LEFT JOIN (
	SELECT int_id, zh_label
	FROM ods_zz_site t
	WHERE t.stat_time =  '2025-07-23') s ON t.related_site = s.int_id
	WHERE t.stat_time = '2025-07-23'
	GROUP BY res_code
	ORDER BY count_res desc
	LIMIT 10;


	SELECT *
	FROM ods_zz_device_high_power t
	LEFT JOIN (
	SELECT int_id, zh_label,province_id
	FROM ods_zz_room t
	WHERE t.stat_time = '2025-07-23') r ON t.related_room = r.int_id
	LEFT JOIN (
	SELECT int_id, zh_label,province_id
	FROM ods_zz_site t
	WHERE t.stat_time =  '2025-07-23') s ON t.related_site = s.int_id
	WHERE t.stat_time = '2025-07-23' AND t.res_code = '134657057'


	SELECT *
	FROM ods_zz_device_high_power WHERE res_code = '134657057'
	
	SELECT *
	FROM ods_zz_device_high_power WHERE province_id = '330000' AND stat_time = '2025-07-23'and res_code = '134657057';

	SELECT * FROM ods_zz_room
		WHERE INT_id = '756245' AND stat_time = '2025-07-23';
	
	SELECT * FROM ods_zz_site
		WHERE INT_id = '755393' AND stat_time = '2025-07-23';
	
	
	
	SELECT COUNT(0)
		FROM ods_zz_device_high_power t
		LEFT JOIN (
		SELECT int_id, zh_label
		FROM ods_zz_room t
		WHERE t.stat_time = '2025-07-23' AND t.province_id IN ('330000')) r ON t.related_room = r.int_id
		LEFT JOIN (
		SELECT int_id, zh_label
		FROM ods_zz_site t
		WHERE t.stat_time = '2025-07-23' AND t.province_id IN ('330000')) s ON t.related_site = s.int_id
		WHERE t.stat_time = '2025-07-23' AND t.province_id IN ('330000')
	
	
	
	
	
SELECT t.int_id,COUNT(1) AS count_int
	FROM ods_zz_room t
	LEFT JOIN (
	SELECT int_id, zh_label
	FROM ods_zz_site t
	WHERE t.stat_time = '2025-07-23') s ON t.related_site = s.int_id
	WHERE t.stat_time = '2025-07-23'	
	GROUP BY t.int_id 
	ORDER BY count_int DESC
	LIMIT 10;


	# 问题：到底哪边才是对的呢，怎么去判断两个表，哪边的省市区编码才是正确的呢
	SELECT *
		FROM ods_zz_room t
			LEFT JOIN (
			SELECT int_id, zh_label
			FROM ods_zz_site t
			WHERE t.stat_time = '2025-07-23') s ON t.related_site = s.int_id
		WHERE t.stat_time = '2025-07-23' AND t.int_id = '305158'
		LIMIT 10;
		
		SELECT int_id,related_site
		FROM ods_zz_room  WHERE int_id = '305158' and stat_time = '2025-07-23';	
		
		SELECT *
		FROM ods_zz_room  WHERE int_id = '305158' and stat_time = '2025-07-23';	
				
		SELECT *
		FROM ods_zz_site  WHERE int_id IN ('264370','304760','304681') and stat_time = '2025-07-23';	
		
		
		
		
		







SELECT COUNT(0)
FROM ods_zz_site_property t
	LEFT JOIN ods_t_cfg_precinct_v p ON p.precinct_name = t.power_monitoring_site_name AND p.precinct_kind = 2 AND p.isdel = 0
	LEFT JOIN (
	SELECT int_id, zh_label, business_type, lifecycle_status, cutin_date
	FROM ods_zz_site t
	WHERE t.stat_time = '2025-07-23') s ON t.zh_label = s.int_id
	WHERE t.stat_time = '2025-07-23';
	
	SELECT COUNT(1) FROM ods_zz_site_property WHERE stat_time = '2025-07-23';
	
	SELECT COUNT(1) FROM ods_t_cfg_precinct_v LIMIT 10;
	
	SELECT t.res_code,COUNT(0) AS count_res
		FROM ods_zz_site_property t
		LEFT JOIN ods_t_cfg_precinct_v p ON p.precinct_name = t.power_monitoring_site_name AND p.precinct_kind = 2 AND p.isdel = 0
		LEFT JOIN (
		SELECT int_id, zh_label, business_type, lifecycle_status, cutin_date
		FROM ods_zz_site t
		WHERE t.stat_time = '2025-07-23') s ON t.zh_label = s.int_id
		WHERE t.stat_time = '2025-07-23'
		GROUP BY t.res_code
		ORDER BY count_res DESC 
		LIMIT 10;
		
		SELECT t.res_code
			FROM ods_zz_site_property t
			LEFT JOIN ods_t_cfg_precinct_v p ON p.precinct_name = t.power_monitoring_site_name AND p.precinct_kind = 2 AND p.isdel = 0
			LEFT JOIN (
			SELECT int_id, zh_label, business_type, lifecycle_status, cutin_date
			FROM ods_zz_site t
			WHERE t.stat_time = '2025-07-23') s ON t.zh_label = s.int_id
			WHERE t.stat_time = '2025-07-23'
			AND res_code = '801072025091908';
		
		SELECT * FROM ods_zz_site_property WHERE res_code = '801072025091908';
		
		SELECT COUNT(1) FROM ods_zz_site_property WHERE stat_time = '2025-07-23';
		
		SELECT t.zh_label
			FROM ods_zz_site_property t
			LEFT JOIN ods_t_cfg_precinct_v p ON p.precinct_name = t.power_monitoring_site_name AND p.precinct_kind = 2 AND p.isdel = 0
			LEFT JOIN (
			SELECT int_id, zh_label, business_type, lifecycle_status, cutin_date
			FROM ods_zz_site t
			WHERE t.stat_time = '2025-07-23') s ON t.zh_label = s.int_id
			WHERE t.stat_time = '2025-07-23'
			GROUP BY t.zh_label
			
			LIMIT 10;	
	
	
	SELECT p.precinct_id AS sitePrecinctId, IFNULL(s.zh_label, t.zh_label) zh_label, s.business_type, s.lifecycle_status, s.cutin_date, t.collect_time, t.res_code, t.province_id, t.city_id, t.county_id, t.batch_num, t.power_site_level, t.mains_backup_method, t.power_is_substations, t.mains_voltage_level, t.mains_nature, t.power_monitoring_site_name, t.total_mains_number, t.mains_capacity, t.mains_configuration_level, t.total_tank_number, t.tatal_tank_volume, t.property_unit, t.power_supply, t.is_attach_idc_room, t.design_pue, t.water_cooling_conf, t.is_cold_storage_install, t.cold_storage_time
	FROM ods_zz_site_property t
		
		LEFT JOIN ods_t_cfg_precinct_v p ON p.precinct_name = t.power_monitoring_site_name AND p.precinct_kind = 2 AND p.isdel = 0
		
		LEFT JOIN (
		SELECT int_id, zh_label, business_type, lifecycle_status, cutin_date
		FROM ods_zz_site t
		WHERE t.stat_time = '2025-07-23') s ON t.zh_label = s.int_id
		WHERE t.stat_time = '2025-07-23'
	ORDER BY county_id, res_code ASC
	LIMIT 20