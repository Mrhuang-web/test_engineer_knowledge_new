SELECT * FROM t_cfg_device;
SELECT * FROM t_cfg_fsu;
SELECT * FROM t_cfg_nmsdevice;
SELECT a.device_name,b.* FROM t_cfg_device a INNER JOIN t_cfg_nmsdevice b ON a.device_id=b.device_id limit 100;

# 00001006000000154108  00001006000001531582  00001006000000154619
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000154619';
SELECT * FROM t_cfg_device WHERE device_id = '00001006000001531582';
SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00001006000001531582';

SELECT * FROM t_cfg_fsu WHERE fsu_origin_code = '847272716181'
SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00001006000001531549';