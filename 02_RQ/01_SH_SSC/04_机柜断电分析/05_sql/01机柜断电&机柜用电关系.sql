SELECT mete_code as meteCode, mete_no as meteNo, device_id as deviceId, config_type as configType, type FROM `energy_cabinet_attribute_config` 
WHERE config_type IN (1,2,3) AND TYPE IN (1,2,3) ;


SELECT id, building_id, building_name, room_id, room_name, cabinet_column_id, cabinet_column_name, cabinet_id, cabinet_name, total_current, current1, current2, current3, alert_start_time, alert_total_threshold, alert_single_threshold 
FROM energy_cabinet_poweroutage_current



SELECT * FROM energy_cabinet_poweroutage_current

SELECT * FROM energy_cabinet_poweroutage_history



# 断电配置规则
# 断电规则生效范围
# 机柜断电分析实时表
# 机柜断电分析历史表
# 服务：v2-sc-m-sh-service

SELECT * FROM t_scheduled_task;
SELECT * FROM energy_cabinet_poweroutage_config;
SELECT * FROM energy_cabinet_poweroutage_config_scope;
SELECT * FROM energy_cabinet_poweroutage_current;
SELECT * FROM energy_cabinet_poweroutage_history;
SELECT * FROM cabinet_data_sync_record;

SELECT * FROM energy_cabinet_attribute_config WHERE device_id = '00001006000000154117';






SELECT * FROM energy_cabinet_poweroutage_history ORDER BY alert_end_time DESC;




SELECT * FROM t_cfg_precinct LIMIT 10;
SELECT * FROM t_cfg_precinct WHERE precinct_id LIKE "01-19%"
























# --------------------------------------------------非本次------------------------------------------------------------------



SELECT * FROM t_cfg_precinct LIMIT 10;
SELECT * FROM t_cfg_device LIMIT 10;
SELECT * FROM t_cfg_mete LIMIT 10;
SELECT * FROM t_cfg_metemodel LIMIT 10;
SELECT * FROM t_cfg_metemodel_detail WHERE mete_code = '088304' LIMIT 10;
SELECT * FROM t_cfg_device WHERE mete_code = '088304' LIMIT 10;


SELECT * FROM t_cfg_device a WHERE a.device_model IN (SELECT model_id FROM t_cfg_metemodel_detail WHERE mete_code = '088304')



SELECT a.device_id,b.precinct_name,a.rated_power,b.precinct_id,c.mete_code,a.device_name,a.manufacturer_id,c.up_mete_id,c.mete_no FROM 
t_cfg_device a 
INNER JOIN t_cfg_precinct b ON a.precinct_id=b.precinct_id 
INNER JOIN t_cfg_metemodel_detail c ON a.device_model=c.model_id 
WHERE  a.device_id = '00001006000000154117' AND c.mete_code = '009302'




SELECT  t2.mete_code AS meteCode,p.precinct_name AS precinctName,t1.rated_power,
t1.precinct_id AS precinctId,tm.dict_code AS temperatureMeteType,t1.manufacturer_id AS manufacturer_id,
t2.mete_no AS signalNumber,t1.index_seq AS index_seq,t1.device_id AS 	deviceId,t1.device_name AS deviceName,
t2.up_mete_id AS desc_data,p.air_type AS air_type,d1.site_type AS siteTypeId,p.room_kind AS room_kind,t1.device_type AS deviceType,
t1.device_kind AS device_kind,d1.dc_class AS centerSiteKind,o.dict_note AS airTypeName,u.precinct_name AS siteName,s.dict_note AS centerSiteKindName,
x.precinct_id AS provinceID,r.dict_note AS meteKindName,building.precinct_id AS buildingID,g.dict_note AS climateName,ar.precinct_id AS areid,
y.precinct_name AS cityName,IFNULL(e.dict_note, e1.dict_note) AS siteTypeName,tm.dict_note AS temperatureMeteTypeName,
t2.mete_kind AS meteKind,m.dict_note AS deviceTypeName,y.precinct_id AS cityID,t3.mete_name AS meteName,building.precinct_name AS buildingName,
t3.unit AS unit,n.dict_note AS roomKindName,d1.site_id AS siteid,x.precinct_name AS provinceName,g.dict_code AS climate_type FROM   
t_cfg_device t1 JOIN t_cfg_metemodel_detail t2 ON t1.device_model=t2.model_id AND t1.device_type IN (6,8,87,92,2,11,12,15,17) AND t1.rated_power >'0' 
AND t1.precinct_id LIKE  %(precinct_id)s   
AND t2.mete_code IN ('006309','008318','008319','008320','008338','','008339','008340','008349','008350','008351','011301','012301','015201','015203','015303','015403','017301','002307','002314','002321','087309','092308','092309','092310','092330') 
LEFT JOIN t_cfg_mete t3 ON t2.mete_code = t3.mete_code 
LEFT JOIN t_cfg_precinct p ON p.precinct_id = t1.precinct_id 
LEFT JOIN t_cfg_site d1 ON d1.site_id = CONCAT(LEFT(p.precinct_id, 14)) 
LEFT JOIN t_cfg_precinct u ON u.precinct_id = d1.site_id 
LEFT JOIN t_cfg_dict e ON e.dict_code = d1.site_type   AND e.col_name = 'site_type' 
LEFT JOIN t_cfg_dict e1 ON e1.dict_code = d1.site_type AND e1.col_name = 'site_type' 
LEFT JOIN t_cfg_climate AS f ON LEFT(p.precinct_id, 5) = f.province_id AND LENGTH(f.province_id) = 5 
LEFT JOIN t_cfg_dict g ON g.dict_note = f.climate_type AND g.col_name = 'climate_type' 
LEFT JOIN t_cfg_dict m ON m.dict_code = t1.device_type AND m.col_name = 'deviceType' 
LEFT JOIN t_cfg_dict n ON n.dict_code = p.room_kind AND n.col_name = 'room_kind' 
LEFT JOIN t_cfg_dict o ON o.dict_code = p.air_type AND o.col_name = 'air_type' 
LEFT JOIN t_cfg_dict r ON r.dict_code = t2.mete_kind AND r.col_name = 'mete_kind' 
LEFT JOIN t_cfg_dict s ON s.dict_code = d1.dc_class AND s.col_name = 'centre_site_kind' 
LEFT JOIN t_cfg_dict tm ON tm.dict_code = (SELECT ttmr.mete_remark_type 
FROM t_temperature_mete_remark ttmr WHERE ttmr.device_id = t1.device_id LIMIT 1) AND tm.col_name ='temperature_mete_type' 
LEFT JOIN t_cfg_precinct AS x ON x.precinct_id =LEFT (t1.precinct_id, 5) LEFT JOIN t_cfg_precinct AS y ON y.precinct_id =
LEFT (t1.precinct_id, 8) LEFT JOIN t_cfg_precinct AS ar ON ar.precinct_id =LEFT (t1.precinct_id, 11) 
LEFT JOIN t_cfg_precinct AS building ON  building.precinct_id  !=(SELECT  tcs.site_id 
FROM t_cfg_site tcs WHERE tcs.site_id=u.precinct_id)  AND building.precinct_id=p.up_precinct_id WHERE p.isdel= 0 



SELECT  t2.mete_code AS meteCode,p.precinct_name AS precinctName,t1.rated_power,t1.precinct_id AS precinctId,tm.dict_code AS temperatureMeteType,
t1.manufacturer_id AS manufacturer_id,t2.mete_no AS signalNumber,t1.index_seq AS index_seq,t1.device_id AS 	deviceId,t1.device_name AS deviceName,
t2.up_mete_id AS desc_data,p.air_type AS air_type,d1.site_type AS siteTypeId,p.room_kind AS room_kind,t1.device_type AS deviceType,
t1.device_kind AS device_kind,d1.dc_class AS centerSiteKind,o.dict_note AS airTypeName,u.precinct_name AS siteName, s.dict_note AS centerSiteKindName,
x.precinct_id AS provinceID,r.dict_note AS meteKindName,building.precinct_id AS buildingID,  g.dict_note AS climateName,ar.precinct_id AS areid,
y.precinct_name AS cityName, IFNULL(e.dict_note, e1.dict_note) AS siteTypeName,tm.dict_note AS temperatureMeteTypeName,t2.mete_kind AS meteKind,m.dict_note AS deviceTypeName,
y.precinct_id AS cityID,t3.mete_name AS meteName,building.precinct_name AS buildingName,  t3.unit AS unit,n.dict_note AS roomKindName,d1.site_id AS siteid,
x.precinct_name AS provinceName,g.dict_code AS climate_type  FROM t_cfg_device t1 JOIN t_cfg_metemodel_detail t2 ON t1.device_model=t2.model_id AND 
t1.precinct_id LIKE  '01-01-08-04-12-01%'  AND t2.mete_code IN ('009301') JOIN t_cfg_mete t3 ON t2.mete_code = t3.mete_code 
LEFT JOIN t_cfg_precinct p ON p.precinct_id = t1.precinct_id LEFT JOIN t_cfg_site d1 ON d1.site_id = CONCAT(LEFT(p.precinct_id, 14))
 LEFT JOIN t_cfg_precinct u ON u.precinct_id = d1.site_id LEFT JOIN t_cfg_dict e ON e.dict_code = d1.site_type   AND e.col_name = 'site_type' 
 LEFT JOIN t_cfg_dict e1 ON e1.dict_code = d1.site_type AND e1.col_name = 'site_type' LEFT JOIN t_cfg_climate AS f ON LEFT(p.precinct_id, 5) = f.province_id AND 
 LENGTH(f.province_id) = 5 LEFT JOIN t_cfg_dict g ON g.dict_note = f.climate_type AND g.col_name = 'climate_type' LEFT JOIN t_cfg_dict m ON m.dict_code = t1.device_type 
 AND m.col_name = 'deviceType' LEFT JOIN t_cfg_dict n ON n.dict_code = p.room_kind AND n.col_name = 'room_kind' LEFT JOIN t_cfg_dict o ON o.dict_code = p.air_type 
 AND o.col_name = 'air_type' LEFT JOIN t_cfg_dict r ON r.dict_code = t2.mete_kind AND r.col_name = 'mete_kind' LEFT JOIN t_cfg_dict s ON s.dict_code = d1.dc_class 
 AND s.col_name = 'centre_site_kind' LEFT JOIN t_cfg_dict tm ON tm.dict_code = (SELECT ttmr.mete_remark_type FROM t_temperature_mete_remark ttmr 
 WHERE ttmr.device_id = t1.device_id ) AND tm.col_name ='temperature_mete_type' LEFT JOIN t_cfg_precinct AS x ON x.precinct_id =LEFT (t1.precinct_id, 5) 
 LEFT JOIN t_cfg_precinct AS y ON y.precinct_id =LEFT (t1.precinct_id, 8) LEFT JOIN t_cfg_precinct AS ar ON ar.precinct_id =LEFT (t1.precinct_id, 11) 
 LEFT JOIN t_cfg_precinct AS building ON  building.precinct_id  !=(SELECT  tcs.site_id FROM t_cfg_site tcs WHERE tcs.site_id=u.precinct_id)  
 AND building.precinct_id=p.up_precinct_id WHERE p.isdel= 0 AND t1.device_id= '00001006000000154117'
 
 
 {'precinct_id': '01-01-08-04-12-01%', 'mete_code': '009301', 'device_id': '1006000000154117'
