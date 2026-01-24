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
	WHERE fsu.address = '10.8.187.2';
	
	
	

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
	WHERE room.precinct_id = '01-01-07-01-01-02-01' AND mete.mete_kind IN (0,1,2) 
	AND device.device_id = '00001006000000201851'
	LIMIT 10;
	

	
SELECT * FROM fsu;
SELECT * FROM device WHERE fsuid = '2025110110'


SELECT * FROM t_cfg_device WHERE device_id = '00713006000000201924';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000019221';


SELECT * FROM t_cfg_device WHERE device_id = '00713006000000201948';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000019221';