SELECT * FROM t_cfg_dict where col_name = 'building_type' LIMIT 100;
SELECT * FROM t_cfg_dict where dict_note = 'IDC机房' LIMIT 100;
SELECT * FROM t_cfg_dict where col_name = 'site_type' LIMIT 100;
SELECT * FROM t_cfg_dict WHERE col_name = 'electricity_type'
SELECT * FROM energy_device_mete_item_202502 WHERE precinct_id = '01-01-03-01-02-10';

# 快速找字段所在表
SELECT 
    c.TABLE_SCHEMA AS '数据库',
    c.TABLE_NAME AS '表名',
    t.TABLE_COMMENT AS '表注释',
    c.COLUMN_NAME AS '字段名',
    c.COLUMN_COMMENT AS '字段注释'  -- 可选添加
FROM INFORMATION_SCHEMA.COLUMNS c
JOIN INFORMATION_SCHEMA.TABLES t
    ON c.TABLE_SCHEMA = t.TABLE_SCHEMA
    AND c.TABLE_NAME = t.TABLE_NAME
WHERE c.COLUMN_NAME LIKE '%lsc_id%'
  AND c.TABLE_SCHEMA = 'spider' 
  AND c.COLUMN_COMMENT LIKE "%用电%";



# 能耗月报表 -- 月度统计表  -device_sum it用电量  01-24-09-04-03   01-24-09-04-03-02

# 月度统计表   -- 区域下按站点类型进行统计了
SELECT * FROM energy_month_summary WHERE area_id = '01-24-09-04' 
AND time BETWEEN  "2025-01" AND "2025-01" AND site_type != 1;

SELECT SUM(pri_device_electric) FROM date_migration_energy_daily WHERE site_id = '01-24-09-04-01' AND DAY BETWEEN '2025-01-01' AND '2025-01-31';


# 01-24-09-04-03-02-15
SELECT * FROM t_cfg_device WHERE precinct_id = '01-24-09-04-03-02-15';
SELECT * FROM t_cfg_mete LIMIT 100;


SELECT SUM(a.cost_ele) FROM energy_device_mete_202501 AS a
INNER JOIN t_cfg_precinct AS b ON a.precinct_id = b.precinct_id
WHERE a.precinct_id = '01-24-09-04-01' AND b.building_type IN (1,2) 
AND device_id IN ('00611006000004591154','00611006000004591155','00611006000004591159','00611006000004591160'
,'00611006000004591209','00611006000004591209','00611006000002822492','00611006000002822493','00611006000002822497',
'00611006000002822502','00611006000002822508','00611006000002822509','00611006000002822510','00611006000002822511',
'00611006000002822512','00611006000004558199','00611006000004558200','00611006000004558201','00611006000004319382');

SELECT SUM(cost_ele) FROM energy_device_mete_202501 WHERE device_id = '00611006000004319384';

LIMIT 100;
SELECT SUM(cost_ele) FROM energy_device_mete_202501 where precinct_id = '01-24-09-04-01' LIMIT 100;


SELECT * FROM t_temperature_mete_detail LIMIT 100;

SELECT * FROM t_cfg_device LIMIT 100;











# 找到满足机房为IDC生产楼栋且配置了用电关系
SELECT room_kind,* from t_cfg_precinct WHERE up_precinct_id IN ("01-01-03-01-02");







# 设备对应表
SELECT * FROM t_cfg_device LIMIT 100;
SELECT * from date_migration_energy_daily WHERE site_id = '01-01-03-01-02'
AND day BETWEEN '2025-02-01' AND '2025-02-28';



# 用电关系
SELECT * FROM energy_formula_config_his LIMIT 100;


# 能耗月报表 -- 月度统计表  -当天数值
SELECT * FROM capacity LIMIT 100;
SELECT * FROM energy_station_building_day_mpp WHERE time BETWEEN "2025-02-01" AND "2025-02-28"
precinct_id IN ("01-01-03-01-02")
AND day BETWEEN "2025-02-01" AND "2025-02-28" AND smps_total_currentele IS NOT NULL;


SELECT * FROM date_migration_energy_daily LIMIT 100; WHERE precinct_id = '01-01-03-01-02-10';







SELECT * FROM user WHERE name = 'alauda';
SELECT * FROM roles_user;
SELECT * FROM user_site_type WHERE ldap_id = 'hjj11';
SELECT * FROM department_user;






SELECT a.precinct_id as roomId, site.precinct_name as siteName, a.precinct_name as roomName, 
building.precinct_name as buildingName, b.precinct_id as cityId, b.precinct_name as cityName, 
c.precinct_id as provinceId, c.precinct_name as provinceName, d.site_type as siteTypeId, 
e.dict_note as siteType, f.climate_type AS climateCondition, p.dict_note as roomKind, 
ifnull(tcd.dict_note,'无') as cloudRoomType FROM t_cfg_precinct AS a 
LEFT JOIN t_cfg_precinct b on LEFT(a.precinct_id,8) = b.precinct_id AND LENGTH(b.precinct_id) = 8 
LEFT JOIN t_cfg_precinct c on LEFT(a.precinct_id,5) = c.precinct_id AND LENGTH(c.precinct_id) = 5 
left join t_cfg_precinct as building on a.up_precinct_id = building.precinct_id and building.precinct_kind = 3 
left join t_cfg_precinct as site on ifnull(building.up_precinct_id,a.up_precinct_id) = site.precinct_id and site.precinct_kind = 2 
LEFT JOIN t_cfg_site d ON d.site_id = site.precinct_id LEFT JOIN t_cfg_dict e ON e.dict_code = d.site_type AND e.col_name = 'site_type' 
LEFT JOIN t_cfg_city_climate AS f ON LEFT(a.precinct_id,8) = f.city_id AND LENGTH(f.city_id) = 8 
LEFT JOIN t_cfg_dict g on g.dict_note = f.climate_type and g.col_name = 'climate_type' 
LEFT JOIN t_cfg_dict p on p.dict_code = a.room_kind and p.col_name = 'room_kind' 
left join hashrate_information hi on hi.precinct_id = a.precinct_id and hi.month = 6 
left join t_cfg_dict tcd on tcd.col_name = 'cloud_room_type' and tcd.dict_code = hi.cloud_room_type 
WHERE a.isdel = 0 AND a.precinct_kind = '5' AND ( a.precinct_id like CONCAT(?,'%') ) 
and ( a.precinct_id like concat(?,'%') or a.precinct_id like CONCAT(?,'%') ) 
and d.site_type in ( ? , ? ) and a.room_kind in ( ? ) LIMIT ?



