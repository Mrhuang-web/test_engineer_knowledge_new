# 获取token
SELECT * FROM t_cfg_appkey;

# 设备
access_control_device
SELECT * FROM entrance_face_work_ord;
SELECT * FROM entrance_face_success_device;


SELECT * from ods_zz_site LIMIT 10
SELECT * from ods_zz_site_property LIMIT 10

SELECT * FROM t_cfg_fsu WHERE `listen_port` = 10101;
SELECT * FROM t_cfg_device WHERE device_id = '00800000025'


delete FROM entrance_face_work_ord;
delete FROM entrance_face_success_device;