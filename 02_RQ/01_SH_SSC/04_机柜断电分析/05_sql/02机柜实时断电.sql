SELECT * FROM fsu_point_data_20251125;
SELECT * FROM fsu_point_data_20251127;
SELECT * FROM fsu_point_data_20251128;
SELECT * FROM energy_cabinet WHERE precinct_id = '01-01-08-04-07-01-01';


SELECT * FROM energy_cabinet_poweroutage_current;
INSERT INTO `energy_cabinet_poweroutage_current` (`id`, `building_id`, `building_name`, `room_id`, `room_name`, `cabinet_column_id`, `cabinet_column_name`, `cabinet_id`, `cabinet_name`, `total_current`, `current1`, `current2`, `current3`, `alert_start_time`, `alert_total_threshold`, `alert_single_threshold`) VALUES ('b0501892bff64fe5bf72f22aedda8dcc', '01-01-08-04-07-01', '黄某某_上海定制1', '01-01-08-04-07-01-01', '黄某测试数据某_上海定制1', '4684ed368dbc44caa047886dbc064f14', '测试机柜列1', '50c5ec059d464c5e9817285984f87356', '测试机柜1', 27, 9, 9, 9, '2025-11-25 17:35:00', 0.1, 10);


INSERT INTO `fsu_point_data_20251128` (`id`, `meteCode`, `deviceId`, `deviceName`, `signalNumber`, `collectTime`, `measureVal`, `unit`, `meteName`, `precinctID`, `precinctName`, `buildingID`, `buildingName`, `create_time`) VALUES (1, '009301', '00001006000000153964', 'UPS配电', '0', '2025-11-28 14:49:03', 0, 'A', '分路XX相电流Ia', '01-01-08-04-07-01-01', '黄某测试数据某_上海定制1', '01-01-08-04-07-01', '黄某某_上海定制1', '2025-11-28 14:49:03');
INSERT INTO `fsu_point_data_20251128` (`id`, `meteCode`, `deviceId`, `deviceName`, `signalNumber`, `collectTime`, `measureVal`, `unit`, `meteName`, `precinctID`, `precinctName`, `buildingID`, `buildingName`, `create_time`) VALUES (2, '009302', '00001006000000153964', 'UPS配电', '0', '2025-11-28 14:49:03', 0, 'A', '分路XX相电流Ib', '01-01-08-04-07-01-01', '黄某测试数据某_上海定制1', '01-01-08-04-07-01', '黄某某_上海定制1', '2025-11-28 14:49:03');
INSERT INTO `fsu_point_data_20251128` (`id`, `meteCode`, `deviceId`, `deviceName`, `signalNumber`, `collectTime`, `measureVal`, `unit`, `meteName`, `precinctID`, `precinctName`, `buildingID`, `buildingName`, `create_time`) VALUES (3, '009303', '00001006000000153964', 'UPS配电', '0', '2025-11-28 14:49:03', 0, 'A', '分路XX相电流Ib', '01-01-08-04-07-01-01', '黄某测试数据某_上海定制1', '01-01-08-04-07-01', '黄某某_上海定制1', '2025-11-28 14:49:03');





SELECT * FROM cabinet_history;
SELECT * FROM energy_cabinet_poweroutage_current;

INSERT INTO `cabinet_history` (`cabinet_id`, `total_current`, `branch1_current`, `branch2_current`, `branch3_current`, `alarm_satisfied`, `collect_time`, `update_time`) 
VALUES ('50c5ec059d464c5e9817285984f87356', 14, 14, 0, 0, 0, '2025-11-28 21:45:49', '2025-11-28 21:45:49');




SELECT * FROM ( 
	select switch_flag from alert_voice_notify_cfg where switch_flag <> 'N' 
	union ALL 
	select switch_flag from alert_mail_notify_cfg where switch_flag <> 'N' ) a;

select * from alert_voice_notify_cfg;
select * from alert_mail_notify_cfg;









# 批量造数
SELECT * FROM t_cfg_device WHERE device_id = '00001006000000153964';
SELECT * FROM t_cfg_metemodel_detail where model_id = '00001008000000016602' LIMIT 10;


SELECT a.precinct_id,b.cabinet_column_number,b.cabinet_column_name,a.id,a.cabinet_name,a.cabinet_number FROM energy_cabinet a INNER JOIN energy_cabinet_column b ON a.cabinet_column_id=b.id WHERE a.precinct_id = '01-01-08-04-07-01-01' and CHAR_LENGTH(a.cabinet_name)>5 AND CHAR_LENGTH(b.cabinet_column_name)>6   ORDER BY b.cabinet_column_number,a.cabinet_number ASC;


SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id = '50c5ec059d464c5e9817285984f87356';





