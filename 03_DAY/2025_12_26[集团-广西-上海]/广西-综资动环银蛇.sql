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
	WHERE room.precinct_id like '01-01-08-07-05-01%' AND mete.mete_kind IN (0,1,2)
	AND mete_detail.mete_no IN (0) 
	AND device.device_id = '00441006000000201315'
	LIMIT 10;
	
SELECT * FROM t_cfg_device WHERE device_code = '2025110110';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-07-01-01-02-01';


SELECT * FROM t_cfg_device WHERE device_code = '2025000000000';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-07-01-01-02-01';



SELECT * FROM t_cfg_monitordevice WHERE device_id = '00713006000000201827';
SELECT * FROM t_cfg_fsu WHERE device_id = '00100006011001768642';
SELECT * FROM t_cfg_device WHERE device_id = '00713006000000201827';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-07-01-01-02-01';




select * from t_zz_space_resources where int_id in(
select res_code from t_zz_power_specialty where gx_power_site_level is not null
);

SELECT * FROM t_zz_power_specialty WHERE res_code = 'SITE-13779';
select * from t_zz_space_resources WHERE int_id = 'SITE-13779';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-05-02-17'


SELECT * FROM t_scheduled_task
