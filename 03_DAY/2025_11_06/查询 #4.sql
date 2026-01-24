-- 插入父设备配置
INSERT INTO t_overdue_service_life_config 
    (device_type, device_sub_type, site_type_dc, site_type_jl, site_type_jd, site_type_jz, is_enabled)
SELECT 
    resource_device_type_name,
    NULL,
    MAX(CASE WHEN site_type = 1 THEN update_cycle END),
    MAX(CASE WHEN site_type = 2 THEN update_cycle END),
    MAX(CASE WHEN site_type = 3 THEN update_cycle END),
    MAX(CASE WHEN site_type = 4 THEN update_cycle END),
    1
FROM overdue_device_detail
WHERE resource_device_type_name IS NOT NULL AND resource_device_type_name != ''
GROUP BY resource_device_type_name
ON DUPLICATE KEY UPDATE 
    site_type_dc = VALUES(site_type_dc),
    site_type_jl = VALUES(site_type_jl),
    site_type_jd = VALUES(site_type_jd),
    site_type_jz = VALUES(site_type_jz),
    update_time = CURRENT_TIMESTAMP;

-- 插入子设备配置
INSERT INTO t_overdue_service_life_config 
    (device_type, device_sub_type, site_type_dc, site_type_jl, site_type_jd, site_type_jz, is_enabled)
SELECT 
    resource_device_type_name,
    device_sub_type_name,
    MAX(CASE WHEN site_type = 1 THEN update_cycle END),
    MAX(CASE WHEN site_type = 2 THEN update_cycle END),
    MAX(CASE WHEN site_type = 3 THEN update_cycle END),
    MAX(CASE WHEN site_type = 4 THEN update_cycle END),
    1
FROM overdue_device_detail
WHERE resource_device_type_name IS NOT NULL AND resource_device_type_name != ''
  AND device_sub_type_name IS NOT NULL AND device_sub_type_name != ''
GROUP BY resource_device_type_name, device_sub_type_name
ON DUPLICATE KEY UPDATE 
    site_type_dc = VALUES(site_type_dc),
    site_type_jl = VALUES(site_type_jl),
    site_type_jd = VALUES(site_type_jd),
    site_type_jz = VALUES(site_type_jz),
    update_time = CURRENT_TIMESTAMP;
    
    
SELECT * from t_overdue_service_life_config where is_enabled = 0 


SELECT device_type from t_zz_power_device GROUP BY device_type LIMIT 100




SELECT * from t_overdue_service_life_config WHERE device_sub_type IS NULL
delete from t_overdue_service_life_config


SELECT * from t_overdue_service_life_config WHERE device_sub_type IS NULL



SELECT * FROM fsu WHERE fsuname LIKE "%上海设备2025年%";
SELECT * FROM device where fsuid IN (SELECT fsuid FROM fsu WHERE fsuname LIKE "%上海设备2025年%");
SELECT * FROM signals where fsuid IN (SELECT fsuid FROM fsu WHERE fsuname LIKE "%上海设备2025年%");


DELETE from fsu WHERE fsuname LIKE "%上海设备2025年%";
DELETE from device where fsuid IN (SELECT fsuid FROM fsu WHERE fsuname LIKE "%上海设备2025年%");
DELETE from signals where fsuid IN (SELECT fsuid FROM fsu WHERE fsuname LIKE "%上海设备2025年%");



SELECT * FROM t_cfg_precinct LIMIT 10;
SELECT * FROM t_cfg_device WHERE precinct_id LIKE "01-01-08-04-15%";

SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-08-04-15'


DELETE FROM t_cfg_precinct WHERE precinct_id LIKE "01-01-08-04-15%";
DELETE FROM t_cfg_device WHERE precinct_id LIKE "01-01-08-04-15%";



SELECT 
