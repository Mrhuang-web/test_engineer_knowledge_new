SELECT * FROM t_cfg_precinct WHERE precinct_name = '性能采集机房10_200快1'


# 查询造数表格【currentmonitor-configuration 接口的请求信息】
SELECT 
	device.device_name,
	device.device_id,
	mete_detail.mete_id,
	mete_detail.mete_code,
	mete_detail.mete_kind,
	mete.mete_name,
	mete_detail.mete_no,
	device.device_type,
	dict.dict_note,
	room.precinct_name,
	mete.mete_kind,
	left(dict_mete.dict_note,2)	
FROM t_cfg_device device 
	LEFT JOIN  t_cfg_metemodel_detail mete_detail ON device.device_model = mete_detail.model_id 
	left join t_cfg_mete mete on mete_detail.mete_code = mete.mete_code
	LEFT JOIN t_cfg_dict dict ON dict.dict_code = device.device_type AND dict.col_name = 'device_type'
	LEFT JOIN t_cfg_precinct room ON device.precinct_id = room.precinct_id
	LEFT JOIN t_cfg_dict dict_mete ON dict_mete.dict_code = mete.mete_kind AND dict_mete.col_name = 'mete_kind'
	WHERE room.precinct_id = '01-01-08-04-16-01-12' AND mete.mete_kind IN (0,1,2) 
	AND device.device_id = '00441006000000201315'
	LIMIT 10;
	
	
	


# 查询对应fsu
SELECT 
	device.device_id,
	fsu.address,
	fsu.listen_port,
	device.device_name,
	room.precinct_name,
	room.precinct_id,
	device.device_code
FROM t_cfg_fsu fsu
	LEFT JOIN t_cfg_device device ON fsu.device_id = device.device_id
	LEFT JOIN t_cfg_precinct room ON device.precinct_id = room.precinct_id
	WHERE fsu.address = '10.1.4.194';




# 验证

SELECT * FROM t_cfg_mete where mete_code = '077001' LIMIT 10 ;
SELECT * FROM t_cfg_metemodel_detail where mete_code = '077001' LIMIT 10 ;

SELECT * FROM t_cfg_monitordevice WHERE device_id = '00441006000000200643';
SELECT * FROM t_cfg_device WHERE device_id = '00441006000000200638';
SELECT * FROM t_cfg_fsu WHERE device_id = '00441006000000200638';

SELECT * FROM t_cfg_monitordevice WHERE device_id = '00441006000000200868';

SELECT * FROM device LIMIT 10;
SELECT * FROM device where deviceid = '00001006000000030190' LIMIT 10;
SELECT * FROM t_cfg_device WHERE device_id =  '00001006000000030190' LIMIT 10;





# 指定机房
SELECT 
	device.device_name,
	device.device_id,
	mete_detail.mete_id,
	mete_detail.mete_code,
	mete_detail.mete_kind,
	mete.mete_name,
	mete_detail.mete_no,
	device.device_type,
	dict.dict_note,
	room.precinct_name,
	mete.mete_kind,
	left(dict_mete.dict_note,2)	
FROM t_cfg_device device 
	LEFT JOIN  t_cfg_metemodel_detail mete_detail ON device.device_model = mete_detail.model_id 
	left join t_cfg_mete mete on mete_detail.mete_code = mete.mete_code
	LEFT JOIN t_cfg_dict dict ON dict.dict_code = device.device_type AND dict.col_name = 'device_type'
	LEFT JOIN t_cfg_precinct room ON device.precinct_id = room.precinct_id
	LEFT JOIN t_cfg_dict dict_mete ON dict_mete.dict_code = mete.mete_kind AND dict_mete.col_name = 'mete_kind'
	WHERE room.precinct_id IN ('01-01-08-07-05-01-01','01-01-08-07-05-01-02','01-01-08-07-05-01-03',
	'01-01-08-07-05-01-04','01-01-08-07-05-01-05','01-01-08-07-05-01-06','01-01-08-07-05-01-07','01-01-08-07-05-01-08',
	'01-01-08-07-05-01-09','01-01-08-07-05-01-10') 
	AND mete_detail.mete_kind  = 2 
	AND mete_detail.mete_code NOT IN (007998)
	AND mete_detail.mete_no = '0'