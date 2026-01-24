# 超期详情表归类 -- 看综资设备和子类的情况
SELECT resource_device_type_name,device_type_name,device_sub_type_name 
FROM overdue_device_detail group by device_type_name,device_sub_type_name LIMIT 200

# 目前新增表字段 -- 查看对应的数据项是否一致（是否存在缺失）
SELECT * FROM t_overdue_service_life_config GROUP BY device_type,device_sub_type;

# 开发日志执行语句
SELECT id, device_type AS deviceType, device_sub_type AS deviceSubType, site_type_dc AS siteTypeDc, 
site_type_jl AS siteTypeJl, site_type_jd AS siteTypeJd, site_type_jz AS siteTypeJz, is_enabled AS isEnabled 
FROM t_overdue_service_life_config WHERE is_enabled = 1 ORDER BY device_type, device_sub_type


# 查看新表配置项是否一致（修改后是否与页面一致）
SELECT COUNT(*) FROM t_overdue_service_life_config
SELECT * FROM t_overdue_service_life_config WHERE device_type = '变压器'


# 补充，修改某个站点类型的设备周期，看是否初始化正常（初始化前，手工修改）
UPDATE overdue_device_detail SET update_cycle = 9 WHERE device_sub_type_name = '分立开关电源' ;
UPDATE overdue_device_detail SET update_cycle = 8 WHERE device_sub_type_name = '壁挂开关电源' ;
UPDATE overdue_device_detail SET update_cycle = 7 WHERE device_sub_type_name = '开关电源01' ;
UPDATE overdue_device_detail SET update_cycle = 6 WHERE device_sub_type_name = '开关电源02' ;
UPDATE overdue_device_detail SET update_cycle = 6 WHERE device_sub_type_name = '组合开关电源' ;

UPDATE overdue_device_detail SET update_cycle = 3 WHERE device_sub_type_name = '极早期烟感' ;
UPDATE overdue_device_detail SET update_cycle = 2 WHERE device_sub_type_name = '极早期烟感01' ;
UPDATE overdue_device_detail SET update_cycle = 1 WHERE device_sub_type_name = '极早期烟感02' ;


# 分组查看各设备（大设备），在各站点数据的年限
SELECT resource_device_type_name,device_type_name,device_sub_type_name,update_cycle ,site_type_name
FROM overdue_device_detail 
WHERE resource_device_type_name = '开关电源' AND site_type_name = '传输节点'
group by device_type_name,device_sub_type_name,site_type_name LIMIT 600


# 查看具体设备子类周期年限
SELECT device_name,device_type_name,device_sub_type_name,update_cycle,site_type_name 
FROM overdue_device_detail WHERE device_sub_type_name = '开关电源锂电池'
GROUP BY device_sub_type_name,site_type_name,update_cycle


# 查看具体站点类型下设备年限，不分组
SELECT device_name,device_type_name,device_sub_type_name,update_cycle,site_type_name 
FROM overdue_device_detail WHERE device_sub_type_name = '开关电源锂电池' AND site_type_name = '数据中心'


# 清空现有配置表
delete from t_overdue_service_life_config


# 初始化语句（composite服务）
curl --location --request POST 'http://localhost:28001/v1/hiddenDanger/overdueService/serviceLifeConfig/init' \
--header 'head_username: alauda' \
--header 'Content-Type: application/json' \