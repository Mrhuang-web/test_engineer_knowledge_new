SELECT * from t_liquid_cooling_config_parameter;
SELECT * from t_liquid_cooling_refrigeration_room_config;
SELECT * from t_liquid_cooling_primary_side_config;
SELECT * from t_liquid_cooling_cdu_reference_info;
SELECT * from t_liquid_cooling_config;


SELECT * from t_liquid_cooling_data_statistics;
SELECT * from t_liquid_cooling_primary_side_statistics;
SELECT * from t_liquid_cooling_refrigeration_room_statistics;
SELECT * from t_liquid_cooling_refrigeration_room_statistics WHERE config_id = 'eaf0a1f45b2a4d7fbfe4ec23a1fa394a'





SELECT * FROM dws_liquid_cooling_mete_detail_day  LIMIT 10
SELECT * FROM fact_dwd_signal_value LIMIT 10
SELECT * FROM fact_dwd_signal_value WHERE  signal_start_time between "2025-11-04 12:00:00"  AND "2025-11-04 12:30:00"
order BY signal_start_time desc LIMIT 10

SELECT * FROM t_cfg_dict WHERE col_name = 'building_type'

SELECT * FROM t_cfg_precinct WHERE precinct_id like '01-08-08-01-11%'

SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-01-11-01'
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-01-11-01-02'
SELECT * FROM t_cfg_precinct WHERE dim_spatial_id = '7054086'


SELECT * FROM fact_dwd_signal_value WHERE device_spatial_id = '9054086';
SELECT * FROM fact_dwd_signal_value WHERE device_id = '9054046';

SELECT COUNT(*) FROM fact_dwd_signal_value LIMIT 10;

UPDATE t_cfg_precinct SET building_type = NULL WHERE precinct_id IN 
('01-08-08-01-11','01-08-08-01-11-01-01','01-08-08-01-11-01-02','01-08-08-01-11-01-03')



