# 广西现网问题
SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM overdue_device_detail where resource_device_type_name != device_type_name GROUP BY resource_device_type_name LIMIT 100;





# 00001006000000154452  250904测试设备 20250904102653
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000154452'
SELECT * FROM t_cfg_device WHERE 








SELECT * from t_cfg_dict LIMIT 10;
SELECT * FROM t_cfg_dict WHERE col_name = 'mete_kind' LIMIT 10;

SELECT d.dict_code,d.dict_note,c.* FROM (SELECT b.dict_note,a.* FROM t_cfg_mete a INNER JOIN  t_cfg_dict b ON a.device_type = b.dict_code
WHERE b.col_name = 'device_type') c 
INNER JOIN t_cfg_dict d ON  c.mete_kind = d.dict_code
WHERE d.col_name = 'mete_kind' AND mete_code IN ('021204')


SELECT * FROM 

SELECT b.dict_code,b.dict_note,a.* FROM t_cfg_mete a INNER JOIN t_cfg_dict b ON  a.mete_kind = b.dict_code WHERE b.col_name = 'mete_kind'



# res_code填铅酸设备的res_code,    
# ralated_power_device填开关电源设备的res_code
# 在t_zz_power_device、t_zz_switch_power 拿完插到t_zz_lead_acid_battery
SELECT * FROM t_zz_power_device;
SELECT * FROM t_zz_switch_power;
SELECT * FROM t_zz_lead_acid_battery WHERE res_code = '161_2028_202801_1757389432';  # 锂电
SELECT * FROM t_zz_lead_acid_battery WHERE ralated_power_device = '161_2028_1432';










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



SELECT * FROM t_ol_device LIMIT 10;



SELECT  * FROM zz_resource_device_analys LIMIT 10
SELECT device_type FROM zz_resource_device_analys GROUP BY device_type;




SELECT * FROM t_cfg_dict WHERE col_name = 'zz_device_type';





