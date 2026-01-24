# 情况1  为空


# 情况2  全为正确的

# 机柜列
SELECT * FROM t_cfg_precinct WHERE precinct_name like "%黄某某_上海定制4%";
SELECT * FROM energy_cabinet_column WHERE precinct_id = "01-01-08-04-11-01-01";
delete FROM energy_cabinet_column WHERE cabinet_column_name LIKE "%test%" AND precinct_id = "01-01-08-04-11-01-01";
delete FROM energy_cabinet_column WHERE cabinet_column_name IN ("test10","test11","test12") AND precinct_id = "01-01-08-04-11-01-01";
# 机柜
SELECT * FROM energy_cabinet LIMIT 10;
SELECT * FROM energy_cabinet WHERE precinct_id = "01-01-08-04-11-01-01";
DELETE FROM energy_cabinet WHERE cabinet_name LIKE "%test%" AND precinct_id = "01-01-08-04-11-01-01";
# 机柜配电关系
SELECT b.cabinet_name,a.* FROM energy_cabinet_attribute_config a INNER JOIN energy_cabinet b ON a.cabinet_id=b.id 
WHERE b.precinct_id = "01-01-08-04-11-01-01";