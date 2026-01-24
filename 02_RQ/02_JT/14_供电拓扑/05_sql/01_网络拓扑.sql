SELECT * FROM zz_data_sync_info;
SELECT * FROM zz_to_rm_rm_area_site;
SELECT * FROM zz_to_rm_rm_area_room;    01-04-01-15-01-01    1842979665   01-08-08-03-07-01-01
SELECT * FROM zz_to_rm_rm_device WHERE device_type LIKE '%电池%';   00751006000005650813

441000000000008088805177


#  查看某个已关联设备，所属站点区域信息
	SELECT city.precinct_name,county.precinct_name,site.precinct_name,room.precinct_name FROM t_cfg_precinct room 
		JOIN t_cfg_precinct site ON room.up_precinct_id = site.precinct_id
		JOIN t_cfg_precinct county ON site.up_precinct_id = county.precinct_id
		JOIN t_cfg_precinct city ON county.up_precinct_id = city.precinct_id
		WHERE room.precinct_id = '01-32-05-05-01-46';
	SELECT city.precinct_name,county.precinct_name,site.precinct_name,room.precinct_name FROM t_cfg_precinct room 
		JOIN t_cfg_precinct site ON room.up_precinct_id = site.precinct_id
		JOIN t_cfg_precinct county ON site.up_precinct_id = county.precinct_id
		JOIN t_cfg_precinct city ON county.up_precinct_id = city.precinct_id
		WHERE room.precinct_id = '01-32-05-05-02';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-05-05-02-28';
		
		
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-03-07-02-01';		
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-03-07-01';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-03-07-01-01';

# 建立站点层级匹配（动环与综资）   
	# site_id :SITE-7b2f9634e97f420db0067d60460beb6d  
	# zh_label:宝鸡麟游常丰镇苏家村村委会用户站点   
	# 匹配逻辑：precinct_name(动环)   -->  zh_label(空间)  --> int_id(空间) --> zh_label(属性表) 
	SELECT * FROM building_area;
	SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州auto数据中心楼栋1';

	# 先确保zz_data_sync_info，批次号与es是否一致
	# external触发：curl --location --request GET 'http://10.12.5.123:31640/migration/v1/zzSyncData/saveZZData?orderIds=SSSP-20241031-000010'
	SELECT * FROM zz_to_rm_rm_area_site;


	# 机房匹配：zg_name:3900844


	# 关联ups设备    01-08-08-03-07-01-01
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-03-07-02-01' AND device_name = 'UPS设备';
	
	# 关联智能电表
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-03-07-02-01' AND device_name = '智能电表';
	
	# 关联UPS配电
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-03-07-02-01' AND device_name = 'UPS配电';
	
	# 关联开关电源
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-03-07-02-01' AND device_name = '开关电源';
	
	# 低压交流配电  
	SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-03-07-01-01' AND device_name like '低压交流配电%';	
	SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002844379';
	SELECT * FROM t_cfg_dict WHERE col_name = 'mete_kind';
	
	SELECT * FROM t_cfg_device WHERE device_name like '五华区昆明高新2号附属楼二楼高低压机房'
	
	
	
	
	
# 关联动环专业内输出分路
	# ups设备： -- res_code:917612135669919744
	
SELECT * FROM t_cfg_topology_v2_configuration 
		where up_precinct_id IN( '01-08-08-03-07-01-01','01-08-08-03-07-02-01') LIMIT 40;
	SELECT * FROM t_cfg_topology_v2_configuration LIMIT 10;
	SELECT * FROM zz_to_rm_rm_device;
	
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-03-07-01-01';
SELECT resource_code FROM t_cfg_device WHERE device_id = '00751006000005652681';

SELECT * FROM t_cfg_topology_v2_configuration where up_device_type LIKE "%电池%" LIMIT 1000;
SELECT * FROM t_cfg_topology_v2_configuration where id = '5270148470';	
SELECT * FROM t_cfg_device WHERE device_id = '00751006000005650806';



SELECT * FROM m_site;
SELECT * FROM m_room WHERE siteid = '2041';
SELECT * FROM m_device WHERE roomid = '204101';
SELECT * FROM m_signal WHERE deviceid = '63906';

SELECT * FROM m_room WHERE siteid = '2042';
SELECT * FROM m_device WHERE roomid = '204201';
SELECT * FROM m_signal WHERE deviceid = '63990';

SELECT * FROM m_device WHERE deviceid = '64661';
SELECT * FROM m_signal WHERE deviceid = '64661';
SELECT * FROM m_signal WHERE siteid IN ('2042')


INSERT INTO `m_signal` (`SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `AlarmLevel`, `Threshold`, `StoragePeriod`, `AbsoluteVal`, `RelativeVal`, `StaticVal`, `Describe`, `NMAlarmID`) 
VALUES ('1', '2042', '63990', 0, '002001', '0', 'A相电压过高告警', 3, 1, NULL, NULL, NULL, NULL, NULL, '601-002-1-002001');


INSERT INTO `m_signal` (`SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `AlarmLevel`, `Threshold`, `StoragePeriod`, `AbsoluteVal`, `RelativeVal`, `StaticVal`, `Describe`, `NMAlarmID`) 
VALUES ('1', '2042', '65924', 0, '002005', '0', 'C相电压过高告警', 3, 1, NULL, NULL, NULL, NULL, NULL, '60002-00-002001');



SELECT * FROM d_activealarm where siteid = '2042'LIMIT 10;
SELECT MAX(id) FROM d_activealarm;   2633190519
SELECT MAX(serialno) FROM d_activealarm;   2633190441
INSERT INTO `d_activealarm` (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `NMAlarmID`, `SerialNo`, `AlarmTime`, `AlarmLevel`, `AlarmStatus`, `AlarmDesc`, `AlarmValue`, `SynNo`, `AlarmRemark`, `rAlertId`, `LscInTime`, `CscInTime`) 
VALUES (2633190479, '1', '2042', '63990', 0, '002001', '0', 'A相电压过高告警', '002001', 2633190442, '2025-12-04 11:07:33', 4, 0, '下限告警-触发值169.5V', 500, 24545837, NULL, NULL, '2025-12-10 11:07:33', '2025-12-10 11:07:33');



SELECT * FROM ci_alarm_sync_history where mete_code = '' LIMIT 10;





SELECT * FROM alert_alerts where room_id like '01-08-08-03-07%' LIMIT 10;