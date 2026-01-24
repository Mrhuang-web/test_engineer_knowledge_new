INSERT INTO `t_cfg_fsu` (`device_id`, `access_device_id`, `address`, `listen_port`, `up_fsu_id`, `up_link_port`, `net_type`, `net_info`, `fsu_state`, `register_server`, `udp_port`, `new_version`, `user_name`, `pass_word`, `ftp_port`, `ftp_proxy`, `http_proxy_url`, `fsu_origin_code`) 
VALUES ('0081300613121900', '000010061231231900', '10.12.5.142', 10011, NULL, NULL, 0, NULL, 0, NULL, NULL, NULL, NULL, NULL, NULL, 0, NULL, '12314121900');

INSERT INTO `t_cfg_device` (`lsc_id`, `device_id`, `device_name`, `precinct_id`, `device_index`, `device_cid`, `isdel`, `device_model`, `device_kind`, `sub_device_kind`, `device_type`, `sub_device_type`, `belong_device_id`, `device_code`, `manufacturer_id`, `device_use_state`, `purchase_time`, `use_time`, `use_years`, `update_time`, `install_site`, `device_principal`, `x`, `y`, `manufacturer_name`, `description`, `version`, `locate_ne_status`, `resource_code`, `leader_phone`, `resource_origin`, `resource_name`, `index_seq`, `use_end_time`, `rated_power`, `load_power`, `device_mark`, `unit`, `rectifierModuleNumber`, `singleModuleRatedCurrent`, `province_index`, `related_rackpos`, `access_type`, `actual_start_time`, `join`, `brand`, `manufacturer`, `battery_single_number`, `battery_single_voltage`, `module_count`, `back_module_count`, `sigle_module_info`, `confirm_content`, `confirm_time`, `convert_efficiency`, `design_reserve_length`, `battery_number`, `max_discharge_efficiency`, `battery_type`, `protocol_convert_type`, `dev_describe`, `power_device_id`, `status`, `sys_no`) 
VALUES ('1', '0081300613121900', '测试设备10015', '01-01-10-02-01-01', 1, NULL, 000, '00001008000000011900', 13, NULL, 76, 1, NULL, '124141231900', 1617, 1, NULL, NULL, NULL, '2026-01-06 09:41:19', NULL, NULL, NULL, NULL, '中兴力维', NULL, 'V1.0', NULL, NULL, NULL, NULL, NULL, 10101900, NULL, NULL, NULL, NULL, NULL, 0, 0, 101, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);


SELECT * FROM t_cfg_fsu WHERE address = '10.12.5.142';
SELECT * FROM t_cfg_device WHERE device_name  LIKE '测试设备100%';


SELECT * FROM access_control_device;
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-10-02-01-01'
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-10';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-10-02';
SELECT * FROM access_control_device WHERE ip_address = '10.12.5.142' AND `PORT` BETWEEN 10014 AND 10019

DELETE FROM access_control_device WHERE ip_address = '10.12.5.142' AND `PORT` BETWEEN 10014 AND 10019


SELECT * FROM  cabinet_history
SELECT * FROM energy_cabinet_poweroutage_current

SELECT cabinet.id FROM energy_cabinet cabinet LEFT JOIN t_cfg_precinct room ON cabinet.precinct_id = room.precinct_id 
left join t_cfg_precinct building on room.up_precinct_id = building.precinct_id WHERE room.precinct_id like '01-01-08-04-16%'


# 门禁卡授权任务
SELECT * FROM entrance_card_auth_task;
# 门禁设备表
SELECT * FROM access_control_device;
# 门禁授权表
SELECT * FROM entrance_card_auth;

SELECT * FROM access_control_event;

SELECT * FROM t_cfg_precinct WHERE precinct_id LIKE '01-01-08-04-16-01%'







SELECT * FROM t_cfg_fsu WHERE address = '10.12.5.142';
SELECT * FROM t_cfg_device WHERE device_name  LIKE '测试设备100%';
SELECT * FROM access_control_device WHERE ip_address = '10.12.5.142' AND `PORT` BETWEEN 10011 AND 10019













"id"	"cabinet_id"	"mete_code"	"mete_no"	"up_mete_id"	"device_id"	"name"	"power_source"	"config_type"	"type"	"update_time"	"update_user"	"data_type"
"101843d665834f5bb9d3509c4f16f9b2"	"f17155de00264610b4387219b443c3ee"	"012301"	"3"	"回风温度"	"00713006000000201911"	"性能采集测试站点/性能采集测试楼栋/性能采集机房2/中央空调末端/回风温度"	\N	"2"	"2"	"2026-01-08 14:01:47"	"alauda"	"2"
"7082b1c2fcf54d9a91ef4c119744191e"	"f17155de00264610b4387219b443c3ee"	"013302"	"4"	"线电压Ubc"	"00713006000000201912"	"性能采集测试站点/性能采集测试楼栋/性能采集机房2/中央空调主机/线电压Ubc"	\N	"1"	"2"	"2026-01-08 14:01:47"	"alauda"	"2"
"9ac3d78ab59f46948020e4be2db7b145"	"f17155de00264610b4387219b443c3ee"	"013301"	"3"	"线电压Uab"	"00713006000000201912"	"性能采集测试站点/性能采集测试楼栋/性能采集机房2/中央空调主机/线电压Uab"	\N	"3"	"2"	"2026-01-08 14:01:47"	"alauda"	"2"




DELETE FROM cabinet_history;
DELETE FROM fsu_point_data_20260108;

SELECT * FROM fsu_point_data_20260108 WHERE collecttime = '2026-01-08 16:35:00'; 
SELECT * FROM  cabinet_history ;

SELECT * FROM energy_cabinet_poweroutage_current;

00713006000000201906
00713006000000201923

SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id IN
(SELECT cabinet_id FROM cabinet_history)

SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id IN
('577745d0b97249c98d6ef0a4027f6cdc')


SELECT * FROM energy_cabinet WHERE id = '1afc1fea94e94325a494e10b88906243'


SELECT * FROM t_cfg_precinct WHERE precinct_name = '性能采集机房2'






# 01-01-08-04-13-01
SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id = '1e2541aa416f4db48e75ec5f5a1f6045'





SELECT * FROM energy_cabinet
SELECT cabinet.id FROM energy_cabinet cabinet LEFT 
JOIN t_cfg_precinct room ON cabinet.precinct_id = room.precinct_id  
WHERE room.precinct_id = '01-01-08-04-13-01'



SELECT * FROM fsu_point_data_20260108



SELECT * FROM energy_cabinet_attribute_config




SELECT id,cabinet_conifg.mete_code AS mete_code,cabinet_conifg.device_id,cabinet_conifg.mete_no 
FROM energy_cabinet_attribute_config as cabinet_conifg 
LEFT JOIN energy_cabinet as cabinet ON cabinet_conifg.cabinet_id = cabinet.id
WHERE cabinet.precinct_id like '01-01-08-04-13-01%'




cabinet_history 数据
SELECT ch.*, e.precinct_id AS room_id
FROM cabinet_history ch
JOIN energy_cabinet e ON ch.cabinet_id = e.id
JOIN energy_cabinet_poweroutage_config_scope s ON e.precinct_id = s.room_id;

SELECT * FROM energy_cabinet WHERE id = '1afc1fea94e94325a494e10b88906243';



SELECT * FROM t_cfg_dict WHERE col_name = 'device_type'
SELECT * from t_cfg_fsu
SELECT * FROM t_cfg_device WHERE device_id = '00100006011001768697'



SELECT *
FROM entrance_guard_device 
SELECT * FROM t_cfg_device WHERE device_id = '58585804499006000005125530'


SELECT * FROM t_cfg_fsu WHERE address = '你的ip' AND `PORT` = '你的端口'
拿到device_id
SELECT device_code FROM t_cfg_device WHERE device_id = '你拿到的'


SELECT * FROM t_cfg_fsu WHERE address = '192.168.100.101'









SELECT * FROM access_control_device;


SELECT * FROM t_cfg_device WHERE device_id 
	IN (
		SELECT device_id FROM t_cfg_fsu WHERE `listen_PORT` = '1001'
	)
	
SELECT * FROM t_cfg_device WHERE device_code = '20250125';	
SELECT * FROM t_cfg_fsu



20251231000000
SELECT * FROM zz_data_sync_info;

SELECT * FROM zz_to_rm_rm_area_site WHERE batch_num = '20200723';

SELECT * FROM zz_to_rm_rm_area_room WHERE batch_num = '20200723';

SELECT * FROM zz_to_rm_rm_area_room WHERE batch_num = '20250723';


SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
SELECT * FROM t_cfg_device WHERE precinct_id LIKE "01-08-08-01-02-01%" AND device_type = '3' AND power_device_id =
'1001001001001' ;


SELECT * FROM zz_to_rm_rm_area_room LIMIT 10;


SELECT * FROM zz_to_rm_rm_device WHERE power_device_id = "1001001001002";
SELECT * FROM zz_to_rm_rm_device WHERE precinct_id LIKE "01-08-08-01-02-01%" ;
SELECT * FROM t_cfg_device WHERE device_id = '00751006000005629492';

update t_cfg_device SET power_device_id = '' WHERE precinct_id LIKE "01-08-08-01-02-01%"

SELECT * FROM t_cfg_device where device_id = '00800000026' LIMIT 10;
SELECT * FROM t_cfg_fsu WHERE device_id = '00800000026';