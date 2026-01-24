# 参考站点
SELECT * FROM t_cfg_site_mapping where mapping_name = '贵州1104数据中心0440楼栋' LIMIT 10;


# 站点接入   -- province_name要与	动环t_cfg_cserverinfo中的lsc_name对应；其余的看笔记即可
# 站点稽核是在页面稽核了
INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('贵州-接入', '安顺市', '紫云苗族布依族自治县', 1, 1, '01-08-08-04-03-02', '贵州贵数据中心_液冷2', '贵州贵数据中心_液冷2', 'siteManage20250102001');

INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('贵州-接入', '安顺市', '紫云苗族布依族自治县', 1, 1, '01-08-08-04-03-01', '贵州贵数据中心_液冷1', '贵州贵数据中心_液冷1', 'siteManage20250102002');

INSERT INTO t_cfg_site_mapping
(province_name, city_name, area_name, site_type, interface_type, lsc_id, lsc_name, mapping_name, mark)
VALUES('贵州-接入', '安顺市', '紫云苗族布依族自治县', 2, 1, '01-08-08-04-02', '贵州贵通信枢纽楼_液冷', '贵州贵通信枢纽楼_液冷', 'siteManage20250102003');


# 补充机房类型  -- 现在动环查出对应的机房类型id，然后手工填写到中间库中
SELECT * FROM t_cfg_dict WHERE col_name = 'room_kind'
SELECT * FROM m_room WHERE siteid  IN ('2025','2026','2027');


# 修改站点类型  -- 通信枢纽楼：2,数据中心：1
SELECT * FROM t_cfg_dict WHERE col_name = 'site_type'
SELECT * FROM m_site where siteid IN ('2025','2026','2027');


# 补充信息（需要把动环的数据中心下的楼栋改为生产楼_building_id  -- dict表中可以看）,修改对应的precinct_id
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-08-08-04-03-01'



# 查询已插入站点、机房、设备、测点内容
SELECT * FROM m_site where siteid IN ('2025','2026','2027');
SELECT * FROM m_room where siteid IN ('2025','2026','2027');
SELECT * FROM m_device WHERE roomid IN ('202503')
SELECT * FROM m_device WHERE deviceid IN ('57604')
SELECT * FROM m_signal where deviceid IN ('57604')
SELECT * FROM m_signal where signalid IN ('012344') LIMIT 10;


# 测点准确性查看
SELECT md.DeviceID,md.DeviceName,ms.SignalID,ms.SignalName,ms.SignalNumber FROM m_device md
	JOIN m_signal ms on md.DeviceID = ms.DeviceID 
	WHERE 
		md.roomid IN ('202503') and
		md.devicename IN ("1#工况环境","系统参数","1#一次侧机组（冷机/冷塔）","CDU") AND 
		ms.signalid IN ("013351","013352","013353","012325","012318","012321","013323","013330","012326","012329","012333"
		,"012339","012340","012334","012345","012344")  and
		ms.signalnumber = 1

SELECT * FROM m_device WHERE devicename = '1#工况环境' 
SELECT * FROM m_signal WHERE deviceid = '57602';



# 查询插入的历史数据（这不能直接用select limit，需要用between或where进行分段，将查询等级提升到type-range）
SELECT * from d_signalh WHERE siteid IN ('2025','2026','2027') limit 10;
SELECT * from d_signalh WHERE siteid = '2025' LIMIT 10;

explain SELECT * FROM d_signalh WHERE (id between 1491000000 AND 1500000000)  AND siteid = 2025  LIMIT 1000
SELECT * FROM d_signalh WHERE (id between 1491000000 AND 1500000000)  AND siteid = 2025  LIMIT 1000
explain DELETE FROM d_signalh WHERE (id between 1491000000 AND 1500000000)  AND siteid IN (2025,2026,2027)
DELETE FROM d_signalh WHERE (id between 1491000000 AND 1500000000)  AND siteid IN (2025,2026,2027)



# 数据清除
DELETE FROM m_device WHERE siteid  IN ('2025','2026','2027');
DELETE FROM m_room WHERE siteid  IN ('2025','2026','2027');
DELETE FROM m_signal WHERE siteid  IN ('2025','2026','2027');
DELETE FROM m_site  WHERE siteid  IN ('2025','2026','2027');
DELETE FROM d_signalh  WHERE siteid  IN ('2025','2026','2027');




# curl
curl -X GET "http://localhost:28016/v1/liquidCoolingReport/scheduleLiquidCoolingReport?precinctId=01-08-08-01-11-01&startTime=2025-11-03&endTime=2025-11-07" -H "accept: application/json"
curl -X GET "http://localhost:28016/v1/liquidCoolingReport/scheduleLiquidCoolingReport?precinctId=01-08-08-01-10-01&startTime=2025-10-01&endTime=2025-10-03" -H "accept: application/json"
curl -X GET "http://localhost:28016/v1/liquidCoolingReport/scheduleLiquidCoolingReport?precinctId=01&startTime=2025-10-01&endTime=2025-10-03" -H "accept: application/json"
只能传入楼栋或站点进行统计




c服务，写道kafka，在写入mpp数据库 
precint 找dim_xxx  找到mpp里面机房信息  -- 在找到devcie_spatixxx
C接口每次重启需要调用reader


修改点：
	1、冷设备名称：机房+液冷
	2、条件不用过滤
	3、测点拖进后机房+测点名称
	4、展开不用到设备层级


没配置测点不会展示







fact_dwd_signal_value
  │— 时段 + 码值过滤
  ▼
tmp_dws_liquid_cooling_mete_1
  │— join dim_liquid_cooling_mete_hour（拿到整点）
  │— row_number 取最近整点
  ▼
tmp_dws_liquid_cooling_mete_2
  │— join dwd_device_detail_v（补维度）
  │— 过滤 site_type in (1,2) 且未删除
  ▼
dws_liquid_cooling_mete_detail_day   （日粒度 + 3 时段 + 最近整点快照）



先要执行mpp的采集,mpp的任务执行完之后  再执行curl



fact_dwd_signal_value 找个表近数据有任务
show all routine LOAD
任务关闭了	
MPP数据库  ：show all routine LOAD


状态多个测点，只取最近的