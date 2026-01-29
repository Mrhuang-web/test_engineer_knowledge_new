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


SELECT COUNT(1) FROM dws_overdue_device_detail where stat_time = '2026-01-28' LIMIT 100;
SELECT * FROM dws_overdue_device_detail where stat_time = '2026-01-28' and manufactor_name is NULL AND city_id = '01-14-03' LIMIT 100;

SELECT COUNT(1) FROM dws_overdue_device_detail WHERE (stat_time = '2026-01-28' 
and manufactor_name is NULL) OR USE_time IS NULL OR start_time IS null
LIMIT 100;


select COUNT(1) FROM (SELECT * FROM dws_overdue_device_detail WHERE (stat_time = '2026-01-28' AND overdue_type IS not NULL)) AS TABLE1
WHERE  TABLE1.site_type_name IS not NULL and TABLE1.site_name IS not NULL AND  
TABLE1.update_cycle IS NOT NULL AND TABLE1.device_type_name IS NOT NULL AND 
manufactor_name IS NOT null
LIMIT 100;


SELECT * FROM dws_overdue_device_detail where stat_time = '2026-01-28' LIMIT 100;
SELECT * FROM dws_overdue_device_detail where stat_time = '2026-01-28' 
AND city_name = '白银市' AND manufactor_name = '中兴' LIMIT 100;

















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




SELECT * FROM fact_dwd_alarm_value LIMIT 10;













SELECT MAX(stat_time) FROM ods_zz_device_switch_power;



# 造数 -- 告警  -- 开关电源

SELECT * FROM ods_zz_irms_site_map LIMIT 10;
INSERT INTO `ods_zz_irms_site_map` (`stat_time`, `zg_id`, `uuid`, `zg_name`, `pms_id`, `dh_id`, `dh_name`, `batch_num`, `province_id`, `pms_name`, `statis_ymd`, `flow_time`) 
VALUES ('2025-12-31', '2026012601', 'c6ac174b-5d4b-40c6-abf2-c0dc2231ew1', '贵1数据中心_液冷2', 'JF-LN-SCDD-9001', '01-08-08-01-11-02', '贵1数据中心_液冷2', '2026-01-26 08:30:24.415865', NULL, NULL, '20251231', '2026-01-26 10:56:10');

SELECT * FROM ods_zz_site LIMIT 10;
INSERT INTO `ods_zz_site` (`stat_time`, `int_id`, `project_code`, `uuid`, `tele_cmn_serv_pro_name`, `pms_address_code`, `project_name`, `business_type`, `area_type`, `cutin_date`, `batch_num`, `collect_time`, `irms_province_code`, `related_dc`, `lifecycle_status`, `qualitor`, `floor_number`, `use_corp`, `standardaddress`, `village_pass_serv_code`, `if_village_pass_serv`, `village_pass_serv_name`, `alias_name`, `china_tower_station_code`, `latitude`, `province_id`, `city_id`, `county_id`, `longitude`, `if_tele_cmn_serv`, `tele_cmn_serv_pro_code`, `is_headquarters_used`, `zh_label`, `site_type`, `address`, `flow_time`) 
VALUES ('2025-12-31', '2026012601', NULL, NULL, NULL, NULL, NULL, '家客集客', NULL, '2018-06-25', '20251231', '2026-01-26 14:10:56', 'GZ', NULL, '在网', NULL, NULL, '其他', NULL, NULL, NULL, NULL, NULL, NULL, '26.5651492', '520000', '520400', '520404', '106.7182', '否', NULL, '否', '贵1数据中心_液冷2', '用户站点', '贵阳市南明区桃园路95号（原电厂旧址）保利凤凰湾售楼部', '2026-01-26 11:24:16');

SELECT * FROM ods_zz_site_property LIMIT 10;
INSERT INTO `ods_zz_site_property` (`stat_time`, `res_code`, `mains_voltage_level`, `mains_nature`, `total_mains_number`, `mains_capacity`, `mains_configuration_level`, `total_tank_number`, `tatal_tank_volume`, `batch_num`, `collect_time`, `irms_province_code`, `power_is_substations`, `cold_storage_time`, `power_supply`, `actual_pue`, `water_cooling_conf`, `is_cold_storage_install`, `province_id`, `city_id`, `county_id`, `zh_label`, `power_site_level`, `design_pue`, `property_unit`, `power_monitoring_site_name`, `power_monitoring_site_id`, `mains_backup_method`, `is_attach_idc_room`, `flow_time`) 
VALUES ('2025-12-31', '202601260101', '10KV', '市电直供', '1', '225', '1市电无油机', NULL, NULL, '20251231', '2026-01-26 16:11:18', 'GZ', '否', '1', '单变电站双母线引入；', NULL, '无', '否', '520000', '520400', '520404', '2026012601', '通信基站', NULL, NULL, '贵1数据中心_液冷2', NULL, '单路引入', '否', '2026-01-26 10:45:06');



SELECT * FROM ods_zz_irms_rom_map LIMIT 10;
INSERT INTO `ods_zz_irms_rom_map` (`stat_time`, `zg_id`, `address_code`, `batch_num`, `province_id`, `uuid`, `zg_name`, `pms_id`, `pms_name`, `dh_id`, `dh_name`, `statis_ymd`, `flow_time`) 
VALUES ('2025-12-03', '2026012602', '202601260201', '2026-01-26 16:11:18.477179', NULL, '5c07c1b3-c869-4bae-b57f-921231293d', '贵1数据中心楼2_综合机房', NULL, NULL, '01-08-08-01-11-02-01', '贵1数据中心楼2_综合机房', '20251203', '2026-01-13 15:41:13');

SELECT * FROM ods_zz_room LIMIT 10;
INSERT INTO `ods_zz_room` (`stat_time`, `int_id`, `tele_cmn_serv_pro_name`, `pms_design_code`, `plan_rack_num`, `loadable_rack_num`, `retire_time`, `zh_label`, `batch_num`, `collect_time`, `qualitor`, `room_area`, `floor_num`, `row_num`, `lifecycle_status`, `column_num`, `end_row`, `start_column`, `end_column`, `length`, `width`, `airconditioner_power`, `asset_address_code`, `equipment_power`, `qr_code_no`, `maintainor_method`, `uuid`, `equiproom_level`, `equiproom_type`, `province_id`, `city_id`, `county_id`, `address_code`, `project_code`, `height`, `project_name`, `row_direction`, `china_tower_operations_id`, `shared_unit`, `china_tower_station_code`, `china_tower_room_type`, `installed_rack_num`, `is_headquarters_used`, `start_row`, `related_site`, `if_village_pass_serv`, `village_pass_serv_name`, `village_pass_serv_code`, `alias_name`, `property_right`, `property_unit`, `cutin_date`, `irms_province_code`, `column_direction`, `if_tele_cmn_serv`, `tele_cmn_serv_pro_code`, `fifth_generation_flag`, `mainit_unit`, `pms_design_name`, `business_unit`, `flow_time`) 
VALUES ('2025-12-31', '2026012602', NULL, NULL, NULL, NULL, NULL, '贵1数据中心楼2_综合机房', '20251231', '2026-01-26 16:11:18', '许兵', '20', '1', NULL, '在网', NULL, NULL, NULL, NULL, NULL, NULL, '0.0', NULL, '0.0', '070524010010000595732', NULL, NULL, '接入', '无线机房', '520000', '520400', '520404', NULL, NULL, NULL, NULL, NULL, NULL, '无', NULL, NULL, NULL, '否', NULL, '2026012601', '否', NULL, NULL, '贵1数据中心楼2_综合机房', '租用', '中国移动', '2011-08-16', 'GZ', NULL, '否', NULL, '否', NULL, NULL, NULL, '2026-01-26 16:11:18');

SELECT * FROM ods_zz_room_property LIMIT 10;
INSERT INTO `ods_zz_room_property` (`stat_time`, `res_code`, `irms_province_code`, `power_related_site_name`, `power_monitor_conf`, `video_monitor_conf`, `batch_num`, `collect_time`, `province_id`, `city_id`, `county_id`, `zh_label`, `power_room_type`, `space_room_type`, `battery_backup_time`, `power_supply_mode`, `power_room_name`, `power_room_id`, `log_saved_time`, `power_supply_type`, `ac_terminal`, `ac_config`, `refrigeration_mode`, `refer_pue`, `flow_time`) 
VALUES ('2025-12-31', '202601260201', 'GZ', '-970402447', '无', '无', '20251231', '2026-01-26 16:11:18', '520000', '520400', '520404', '2026012602', '基站机房', '无线机房', '15', '单电源双回路供电', '新化县化溪白溪村无线机房', '121812', '1', '交流220V', '精密空调', '其他', '风冷', '1.1', '2026-01-26 16:11:18');


# 上游  开关电源    00123123
441000000000008089010115
ods_zz_device_switch_power

SELECT * FROM ods_zz_device_switch_power WHERE res_code IN ('441000000000008089010115');
SELECT * FROM ods_zz_device_switch_power WHERE res_code IN ('44100000000000808901111');
	# 插入综资
	INSERT INTO `ods_zz_device_switch_power` (`stat_time`, `res_code`, `qualitor`, `related_rackpos`, `qr_code_no`, `power_device_id`, `device_number`, `power_device_name`, `assets_no`, `batch_num`, `collect_time`, `irms_province_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `related_system`, `rated_output_voltage`, `monitoring_module_model`, `total_rack_loading_modules`, `total_rack_match_modules`, `signal_output_rated_capacity`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `total_rack_loading_modules_number`, `total_rack_match_modules_number`, `flow_time`) 
	VALUES ('2025-12-31', '44100000000000808901111', 'admin', NULL, NULL, '00123123', '1', '开关电源[珠江电源](GZM42B7局)', '2121-A2515419,2121-01078588,2121-01078577,2121-01078578,2121-01078579,2121-01078580,2121-01078581,2121-01078582,2121-01078583,2121-01078584,2121-01078585,2121-01078586', '20251231', '2026-01-26 15:03:32', 'GZ', '520000', '520400', '520404', '2026012601', '2026012602', '开关电源', '分立开关电源', '广州从化青云四楼机房交换1-分立开关电源-4F-6-1', '06010001', 'PRS6300', '珠江', '441000000000008732898964', '-48V', 'PRS6300', NULL, NULL, '100', '2011-11-21', '2023-11-21', '在网', 'liminyi5', '15', '10.0', '2026-01-13 15:17:10');


# 开关电源  006035
SELECT * FROM fact_dwd_alarm_value LIMIT 10;

SELECT MAX(serial_no) FROM fact_dwd_alarm_value LIMIT 10;
SELECT * FROM fact_dwd_alarm_value where alarm_meta_code = '006035' LIMIT 100;


SELECT * FROM fact_dwd_signal_value LIMIT 10;
SELECT * FROM fact_dwd_signal_value where device_spatial_id = '10016449' LIMIT 10;
SELECT * FROM fact_dwd_signal_value where device_spatial_id = '10016449' LIMIT 10;
SELECT * FROM fact_dwd_signal_value where device_id = '10016449' LIMIT 10;


SELECT * FROM t_cfg_device where precinct_id like '01-08-08-01-11-02-01%' LIMIT 10;
SELECT * FROM t_cfg_device WHERE dim_device_id = '110637'


SELECT * FROM t_cfg_precinct where precinct_id like '01-08-08-01-11-02-01%' and dim_spatial_id = '12766' LIMIT 10;


# 区县：12766   机房：9054062   设备：10016450
# 2999673599
INSERT INTO `fact_dwd_alarm_value` (`alarm_meta_code`, `device_id`, `serial_no`, `alarm_start_time`, `alarm_level`, `alarm_value`, `alarm_content`, `alarm_status`, `alarm_end_time`, `alarm_duration_sec`, `revoke_type`, `chief_spatial_id`, `device_spatial_id`, `site_type`, `engineering_status`) 
VALUES ('006035', 10016450, 2999673599, '2026-01-01 09:45:36', 3, 501, '下限告警-触发值169.5V', 2, '2026-01-01 10:49:10', 215, 0, 12766, 9054062, 1, 0);
INSERT INTO `fact_dwd_alarm_value` (`alarm_meta_code`, `device_id`, `serial_no`, `alarm_start_time`, `alarm_level`, `alarm_value`, `alarm_content`, `alarm_status`, `alarm_end_time`, `alarm_duration_sec`, `revoke_type`, `chief_spatial_id`, `device_spatial_id`, `site_type`, `engineering_status`) 
VALUES ('006035', 10016450, 2999673599, '2026-12-31 09:45:36', 3, 501, '下限告警-触发值169.5V', 2, '2026-12-31 10:59:10', 215, 0, 12766, 9054062, 1, 0);


SELECT * FROM dws_overdue_device_alert_monthly;

SELECT * FROM dwd_device_detail_v where dim_device_id = '10016450' LIMIT 10;
SELECT * FROM dws_zz_dh_device LIMIT 10;

SELECT MAX(`date`) FROM overdue_device_detail
SELECT * FROM overdue_device_detail LIMIT 10;


















select to_date(date_trunc('month',min(alarm_start_time))) as stat_time,
		dv.device_id,
		DATE_FORMAT(min(alarm_start_time), '%Y-%m') alert_month,
		a.device_id  as dim_device_id,
		count(1) as alert_times,
		now() as flow_time
from 	
	fact_dwd_alarm_value a
	
	join 
		dwd_device_detail_v dv on dv.dim_device_id=a.device_id
 

 where  a.alarm_start_time >=date_trunc('month','2026-01-29')
 and a.alarm_start_time <=concat('2026-01-29',' 23:59:59')
AND a.alarm_meta_code in ('008020','008021','008030','008034','008040','008044','008045','008046','008047','008052','008053'
		,'008054','003002','003006','001034','001038','001040','087002','087012','087031','087040','087043','088003','002022'
		,'002023','002034','002035','002013','004003','005001','005015','005022','005049','006001','006011','006015','006023'
		,'006035','006040','007005','007012','015012','015016','011087','011088','011093','011094','012001','012003','012030'
		,'012031','012033','076010','076040','076041','076042'
		)
		
		
		
		
		
		
SELECT * FROM dim_overdue_type LIMIT 10;		
		
		
select to_date(date_trunc('month',min(alarm_start_time))) as stat_time,
		dv.device_id,
		DATE_FORMAT(min(alarm_start_time), '%Y-%m') alert_month,
		a.device_id  as dim_device_id,
		count(1) as alert_times,
		now() as flow_time
from 	fact_dwd_alarm_value a
join dwd_device_detail_v dv on dv.dim_device_id=a.device_id
 where  a.alarm_start_time >=date_trunc('month','2025-12-31')
 and a.alarm_start_time <add_months(date_trunc('month','2025-12-31'),1)
and alarm_meta_code in ('008020','008021','008030','008034','008040','008044','008045','008046','008047','008052','008053'
		,'008054','003002','003006','001034','001038','001040','087002','087012','087031','087040','087043','088003','002022'
		,'002023','002034','002035','002013','004003','005001','005015','005022','005049','006001','006011','006015','006023'
		,'006035','006040','007005','007012','015012','015016','011087','011088','011093','011094','012001','012003','012030'
		,'012031','012033','076010','076040','076041','076042'
		)
group by dv.device_id,a.device_id;
	
	
	
	
	
	
	
	
	
	
	
	
	
	
select 
a.room_id
,a.room_name 
,a.province_id 
,a.province_name 
,a.city_id 
,a.city_name 
,a.county_id 
,a.county_name 
,a.site_id 
,a.site_name 
,a.site_type 
,a.site_type_name 
,a.device_name
,a.device_code
,a.sys_device_id
,a.resource_device_type_name
,a.device_type_name
,a.device_sub_type_name
,a.manufactor_name
,a.type_name
,a.use_time
,a.start_time
,COALESCE (b.update_cycle,c.update_cycle) as update_cycle
,a.run_time
,a.run_time/COALESCE (b.update_cycle,c.update_cycle)*100.00 as overdue_value
 from temp_dws_overdue_device_detail_1 a
 left join jdbc1.spider.overdue_device_type_dict b
   on a.device_type_name=b.device_type
  and a.device_sub_type_name=b.device_subclass
 left join (select device_type as device_type,
	               max(update_cycle) as update_cycle
              from jdbc1.spider.overdue_device_type_dict
             group by device_type) c 
   on a.device_type_name=c.device_type
) m
left join dim_overdue_type n 
  on n.is_valid=1 and 1=1
left join (select device_id,
		         sum(alert_times) as alert_times
             from dws_overdue_device_alert_monthly
            where alert_month =to_date(months_sub(date_trunc('month','2025-12-31'),1))
             group by device_id