SELECT  t2.mete_code AS meteCode,
	p.precinct_name AS precinctName,
	t1.rated_power,
	t1.precinct_id AS precinctId,
	tm.dict_code AS temperatureMeteType,
	t1.manufacturer_id AS manufacturer_id,
	t2.mete_no AS signalNumber,
	t1.index_seq AS index_seq,
	t1.device_id AS 	deviceId,
	t1.device_name AS deviceName,
	t2.up_mete_id AS desc_data,
	p.air_type AS air_type,
	d1.site_type AS siteTypeId,
	p.room_kind AS room_kind,
	t1.device_type AS deviceType,
	t1.device_kind AS device_kind,
	d1.dc_class AS centerSiteKind,
	o.dict_note AS airTypeName,
	u.precinct_name AS siteName,
	s.dict_note AS centerSiteKindName,
	x.precinct_id AS provinceID,
	r.dict_note AS meteKindName,
	building.precinct_id AS buildingID,
	g.dict_note AS climateName,
	ar.precinct_id AS areid,
	y.precinct_name AS cityName,
	IFNULL(e.dict_note, e1.dict_note) AS siteTypeName,
	tm.dict_note AS temperatureMeteTypeName,
	t2.mete_kind AS meteKind,
	m.dict_note AS deviceTypeName,
	y.precinct_id AS cityID,
	t3.mete_name AS meteName,
	building.precinct_name AS buildingName,
	t3.unit AS unit,
	n.dict_note AS roomKindName,
	d1.site_id AS siteid,
	x.precinct_name AS provinceName,
	g.dict_code AS climate_type
FROM   t_cfg_device t1
 JOIN t_cfg_metemodel_detail t2 ON t1.device_model=t2.model_id AND t1.device_type IN (6,8,87,92,2,11,12,15,17) AND t1.rated_power >'0' AND t1.precinct_id LIKE  :precinct_id   AND t2.mete_code IN ('006309','008318','008319','008320','008338','','008339','008340','008349','008350','008351','011301','012301','015201','015203','015303','015403','017301','002307','002314','002321','087309','092308','092309','092310','092330')
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
 LEFT JOIN t_cfg_dict tm ON tm.dict_code = (SELECT ttmr.mete_remark_type FROM t_temperature_mete_remark ttmr WHERE ttmr.device_id = t1.device_id LIMIT 1) AND tm.col_name ='temperature_mete_type'
 LEFT JOIN t_cfg_precinct AS x ON x.precinct_id =LEFT (t1.precinct_id, 5)
 LEFT JOIN t_cfg_precinct AS y ON y.precinct_id =LEFT (t1.precinct_id, 8)
 LEFT JOIN t_cfg_precinct AS ar ON ar.precinct_id =LEFT (t1.precinct_id, 11)
 LEFT JOIN t_cfg_precinct AS building ON  building.precinct_id  !=(SELECT  tcs.site_id FROM t_cfg_site tcs WHERE tcs.site_id=u.precinct_id)  AND building.precinct_id=p.up_precinct_id
 WHERE p.isdel= 0 ;


SELECT  t2.mete_code AS meteCode,
	p.precinct_name AS precinctName,
	t1.rated_power,
	t1.precinct_id AS precinctId,
	tm.dict_code AS temperatureMeteType,
	t1.manufacturer_id AS manufacturer_id,
	t2.mete_no AS signalNumber,
	t1.index_seq AS index_seq,
	t1.device_id AS 	deviceId,
	t1.device_name AS deviceName,
	t2.up_mete_id AS desc_data,
	p.air_type AS air_type,
	d1.site_type AS siteTypeId,
	p.room_kind AS room_kind,
	t1.device_type AS deviceType,
	t1.device_kind AS device_kind,
	d1.dc_class AS centerSiteKind,
	o.dict_note AS airTypeName,
	u.precinct_name AS siteName, 
	s.dict_note AS centerSiteKindName,
	x.precinct_id AS provinceID,
	r.dict_note AS meteKindName,
	building.precinct_id AS buildingID,  
	g.dict_note AS climateName,
	ar.precinct_id AS areid,
	y.precinct_name AS cityName, 
	IFNULL(e.dict_note, e1.dict_note) AS siteTypeName,
	tm.dict_note AS temperatureMeteTypeName,
	t2.mete_kind AS meteKind,
	m.dict_note AS deviceTypeName,
	y.precinct_id AS cityID,
	t3.mete_name AS meteName,
	building.precinct_name AS buildingName,  
	t3.unit AS unit,
	n.dict_note AS roomKindName,
	d1.site_id AS siteid,
	x.precinct_name AS provinceName,
	g.dict_code AS climate_type 
FROM t_cfg_device t1
 JOIN t_cfg_metemodel_detail t2 ON t1.device_model=t2.model_id AND t1.precinct_id LIKE  CONCAT(:precinct_id, '%%') AND t2.mete_code IN (:mete_code)
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
 LEFT JOIN t_cfg_dict tm ON tm.dict_code = (SELECT ttmr.mete_remark_type FROM t_temperature_mete_remark ttmr WHERE ttmr.device_id = t1.device_id ) AND tm.col_name ='temperature_mete_type'
 LEFT JOIN t_cfg_precinct AS x ON x.precinct_id =LEFT (t1.precinct_id, 5)
 LEFT JOIN t_cfg_precinct AS y ON y.precinct_id =LEFT (t1.precinct_id, 8)
 LEFT JOIN t_cfg_precinct AS ar ON ar.precinct_id =LEFT (t1.precinct_id, 11)
 LEFT JOIN t_cfg_precinct AS building ON  building.precinct_id  !=(SELECT  tcs.site_id FROM t_cfg_site tcs WHERE tcs.site_id=u.precinct_id)  AND building.precinct_id=p.up_precinct_id
 WHERE p.isdel= 0 AND t1.device_id= :device_id;



SELECT  t2.mete_code AS meteCode,
	p.precinct_name AS precinctName,
	t1.rated_power,
	t1.precinct_id AS precinctId,
	tm.dict_code AS temperatureMeteType,
	t1.manufacturer_id AS manufacturer_id,
	t2.mete_no AS signalNumber,
	t1.index_seq AS index_seq,
	t1.device_id AS 	deviceId,
	t1.device_name AS deviceName,
	t2.up_mete_id AS desc_data,
	p.air_type AS air_type,
	d1.site_type AS siteTypeId,
	p.room_kind AS room_kind,
	t1.device_type AS deviceType,
	t1.device_kind AS device_kind,
	d1.dc_class AS centerSiteKind,
	o.dict_note AS airTypeName,
	u.precinct_name AS siteName, 
	s.dict_note AS centerSiteKindName,
	x.precinct_id AS provinceID,
	r.dict_note AS meteKindName,
	building.precinct_id AS buildingID,  
	g.dict_note AS climateName,
	ar.precinct_id AS areid,
	y.precinct_name AS cityName, 
	IFNULL(e.dict_note, e1.dict_note) AS siteTypeName,
	tm.dict_note AS temperatureMeteTypeName,
	t2.mete_kind AS meteKind,
	m.dict_note AS deviceTypeName,
	y.precinct_id AS cityID,
	t3.mete_name AS meteName,
	building.precinct_name AS buildingName,  
	t3.unit AS unit,
	n.dict_note AS roomKindName,
	d1.site_id AS siteid,
	x.precinct_name AS provinceName,
	g.dict_code AS climate_type 
FROM t_cfg_device t1   
 JOIN t_cfg_metemodel_detail t2 ON t1.device_model=t2.model_id AND t1.precinct_id LIKE  CONCAT(:precinct_id, '%%') AND t2.mete_code IN (:mete_code)
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
 LEFT JOIN t_cfg_dict tm ON tm.dict_code = (SELECT ttmr.mete_remark_type FROM t_temperature_mete_remark ttmr WHERE ttmr.device_id = t1.device_id ) AND tm.col_name ='temperature_mete_type'
 LEFT JOIN t_cfg_precinct AS x ON x.precinct_id =LEFT (t1.precinct_id, 5)
 LEFT JOIN t_cfg_precinct AS y ON y.precinct_id =LEFT (t1.precinct_id, 8)
 LEFT JOIN t_cfg_precinct AS ar ON ar.precinct_id =LEFT (t1.precinct_id, 11)
 LEFT JOIN t_cfg_precinct AS building ON  building.precinct_id  !=(SELECT  tcs.site_id FROM t_cfg_site tcs WHERE tcs.site_id=u.precinct_id)  AND building.precinct_id=p.up_precinct_id
 WHERE p.isdel= 0
 limit 1;




SELECT  aah.cancel_people AS cancel_people,
	IFNULL(e.dict_note, e1.dict_note) AS siteType,
	aah.alert_start_time AS alert_start_time,
	aah.cancel_remark AS cancel_remark,
	t1.device_type AS deviceType,
	aah.threshold AS threshold,
	t1.precinct_id AS source_room,
	aah.force_clear_reason AS force_clear_reason,
	aah.order_status AS order_status,
	aah.index_seq AS index_seq,
	aah.biz_sys AS biz_sys,
	aah.mete_name AS mete_name,
	aah.classify_type AS classify_type,
	aah.alert_id AS alert_id,
	aah.engineering_status AS engineering_status,
	aah.alert_level AS alert_level,
	aah.alert_explain AS alert_explain,
	aah.order_type AS order_type,
	aah.status_masks AS status_masks,
	aah.cancel_time AS cancel_time,
	aah.third_party_flag AS third_party_flag,
	t1.device_id AS device_id,
	aah.task_flag AS task_flag,
	aah.create_time AS create_time,
	ar.precinct_id AS precinct_id,
	aah.object_id AS object_id,
	x.precinct_name AS provinceName,
	aah.lsc_id AS lsc_id,
	u.precinct_name AS siteName,
	p.precinct_name AS room_name,
	CONCAT(y.precinct_name, '#', ar.precinct_name) AS full_name,
	aah.change_plan AS change_plan,
	aah.source_clear_alert_id AS source_clear_alert_id,
	aah.fixed AS fixed,
	aah.confirm_people AS confirm_people,
	aah.order_id AS order_id,
	aah.serial_no AS serial_no,
	t1.precinct_id AS room_id   ,
	n.dict_note AS roomKindName   ,
	aah.raw_mete_code AS raw_mete_code,
	aah.remark AS remark,
	aah.alert_type AS alert_type,
	t1.device_name AS  device_name,
	y.precinct_name AS cityName,
	aah.source_alert_id AS source_alert_id,
	aah.sub_logical_type AS sub_logical_type,
	m.dict_note AS deviceTypeName,
	t2.mete_id AS mete_id,
	aah.confirm_remark AS confirm_remark,
	aah.object_type AS object_type,
	aah.force_clear AS force_clear,
	aah.lsc_name AS lsc_name,
	aah.raw_mete_name AS raw_mete_name,
	aah.r_alert_id AS r_alert_id,
	t1.manufacturer_name AS manufacturer_name,
	t2.mete_code AS mete_code,
	aah.confirm_state AS confirm_state,
	aah.confirm_time AS confirm_time,
	aah.clear_value AS clear_value,
	aah.is_standard_level AS is_standard_level,
	aah.cur_moni_time AS cur_moni_time,
	aah.cur_moni_time AS cur_moni_time,
	aah.logical_type AS logical_type,
	aah.namespace AS namespace,
	aah.alert_reason AS alert_reason,
	u.precinct_name AS siteName   
FROM t_cfg_device t1   
 JOIN t_cfg_metemodel_detail t2 ON t1.device_model=t2.model_id AND t2.mete_code IN (:mete_code)
 LEFT JOIN t_cfg_mete t3 ON t2.mete_code = t3.mete_code
 LEFT JOIN t_cfg_precinct p ON p.precinct_id = t1.precinct_id
 LEFT JOIN t_cfg_site d1 ON d1.site_id = CONCAT(LEFT(p.precinct_id, 14))
 LEFT JOIN t_cfg_precinct u ON u.precinct_id = d1.site_id
 LEFT JOIN alert_alerts_his aah   ON  t1.precinct_id=aah.room_id AND  aah.mete_code=:mete_code1  AND aah.device_name=t1.device_name
 LEFT JOIN t_cfg_dict e ON e.dict_code = d1.site_type   AND e.col_name = 'site_type'
 LEFT JOIN t_cfg_dict e1 ON e1.dict_code = d1.site_type AND e1.col_name = 'site_type'
 LEFT JOIN t_cfg_climate AS f ON LEFT(p.precinct_id, 5) = f.province_id AND LENGTH(f.province_id) = 5
 LEFT JOIN t_cfg_dict g ON g.dict_note = f.climate_type AND g.col_name = 'climate_type'
 LEFT JOIN t_cfg_dict m ON m.dict_code = t1.device_type AND m.col_name = 'deviceType'
 LEFT JOIN t_cfg_dict n ON n.dict_code = p.room_kind AND n.col_name = 'room_kind'
 LEFT JOIN t_cfg_dict o ON o.dict_code = p.air_type AND o.col_name = 'air_type'
 LEFT JOIN t_cfg_dict r ON r.dict_code = t2.mete_kind AND r.col_name = 'mete_kind'
 LEFT JOIN t_cfg_dict s ON s.dict_code = d1.dc_class AND s.col_name = 'centre_site_kind'
 LEFT JOIN t_cfg_dict tm ON tm.dict_code = (SELECT ttmr.mete_remark_type FROM t_temperature_mete_remark ttmr WHERE ttmr.device_id = t1.device_id ) AND tm.col_name ='temperature_mete_type'
 LEFT JOIN t_cfg_precinct AS x ON x.precinct_id =LEFT (t1.precinct_id, 5)
 LEFT JOIN t_cfg_precinct AS y ON y.precinct_id =LEFT (t1.precinct_id, 8)
 LEFT JOIN t_cfg_precinct AS ar ON ar.precinct_id =LEFT (t1.precinct_id, 11)
 LEFT JOIN t_cfg_precinct AS building ON  building.precinct_id  !=(SELECT  tcs.site_id FROM t_cfg_site tcs WHERE tcs.site_id=u.precinct_id)  AND building.precinct_id=p.up_precinct_id
 WHERE p.isdel= 0  AND t1.device_id = :device_id
 LIMIT 1  ;





SELECT  t2.mete_code AS meteCode,
	p.precinct_name AS precinctName,
	t1.rated_power,
	t1.precinct_id AS precinctId,
	tm.dict_code AS temperatureMeteType,
	t1.manufacturer_id AS manufacturer_id,
	t2.mete_no AS signalNumber,
	t1.index_seq AS index_seq,
	t1.device_id AS 	deviceId,
	t1.device_name AS deviceName,
	t2.up_mete_id AS desc_data,
	p.air_type AS air_type,
	d1.site_type AS siteTypeId,
	p.room_kind AS room_kind,
	t1.device_type AS deviceType,
	t1.device_kind AS device_kind,
	d1.dc_class AS centerSiteKind,
	o.dict_note AS airTypeName,
	u.precinct_name AS siteName,
	s.dict_note AS centerSiteKindName,
	x.precinct_id AS provinceID,
	r.dict_note AS meteKindName,
	building.precinct_id AS buildingID,
	g.dict_note AS climateName,
	ar.precinct_id AS areid,
	y.precinct_name AS cityName,
	IFNULL(e.dict_note, e1.dict_note) AS siteTypeName,
	tm.dict_note AS temperatureMeteTypeName,
	t2.mete_kind AS meteKind,
	m.dict_note AS deviceTypeName,
	y.precinct_id AS cityID,
	t3.mete_name AS meteName,
	building.precinct_name AS buildingName,
	t3.unit AS unit,
	n.dict_note AS roomKindName,
	d1.site_id AS siteid,
	x.precinct_name AS provinceName,
	g.dict_code AS climate_type
 FROM   t_cfg_device t1
 JOIN t_cfg_metemodel_detail t2 ON t1.device_model=t2.model_id AND t1.device_type IN (2,4,6,8,9,78,88,87,92,2,11,12,15,17)   AND t1.precinct_id LIKE  :precinct_id
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
 LEFT JOIN t_cfg_dict tm ON tm.dict_code = (SELECT ttmr.mete_remark_type FROM t_temperature_mete_remark ttmr WHERE ttmr.device_id = t1.device_id LIMIT 1) AND tm.col_name ='temperature_mete_type'
 LEFT JOIN t_cfg_precinct AS x ON x.precinct_id =LEFT (t1.precinct_id, 5)
 LEFT JOIN t_cfg_precinct AS y ON y.precinct_id =LEFT (t1.precinct_id, 8)
 LEFT JOIN t_cfg_precinct AS ar ON ar.precinct_id =LEFT (t1.precinct_id, 11)
 LEFT JOIN t_cfg_precinct AS building ON  building.precinct_id  !=(SELECT  tcs.site_id FROM t_cfg_site tcs WHERE tcs.site_id=u.precinct_id)  AND building.precinct_id=p.up_precinct_id
 WHERE p.isdel= 0 ;
