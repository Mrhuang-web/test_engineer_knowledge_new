SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM overdue_count_total LIMIT 10;
SELECT * FROM overdue_count_device LIMIT 10;
SELECT * FROM overdue_count_manufactor LIMIT 10;
SELECT * FROM overdue_count_city order by update_time desc LIMIT 10;
SELECT * FROM overdue_device_type_dict;
SELECT * FROM overdue_count_room LIMIT 10;
SELECT * FROM overdue_device_alert_monthly LIMIT 10;
SELECT * FROM zz_data_sync_info;

-- 脏数据判断
SELECT UPDATE_time,* FROM overdue_device_detail group by update_time;

-- 大类分类
SELECT odd.device_type_name,odd.device_sub_type_name,odt.update_cycle 
	FROM overdue_device_detail odd  JOIN overdue_device_type_dict odt ON odd.device_type_name = odt.device_type
	GROUP BY odd.device_type_name;

-- 子类分类
SELECT odd.device_type_name,odd.device_sub_type_name,odt.update_cycle 
	FROM overdue_device_detail odd  JOIN overdue_device_type_dict odt ON odd.device_type_name = odt.device_type
	GROUP BY odd.device_type_name,odd.device_sub_type_name;
	





-- 统计分析表
SELECT tcp3.precinct_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	GROUP BY tcp3.precinct_id,odd.overdue_type;

SELECT tcp3.precinct_name,tcp2.precinct_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	GROUP BY tcp2.precinct_id,odd.overdue_type;
	
SELECT tcp3.precinct_name,tcp2.precinct_name,tcp1.precinct_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	GROUP BY tcp1.precinct_id,odd.overdue_type
	ORDER BY tcp.precinct_name;
	

SELECT tcp3.precinct_name,tcp2.precinct_name,tcp1.precinct_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	JOIN t_cfg_site tcs ON odd.site_id = tcs.site_id
	WHERE tcs.site_type = 1
	GROUP BY tcp1.precinct_id,odd.overdue_type
	ORDER BY tcp.precinct_name;





-- 统计分析表 		设备分类(需要区分日期 - 因为可能存在多日期)
SELECT tcp3.precinct_name,odd.device_type_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	GROUP BY tcp3.precinct_id,odd.device_type_name,odd.overdue_type
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	ORDER BY tcp.precinct_name;
	

SELECT tcp3.precinct_name,tcp2.precinct_name,odd.device_type_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	GROUP BY tcp2.precinct_id,odd.device_type_name,odd.overdue_type
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	ORDER BY tcp.precinct_name;
	
SELECT tcp3.precinct_name,tcp2.precinct_name,tcp1.precinct_name,odd.device_type_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	GROUP BY tcp1.precinct_id,odd.device_type_name,odd.overdue_type
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	ORDER BY tcp.precinct_name;
	

SELECT tcp3.precinct_name,tcp2.precinct_name,tcp1.precinct_name,odd.device_type_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	JOIN t_cfg_site tcs ON odd.site_id = tcs.site_id
	WHERE tcs.site_type = 1
	GROUP BY tcp1.precinct_id,odd.device_type_name,odd.overdue_type
	ORDER BY tcp.precinct_name;



-- 统计分析表 		厂家分类(需要区分日期 - 因为可能存在多日期)
SELECT tcp3.precinct_name,odd.device_type_name,odd.manufactor_name,odd.overdue_type,count(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	GROUP BY tcp3.precinct_id,odd.device_type_name,odd.manufactor_name,odd.overdue_type
	ORDER BY tcp.precinct_name;
	

SELECT tcp3.precinct_name,tcp2.precinct_name,odd.device_type_name,odd.manufactor_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	GROUP BY tcp2.precinct_id,odd.device_type_name,odd.manufactor_name,odd.overdue_type
	ORDER BY tcp.precinct_name;
	
SELECT tcp3.precinct_name,tcp2.precinct_name,tcp1.precinct_name,odd.device_type_name,odd.manufactor_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	GROUP BY tcp1.precinct_id,odd.device_type_name,odd.manufactor_name,odd.overdue_type
	ORDER BY tcp.precinct_name;
	

SELECT tcp3.precinct_name,tcp2.precinct_name,tcp1.precinct_name,odd.device_type_name,odd.manufactor_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	JOIN t_cfg_site tcs ON odd.site_id = tcs.site_id
	WHERE tcs.site_type = 1
	GROUP BY tcp1.precinct_id,odd.device_type_name,odd.manufactor_name,odd.overdue_type
	ORDER BY tcp.precinct_name;





	
-- 统计分析表 		地市分类（要区分日期 - 因为可能存在多日期)	 - 总设备
SELECT tcp3.precinct_name,odd.device_type_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	GROUP BY tcp3.precinct_id,odd.device_type_name,odd.overdue_type
	ORDER BY tcp.precinct_name;
	

SELECT tcp3.precinct_name,tcp2.precinct_name,odd.device_type_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	GROUP BY tcp2.precinct_id,odd.device_type_name,odd.overdue_type
	ORDER BY tcp.precinct_name;
	
SELECT tcp3.precinct_name,tcp2.precinct_name,tcp1.precinct_name,odd.device_type_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	WHERE odd.site_type  IS NOT NULL AND overdue_type IS NOT null
	GROUP BY tcp1.precinct_id,odd.device_type_name,odd.overdue_type
	ORDER BY tcp.precinct_name;
	

SELECT tcp3.precinct_name,tcp2.precinct_name,tcp1.precinct_name,odd.device_type_name,odd.overdue_type,COUNT(*) FROM overdue_device_detail odd 
	JOIN t_cfg_precinct tcp ON odd.site_id = tcp.precinct_id
	JOIN t_cfg_precinct tcp1 ON tcp.up_precinct_id = tcp1.precinct_id
	JOIN t_cfg_precinct tcp2 ON tcp1.up_precinct_id = tcp2.precinct_id
	JOIN t_cfg_precinct tcp3 ON tcp2.up_precinct_id = tcp3.precinct_id
	JOIN t_cfg_site tcs ON odd.site_id = tcs.site_id
	WHERE tcs.site_type = 1
	GROUP BY tcp1.precinct_id,odd.device_type_name,odd.overdue_type
	ORDER BY tcp.precinct_name;
	
	


-- 告警
SELECT * FROM overdue_device_detail WHERE char_length(sys_device_id)>1;


SELECT tcdt.dict_note,tcd.* FROM t_cfg_device tcd
	JOIN t_cfg_dict tcdt ON tcd.device_type = tcdt.dict_code
	where 
		(
			tcdt.col_name = 'device_type' AND
			tcd.precinct_id IN (SELECT odd1.room_id FROM overdue_device_detail AS odd1 WHERE char_length(odd1.sys_device_id)>1) AND 
			tcd.device_id IN (SELECT odd3.sys_device_id FROM overdue_device_detail AS odd3 WHERE char_length(odd3.sys_device_id)>1)
		)
		OR 
		(
			tcdt.col_name = 'device_type' AND
			tcd.precinct_id IN (SELECT odd1.room_id FROM overdue_device_detail AS odd1 WHERE char_length(odd1.sys_device_id)>1) AND 
			tcdt.dict_note IN (SELECT odd2.device_type_name FROM overdue_device_detail AS odd2 WHERE char_length(odd2.sys_device_id)>1)
		);









-- 待整理








SELECT * FROM overdue_device_detail WHERE resource_device_type_name = '高压直流电源' AND site_type IS NOT NULL; 
SELECT * FROM overdue_device_detail WHERE resource_device_type_name = '高压直流开关电源' AND site_type IS NOT NULL ;
SELECT * FROM overdue_device_detail WHERE resource_device_type_name = '高压配电' AND site_type IS NOT NULL; 

SELECT * FROM t_cfg_precinct WHERE precinct_name = '四川甘孜藏族自治州康定市0401枢纽楼0103机房' LIMIT 10


SELECT sum(high_distribution_num) FROM overdue_count_city  where update_time like '2025-10-09 12:39%' LIMIT 10;
SELECT sum(high_power_num) FROM overdue_count_city where update_time = '2025-10-09 12:39:44'  LIMIT 10;
SELECT * FROM overdue_count_city where update_time like '2025-10-09 13%' LIMIT 10;
SELECT * FROM overdue_count_city where update_time = '2025-10-09 12:39:44'  limit 10;


SELECT SUM(overdue1_num),SUM(overdue2_num),SUM(overdue3_num),SUM(overdue4_num) FROM overdue_count_total  
	where update_time like '2025-10-09 12%' and device_type_name IN ('高压直流电源','高压直流开关电源')
	AND site_type IS NOT null;

SELECT * FROM overdue_count_total  
	where update_time like '2025-10-09 12%' and device_type_name IN ('高压直流电源','高压直流开关电源')
	AND site_type IS NOT null;
	

SELECT * FROM overdue_count_total  
	where date like '2025-10-07%' and device_type_name IN ('高压直流电源','高压直流开关电源')
	AND site_type IS NOT null;
	
SELECT * FROM overdue_count_city order by update_time desc LIMIT 10;

SELECT SUM(high_power_num) FROM overdue_count_city 
	where date like '2025-10-09 13%' AND site_type IS NOT null
	order by update_time desc LIMIT 100;
	
	
	




SELECT precinct_id,sub_precinct_name,device_type_name,manufactor_name,overdue1_num, overdue2_num,overdue3_num,overdue4_num
FROM overdue_count_manufactor where manufactor_name = '其他' AND precinct_id = '01-01' 
and device_type_name = '高压配电' and DATE = '2025-11-01' LIMIT 10 ;