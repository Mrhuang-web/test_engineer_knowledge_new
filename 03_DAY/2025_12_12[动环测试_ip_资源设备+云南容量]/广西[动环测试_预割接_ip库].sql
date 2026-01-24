# t.lifecycle_status：工程试运行
SELECT COUNT(0)
FROM (
SELECT res_code, device_id, zh_label, lifecycle_status, device_type, related_room, related_site, device_subclass
FROM t_zz_power_device t
WHERE 1 = 1 AND t.lifecycle_status IN ('工程试运行')) device
LEFT JOIN t_zz_space_resources zz_room ON zz_room.int_id = device.related_room AND zz_room.space_type = 102 AND zz_room.related_site = device.related_site
LEFT JOIN t_zz_space_resources zz_site ON zz_room.related_site = zz_site.int_id
LEFT JOIN t_cfg_precinct room ON room.precinct_id = zz_room.precinct_id
LEFT JOIN t_cfg_precinct build ON room.up_precinct_id = build.precinct_id AND build.precinct_kind = 3 AND build.isdel = '0'
LEFT JOIN t_cfg_precinct site ON IFNULL(build.up_precinct_id, room.up_precinct_id) = site.precinct_id AND site.precinct_kind = 2 AND site.isdel = '0'
LEFT JOIN t_cfg_precinct area ON area.precinct_id =
LEFT(room.precinct_id, 11)
LEFT JOIN t_cfg_precinct city ON city.precinct_id =
LEFT(room.precinct_id, 8)
LEFT JOIN t_cfg_site site_type ON site_type.site_id = site.precinct_id
LEFT JOIN t_cfg_dict p ON p.dict_code = site_type.site_type AND p.col_name = 'site_type'
WHERE room.precinct_kind = 5 AND room.isdel = '0';


	SELECT *
	FROM (
	SELECT res_code, device_id, zh_label, lifecycle_status, device_type, related_room, related_site, device_subclass
	FROM t_zz_power_device t
	WHERE 1 = 1 AND t.lifecycle_status IN ('工程试运行')) device
	LEFT JOIN t_zz_space_resources zz_room ON zz_room.int_id = device.related_room AND zz_room.space_type = 102 AND zz_room.related_site = device.related_site
	LEFT JOIN t_zz_space_resources zz_site ON zz_room.related_site = zz_site.int_id
	LEFT JOIN t_cfg_precinct room ON room.precinct_id = zz_room.precinct_id
	LEFT JOIN t_cfg_precinct build ON room.up_precinct_id = build.precinct_id AND build.precinct_kind = 3 AND build.isdel = '0'
	LEFT JOIN t_cfg_precinct site ON IFNULL(build.up_precinct_id, room.up_precinct_id) = site.precinct_id AND site.precinct_kind = 2 AND site.isdel = '0'
	LEFT JOIN t_cfg_precinct area ON area.precinct_id =
	LEFT(room.precinct_id, 11)
	LEFT JOIN t_cfg_precinct city ON city.precinct_id =
	LEFT(room.precinct_id, 8)
	LEFT JOIN t_cfg_site site_type ON site_type.site_id = site.precinct_id
	LEFT JOIN t_cfg_dict p ON p.dict_code = site_type.site_type AND p.col_name = 'site_type'
	WHERE room.precinct_kind = 5 AND room.isdel = '0';
	
	
# zh_label:南宁武鸣县宝城公寓
SELECT zh_label AS Id, gx_power_site_level AS name
FROM t_zz_power_specialty
WHERE device_type_id = 0 AND zh_label IN ('南宁武鸣县宝城公寓');



# 查看对应设备采集器名称    ：site_id -- 站点为综资的
SELECT 
id, site_id AS siteId, device_name AS collectorName, 
INET_NTOA(ip) AS collectorIp, room_name AS collectorRoomName
FROM t_cfg_ip
WHERE 1=1 
	AND device_name IS NOT NULL 
	AND device_type = 6 
	AND site_id IN ('SITE-ff80808155de01c501560093ff3e0030');
	
	SELECT * FROM t_cfg_ip;
	



# 综资表

SELECT * from t_zz_space_resources LIMIT 400;		# 站点机房都有(101-站点，102-机房，103?)
	SELECT * from t_zz_space_resources WHERE space_type = '101' LIMIT 500;
		SELECT * from t_zz_space_resources WHERE int_id = 'SITE-ff80808155de01c501560093ff3e0030';
		SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-16-05-04';
		SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-16-05';
		SELECT * FROM t_zz_space_resources WHERE precinct_id LIKE "01-07-16-05-13%";
		SELECT * FROM t_zz_space_resources WHERE precinct_id LIKE "01-07-16-05%";
		SELECT * FROM t_zz_space_resources WHERE zh_label LIKE "%河西%";
		SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-16-05-13';
		SELECT * FROM t_cfg_precinct WHERE precinct_id like '01-07-16-05-04%';
		SELECT * FROM t_cfg_precinct WHERE precinct_name = '梧州测试数据区河西基站传输机房';
		
	SELECT * from t_zz_space_resources WHERE space_type = '102' LIMIT 500;
		SELECT MAX(id) FROM t_zz_space_resources;
		INSERT INTO `t_zz_space_resources` (`id`, `data_time`, `precinct_id`, `int_id`, `zh_label`, `related_site`, `space_type`, `city_id`, `county_id`, `create_time`) 
		VALUES (12129587, '20250224', '01-07-16-04-05-01', 'ROOM-ff808081529cf01b0153ab810eda0532', '万秀天等县天宝北路财政局旁390号居民楼基站无线机房', 'SITE-664cc21c10c44c03ac884bd9c35ce6d4', 102, '万秀', '天等', '2025-02-25 08:05:10');
		SELECT * from t_zz_space_resources WHERE related_site = 'SITE-664cc21c10c44c03ac884bd9c35ce6d4';
		
	SELECT * from t_zz_space_resources WHERE space_type = '103' LIMIT 500;


SELECT * from t_zz_power_specialty LIMIT 400;
	SELECT * FROM t_cfg_dict WHERE dict_note = '%市区重要汇聚机房%';
	SELECT * FROM t_zz_power_specialty WHERE zh_label = '梧州万秀区河西';
	SELECT * FROM t_zz_power_specialty WHERE related_site IS NOT NULL LIMIT 100;
	SELECT * FROM t_zz_power_specialty GROUP BY device_type_id;
	SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
	
	
SELECT * FROM t_zz_site_property LIMIT 400;
	SELECT * FROM t_zz_site_property where res_code = '441000000000007995033571' LIMIT 400;
	SELECT * FROM t_sync_field_config;
	
select * from t_device_type_mapped




SELECT DISTINCT gx_power_site_level AS value, gx_power_site_level AS name
FROM t_zz_power_specialty
WHERE gx_power_site_level IS NOT NULL AND gx_power_site_level !='' AND zh_label = '梧州万秀区富民街道鸳江路业务';






SELECT * FROM t_sync_field_config;
SELECT * FROM t_zz_space_resources WHERE precinct_id = "01-07-16-05-04";

select * FROM t_cfg_precinct WHERE precinct_id = '01-07-07-03-01'

SELECT * FROM t_zz_space_resources WHERE zh_label = "北海银海区福成镇宁海村";   # SITE-4033
SELECT * FROM t_zz_space_resources WHERE zh_label = "北海银海区福成镇宁海村基站无线机房";    ROOM-4034
SELECT * from t_zz_space_resources WHERE related_site = 'SITE-664cc21c10c44c03ac884bd9c35ce6d4';
SELECT * FROM t_zz_power_specialty where zh_label = '北海银海区福成镇宁海村' LIMIT 10;
SELECT * FROM t_zz_power_specialty where res_code = 'SITE-4033' LIMIT 10
SELECT * FROM t_cfg_ip where site_name = '北海银海区福成镇宁海村' LIMIT 10
SELECT * FROM t_cfg_ip WHERE site_id = 'SITE-4033';
select * FROM t_cfg_precinct WHERE precinct_name LIKE "%梧州测试数据区工业园生产楼二楼电力机房%"
SELECT * FROM t_cfg_ip WHERE room_name LIKE '%梧州测试数据区工业园生产楼二楼电力机房%';
SELECT * FROM t_cfg_ip WHERE site_name LIKE 	'%梧州测试数据区工业园生产楼%'




SELECT * FROM t_zz_power_device WHERE device_subclass = 'FSU' LIMIT 1000
SELECT * FROM t_zz_power_device WHERE device_subclass = 'FSU' LIMIT 1000
SELECT * FROM t_zz_power_device WHERE related_site = 'SITE-4033' LIMIT 1000
SELECT * FROM t_cfg_device WHERE  device_id = '00771006000002949620';
SELECT * FROM t_cfg_device LIMIT 10;


SELECT * FROM t_zz_power_specialty LIMIT 10;
SELECT * FROM t_zz_power_specialty LIMIT 10;
SELECT * FROM t_zz_power_specialty where zh_label = '北海银海区福成镇宁海村' LIMIT 10;
SELECT * FROM t_zz_power_specialty where zh_label = '梧州测试数据区工业园生产楼' LIMIT 10;













SELECT id, site_id AS siteId, device_name AS collectorName, 
INET_NTOA(ip) AS collectorIp, room_name AS collectorRoomName
FROM t_cfg_ip
WHERE 1=1 AND device_name IS NOT NULL AND device_type = 6 AND 
site_id IN ('SITE-ff80808155de01c501560093ff3e0030')



SELECT  *
FROM t_cfg_ip
WHERE 1=1 AND device_name IS NOT NULL AND device_type = 6 AND 
site_id IN ('SITE-ff80808155de01c501560093ff3e0030')






















SELECT device.res_code AS resCode, device.device_id AS deviceId, device.device_type AS deviceType, device.zh_label AS deviceName, device.device_subclass AS deviceSubclass, city.precinct_name AS cityName, area.precinct_name AS areaName, p.dict_note AS siteType, site.precinct_name AS siteName, device.related_site AS siteId, room.precinct_id AS roomId, room.precinct_name AS roomName, zz_site.zh_label AS intId, device.lifecycle_status AS lifecycleStatus
FROM (
SELECT res_code, device_id, zh_label, lifecycle_status, device_type, related_room, related_site,device_subclass
FROM t_zz_power_device t
WHERE 1=1 AND (t.device_type LIKE CONCAT('开关电源','%'))) device
LEFT JOIN t_zz_space_resources zz_room ON zz_room.int_id = device.related_room AND zz_room.space_type = 102 AND zz_room.related_site = device.related_site
LEFT JOIN t_zz_space_resources zz_site ON zz_room.related_site = zz_site.int_id
LEFT JOIN t_cfg_precinct room ON room.precinct_id = zz_room.precinct_id
LEFT JOIN t_cfg_precinct build ON room.up_precinct_id = build.precinct_id AND build.precinct_kind = 3 AND build.isdel = '0'
LEFT JOIN t_cfg_precinct site ON IFNULL(build.up_precinct_id, room.up_precinct_id) = site.precinct_id AND site.precinct_kind = 2 AND site.isdel = '0'
LEFT JOIN t_cfg_precinct area ON area.precinct_id =
LEFT(room.precinct_id,11)
LEFT JOIN t_cfg_precinct city ON city.precinct_id =
LEFT(room.precinct_id,8)
LEFT JOIN t_cfg_site site_type ON site_type.site_id = site.precinct_id
LEFT JOIN t_cfg_dict p ON p.dict_code = site_type.site_type AND p.col_name = 'site_type'
WHERE room.precinct_kind = 5 AND room.isdel = '0'
LIMIT 15