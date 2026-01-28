SELECT 
	resource_site.zh_label AS site_label,
	resource_site.int_id AS site_int_id,
	resource_room.zh_label AS room_label,
	resource_room.int_id AS room_int_id,
	site.precinct_id AS site_id,
	site.precinct_name AS site_name,
	room.precinct_id AS room_id,
	room.precinct_name AS room_name,
	zz_device.zh_label,
	zz_device.res_code,
	zz_device.device_type,
	zz_device.lifecycle_status,
	zz_ip.city_name,
	zz_ip.device_name
FROM 
	t_zz_space_resources resource_site
LEFT JOIN 
	t_zz_space_resources resource_room ON resource_site.int_id = resource_room.related_site
LEFT JOIN 
	t_cfg_precinct site ON site.precinct_id = resource_site.precinct_id
LEFT JOIN 
	t_cfg_precinct room ON room.precinct_id = resource_room.precinct_id
LEFT JOIN 
	t_zz_power_device zz_device ON zz_device.related_site = resource_site.int_id	AND zz_device.related_room = resource_room.int_id
LEFT JOIN
	t_cfg_ip zz_ip ON zz_ip.site_id = resource_site.int_id	AND zz_ip.room_id = resource_room.int_id
WHERE 
	resource_room.zh_label IS NOT NULL 
	AND site.precinct_id IS NOT NULL 
	AND room.precinct_id IS NOT NULL 
	AND resource_site.space_type = '101'
	AND resource_room.space_type = '102'
	AND device_name IS NOT null
	AND zz_device.device_type = '开关电源'
	
	
	
	
	
	
	
	
	
select uuid, name from entrance_user where name in ('UDP-中达1_已授权')

SELECT * FROM access_control_device WHERE device_id in ('4845d10a-a17f-4b9b-90d7-5c16d265a399', '26c35818-6922-4513-8d91-16781fde8b86', '250ecc4d-3772-49f8-b5e8-1250ca25a976', '24537e2c-d925-47a7-bcb3-5d232002c455')


SELECT * FROM entrance_user;
SELECT * FROM entrance_card;
SELECT name FROM entrance_user WHERE name IN ('UDP-盈佳1_已授权','UDP-盈佳_未授权','UDP-力维1_已授权','UDP-力维_未授权','HTTP-大华1_已授权','HTTP-大华_未授权','UDP-亚奥1_已授权','UDP-亚奥_未授权','UDP-海能1_已授权','UDP-海能_未授权','UDP-邦讯-新版1_已授权','UDP-邦讯-新版_未授权','UDP-高新兴1_已授权','UDP-高新兴_未授权','SDK-大华1_已授权','SDK-大华_未授权','UDP-中达1_已授权','UDP-中达_未授权','TCP-力维1_已授权','TCP-力维_未授权','UDP-CH803LM1_已授权','UDP-CH803LM_未授权','UDP-ES10001_已授权','UDP-ES1000_未授权','UDP-邦讯-旧版1_已授权','UDP-邦讯-旧版_未授权','TCP-邦讯-旧版1_已授权','TCP-邦讯-旧版_未授权','UDP-高新兴V21_已授权','UDP-高新兴V2_未授权')



965a226f-f697-42fe-93a9-921cc976d80d

SELECT * FROM entrance_card_auth
SELECT * FROM entrance_user WHERE 

SELECT ac.card_id,acd.device_name,aca.* FROM access_control_device acd
	LEFT JOIN entrance_card_auth  aca ON acd.device_id = aca.device_id
	LEFT JOIN entrance_card ac ON ac.card_id = aca.card_id
	WHERE acd.room_id = '01-01-17-02-05-01'
	


SELECT COUNT(1) FROM wb_log;
SELECT * FROM wb_log group by operation_date desc LIMIT 100;


SELECT * FROM t_cfg_precinct WHERE precinct_name LIKE "%桂林%" LIMIT 10;

SELECT * FROM t_cfg_precinct WHERE precinct_id = "01-07-04-03-31-04" LIMIT 10;

SELECT * FROM t_cfg_device WHERE precinct_id LIKE "01-07-04-03-31-04%" and device_type = '92' LIMIT 100;

SELECT * FROM t_cfg_dict WHERE col_name = "device_type";

SELECT * FROM t_cfg_metemodel_detail WHERE device_type = 92 LIMIT 100;



SELECT  * FROM overdue_device_detail LIMIT 10;


01-02   340000
3
SELECT * FROM t_cfg_dict WHERE col_name = "device_type";
SELECT COUNT(1) FROM t_cfg_device; 
SELECT * FROM t_cfg_precinct WHERE precinct_name LIKE "%安徽%" LIMIT 10;


SELECT * FROM t_cfg_precinct WHERE precinct_name LIKE "%安徽淮南市田家庵区0303枢纽楼%" LIMIT 10;


SELECT d.*, s.*
FROM t_cfg_device d
/* 1. 机房本身 */
JOIN t_cfg_precinct pc ON pc.precinct_id = d.precinct_id
/* 2. 上级的 precinct 记录（可能是站点，也可能是楼栋） */
LEFT JOIN t_cfg_precinct p_parent
       ON p_parent.precinct_id = pc.up_precinct_id
/* 3. 再追一层：如果上级是楼栋，就继续拿它的上级（站点） */
LEFT JOIN t_cfg_precinct p_site
       ON p_site.precinct_id = CASE
            WHEN p_parent.precinct_kind = 2 THEN p_parent.precinct_id   -- 上级就是站点
            WHEN p_parent.precinct_kind = 3 THEN p_parent.up_precinct_id -- 上级是楼栋，再往上
          END
/* 4. 用追到的站点 ID 去 t_cfg_site 取 site_type */
JOIN t_cfg_site s ON s.site_id = p_site.precinct_id
WHERE d.precinct_id LIKE '01-02%'
  AND d.device_type = '3'
  AND s.site_type IN (1,2);
  
  
SELECT * FROM t_cfg_device WHERE precinct_id = '01-02-05-03-03-01' AND device_type = '3'; 

SELECT * FROM zz_to_rm_rm_area_room where precinct_id = '01-02-05-03-03-01' LIMIT 10;



SELECT * FROM energy_cabinet LIMIT 10;
SELECT * FROM energy_cabinet_attribute_config LIMIT 10;
SELECT * FROM energy_cabinet_poweroutage_config_scope LIMIT 10;


SELECT * from zz_data_sync_info

SELECT * FROM t_cfg_dict WHERE col_name LIKE "device_type";
SELECT * FROM t_cfg_dict WHERE col_name LIKE "%sub%" and dict_code = 1;

SELECT * FROM t_cfg_dict WHERE col_name = 'precinct_kind'
SELECT * FROM energy_cabinet LIMIT 10 WHERE col_name = 'precinct_kind'
SELECT * FROM t_cfg_precinct where precinct_kind = '8' LIMIT 10 WHERE col_name = 'precinct_kind'

SELECT * FROM energy_cabinet_column LIMIT 10 

SELECT * FROM t_cfg_device LIMIT 10;


SELECT * FROM t_cfg_dict WHERE col_name LIKE '%system%'
SELECT * FROM t_cfg_dict WHERE dict_note LIKE '%系统%'
SELECT * FROM device_system_info LIMIT 10;
SELECT * FROM t_cfg_subsystem LIMIT 10;

SELECT * FROM t_cfg_dict WHERE col_name LIKE '%system%'

SELECT * FROM t_high_voltage_system WHERE col_name LIKE '%system%'

SELECT device_type,device_type_id,es_index_name FROM t_sync_field_config GROUP BY device_type_id

SELECT * FROM t_sync_field_config


SELECT * FROM t_zz_power_device WHERE device_type_id = '68'  AND LEFT(create_time,10) = '2026-01-25' ORDER BY create_time DESC LIMIT 10

SELECT COUNT(1) FROM t_zz_power_device WHERE device_type_id = '68'  AND LEFT(create_time,10) = '2026-01-25'


SELECT * FROM entrance_face_work_ord;
SELECT * FROM entrance_face_success_device;









# 00100006011001768642
# access :0012025000000000
# fsu_orgin :100100000000018
SELECT * FROM t_cfg_fsu;
SELECT * FROM t_cfg_device WHERE device_id = '00100006011001768642';
SELECT * FROM t_cfg_monitordevice WHERE fsu_device_id = '00100006011001768642';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-08-07-05-01-01';


SELECT * FROM access_control_device_20260122 WHERE device_id = 'f3dd12e1-3435-49d5-a088-afb0bff6b8b4';
SELECT * FROM t_cfg_device WHERE device_id = 'ed7393ec-65e2-4607-8ba0-429d3b52c447';



SELECT * FROM dws_overdue_device_alert_monthly;
IN ('变压器'、'高压配电'、'高压直流电源'、'高压直流配电'、'低压交流配电'
    '发电机组'、'开关电源'、'低压直流配电'、'UPS设备'
    '蓄电池'、'空调'、'动环监控')
    
SELECT COUNT(*) FROM dwd_zz_device_total WHERE device_type IN ('变压器','高压配电','高压直流电源','高压直流配电','低压交流配电','发电机组','开关电源','低压直流配电','UPS设备','蓄电池','空调','动环监控')
AND stat_time = '2025-12-31'
LIMIT 10;








SELECT stat_time,COUNT(device_type) FROM dwd_zz_device_total GROUP BY stat_time

SELECT * FROM dws_zz_audit_site_summary LIMIT 10;
SELECT * FROM dws_zz_dh_device LIMIT 10;

SELECT COUNT(1) FROM dws_zz_dh_device LIMIT 10;
SELECT COUNT(1) FROM dws_overdue_device_detail LIMIT 10;
SELECT MAX(stat_time) FROM dws_overdue_device_detail LIMIT 100;


SELECT COUNT(1) FROM dws_overdue_device_detail where stat_time = '2026-01-27' LIMIT 100;
SELECT * FROM dws_overdue_device_detail where stat_time = '2026-01-27' LIMIT 100;
















SELECT * 
FROM dws_zz_dh_room r 
 
INNER  JOIN dwd_room_detail_v c 
  ON r.precinct_id=c.room_id 
 
INNER  JOIN dwd_zz_device_total d 
	 ON r.int_id=d.related_room  AND r.county_id = d.county_id

WHERE d.device_type  IN ('变压器','高压配电','高压直流电源','高压直流配电','低压交流配电','发电机组','开关电源','低压直流配电','UPS设备','蓄电池','空调','动环监控')
 AND stat_time = '2025-12-31'

LIMIT 10;



SELECT COUNT(1)
FROM dws_zz_dh_room r              -- 机房维表（提供空间坐标）
INNER JOIN dwd_room_detail_v c     -- 机房明细（获取行政区划）  
    ON r.precinct_id = c.room_id
INNER JOIN dwd_zz_device_total d   -- 【设备数据源】（DWD层）
    ON r.int_id = d.related_room   -- 关联条件1：机房ID匹配
    AND r.county_id = d.county_id  -- 关联条件2：区县一致性校验
LEFT JOIN dws_zz_dh_device e       -- 设备维表（获取系统设备ID）
    ON r.precinct_id = e.precinct_id 
    AND d.res_code = e.res_code
WHERE d.table_name IN (
    'ods_zz_device_transform',           -- 变压器
    'ods_zz_device_high_distribution',   -- 高压配电
    'ods_zz_device_high_power',          -- 大功率设备
    'ods_zz_device_high_dc_distribution',-- 高压直流配电
    'ods_zz_device_low_ac_distribution', -- 低压交流配电
    'ods_zz_device_power_generation',    -- 发电机组
    'ods_zz_device_switch_power',        -- 开关电源
    'ods_zz_device_low_dc_distribution', -- 低压直流配电
    'ods_zz_device_ups',                 -- UPS
    'ods_zz_device_battery',             -- 蓄电池
    'ods_zz_device_air',                 -- 空调
    'ods_zz_device_power_monitor'        -- 动力环境监控
)
LIMIT 10;







SELECT COUNT(1) FROM dws_overdue_device_detail where stat_time = '2026-01-27' LIMIT 100;
SELECT * FROM dws_overdue_device_detail where stat_time = '2026-01-27' LIMIT 100;


