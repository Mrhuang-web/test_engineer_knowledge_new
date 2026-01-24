-- 6200900009301000001
-- 6200900009301000001
SELECT c.* from t_cfg_metemodel_detail c JOIN 
	(SELECT b.device_model,a.* FROM energy_cabinet_attribute_config a INNER JOIN t_cfg_device b ON a.device_id = b.device_id LIMIT 10) AS ONE ON 
	c.model_id = ONE.device_model WHERE ONE.device_id = '00001006000000154079' AND c.mete_code = '009301';


SELECT * FROM t_cfg_device WHERE device_model = "00001008000000018855"
SELECT * FROM t_cfg_mete LIMIT 10;
SELECT * FROM t_cfg_metemodel LIMIT 10;



SELECT device_type,mete_id,mete_code,up_mete_id,mete_kind,mete_no FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000018855' AND up_mete_id IN ('分路XX相电流Ia','分路XX相电流Ib','分路XX相电流Ic','分路XX相电压Ua',
'分路XX相电压Ub','分路XX相电压Uc','分路XX有功功率Pa','分路XX有功功率Pb','分路XX有功功率Pc');


SELECT a.precinct_id,b.cabinet_column_number,b.cabinet_column_name,a.id,a.cabinet_name,a.cabinet_number FROM energy_cabinet a INNER JOIN energy_cabinet_column b ON a.cabinet_column_id=b.id WHERE a.precinct_id = '01-01-08-04-15-G97-02' and CHAR_LENGTH(a.cabinet_name)>5 AND CHAR_LENGTH(b.cabinet_column_name)>6   ORDER BY b.cabinet_column_number,a.cabinet_number ASC;
SELECT * FROM energy_cabinet_attribute_config WHERE NAME LIKE "黄某某_上海断电测试站点/上海楼栋1/上海机房1/UPS配电04/%";



SELECT device_id,device_name FROM t_cfg_device WHERE device_model = "00001008000000018855" and CHAR_LENGTH(device_name) > 8;


SELECT * FROM fsu_point_data_20250923 LIMIT 10;
