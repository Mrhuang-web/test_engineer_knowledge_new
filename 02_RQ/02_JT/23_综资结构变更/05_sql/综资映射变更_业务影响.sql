SELECT * FROM zz_data_sync_info;

SELECT * FROM overdue_device_detail LIMIT 1000;

SELECT * FROM t_cfg_precinct WHERE precinct_name = '辽宁抚顺市抚顺开发区0801枢纽楼0102机房';
SELECT * FROM zz_to_rm_rm_area_room where zh_label = '辽宁抚顺市抚顺开发区0801枢纽楼0102机房';
SELECT * FROM zz_to_rm_rm_area_room where precinct_id = '01-38-09-08-01-02';
SELECT * FROM zz_to_rm_rm_area_room;


SELECT * FROM t_cfg_device WHERE device_name = '抚顺沈抚新城通信楼8层IDC机房-低压交流配电-7883';

SELECT * FROM zz_to_rm_rm_area_site;
SELECT update_time FROM zz_to_rm_rm_area_site ORDER BY update_time DESC ;
SELECT * FROM zz_to_rm_rm_area_room ORDER BY update_time;


SELECT * FROM zz_data_sync_info;
SELECT * FROM t_cfg_topology_v2_configuration LIMIT 10;
SELECT COUNT(1) FROM t_cfg_topology_v2_configuration LIMIT 10;


# 触发综资站点入库  -- 统计查询业务
SELECT * FROM zz_to_rm_rm_area_site WHERE left(update_time,10) = '2025-12-29';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-22-14-01-01';

# 触发综资机房入库
SELECT * FROM zz_to_rm_rm_area_room WHERE left(collect_time,10) = '2025-07-23';

# 触发综资设备入库
SELECT * FROM zz_to_rm_rm_device where device_type = '高压配电' LIMIT 1000;
SELECT * FROM t_cfg_precinct WHERE precinct_name = '安徽安庆市大观区0601枢纽楼';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-02-08-06-01';
SELECT * FROM zz_to_rm_rm_device WHERE precinct_id like '01-02-08-06-01%' AND device_type = '高压配电';
SELECT * FROM t_cfg_device WHERE precinct_id LIKE "01-02-08-06-01%" AND device_type = '1';


# 查看匹配情况
SELECT device.device_id,device.device_name,device.device_type,device.device_name,device.precinct_id FROM  t_cfg_device device WHERE left(device.precinct_id,14) IN 
(SELECT site.precinct_id FROM zz_to_rm_rm_area_site site WHERE left(site.update_time,10) = '2025-12-29');

SELECT * FROM overdue_device_type_dict;



# 查看超期服役
SELECT * FROM overdue_device_detail order by update_time desc LIMIT 10;
SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
SELECT * FROM t_cfg_device WHERE device_type = '3';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '四川成都市双流区0301数据中心';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '四川成都市双流区0301数据中心0104楼栋0416机房';

# 变压器
SELECT * FROM overdue_device_detail where device_type_name = '变压器' and site_type IN (1,2) LIMIT 10;



# 供电拓扑 
SELECT COUNT(1) FROM t_cfg_topology_v2_configuration;
SELECT * FROM t_cfg_topology_v2_configuration ORDER BY updated_at DESC LIMIT 100;
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-17-01-01-50';

SELECT * FROM t_cfg_precinct WHERE precinct_name = '浙中信息产业园D01-307动力机房';
SELECT * FROM t_cfg_topology_v2_configuration WHERE up_precinct_id LIKE "01-33-02-06-07-02%"