SELECT * FROM zz_data_room_device_type LIMIT 100;
SELECT * FROM t_zz_device_type;
SELECT * FROM zz_data_sync_info;

SELECT * FROM t_cfg_device LIMIT 10;

SELECT * FROM fsu_point_data_20250924;



UPDATE  fsu_point_data_20250924 SET collectTime = '2025-09-24 18:01:03';
UPDATE  fsu_point_data_20250924 SET create_time = '2025-09-24 18:03:03';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-08-04-15-G97'

SELECT * FROM energy_cabinet_attribute_config WHERE up_mete_id = '分路XX相电流Ic' AND NAME LIKE "黄某某_上海断电测试站点/上海楼栋1/%"  and update_user = 'alauda' GROUP BY cabinet_id 
SELECT * FROM energy_cabinet_attribute_config WHERE cabinet_id = '108522ca1ba1426083ba67b5565b68e1'








SELECT * FROM t_cfg_precinct LIMIT 10;

SELECT * FROM t_cfg_precinct WHERE precinct_name LIKE "广东云浮市云城区0402枢纽楼0209机房%";



SELECT * FROM t_cfg_device LIMIT 10;
SELECT * FROM t_cfg_device WHERE device_name LIKE "云浮云城区金山综合楼四楼机房交换1-模块化高频UPS-4F-2-1%"







--   ----------------------------------  集团  ----------------------------------



overdue_device_detail				超期服役-设备详情表
overdue_count_total					超期服役统计分析总表
overdue_count_manufactor			超期服役-厂家统计分析报表		
overdue_count_device					超期服役-设备类型统计分析	
overdue_count_city					超期服役-地市统计分析报表
overdue_device_type_dict			超期服役-更新周期字典表
overdue_count_room					机房超期服役统计分组表
overdue_device_alert_monthly		超期服役-设备月度告警频次表
zz_data_sync_info						综资同步数据配置表
t_scheduled_task


SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-24' LIMIT 10;



SELECT * FROM overdue_device_detail order by update_time desc LIMIT 10;
SELECT * FROM overdue_device_detail WHERE device_name = '云浮云城区金山综合楼四楼机房交换1-模块化高频UPS-4F-2-1' LIMIT 10;
SELECT site_type_name FROM overdue_device_detail GROUP BY site_type_name;


SELECT * FROM overdue_count_total LIMIT 10;
SELECT * FROM overdue_count_manufactor LIMIT 10;
SELECT * FROM overdue_count_city LIMIT 10;
SELECT * FROM overdue_device_type_dict;
SELECT * FROM overdue_count_room LIMIT 10;
SELECT * FROM overdue_device_alert_monthly LIMIT 10;
SELECT * FROM t_scheduled_task;
SELECT * FROM zz_data_sync_info;			综资同步数据配置表
SELECT * FROM zz_to_rm_rm_area_dc;
SELECT * from zz_data_room_device_type LIMIT 20;




--   ----------------------------------  超期服役设备详情   ----------------------------------

-- 设备周期类别 周期年限
SELECT device_type_name,device_sub_type_name,update_cycle FROM overdue_device_detail 
WHERE device_type_name = '交流母线配电'  GROUP BY device_type_name,device_sub_type_name ;


--
SELECT * FROM overdue_device_detail WHERE device_type_name = '交流母线配电' LIMIT 10 ;

-- 周期字典
SELECT * FROM overdue_device_type_dict;

-- 验证es数据与综资表数据
SELECT * FROM overdue_count_total LIMIT 10;


-- 设备类型分类数量  -- 统计表
SELECT device_type_name,COUNT(*) FROM overdue_device_detail GROUP BY device_type_name



--   ----------------------------------  超期服役设备详情  以上海为例统计站点数  ----------------------------------
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-20-02-03-01-06'





--   ----------------------------------  告警统计关联  ----------------------------------

SELECT * FROM t_cfg_device LIMIT 10;


