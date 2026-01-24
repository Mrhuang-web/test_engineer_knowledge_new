SELECT a.precinct_id,b.cabinet_column_number,b.cabinet_column_name,a.id,a.cabinet_name,a.cabinet_number FROM energy_cabinet a INNER JOIN energy_cabinet_column b ON a.cabinet_column_id=b.id WHERE a.precinct_id = '01-01-08-04-07-01-01' and CHAR_LENGTH(a.cabinet_name)>5 AND CHAR_LENGTH(b.cabinet_column_name)>6   ORDER BY b.cabinet_column_number,a.cabinet_number ASC;



INSERT INTO `energy_cabinet_attribute_config` (`id`, `cabinet_id`, `mete_code`, `mete_no`, `up_mete_id`, `device_id`, `name`, `power_source`, `config_type`, `type`, `update_time`, `update_user`, `data_type`) VALUES ('0e984772acd74c79aad78b84816a0124', '2ced2ebbef944943919398bbed4089c2', '009303', '0', '分路XX相电流Ic', '00001006000000153964', '黄某测试数据某_上海定制1/黄某某_上海定制1/黄某测试数据某_上海定制1/UPS配电/分路XX相电流Ic', NULL, 3, 2, '2025-11-21 15:35:35', 'alauda', '2');
INSERT INTO `energy_cabinet_attribute_config` (`id`, `cabinet_id`, `mete_code`, `mete_no`, `up_mete_id`, `device_id`, `name`, `power_source`, `config_type`, `type`, `update_time`, `update_user`, `data_type`) VALUES ('86302e1b38c546ab849e7215b9e6347f', '2ced2ebbef944943919398bbed4089c2', '009302', '0', '分路XX相电流Ib', '00001006000000153964', '黄某测试数据某_上海定制1/黄某某_上海定制1/黄某测试数据某_上海定制1/UPS配电/分路XX相电流Ib', NULL, 2, 2, '2025-11-21 15:35:35', 'alauda', '2');
INSERT INTO `energy_cabinet_attribute_config` (`id`, `cabinet_id`, `mete_code`, `mete_no`, `up_mete_id`, `device_id`, `name`, `power_source`, `config_type`, `type`, `update_time`, `update_user`, `data_type`) VALUES ('8a50a5d52e3f48a886b5627314b5de2c', '2ced2ebbef944943919398bbed4089c2', '009301', '0', '分路XX相电流Ia', '00001006000000153964', '黄某测试数据某_上海定制1/黄某某_上海定制1/黄某测试数据某_上海定制1/UPS配电/分路XX相电流Ia', NULL, 1, 2, '2025-11-21 15:35:35', 'alauda', '2');


SELECT * FROM energy_cabinet;
SELECT * FROM energy_cabinet_column;

SELECT * FROM cabinet_history;

INSERT INTO `cabinet_history` (`cabinet_id`, `total_current`, `branch1_current`, `branch2_current`, `branch3_current`, `alarm_satisfied`, `collect_time`, `update_time`) 
VALUES ('2ced2ebbef944943919398bbed4089c2', 14, 14, 0, 0, 0, '2025-11-28 21:45:49', '2025-11-28 23:10:49');





 SELECT DISTINCT e.id as cabinetId, e.cabinet_name as cabinetName, e.precinct_id as roomId, p1.precinct_name as roomName, p2.precinct_id as buildingId, p2.precinct_name as buildingName, e.cabinet_column_id as cabinetColumnId, co.cabinet_column_name as cabinetColumnName 
	 FROM energy_cabinet e 
	 JOIN t_cfg_precinct p1 ON e.precinct_id = p1.precinct_id 
	 LEFT JOIN t_cfg_precinct p2 ON p1.up_precinct_id = p2.precinct_id 
	 LEFT JOIN energy_cabinet_column co ON e.cabinet_column_id = co.id 
	 JOIN energy_cabinet_attribute_config config ON e.id = config.cabinet_id WHERE config.type = '2';
	 
 
 SELECT id as id, cabinet_id, mete_code as meteCode, mete_no as meteNo, device_id as deviceId, config_type as configType, type 
 FROM `energy_cabinet_attribute_config` WHERE config_type IN (1,2,3) AND TYPE IN (1,2,3);


 SELECT * FROM energy_cabinet_attribute_config;
 SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id = '4684ed368dbc44caa047886dbc064f14';
 


 SELECT * FROM energy_cabinet_column WHERE id = '4684ed368dbc44caa047886dbc064f14';
 SELECT * FROM energy_cabinet WHERE cabinet_number = '7368997111368785920';
 SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id = '50c5ec059d464c5e9817285984f87356';




 SELECT * FROM energy_cabinet_attribute_config ;
 
 SELECT a.precinct_id,b.cabinet_column_number,b.cabinet_column_name,a.id,a.cabinet_name,a.cabinet_number FROM energy_cabinet a INNER JOIN energy_cabinet_column b ON a.cabinet_column_id=b.id WHERE a.precinct_id = '01-01-08-04-07-01-01' and CHAR_LENGTH(a.cabinet_name)>5 AND CHAR_LENGTH(b.cabinet_column_name)>6   
 AND a.id NOT IN ( '4684ed368dbc44caa047886dbc064f14','2ced2ebbef944943919398bbed4089c2')
 ORDER BY b.cabinet_column_number,a.cabinet_number ASC;
 
 
 
 SELECT * FROM energy_cabinet_attribute_config WHERE NAME LIKE  '黄某测试数据某_上海定制1/黄某某_上海定制1/黄某测试数据某_上海定制1/UPS配电/分路XX相电%' AND 
 	cabinet_id NOT IN ('4684ed368dbc44caa047886dbc064f14','2ced2ebbef944943919398bbed4089c2');
 
 delete FROM energy_cabinet_attribute_config WHERE NAME LIKE  '黄某测试数据某_上海定制1/黄某某_上海定制1/黄某测试数据某_上海定制1/UPS配电/分路XX相电%' AND 
 	cabinet_id NOT IN ('4684ed368dbc44caa047886dbc064f14','2ced2ebbef944943919398bbed4089c2');
 	
 	
 	
 	
 	
 	
 	
 	
 	
 	
 	
 	
 	
	


 SELECT * FROM energy_cabinet_column WHERE id = '99c9c49617244c24b71681ea23af30f5';
 SELECT * FROM energy_cabinet WHERE cabinet_number = '7393278556639600640';
 SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id = '2ced2ebbef944943919398bbed4089c2';
 
 
 SELECT * FROM energy_cabinet_column WHERE id = '99c9c49617244c24b71681ea23af30f5';
 SELECT * FROM energy_cabinet WHERE id = '8509da1e9c034309ad5c198ff1d22606';
 
 
 SELECT * FROM cabinet_history;