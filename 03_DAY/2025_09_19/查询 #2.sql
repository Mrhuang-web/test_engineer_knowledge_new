SELECT * FROM t_cfg_fsu WHERE fsu_origin_code = '847272716181';
SELECT * FROM t_cfg_nmsdevice;

SELECT * FROM t_cfg_device;
SELECT * FROM t_cfg_fsu;
SELECT b.device_name,a.* FROM t_cfg_nmsdevice a INNER JOIN t_cfg_device b WHERE a.device_id = b.device_id AND b.device_id = '00001006000001531581';


SELECT * FROM alarm_record_log


SELECT * FROM t_cfg_device WHERE device_id = '00771006000002944984'
SELECT * FROM t_cfg_fsu WHERE device_id = '00771006000002945668'
SELECT * FROM t_cfg_mete LIMIT 10 WHERE device_id = '00771006000002945668'
SELECT * FROM t_cfg_metemodel LIMIT 10;
SELECT * FROM t_cfg_metemodel_detail LIMIT 10;



SELECT * FROM t_zz_power_specialty LIMIT 10;
SELECT * FROM t_zz_power_device LIMIT 10;
SELECT * FROM t_zz_power_device_sys LIMIT 10;
SELECT * FROM t_zz_lead_acid_battery LIMIT 10;

SELECT * FROM zz_resource_device_analys LIMIT 10;

SELECT * FROM overdue_device_detail LIMIT 10;


SELECT * FROM t_cfg_precinct  WHERE precinct_name = '黄某某_上海定制6'
SELECT * FROM t_cfg_device LIMIT 10;


SELECT * FROM t_cfg_device WHERE device_name LIKE '%黄某某%';
SELECT * FROM t_cfg_fsu  WHERE device_id = '00001006000000154147';
SELECT * FROM t_ol_device LIMIT 10;


SELECT * FROM t_cfg_device WHERE device_id = '00001006000001531549'


SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00001006000001531549'

SELECT * FROM t_cfg_device WHERE device_code = '0081300600026157'




SELECT * FROM t_zz_power_device LIMIT 10





