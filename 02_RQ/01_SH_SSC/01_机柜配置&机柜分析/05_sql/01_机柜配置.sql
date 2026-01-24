SELECT 
    c.TABLE_SCHEMA AS '数据库',
    c.TABLE_NAME AS '表名',
    t.TABLE_COMMENT AS '表注释',
    c.COLUMN_NAME AS '字段名',
    c.COLUMN_COMMENT AS '字段注释' 
FROM INFORMATION_SCHEMA.COLUMNS c
JOIN INFORMATION_SCHEMA.TABLES t
    ON c.TABLE_SCHEMA = t.TABLE_SCHEMA
    AND c.TABLE_NAME = t.TABLE_NAME
WHERE c.COLUMN_NAME LIKE '%clogusrname%'
  AND c.TABLE_SCHEMA = 'spider2';
  






SELECT * FROM energy_cabinet  LIMIT 10;
SELECT * FROM energy_cabinet  WHERE cabinet_name LIKE "%黄某某%";


# 黄某某4 01-01-08-04-1  		机房：01-01-08-04-11-01-01
# 黄某某5 01-01-08-04-12		机房：01-01-08-04-12-01-01
# 黄某某6 01-01-08-04-13		机房：01-01-08-04-13-01-01
SELECT * FROM energy_cabinet_column WHERE precinct_id = '01-01-08-04-11-01-01';
SELECT * FROM energy_cabinet_column WHERE precinct_id = '01-01-08-04-12-01-01';
SELECT * FROM energy_cabinet_column WHERE precinct_id = '01-01-08-04-13-01-01';

SELECT * FROM energy_cabinet WHERE precinct_id = '01-01-08-04-11-01-01';
SELECT * FROM energy_cabinet WHERE precinct_id = '01-01-08-04-12-01-01';
SELECT * FROM energy_cabinet WHERE precinct_id = '01-01-08-04-13-01-01';



# 查看站点对应机房precinct_id 用于定位机柜列和机柜的中precinct_id对比
SELECT * FROM t_cfg_precinct WHERE precinct_name LIKE "%黄某某%";



# 查看机柜下已配置的用电关系
SELECT b.cabinet_column_name,a.* FROM energy_cabinet a inner join energy_cabinet_column b ON b.id = a.cabinet_column_id WHERE a.precinct_id = '01-01-08-04-12-01-01' AND is_config = 1;


# 查看机柜下已配置的用电关系的配置项
SELECT a.precinct_id,b.cabinet_column_name,a.cabinet_name,b.channel_type,d.device_type_name,c.* FROM energy_cabinet a 
inner join energy_cabinet_column b ON b.id = a.cabinet_column_id 
INNER JOIN energy_cabinet_attribute_config c ON c.cabinet_id = a.id
INNER JOIN energy_cabinet_mete d ON c.mete_code = d.mete_code
WHERE a.precinct_id = '01-01-08-04-12-01-01' AND a.is_config = 1 AND c.up_mete_id LIKE "%电流%";
