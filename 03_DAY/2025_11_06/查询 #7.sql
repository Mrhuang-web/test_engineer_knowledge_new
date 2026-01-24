SELECT * FROM m_device WHERE siteid IN (2026) 
SELECT * FROM m_signal WHERE deviceid = '58213'

SELECT * FROM t_cfg_fsu WHERE fsu_origin_code = '20251105000'
SELECT * FROM t_cfg_nmsdevice
SELECT * FROM t_cfg_device WHERE device_id = '00001006000000154226'


SELECT device_name from t_cfg_device where device_id  IN (SELECT device_id FROM t_cfg_nmsdevice )

SELECT 


SELECT * FROM t_cfg_device WHERE device_name = 'B接口汕头代理'




SELECT * FROM t_cfg_fsu WHERE access_device_id = '00001006000001531581'
SELECT * FROM t_cfg_nmsdevice WHERE device_id = '00001006000001531581'
SELECT * FROM t_cfg_device WHERE device_id = '00001006000001531581'