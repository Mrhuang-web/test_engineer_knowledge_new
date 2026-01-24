SELECT * FROM zz_data_sync_info;

SELECT * FROM dim_zz_data_sync_info;

SELECT * FROM ods_zz_site LIMIT 10
	SELECT COUNT(1) FROM ods_zz_site; 
	SELECT COUNT(1) FROM ods_zz_site  WHERE stat_time = '20250723';         # 8246520
	
	SELECT province_id,COUNT(1) FROM ods_zz_site WHERE stat_time = '20250723' GROUP BY province_id; 
	SELECT COUNT(1) FROM ods_zz_site  WHERE batch_num = '20250723' AND province_id = '420000' AND city_id = '421100'
	AND county_id = '421181' AND site_type = '汇聚站点'; 
	SELECT COUNT(1) FROM ods_zz_site  WHERE stat_time = '2025-07-23' AND province_id = '420000'; 
	
	SELECT * FROM 
	SELECT
    CASE
        WHEN batch_num = '20250723' AND stat_time <> '2025-07-23' THEN 'batch_num=20250723 但 stat_time≠2025-07-23'
        WHEN batch_num <> '20250723' AND stat_time = '2025-07-23' THEN 'stat_time=2025-07-23 但 batch_num≠20250723'
    END AS reason,
    ods_zz_site.*
	FROM ods_zz_site
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23')
		GROUP BY reason;
	
	-- 换成你表里的主键列
	SELECT  *
		FROM ods_zz_site
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23');
	SELECT * FROM ods_zz_site WHERE int_id = '441100000000077631092704';
	
	DELETE FROM  ods_zz_site  WHERE int_id = '441100000000077631092704';
	
	SELECT province_id,COUNT(1) FROM ods_zz_site where province_id = '440000' AND stat_time = '20250723' GROUP BY province_id;     # 1792665
	SELECT city_id,COUNT(1) FROM ods_zz_site where city_id = '440500' AND stat_time = '20250723' GROUP BY city_id;  # 55146
		INSERT INTO `ods_zz_site` (`stat_time`, `int_id`, `project_code`, `uuid`, `tele_cmn_serv_pro_name`, `pms_address_code`, `project_name`, `business_type`, `area_type`, `cutin_date`, `batch_num`, `collect_time`, `irms_province_code`, `related_dc`, `lifecycle_status`, `qualitor`, `floor_number`, `use_corp`, `standardaddress`, `village_pass_serv_code`, `if_village_pass_serv`, `village_pass_serv_name`, `alias_name`, `china_tower_station_code`, `latitude`, `province_id`, `city_id`, `county_id`, `longitude`, `if_tele_cmn_serv`, `tele_cmn_serv_pro_code`, `is_headquarters_used`, `zh_label`, `site_type`, `address`, `flow_time`) VALUES ('2025-07-23', '441100000000077631092704', NULL, NULL, NULL, NULL, NULL, '家客集客', '县城', '2025-01-03', '20250723', '2025-07-23 14:27:54', 'GD', NULL, '在网', 'linbin6', '1', '中国移动', '4148743088', NULL, '否', NULL, NULL, NULL, '23.5338072746077', '440000', '440500', '440515', '116.815117351405', '否', NULL, '否', '汕头澄海区汕头益鑫燃气分布式能源有限公司', '用户站点', '汕头市澄海区溪南镇324国道外蚁村汕头益鑫燃气分布式能源有限公司', '2025-12-31 10:51:45');




SELECT COUNT(1) FROM ods_zz_room WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_room WHERE stat_time = '20250723';
	
	SELECT COUNT(1) FROM ods_zz_room WHERE stat_time = '20250723'
	SELECT province_id,COUNT(1) FROM ods_zz_room WHERE stat_time = '20250723' GROUP BY province_id; 

	SELECT count(0) FROM ods_zz_room t 
	LEFT JOIN (SELECT int_id, zh_label FROM ods_zz_site t WHERE t.stat_time = '2025-07-23') s 
		ON t.related_site = s.int_id 
	WHERE t.stat_time = '2025-07-23'
	LIMIT 10
		
		SELECT  COUNT(1)
		FROM ods_zz_room
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23');
		
		SELECT  *
		FROM ods_zz_room
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23');



SELECT COUNT(1) FROM ods_zz_room_property WHERE stat_time = '20250723';

		SELECT  COUNT(1)
		FROM ods_zz_room_property
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23');

SELECT COUNT(1) FROM ods_zz_site_property WHERE stat_time = '20250723';
		SELECT  COUNT(1)
		FROM ods_zz_site_property
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23');



SELECT COUNT(1) FROM ods_zz_device_transform WHERE stat_time = '20250723';
		SELECT  COUNT(1)
		FROM ods_zz_device_transform
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23');
		
SELECT COUNT(1) FROM ods_zz_device_transform_device WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_high_distribution WHERE stat_time = '20250723';


SELECT COUNT(1) FROM ods_zz_device_high_power WHERE stat_time = '20250723';
	SELECT province_id,COUNT(1) FROM ods_zz_device_high_power WHERE stat_time = '20250723' GROUP BY province_id
	SELECT stat_time,COUNT(1) FROM ods_zz_device_high_power GROUP BY stat_time
	SELECT COUNT(*) FROM ods_zz_device_high_power 
	
	
	
SELECT COUNT(1) FROM ods_zz_device_high_dc_distribution WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_low_ac_distribution WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_power_generation WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_switch_power WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_low_dc_distribution WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_ups WHERE stat_time = '20251210' AND province_id = '450000';
SELECT COUNT(1) FROM ods_zz_device_battery WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_air WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_energy_save WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_power_monitor WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_smart_meter WHERE stat_time = '20250723';
SELECT COUNT(1) FROM ods_zz_device_other WHERE stat_time = '20250723';


SELECT COUNT(1) FROM ods_zz_link_pe_in WHERE stat_time = '20250723';
SELECT COUNT(1) FROM zz_irms_dc_site_rackrate;



SELECT COUNT(1) FROM ods_zz_irms_site_map WHERE batch_num = '20250723';
		SELECT  COUNT(1)
		FROM ods_zz_irms_site_map
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23');
		
SELECT COUNT(1) FROM ods_zz_irms_dc_map WHERE batch_num = '20250723';
		SELECT  COUNT(1)
		FROM ods_zz_irms_dc_map
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23');
		
		
SELECT COUNT(1) FROM ods_zz_irms_rom_map WHERE batch_num = '20250723';
		SELECT  COUNT(1)
		FROM ods_zz_irms_rom_map
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23');
		
		SELECT  *
		FROM ods_zz_irms_rom_map
		WHERE (batch_num = '20250723') <> (stat_time = '2025-07-23')
		LIMIT 10;




SELECT * FROM zz_data_sync_info;
SELECT * FROM t_cfg_precinct 





SELECT int_id AS intId, collect_time AS collectTime, res_code AS resCode, zh_label AS zhLabel, province_id AS provinceId, city_id AS cityId, county_id AS countyId, related_dc AS relatedSite, NULL AS relatedRoom, NULL AS batchNum, lifecycle_status AS lifecycleStatus, NULL AS sitePrecinctId, power_site_level AS powerSiteLevel, business_type AS businessType, mains_backup_method AS mainsBackupMethod, power_is_substations AS powerIsSubstations, mains_voltage_level AS mainsVoltageLevel, mains_nature AS mainsNature, cutin_date AS cutinDate, power_monitoring_site_name AS powerMonitoringSiteName, total_mains_number AS totalMainsNumber, mains_capacity AS mainsCapacity, mains_configuration_level AS mainsConfigurationLevel, total_tank_number AS totalTankNumber, tatal_tank_volume AS tatalTankVolume, property_unit AS propertyUnit, power_supply AS powerSupply, is_attach_idc_room AS isAttachIdcRoom, design_pue AS designPue, water_cooling_conf AS waterCoolingConf, is_cold_storage_install AS isColdStorageInstall, cold_storage_time AS coldStorageTime
FROM dwd_zz_site_property
WHERE power_site_level IN (?, ?)
ORDER BY int_id ASC
LIMIT ?




SELECT int_id AS intId, collect_time AS collectTime, res_code AS resCode, zh_label AS zhLabel, province_id AS provinceId, city_id AS cityId, county_id AS countyId, related_dc AS relatedSite, NULL AS relatedRoom, NULL AS batchNum, lifecycle_status AS lifecycleStatus, NULL AS sitePrecinctId, power_site_level AS powerSiteLevel, business_type AS businessType, mains_backup_method AS mainsBackupMethod, power_is_substations AS powerIsSubstations, mains_voltage_level AS mainsVoltageLevel, mains_nature AS mainsNature, cutin_date AS cutinDate, power_monitoring_site_name AS powerMonitoringSiteName, total_mains_number AS totalMainsNumber, mains_capacity AS mainsCapacity, mains_configuration_level AS mainsConfigurationLevel, total_tank_number AS totalTankNumber, tatal_tank_volume AS tatalTankVolume, property_unit AS propertyUnit, power_supply AS powerSupply, is_attach_idc_room AS isAttachIdcRoom, design_pue AS designPue, water_cooling_conf AS waterCoolingConf, is_cold_storage_install AS isColdStorageInstall, cold_storage_time AS coldStorageTime
FROM dwd_zz_site_property
WHERE cutin_date >= ? AND cutin_date <= ? AND power_site_level IN (?, ?)
ORDER BY int_id ASC
LIMIT ?





SELECT int_id AS intId, collect_time AS collectTime, res_code AS resCode, zh_label AS zhLabel, province_id AS provinceId, city_id AS cityId, county_id AS countyId, related_dc AS relatedSite, NULL AS relatedRoom, NULL AS batchNum, lifecycle_status AS lifecycleStatus, NULL AS sitePrecinctId, power_site_level AS powerSiteLevel, business_type AS businessType, mains_backup_method AS mainsBackupMethod, power_is_substations AS powerIsSubstations, mains_voltage_level AS mainsVoltageLevel, mains_nature AS mainsNature, cutin_date AS cutinDate, power_monitoring_site_name AS powerMonitoringSiteName, total_mains_number AS totalMainsNumber, mains_capacity AS mainsCapacity, mains_configuration_level AS mainsConfigurationLevel, total_tank_number AS totalTankNumber, tatal_tank_volume AS tatalTankVolume, property_unit AS propertyUnit, power_supply AS powerSupply, is_attach_idc_room AS isAttachIdcRoom, design_pue AS designPue, water_cooling_conf AS waterCoolingConf, is_cold_storage_install AS isColdStorageInstall, cold_storage_time AS coldStorageTime
FROM dwd_zz_site_property
WHERE cutin_date >= ? AND cutin_date <= ? AND power_site_level IN (?, ?) AND business_type IN (?)
ORDER BY int_id ASC
LIMIT ?

SELECT * FROM dwd_zz_site_property LIMIT 10


