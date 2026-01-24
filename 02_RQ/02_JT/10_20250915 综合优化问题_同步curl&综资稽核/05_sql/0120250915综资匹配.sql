SELECT * FROM zz_data_sync_info;
SELECT * FROM zz_to_rm_rm_area_dc;
SELECT * FROM zz_to_rm_rm_area_site;
SELECT * FROM zz_to_rm_rm_area_room;
SELECT * FROM zz_to_rm_rm_device;
SELECT * FROM building_area;


#  440000   440500   01-01-25-01-09-01
SELECT * FROM t_cfg_precinct where precinct_id LIKE "01-01%" and precinct_kind = 3 LIMIT 10;
SELECT * FROM t_cfg_site LIMIT 10

# 01-01-03-01-01
SELECT * FROM t_cfg_precinct where precinct_id LIKE "01-01%" and precinct_kind = 2;


# 非楼栋  01-01-08-04-03
SELECT * FROM t_cfg_precinct where precinct_id LIKE "01-01%" and precinct_kind = 2 AND precinct_name LIKE "%数据中心%" LIMIT 10;


SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-13-15-04-02-77'
	
# id 法
SELECT * FROM t_cfg_precinct where precinct_id LIKE "01-01%" and precinct_kind = 2 AND precinct_name LIKE "%数据中心%" LIMIT 10;

SELECT * FROM t_cfg_precinct WHERE precinct_kind IN (3) AND precinct_id LIKE "01-39%"
SELECT * FROM t_cfg_precinct WHERE precinct_kind IN (2) AND precinct_id LIKE "01-39%"
SELECT * FROM t_cfg_precinct WHERE precinct_name = '专业公司江苏苏州市0101数据中心'
SELECT * FROM t_cfg_site WHERE site_id = '01-39-02-01-01'



# 数据中心 
SELECT * FROM t_cfg_precinct WHERE precinct_kind IN (2) AND precinct_id IN 
	(SELECT site_id FROM t_cfg_site WHERE site_id LIKE "01-01%" AND site_type = 1);
	
	

# 局站
SELECT * FROM t_cfg_precinct WHERE precinct_name = '广东汕头市濠江区0403数据中心0301楼栋';




# 设备
SELECT * FROM building_area;
SELECT * FROM t_cfg_precinct WHERE 

SELECT * FROM t_cfg_device a
	JOIN t_cfg_precinct b ON a.precinct_id = b.precinct_id AND b.isdel = '000' AND b.room_kind IS NOT NULL 
	JOIN t_cfg_precinct c ON b.up_precinct_id = c.precinct_id AND c.precinct_id = '01-01-08-04-03-01' 
	WHERE a.device_type = '3' AND a.isdel = '000';
	
	
	
SELECT COUNT(*) FROM t_cfg_precinct_newname LIMIT 10