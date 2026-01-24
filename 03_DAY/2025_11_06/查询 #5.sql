SELECT * FROM t_cfg_topology_config;
SELECT * FROM t_cfg_topology_config_part WHERE site_id = '01-07-05-07-53';


`gx-spider`
SELECT * FROM overdue_device_type_dict WHERE device_type = '变压器';

SELECT p.update_cycle,p.*
FROM overdue_device_detail p
WHERE p.device_type_name = '变压器' AND p.device_sub_type_name = '非晶合金变压器' 
LIMIT 100;

# 中央空调主机  中央空调主机
# UPS配电 UPS电池开关柜
# UPS设备 UPS设备01
# 低压交流配电 低压出线柜

SELECT device_type FROM t_zz_power_specialty  GROUP BY device_type LIMIT 10 ;
SELECT device_type FROM t_zz_power_device GROUP BY device_type;
SELECT * FROM t_cfg_device WHERE device_name = '高压直流电源配电' LIMIT 10;



SELECT * FROM t_overdue_service_life_config 


SELECT * FROM t_gathering_config_device 
ORDER BY CREATE_time desc
WHERE union_id = '671bcded-5e0b-4af5-a54a-3a4627e6b3e4'; 










 select a.res_code              as resCode,
               a.device_id             as deviceId,
               a.zh_label              as deviceName,
               a.related_site          as relatedSite,
               c.system_rated_capacity as systemRatedCapacity,
               c.system_code           as systemCode
        from t_zz_power_device_sys a
        join t_zz_space_resources b on a.related_site = b.int_id
        left join t_zz_ups_system c on a.res_code = c.res_code
        where a.device_type_id = 201 and b.precinct_id = '01-07-10-02-01'



SELECT * FROM t_cfg_device WHERE precinct_id = '01-07-10-02-01'  LIMIT 10; 
SELECT * FROM t_cfg_precinct  WHERE precinct_id = '01-07-21-01-01-03' LIMIT 10;










SELECT * FROM t_cfg_fsu LIMIT 10
SELECT * FROM t_cfg_cserverinfo LIMIT 10


SELECT * FROM t_cfg_device WHERE precinct_id = '01-07-21-01-01-04-01'  LIMIT 30;
SELECT * FROM t_cfg_devicesys  WHERE up_id = '01-07-21-01-01-04'  LIMIT 10;
SELECT * FROM t_cfg_devicesys WHERE devicesys_id = 'd341464eeaa54425a6dcc3c34f61ef43';


# 01-07-21-01-01-04
SELECT * FROM t_zz_power_device_sys LIMIT 10;
SELECT * FROM t_zz_space_resources LIMIT 10;
SELECT * FROM t_zz_space_resources where related_site is not null LIMIT 10;
SELECT * FROM t_zz_power_device_sys where related_site = '07977e6db645423bb8b61a3fd1ccb542' LIMIT 10;
SELECT * FROM t_zz_power_device_sys LIMIT 10
SELECT * FROM t_zz_power_device_sys where zh_label = '%UPS%' LIMIT 10;
SELECT * FROM t_zz_power_device_sys where device_type_id = 201 LIMIT 10;


SELECT * FROM t_zz_ups_system WHERE res_code = '02b13412a9ec461d900b7091a4549590'



# 要改的
# related_site SITE-386fe67f6e834a15abdb64d013d88503
SELECT * FROM t_zz_power_device_sys where res_code = '02b13412a9ec461d900b7091a4549590'



# 要改的
SELECT * FROM t_zz_power_device_sys where related_site = '07977e6db645423bb8b61a3fd1ccb542' LIMIT 10;



# 要改的
# precinct_id:01-07-21-01-01-01
# related_site SITE-ff8080815f04e571015fae1b63f42dc1
# int_id  空
SELECT * FROM t_zz_space_resources WHERE zh_label = '柳州城中区东祥福苑路灯杆'



# 要改的
# related_site 07977e6db645423bb8b61a3fd1ccb542
# int_id  448184474aac43019e85cf354c2af1c5
SELECT * FROM t_zz_space_resources WHERE zh_label = '柳州鹿寨县金科集美江山普通汇聚站点传输机房'










SELECT DISTINCT CASE WHEN c.pe_entity_type = 1 THEN 1 WHEN c.pe_entity_type = 3 THEN 2 END AS chargeType
FROM t_cfg_device a
LEFT JOIN t_cfg_devicesys_detail b ON a.device_id = b.sub_id
LEFT JOIN t_cfg_devicesys c ON c.devicesys_id = b.devicesys_id
WHERE a.isdel = 0 AND (c.up_id = '01-07-21-01-01-04' OR c.up_id LIKE CONCAT('01-07-21-01-01-04','%')) 
AND c.pe_entity_type in (1,3)

SELECT * FROM t_gathering_config_device WHERE site_id = '01-07-21-01-01-04'

SELECT devicesys_name deviceSystemName, sys.devicesys_id deviceSystemId, d.rated_power systemRatedCapacity
FROM t_cfg_device d
LEFT JOIN device_es_mete m ON d.device_id = m.device_id AND m.is_normal != 'N'
LEFT JOIN t_cfg_devicesys_detail de ON de.sub_id = d.device_id AND m.sys_id = de.devicesys_id
LEFT JOIN t_cfg_devicesys sys ON de.devicesys_id = sys.devicesys_id
WHERE 1=1 AND sys.pe_entity_type = 1 AND d.precinct_id LIKE CONCAT('01-07-21-01-01-04','%') 
AND sys.devicesys_id IS NOT NULL
GROUP BY sys.devicesys_id


SELECT a.res_code AS resCode, a.device_id AS deviceId, a.zh_label AS deviceName, a.related_site AS relatedSite, 
c.system_rated_capacity AS systemRatedCapacity, c.system_code AS systemCode
FROM t_zz_power_device_sys a
JOIN t_zz_space_resources b ON a.related_site = b.int_id
LEFT JOIN t_zz_ups_system c ON a.res_code = c.res_code
WHERE a.device_type_id = 201 AND b.precinct_id = '01-07-21-01-01-04'


# a
SELECT * FROM t_zz_power_device_sys where res_code = '02b13412a9ec461d900b7091a4549590'
# b
SELECT * FROM t_zz_space_resources WHERE zh_label = '柳州城中区东祥福苑路灯杆'
# c
SELECT * FROM t_zz_ups_system WHERE res_code = '02b13412a9ec461d900b7091a4549590'









SELECT DISTINCT
 e.related_site AS siteId,
 r.zh_label AS siteName,
 e.related_device AS deviceName,
 e.down_device_type AS parentDeviceType,e.down_device_name,
 ( SELECT res_code FROM t_zz_power_device d WHERE d.zh_label = e.related_device AND d.related_site = e.related_site ) AS resCode 
FROM
 t_zz_branch_dynamic_env e
 LEFT JOIN t_zz_space_resources r ON r.int_id = e.related_site 
WHERE
 e.down_device_type NOT IN ( '发电机组', '变压器' ) 
 AND e.related_site = '448184474aac43019e85cf354c2af1c5' 
 AND e.down_device_name IN ( 'c9b5c989b5bf409da4e9a9bf74b6ba2f' )
 
 
SELECT * FROM t_zz_branch_dynamic_env where related_site = 'SITE-e212790d07b04ff8b79c76e59cd2218f' LIMIT 10
SELECT * FROM t_cfg_devicesys WHERE up_id = '01-07-21-01-01-04'
SELECT * FROM t_cfg_devicesys WHERE up_id = '01-07-10-02-01'



 
 # 需修改
 # 南宁高新第一生产楼
 # precinct_id = '01-07-10-04-14'
 # 01-07-21-01-01-04
SELECT * FROM t_zz_space_resources WHERE zh_label = '南宁高新第一生产楼'

SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-10-02-01'
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-21-01-01-04'










SELECT c.id AS id, SUBSTRING_INDEX(c.node_level,'-', -1) AS seq, c.device_name AS deviceName, 
c.parent_device_name AS parentDeviceName, c.device_type AS deviceType, 
CONCAT(CONVERT(c.device_charge_load_rate * 100, DECIMAL (18, 2)),'%') AS deviceChargeLoadRate, 
c.node_level nodeLevel, c.number
FROM capacity_electric_estimate a
LEFT JOIN capacity_electric_budget b ON a.id = b.estimate_id
LEFT JOIN capacity_electric_budget_device c ON b.id = c.budget_id
WHERE a.id = 422 AND b.id = 384 AND c.id IS NOT NULL
ORDER BY c.node_level ASC






SELECT * FROM d_signalh where siteid = 2026 LIMIT 10;

SELECT * FROM d_signalh where id = '1496549194' LIMIT 10;
SELECT * FROM m_signal LIMIT 10;


explain SELECT * FROM d_signalh WHERE (id between 1496000000 AND 1500000000)  AND siteid = 2025  LIMIT 1000


DELETE FROM d_signalh WHERE (id between 1496000000 AND 1500000000)  AND siteid IN (2025,2026,2027)
explain DELETE FROM d_signalh WHERE (id between 1416000000 AND 1470000000)  AND siteid IN (2025,2026,2027)
DELETE FROM d_signalh WHERE (id between 1540000000 AND 1545000000)  AND siteid IN (2025,2026,2027)


SELECT * FROM m_device WHERE deviceid = '57743'

SELECT * FROM  m_device where roomid = 202507 and devicename = '系统参数'