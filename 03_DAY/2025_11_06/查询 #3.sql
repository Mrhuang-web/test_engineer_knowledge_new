# 超期详情表归类 -- 看综资设备和子类的情况
SELECT resource_device_type_name,device_type_name,device_sub_type_name 
FROM overdue_device_detail group by device_type_name,device_sub_type_name LIMIT 200


# 目前新增表字段 -- 查看对应的数据项是否一致（是否存在缺失）
SELECT * FROM t_overdue_service_life_config GROUP BY device_type,device_sub_type;

UPDATE overdue_device_detail SET update_cycle = 9 WHERE device_sub_type_name = '分立开关电源' ;
UPDATE overdue_device_detail SET update_cycle = 8 WHERE device_sub_type_name = '壁挂开关电源' ;
UPDATE overdue_device_detail SET update_cycle = 7 WHERE device_sub_type_name = '开关电源01' ;
UPDATE overdue_device_detail SET update_cycle = 6 WHERE device_sub_type_name = '开关电源02' ;
UPDATE overdue_device_detail SET update_cycle = 6 WHERE device_sub_type_name = '组合开关电源' ;

delete from t_overdue_service_life_config;



SELECT * FROM overdue_device_type_dict



SELECT resource_device_type_name AS deviceType, NULL AS deviceSubType, MAX(CASE WHEN site_type = 1 THEN update_cycle END) AS siteTypeDc, MAX(CASE WHEN site_type = 2 THEN update_cycle END) AS siteTypeJl, MAX(CASE WHEN site_type = 3 THEN update_cycle END) AS siteTypeJd, MAX(CASE WHEN site_type = 4 THEN update_cycle END) AS siteTypeJz, 1 AS isEnabled
FROM overdue_device_detail
WHERE resource_device_type_name IS NOT NULL AND resource_device_type_name != ''
GROUP BY resource_device_type_name UNION



SELECT resource_device_type_name AS deviceType, device_sub_type_name AS deviceSubType, MAX(CASE WHEN site_type = 1 THEN update_cycle END) AS siteTypeDc, MAX(CASE WHEN site_type = 2 THEN update_cycle END) AS siteTypeJl, MAX(CASE WHEN site_type = 3 THEN update_cycle END) AS siteTypeJd, MAX(CASE WHEN site_type = 4 THEN update_cycle END) AS siteTypeJz, 1 AS isEnabled
FROM overdue_device_detail
WHERE resource_device_type_name IS NOT NULL AND resource_device_type_name != '' AND device_sub_type_name IS NOT NULL AND device_sub_type_name != ''
GROUP BY resource_device_type_name, device_sub_type_name
ORDER BY deviceType, deviceSubType





# 查看具体设备子类周期年限
SELECT device_name,device_type_name,device_sub_type_name,update_cycle,site_type_name 
FROM overdue_device_detail WHERE device_sub_type_name = '开关电源锂电池'
GROUP BY device_sub_type_name,site_type_name,update_cycle




SELECT device_name,device_type_name,device_sub_type_name,update_cycle,site_type,site_type_name 
FROM overdue_device_detail 
WHERE device_sub_type_name = '开关电源锂电池' AND 
site_type = 1
site_type_name = '数据中心'



SELECT resource_device_type_name,device_type_name,device_sub_type_name,site_type,update_cycle
FROM overdue_device_detail 
group by device_type_name,device_sub_type_name,site_type,max(update_cycle) 
LIMIT 500



SELECT * FROM t_cfg_topology_config_part;
SELECT * FROM t_cfg_topology_config;



SELECT *
FROM overdue_device_detail LIMIT 10;


SELECT *
FROM overdue_device_detail
WHERE device_type_name = '开关电源' AND device_sub_type_name = '分立开关电源' AND site_type = '2'
AND run_time < 1

SELECT *
FROM overdue_device_detail
WHERE device_type_name = '开关电源' AND device_sub_type_name = '分立开关电源' AND site_type = '4'
AND run_time < 1


SELECT *
FROM overdue_device_detail
WHERE device_type_name = '开关电源' AND device_sub_type_name = '分立开关电源' AND site_type = '4'
AND overdue_type = 2


SELECT *
FROM overdue_device_detail
WHERE device_type_name = '开关电源' AND device_sub_type_name = '分立开关电源' AND site_type = '4'
AND overdue_type = 1 AND run_time <= 4.2


SELECT *
FROM overdue_device_detail
WHERE device_type_name = '开关电源' AND device_sub_type_name = '分立开关电源' AND site_type = '4'
AND overdue_type = 4 AND run_time < 3




SELECT *
FROM overdue_device_detail
WHERE device_type_name = '高压配电' AND device_sub_type_name = '高压计量柜' AND site_type = '2'
AND overdue_type = 4 AND run_time < 3





SELECT * FROM overdue_device_detail WHERE device_code = '07c57152165a4d6aaf091ef9abfc2403'


SELECT * FROM t_cfg_dict WHERE col_name = 'overdue_type'


SELECT * FROM t_zz_power_specialty WHERE zh_label = '百色测试数据二节点'


SELECT * FROM t_zz_power_specialty WHERE power_site_level IS NOT NULL LIMIT 10;


SELECT * FROM t_zz_power_specialty LIMIT 10



SELECT MAX(update_cycle) FROM  t_overdue_service_life_config WHERE device_type_name = '开关电源' LIMIT 10