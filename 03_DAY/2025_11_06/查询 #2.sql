SELECT * FROM t_cfg_device LIMIT 10;

SELECT tcd.dict_note,COUNT(td.device_name) FROM t_cfg_device td 
	JOIN t_cfg_site ts ON left(td.precinct_id,14) = ts.site_id
	JOIN t_cfg_dict tcd ON tcd.dict_code = ts.site_type
	WHERE 
		tcd.col_name = 'site_type' AND 
		td.device_name = '变压器'
	GROUP by 
		ts.site_type
	
	
SELECT * FROM t_cfg_site LIMIT 10;

SELECT COUNT(1) FROM t_cfg_device td 
	JOIN t_cfg_site ts ON left(td.precinct_id,14) = ts.site_id
	
	
SELECT * FROM t_current_capacity

