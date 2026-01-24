# 补充：precint 找dim_xxx  找到mpp里面机房信息  -- 在找到devcie_spatixxx




# 中间库-cinterdb_400_jt_gz
SELECT * FROM m_site WHERE siteid IN ('2034')
SELECT * FROM m_room where siteid IN ('2034');
SELECT * FROM m_site where siteid IN ('2031','2032','2033');
SELECT * FROM m_room where siteid IN ('2031','2032','2033');
SELECT * FROM m_room WHERE roomid IN ('203201')
SELECT * FROM m_device WHERE roomid IN ('203101')
SELECT * FROM m_signal where siteid = '2026' and deviceid IN ('013405')
SELECT * FROM m_site where siteid IN ('2028','2029','2030');
SELECT * FROM m_room where siteid IN ('2028','2029','2030');
SELECT * FROM m_device WHERE roomid IN ('202801')
SELECT * FROM m_device WHERE deviceid IN ('60121')
SELECT * FROM m_signal where deviceid IN ('57604')
SELECT * FROM m_signal where deviceid IN (SELECT deviceid FROM m_device WHERE roomid IN ('202801')) AND signalid IN ('013351', '013352', '013353', '012325', '012318', '012321', '013323'
            , '013330', '012326', '012329', '012333', '012339', '012340', '012334', '012345', '012344', '013405')
SELECT * FROM m_signal where signalid IN ('012344') LIMIT 10;

SELECT MAX(id) FROM d_signalh
SELECT * FROM d_signalh where id BETWEEN 1115224971 and 1115947031 AND siteid IN (2028,2029,2030)LIMIT 1000

SELECT * FROM d_signalh WHERE id BETWEEN 1105024971 and 1125997031 AND siteid IN ('2028')  AND signalid IN ('013405') 

SELECT * FROM d_signalh WHERE id BETWEEN 1005024971 and 1205997031 AND siteid IN ('2028')  AND signalid IN ('013405') 
SELECT * FROM d_signalh WHERE id BETWEEN 1305997031 AND 1389997031 AND siteid IN ('2028')  AND signalid IN ('013405') 
SELECT * FROM d_signalh WHERE id = '1352626392'
SELECT MAX(id) FROM d_signalh






# 集团动环-spider
SELECT * FROM t_liquid_cooling_config 
	WHERE config_id = 'eaf0a1f45b2a4d7fbfe4ec23a1fa394a';
SELECT * FROM t_liquid_cooling_primary_side_config;

SELECT * from t_liquid_cooling_config_parameter;
SELECT * from t_liquid_cooling_refrigeration_room_config;
SELECT * from t_liquid_cooling_primary_side_config 
	WHERE config_id = 'eaf0a1f45b2a4d7fbfe4ec23a1fa394a'
	AND id = '97392c697e0e44b799425a69511841ed';
SELECT * from t_liquid_cooling_cdu_reference_info;


SELECT * from t_liquid_cooling_data_statistics;
SELECT * from t_liquid_cooling_primary_side_statistics;
SELECT * from t_liquid_cooling_refrigeration_room_statistics;
SELECT * from t_liquid_cooling_refrigeration_room_statistics WHERE config_id = 'eaf0a1f45b2a4d7fbfe4ec23a1fa394a'

# 01-08-08-01-11-02
SELECT * FROM t_cfg_dict WHERE col_name = 'building_type'
SELECT * FROM t_cfg_precinct WHERE precinct_id like '01-08-08-01-11%'
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-01-11-01'
SELECT * FROM t_cfg_precinct WHERE precinct_id like '01-08-08-01-11%'
SELECT * FROM t_cfg_precinct WHERE precinct_id like '01-08-08-01-11-02%'
SELECT * FROM t_cfg_precinct WHERE precinct_id like '01-08-08-04-03%' AND precinct_kind = 3
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-01-11-01-02'
SELECT * FROM t_cfg_precinct WHERE dim_spatial_id = '9054084'
SELECT * FROM t_cfg_device 
	WHERE precinct_id = '01-08-08-01-11-01-02' AND device_id = '00751006000005648496'
SELECT * FROM t_cfg_device WHERE dim_device_id = '10017192'

SELECT * from t_liquid_cooling_config_parameter 
	WHERE config_id = 'eaf0a1f45b2a4d7fbfe4ec23a1fa394a'  AND mete_code = '012326'
	AND system_id = '64bdd917c27543a1a504c59108b6c1f0'
	AND room_id = '01-08-08-01-11-01-02';

SELECT * from t_liquid_cooling_primary_side_statistics WHERE statistics_date = '2025-10-01';
SELECT * FROM t_cfg_device WHERE device_id = '00751006000005648386'







# 集团mpp-dh
# 9054046
SELECT * FROM dws_liquid_cooling_mete_detail_day  LIMIT 10
SELECT * FROM fact_dwd_signal_value LIMIT 10
SELECT * FROM fact_dwd_signal_value WHERE  signal_start_time between "2025-11-02 12:00:00"  AND "2025-11-02 12:30:00"
order BY signal_start_time desc LIMIT 10


	# 综合机房
	SELECT * FROM fact_dwd_signal_value WHERE device_spatial_id = '9054084';
	SELECT * FROM fact_dwd_signal_value WHERE device_id = '10017181' AND signal_meta_code = 013405;
	SELECT * FROM fact_dwd_signal_value 
		WHERE RIGHT(signal_start_time, 5) IN ('59:59', '00:00', '00:01', '30:00')
  		AND device_spatial_id = '9054084'
		AND LEFT(signal_start_time,10) IN ('2025-11-07');
	SELECT * FROM fact_dwd_signal_value 
		WHERE device_spatial_id = '9054084'
		AND LEFT(signal_start_time,10) IN ('2025-11-07');
	# 013351,013352,013353			—— 5个
	# 012318,012321,012325			—— 5个
	# 013405,013323,013330
	# 012326,012329					—— 5个
	# 012333,012339,012340,012334,012345,012344    
	# 9054084，9054086
	SELECT * FROM fact_dwd_signal_value 
		WHERE device_spatial_id = '9054086'
		AND signal_start_time BETWEEN '2025-11-07 19:00:00' AND '2025-11-07 21:00:00' 
		AND signal_meta_code like '012345'
		AND signal_number IN (0,1,2,3,4,5);
	SELECT * FROM fact_dwd_signal_value 
		WHERE 
		signal_start_time BETWEEN '2025-11-07 19:00:00' AND '2025-11-07 21:00:00' 
		AND signal_meta_code like '012345'
		AND signal_number IN (0,1,2,3,4,5);
	SELECT * FROM fact_dwd_signal_value 
		WHERE 
		signal_start_time BETWEEN '2025-10-01 02:30:00' AND '2025-10-02 21:00:00' 
		AND signal_meta_code LIKE '013405'
		AND signal_number IN (0,1,2,3,4,5);
	


	SELECT * FROM dim_liquid_cooling_mete_hour ;
	SELECT * FROM dwd_device_detail_v LIMIT 10;
	SELECT * FROM dws_liquid_cooling_mete_detail_day; 
	
	SELECT MAX(id) FROM dwd_device_detail_v LIMIT 10;
	
	SELECT stat_hour,dim_device_id,mete_code,signal_number,device_name,VALUE,signal_start_time 
		FROM dws_liquid_cooling_mete_detail_day 
		WHERE 
		left(signal_start_time,10) = '2025-10-02'
		mete_code = '013405'
		AND signal_start_time BETWEEN '2025-11-01 02:00:00' AND '2025-11-03 21:00:00' ;
		# AND signal_start_time BETWEEN '2025-11-07 19:00:00' AND '2025-11-07 21:00:00' ;
	
	SELECT stat_hour,dim_device_id,mete_code,signal_number,device_name,VALUE,signal_start_time 
		FROM dws_liquid_cooling_mete_detail_day 
		WHERE 
		left(signal_start_time,10) = '2025-10-14'
		AND mete_code = '013405'
	
	# 测点取值计算
		# 013351,013352,013353			—— 5个
		# 012318,012321,012325			—— 5个
		# 013405,013323,013330
		# 012326,012329					—— 5个
		# 012333,012339,012340,012334,012345,012344    
		# 9054084，9054086, 8054048, 9054062, 9054063
		SELECT * FROM fact_dwd_signal_value 
			WHERE device_spatial_id = '9054084'
			AND signal_start_time BETWEEN '2025-10-16 02:00:00' AND '2025-10-16 06:00:00' 
			AND signal_meta_code like '012326'
			AND signal_number IN (0,1,2,3,4,5);



		SELECT stat_hour,dim_device_id,mete_code,signal_number,device_name,VALUE,signal_start_time 
			FROM dws_liquid_cooling_mete_detail_day 
			WHERE 
			left(signal_start_time,10) = '2025-10-06'
			AND mete_code = '012334'


		
		UPDATE dws_liquid_cooling_mete_detail_day SET VALUE = 0 WHERE 
			left(signal_start_time,10) = '2025-10-16'
			AND mete_code = '012326'
		
	
	SHOW ALL ROUTINE LOAD;

explain SELECT * FROM dim_liquid_cooling_mete_hour ;

