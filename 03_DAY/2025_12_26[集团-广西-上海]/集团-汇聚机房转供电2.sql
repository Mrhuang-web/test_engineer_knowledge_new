SELECT * FROM t_scheduled_task;
SELECT * FROM zz_data_sync_info;

delete from zz_to_rm_agg_convergence_site;


SELECT res_code FROM zz_to_rm_site_property_copy1219;




SELECT res_code FROM zz_to_rm_site_property;
SELECT * FROM zz_to_rm_site_property LIMIT 10;
SELECT * FROM zz_to_rm_site_property where int_id = '-993085341' LIMIT 10;
SELECT * FROM zz_to_rm_site_property where power_ LIMIT 10;


SELECT * FROM zz_to_rm_agg_convergence_site;



核心机楼
UPDATE zz_to_rm_site_propertyzz_to_rm_site_property_copy1219 SET power_site_level = '通信机楼' WHERE int_id = '-993085341'



SELECT * FROM t_cfg_device WHERE device_id = '00001006000000201851';
SELECT * FROM t_cfg_fsu WHERE device_id = '00001006000000201851' ;




# 137050845982925094

SELECT * FROM zz_to_rm_agg_convergence_site WHERE province_id = '310000' AND power_site_level = '传输节点'
 GROUP BY site_name;
 
SELECT * FROM zz_to_rm_site_property LIMIT 10;

SELECT COUNT(*) FROM zz_to_rm_site_property WHERE power_site_level not IN( '通信基站') AND province_id IS NOT NULL
AND city_id IS NOT NULL AND county_id IS NOT NULL and power_site_level IS NOT NULL;


SELECT COUNT(*) FROM zz_to_rm_site_property WHERE power_site_level = '通信基站';



SELECT * FROM t_cfg_fsu WHERE 

SELECT u.device_id, u.address, u.listen_port, u.udp_port, u.new_version, u.user_name, u.pass_word, u.ftp_port, u.ftp_proxy, u.http_proxy_url, d.manufacturer_id, d.device_code
FROM t_cfg_fsu u,t_cfg_device d
WHERE u.device_id=d.device_id AND d.isdel = 0


# 9054086   # 10017254
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-01-11-01-02';

SELECT * FROM t_cfg_dict WHERE col_name = 'device_type'

# 10017254
SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-01-11-01-02';

# - 10017246
SELECT * FROM t_cfg_device WHERE device_id = '00751006000005648509';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002844392' AND mete_code = '012325';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002848261' AND mete_code = '012340';

SELECT * FROM t_cfg_device WHERE device_id = '00751006000005648467';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002844392' AND mete_code = '013323';


# 设备-10017187    机房-9054084
SELECT * FROM t_cfg_device WHERE device_id = '00751006000005648397';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-01-11-01-01';



SELECT * FROM m_site WHERE siteid = '2028';
SELECT * FROM m_room WHERE roomid = '202801';
SELECT * FROM m_device WHERE roomid = '202801' AND devicetype = '12' AND deviceid = '60135';
SELECT * FROM m_signal WHERE deviceid = '60135';


# 中央空调
SELECT * FROM m_device WHERE roomid = '202801' AND devicetype = '13' AND deviceid = '60133';  
SELECT * FROM m_signal WHERE deviceid = '60133' AND signalid = '013323';

INSERT INTO `m_signal` (`SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `AlarmLevel`, `Threshold`, `StoragePeriod`, `AbsoluteVal`, `RelativeVal`, `StaticVal`, `Describe`, `NMAlarmID`) 
VALUES ('1', '2028', '60133', 2, '013205', '5', '出水温度', 4, 1, NULL, NULL, NULL, NULL, NULL, '');




SELECT * FROM fact_dwd_signal_value LIMIT 1;

SELECT * FROM fact_dwd_signal_value WHERE 
device_id = '10017187' AND device_spatial_id = '9054084' 
AND LEFT(signal_start_time,10) = '2025-12-10'
LIMIT 10000;


SELECT * FROM d_signalh WHERE id BETWEEN 3070034685 AND 3072034685; 

INSERT INTO `fact_dwd_signal_value` (`signal_meta_code`, `device_id`, `signal_number`, `signal_value`, `signal_start_time`, `send_time`, `chief_spatial_id`, `device_spatial_id`) 
VALUES ('012339', 10017187, '5', 10.578, '2025-12-10 04:00:00', '2024-08-15 14:03:12', 12766, 9054084);
INSERT INTO `fact_dwd_signal_value` (`signal_meta_code`, `device_id`, `signal_number`, `signal_value`, `signal_start_time`, `send_time`, `chief_spatial_id`, `device_spatial_id`) 
VALUES ('012339', 10017187, '5', 20.578, '2025-12-10 12:00:00', '2024-08-15 14:03:12', 12766, 9054084);
INSERT INTO `fact_dwd_signal_value` (`signal_meta_code`, `device_id`, `signal_number`, `signal_value`, `signal_start_time`, `send_time`, `chief_spatial_id`, `device_spatial_id`) 
VALUES ('012339', 10017187, '5', 30.578, '2025-12-10 20:00:00', '2024-08-15 14:03:12', 12766, 9054084);


INSERT INTO `fact_dwd_signal_value` (`signal_meta_code`, `device_id`, `signal_number`, `signal_value`, `signal_start_time`, `send_time`, `chief_spatial_id`, `device_spatial_id`) 
VALUES ('012340', 10017187, '1', 10.578, '2025-12-10 03:59:00', '2024-08-15 14:03:12', 12766, 9054084);
INSERT INTO `fact_dwd_signal_value` (`signal_meta_code`, `device_id`, `signal_number`, `signal_value`, `signal_start_time`, `send_time`, `chief_spatial_id`, `device_spatial_id`) 
VALUES ('012340', 10017187, '1', 10.578, '2025-12-10 04:00:00', '2024-08-15 14:03:12', 12766, 9054084);



SELECT * FROM dws_liquid_cooling_mete_detail_day WHERE LEFT(signal_start_time,10) > '2025-12-10' AND mete_code = '013206'

show all routine LOAD



SELECT * FROM t_cfg_monitordevice WHERE device_id =  "00713006000000201850";
SELECT * FROM t_cfg_device WHERE device_id = '00713006000000201850';
SELECT * FROM t_cfg_fsu WHERE device_id = '00100006011001768642';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000019221'






# 设备-10017187    机房-9054084 - dim_spatial
SELECT * FROM fact_dwd_signal_value WHERE LEFT(signal_start_time,10) >= '2025-12-20' AND mete_code = '013323'
# 9054086   # 10017254
SELECT * FROM fact_dwd_signal_value WHERE LEFT(signal_start_time,10) = '2025-08-01' AND signal_meta_code = '013323'





SELECT * FROM dws_liquid_cooling_mete_detail_day WHERE LEFT(signal_start_time,10) = '2025-08-02' AND mete_code = '013206' 
AND LEFT(signal_start_time,10) <= '2025-08-02' AND  mete_code = '013323'


SELECT (38.48+37.83+38.88+33.52) 
SELECT (33.27+32.65+33.26+38.31+31.35) 
SELECT (35.59+33.27+32.65+33.26+38.31) 
SELECT (36.69+37.66+31.41+30.07+33.79) / 5
SELECT (32.34+32.63+36.47+33.84+36.38) / 5

SELECT (35.37+34.18+35.93+35.28) / 4