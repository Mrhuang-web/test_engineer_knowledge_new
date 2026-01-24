# 01业务说明

```
ip申请：
    IP入网：
        就是把综资的设备入网到动环里面
    IP退网：
        就是把已经入到动环的综资设备进行退网
    因此需要先建立 -- 站点机房设备的综资与动环关联

涉及服务：
	resource
```

## 02查询关联数据

```
查看站点-（仅匹配precinct和resource表）
SELECT 
	resource_site.zh_label AS site_label,
	resource_site.int_id AS site_int_id,
	resource_room.zh_label AS room_label,
	resource_room.int_id AS room_int_id,
	site.precinct_id AS site_id,
	site.precinct_name AS site_name,
	room.precinct_id AS room_id,
	room.precinct_name AS room_name
FROM 
	t_zz_space_resources resource_site
LEFT JOIN 
	t_zz_space_resources resource_room ON resource_site.int_id = resource_room.related_site
LEFT JOIN 
	t_cfg_precinct site ON site.precinct_id = resource_site.precinct_id
LEFT JOIN 
	t_cfg_precinct room ON room.precinct_id = resource_room.precinct_id
WHERE 
	resource_room.zh_label IS NOT NULL 
	AND site.precinct_id IS NOT NULL 
	AND room.precinct_id IS NOT NULL 
	AND resource_site.space_type = '101'
	AND resource_room.space_type = '102'




查看站点-机房（综资关联情况 --> resource和special都匹配上）

SELECT 
	resource_site.zh_label AS site_label,
	resource_site.int_id AS site_int_id,
	resource_room.zh_label AS room_label,
	resource_room.int_id AS room_int_id,
	site.precinct_id AS site_id,
	site.precinct_name AS site_name,
	room.precinct_id AS room_id,
	room.precinct_name AS room_name,
	specialty_site.zh_label AS specialty_site_label,
	specialty_room.zh_label AS specialty_room_label
FROM 
	t_zz_space_resources resource_site
LEFT JOIN 
	t_zz_space_resources resource_room ON resource_site.int_id = resource_room.related_site
LEFT JOIN 
	t_cfg_precinct site ON site.precinct_id = resource_site.precinct_id
LEFT JOIN 
	t_cfg_precinct room ON room.precinct_id = resource_room.precinct_id
LEFT JOIN 
	t_zz_power_specialty specialty_site ON specialty_site.res_code = resource_site.int_id
LEFT JOIN 
	t_zz_power_specialty specialty_room ON specialty_room.res_code = resource_room.int_id
WHERE 
	resource_room.zh_label IS NOT NULL 
	AND site.precinct_id IS NOT NULL 
	AND room.precinct_id IS NOT NULL 
	AND resource_site.space_type = '101'
	AND resource_room.space_type = '102'
	AND specialty_site.zh_label IS NOT null
	AND specialty_room.zh_label IS NOT null
	
	
查看站点-机房-设备-ip（综资关联情况 -- 用于动环割接、动环测试等地方的资源设备）

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

```



# 03IP申请举例说明

```
将百色-德保-百色测试数据县大旺-百色测试数据县大旺基站无线机房 匹配到综资

SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-05-02';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-05-02-17';
SELECT * FROM t_zz_space_resources where space_type = '101';
SELECT * FROM t_zz_space_resources where int_id = 'SITE-13779' LIMIT 10; 
SELECT * FROM t_zz_power_specialty where res_code = 'SITE-13779'  LIMIT 1000;
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-05-02-17-01';
SELECT * FROM t_zz_space_resources where space_type = '102';
SELECT * FROM t_zz_space_resources where int_id = 'ROOM-8a380d9d42c2f44b014365a827954205' LIMIT 1000; 
SELECT * FROM t_zz_power_specialty where res_code = 'SITE-13779'  LIMIT 1000;
SELECT MAX(id) FROM t_zz_power_specialty;


INSERT INTO `t_zz_power_specialty` (`id`, `res_code`, `zh_label`, `data_time`, `device_id`, `device_type_id`, `device_type`, `device_code`, `related_site`, `related_room`, `lifecycle_status`, `rated_power`, `device_subclass`, `start_time`, `product_name`, `vendor_id`, `power_device_id`, `power_site_level`, `gx_power_site_level`, `estimated_retirement_time`, `create_time`, `sys_no_uuid`, `city_id`, `county_id`, `province_id`, `asset_code`, `device_brand`, `power_monitor_dev_name`, `power_room_type`, `serial_number`, `accept_date`, `factory_number`, `upper_device_name`, `upper_device_type`, `ralated_power_device`) VALUES (40813085, 'ROOM-8a380d9d42c2f44b014365a827954205', '百色测试数据县大旺基站无线机房', '20250901', NULL, 0, NULL, NULL, NULL, NULL, '工程', NULL, NULL, NULL, NULL, NULL, NULL, '通信基站', '普通基站', NULL, '2025-09-02 16:24:13', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);
```



```
查询已有数据

```

