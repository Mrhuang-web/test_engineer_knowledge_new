SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
SELECT * FROM t_cfg_device WHERE precinct_id LIKE "01-08-08-01-02-01%" AND device_type = '3' AND power_device_id =
'1001001001001' ;

SELECT * FROM t_cfg_device WHERE precinct_id LIKE "01-08-08-01-02-01%";
update t_cfg_device SET power_device_id = '' WHERE precinct_id LIKE "01-08-08-01-02-01%" ;


20251231000000
SELECT * FROM zz_data_sync_info;

SELECT * FROM zz_to_rm_rm_area_site WHERE batch_num = '20200723';

SELECT * FROM zz_to_rm_rm_area_room WHERE batch_num = '20200723';

SELECT * FROM zz_to_rm_rm_area_room WHERE batch_num = '20250723';


SELECT * FROM zz_to_rm_rm_device WHERE power_device_id = "1001001001002";


SELECT * FROM zz_to_rm_rm_device WHERE precinct_id LIKE "01-08-08-01-02-01%" ;