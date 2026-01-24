SELECT * from t_zz_space_resources WHERE related_site IS NOT null LIMIT 10;
SELECT * from t_zz_power_specialty LIMIT 10;
SELECT * from t_zz_power_specialty WHERE device_id IS NOT null LIMIT 10;
SELECT * FROM t_cfg_precinct LIMIT 10;

SELECT * FROM t_cfg_device WHERE device_id = '00161006000000024796'


SELECT * FROM t_zz_power_device LIMIT 10;
02b13412a9ec461d900b7091a4549590
SELECT device_type FROM t_zz_power_device GROUP BY device_type;
SELECT device_type from t_zz_power_specialty  GROUP BY device_type;


SELECT device_type from t_zz_power_device_sys LIMIT 10;  GROUP BY device_type;
SELECT zh_label from t_zz_power_device_sys GROUP BY zh_label;
SELECT * from t_zz_power_device_sys 


SELECT * FROM t_zz_switch_power LIMIT 10;
SELECT * FROM t_zz_switch_power LIMIT 10;

SELECT * FROM t_device_link LIMIT 10;
SELECT * FROM t_device_link LIMIT 10;

SELECT * FROM t_zz_smart_meter WHERE collected_device IS NOT NULL  LIMIT 10;


SELECT * FROM t_zz_switch_power WHERE res_code = '161_2028_202801_1757389505';

00161006000000024845
00161006000000024897
00161006000000024971
00161006000000024948    01-07-05-02-41-04
SELECT * FROM t_zz_power_device WHERE res_code = '00024263dfa0489c8728a0c550d858ff';


SELECT * from t_zz_power_specialty WHERE res_code = '161_2028_202801_1757389505';


SELECT * FROM t_cfg_device WHERE device_id = '00161006000000024845'





SELECT * FROM t_cfg_device WHERE device_id = '00771006000002944984'
SELECT * FROM t_zz_power_device WHERE  device_id = '00771006000002944984'




SELECT * FROM t_device_link;
SELECT * FROM t_zz_power_device WHERE res_code = 'T_PHY_COM_POWER_DISTRIBU_LS-ff8080817c1180bc017d04055cc55615';

SELECT * FROM t_zz_power_device WHERE zh_label = '深圳科信空调配电柜415/1'


SELECT * FROM t_zz_space_resources limit 10;
SELECT * FROM t_cfg_device WHERE device_name = '维谛技术水冷专用空调411'


SELECT * FROM information_schema.columns LIMIT 10;

SELECT * FROM t_cfg_devicesys LIMIT 10;
SELECT * FROM t_cfg_device WHERE device_name = '维谛技术UPS系统36-2';
SELECT * FROM t_zz_switch_power LIMIT 10;
SELECT * FROM t_zz_power_device_sys WHERE zh_label = '维谛技术UPS系统36';



SELECT 
    COLUMN_NAME AS '列名',
    COLUMN_TYPE AS '数据类型',
    IS_NULLABLE AS '允许空',
    COLUMN_DEFAULT AS '默认值',
    COLUMN_KEY AS '索引',
    EXTRA AS '额外信息',
    COLUMN_COMMENT AS '列注释'
FROM 
    information_schema.columns 
WHERE 
    TABLE_SCHEMA = 'gx-spider'  -- 指定数据库名
    AND TABLE_NAME = 't_cfg_devicesys_detail' -- 指定表名
ORDER BY 
    ORDINAL_POSITION;
    
    
    
    
    
SELECT * FROM t_cfg_precinct WHERE precinct_id  = '01-07-05-02';
    
  
SELECT * FROM t_cfg_mete WHERE mete_code = '087001'    
SELECT * FROM t_cfg_device where device_name = '高压直流电源'   LIMIT 10;
SELECT * FROM t_cfg_metemodel LIMIT 10;
SELECT * FROM t_cfg_metemodel WHERE model_id = '00001008000000085116';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000085116' LIMIT 10;
    
select * from temperature_root_monthly 
where report_type = 3 and t1>=30 and t1 <50 and air_type_id!=4 and statistics_time = '2025-08-01';

SELECT * FROM t_cfg_precinct WHERE up_precinct_id = '01-07-05-02-41'


SELECT * FROM t_cfg_nmsdevice 







SELECT * FROM t_zz_power_device WHERE device_id = '00771006000002943063'
SELECT * FROM t_cfg_device WHERE device_id = '00771006000002943063'
SELECT * FROM t_cfg_metemodel WHERE model_id = '00001008000000685211'
SELECT * FROM t_cfg_metemodel_detail LIMIT 10  WHERE model_id = '00001008000000685211'



SELECT * FROM overdue_device_detail LIMIT 10;
SELECT site_type_name,resource_device_type_name,COUNT(resource_device_type_name) AS '站点类型' FROM overdue_device_detail GROUP BY device_type_name;
SELECT site_type_name,resource_device_type_name,COUNT(resource_device_type_name) AS '站点类型' FROM overdue_device_detail GROUP BY resource_device_type_name;

SELECT * FROM overdue_device_detail WHERE site_type_name = '数据中心' LIMIT 10;
SELECT COUNT(site_type_name) AS '站点类型' FROM overdue_device_detail GROUP BY site_type_name;




SELECT * FROM overdue_device_detail where sys_device_id is not null LIMIT 20;






















SELECT * FROM t_cfg_precinct where precinct_name LIKE "%上海定制6%"