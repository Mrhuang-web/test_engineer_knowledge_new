SELECT * FROM zz_data_sync_info;


-- ------------------------------冷源与末端（免考核）------------------------------------------------
SELECT * FROM platform_analysis_report_col_terminal_detail;
-- 01-26-04-20-34(四川),01-15-02-08-01(吉林),01-25-01-11-36(上海)
SELECT * FROM platform_analysis_report_col_terminal_detail_exemption;
SELECT * FROM t_cfg_precinct 
	WHERE precinct_id 
		IN (SELECT site_id FROM platform_analysis_report_col_terminal_detail_exemption);
SELECT * FROM t_cfg_precinct WHERE precinct_name = '山西测试核心机楼2006中心';




-- --------------------------原始数据（新增数据中心表）------------------------------------
SELECT * FROM building_area;  -- 区域编码对应名称
SELECT * FROM building_mapping;  -- 区域编码对应名称
SELECT * FROM zz_to_rm_rm_area_dc LIMIT 10;

SELECT ba1.area_name,ba2.area_name,ztr.city_id,ztr.county_id,ztr.* FROM zz_to_rm_rm_area_dc ztr
	JOIN building_area ba1 ON ztr.province_id = ba1.area_id
	JOIN building_area ba2 ON ztr.city_id = ba2.area_id
	WHERE 
		ba1.area_name = '山西' and
		ztr.county_id = '440112'
	GROUP BY county_id;



-- 为空情况
SELECT * FROM zz_to_rm_rm_area_dc WHERE char_length(province_id) < 1;
SELECT * FROM zz_to_rm_rm_area_dc WHERE char_length(city_id) < 1;
SELECT * FROM zz_to_rm_rm_area_dc WHERE char_length(county_id) < 1;  -- 存在空
SELECT * FROM zz_to_rm_rm_area_dc WHERE char_length(zh_label) < 1;
SELECT * FROM zz_to_rm_rm_area_dc WHERE char_length(standardaddress) < 1;  -- 存在空
SELECT * FROM zz_to_rm_rm_area_dc WHERE char_length(address) < 1;	-- 存在空
SELECT * FROM zz_to_rm_rm_area_dc WHERE char_length(longitude) < 1;	-- 存在空
SELECT * FROM zz_to_rm_rm_area_dc WHERE char_length(latitude) < 1;	-- 存在空


SELECT * FROM zz_to_rm_rm_area_dc where int_id = '441000000000007995689853' LIMIT 10;



-- --------------------------供电拓扑（）------------------------------------
SELECT * FROM t_cfg_topology_v2_configuration LIMIT 10;


SELECT tcd.*FROM t_cfg_precinct tcd
	WHERE 
		EXISTS (
		    SELECT 1
		    FROM t_cfg_topology_v2_configuration tct
		    WHERE tct.up_precinct_id = tcd.precinct_id
		)
	LIMIT 10;
	
	
	
	
SELECT * FROM t_cfg_precinct WHERE precinct_id LIKE '01-04-01%' AND CHAR_LENGTH(precinct_id) = 11
SELECT * FROM t_cfg_precinct WHERE area_code = '440840'

SELECT * FROM t_cfg_precinct WHERE precinct_id LIKE '01-19%' AND CHAR_LENGTH(precinct_id) <= 8




SELECT * FROM t_cfg_precinct WHERE area_code = '110000'