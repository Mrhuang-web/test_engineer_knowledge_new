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






overdue_device_detail				超期服役-设备详情表
overdue_count_total					超期服役统计分析总表
overdue_count_manufactor			超期服役-厂家统计分析报表		
overdue_count_device					超期服役-设备类型统计分析	
overdue_count_city					超期服役-地市统计分析报表
overdue_device_type_dict			超期服役-更新周期字典表
overdue_count_room					机房超期服役统计分组表
overdue_device_alert_monthly		超期服役-设备月度告警频次表
t_scheduled_task


SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-24' LIMIT 10;

SELECT * FROM overdue_device_detail LIMIT 10;
SELECT site_type_name FROM overdue_device_detail GROUP BY site_type_name;



SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM overdue_count_total LIMIT 10;
SELECT * FROM overdue_count_device LIMIT 10;
SELECT * FROM overdue_count_manufactor LIMIT 10;
SELECT * FROM overdue_count_city LIMIT 10;
SELECT * FROM overdue_device_type_dict;
SELECT * FROM overdue_count_room LIMIT 10;
SELECT * FROM overdue_device_alert_monthly LIMIT 10;
SELECT * FROM zz_data_sync_info;

SELECT * FROM overdue_device_detail WHERE sys_device_id = '00751006000005629507'






-- 下面所有的内容都是12类型设备





--   ----------------------------------  超期服役设备详情   上海站点  ----------------------------------

-- 设备周期类别 周期年限
SELECT device_type_name,device_sub_type_name,update_cycle FROM overdue_device_detail 
WHERE device_type_name = '交流母线配电'  GROUP BY device_type_name,device_sub_type_name ;


--
SELECT * FROM overdue_device_detail WHERE device_type_name = '交流母线配电' LIMIT 10 ;

-- 周期字典
SELECT * FROM overdue_device_type_dict;

-- 验证es数据与综资表数据
SELECT * FROM overdue_count_total LIMIT 10;




--   ----------------------------------  超期服役设备详情   新旧数据区分  ----------------------------------

-- 里面存在部分旧数据：为9-15号的，因此导致页面数据不一致，真实环境不会
SELECT UPDATE_time,* FROM overdue_device_detail ORDER BY update_time asc LIMIT 10;





--   ----------------------------------  超期服役设备详情   类型周期统计判断  ----------------------------------
SELECT * FROM overdue_device_detail LIMIT 10;

-- 变压器
SELECT * FROM overdue_device_detail WHERE device_type_name = '变压器' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- 高压配电
SELECT * FROM overdue_device_detail WHERE device_type_name = '高压配电' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- 高压直流电源
SELECT * FROM overdue_device_detail WHERE device_type_name = '高压直流电源' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;


-- 高压直流配电
SELECT * FROM overdue_device_detail WHERE device_type_name = '高压直流配电' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- 低压交流配电
SELECT * FROM overdue_device_detail WHERE device_type_name = '低压交流配电' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- 发电机组
SELECT * FROM overdue_device_detail WHERE device_type_name = '发电机组' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- 开关电源
SELECT * FROM overdue_device_detail WHERE device_type_name = '开关电源' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- 低压直流配电
SELECT * FROM overdue_device_detail WHERE device_type_name = '低压直流配电' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- UPS设备
SELECT * FROM overdue_device_detail WHERE device_type_name = 'UPS设备' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- 蓄电池
SELECT * FROM overdue_device_detail WHERE device_type_name = '蓄电池' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- 空调
SELECT * FROM overdue_device_detail WHERE device_type_name = '空调' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;

-- 动环监控
SELECT * FROM overdue_device_detail WHERE device_type_name = '动环监控' GROUP BY device_type_name,device_sub_type_name,update_cycle LIMIT 1000;



--   ----------------------------------  统计分析总表   统计一致性  ----------------------------------
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-04-01-09';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '广西';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '阜阳市';
SELECT * FROM overdue_device_detail LIMIT 10;

-- 全省数据  -不一致
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name 
	IN (SELECT device_type FROM overdue_device_type_dict GROUP BY device_type);
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '高压直流配电';
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '高压直流开关电源';
	


-- 安徽省
SELECT COUNT(*) FROM overdue_device_detail WHERE room_id LIKE "01-02%";
SELECT * FROM overdue_device_detail WHERE device_type_name = '变压器' AND  room_id LIKE "01-02%";
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND  room_id LIKE "01-02%";

-- 北京省
SELECT COUNT(*) FROM overdue_device_detail WHERE room_id LIKE "01-04%";
SELECT * FROM overdue_device_detail WHERE device_type_name = '变压器' AND  room_id LIKE "01-04%";
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND  room_id LIKE "01-04%";


-- 安徽省 - 阜阳市（统计导出10条，但是详情表只有9条）
SELECT * FROM overdue_device_detail WHERE device_type_name = '变压器' AND  room_id LIKE "01-02-02%";
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND  room_id LIKE "01-02-02%";

-- 北京省 -昌平区
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND  room_id LIKE "01-04-01-09%";


-- 统一分析表  最新数据
SELECT * FROM overdue_count_total order by date desc LIMIT 10;
SELECT DATE FROM overdue_count_total WHERE sub_precinct_id LIKE "01-02%" GROUP BY DATE ;
SELECT * FROM overdue_count_total WHERE device_type_name = '变压器' AND   sub_precinct_id = "01-02" AND city_name IS NOT NULL AND DATE = '2025-09-28';
SELECT SUM(overdue1_num)+SUM(overdue2_num)+SUM(overdue3_num)+SUM(overdue4_num) FROM overdue_count_total WHERE device_type_name = '变压器' AND   sub_precinct_id = "01-02" AND DATE = '2025-09-28';
SELECT * FROM overdue_count_total WHERE DATE = '2025-09-28' AND sub_precinct_id = '01-02' AND device_type_name = '变压器';



-- 新一轮筛选，有过滤的
	
SELECT * FROM t_cfg_precinct WHERE precinct_name = '昌平区';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '中国移动北京昌平区0940枢纽楼';
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='UPS设备' AND room_id LIKE "01-07%" AND manufactor_name = '厦门科华恒盛股份有限公司' AND site_type_name = '传输节点';


SELECT * FROM overdue_device_detail WHERE device_type_name='UPS设备' AND room_id LIKE "01-04%" AND manufactor_name = '中国' AND site_type_name = '通信枢纽楼';
SELECT * FROM overdue_device_detail WHERE device_type_name='UPS设备' AND room_id LIKE "01-04-01-09-40%" AND manufactor_name = '华为' AND site_type_name = '通信枢纽楼';


SELECT * FROM overdue_device_detail WHERE device_type_name='UPS设备' AND room_id LIKE "01-04-01-09%" AND site_type_name = '通信枢纽楼';
SELECT * FROM overdue_device_detail WHERE device_type_name='UPS设备' AND room_id LIKE "01-04-01-09-40%" AND site_type_name = '通信枢纽楼';

SELECT * FROM overdue_device_detail WHERE room_id LIKE "01-04%" AND site_type_name = '通信枢纽楼';
SELECT * FROM overdue_device_detail WHERE room_id LIKE "01-04-01%" AND site_type_name = '通信枢纽楼';
SELECT * FROM overdue_device_detail WHERE room_id LIKE "01-04-01-09%" AND site_type_name = '通信枢纽楼';







--   ----------------------------------  设备类型统计表   统计一致性  ----------------------------------
SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM t_cfg_precinct WHERE precinct_name = '湖南';


-- 随意类型
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='高压直流配电' and DATE = '2025-09-30' AND site_type_name IS NOT null AND site_type_name !='通信枢纽楼';
SELECT * FROM overdue_device_detail WHERE device_type_name='UPS设备' and DATE = '2025-09-30' AND site_type_name IS NOT null AND site_type_name !='通信枢纽楼';

SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='高压直流开关电源' and DATE = '2025-09-30' AND site_type_name IS NOT null;

SELECT * FROM overdue_device_detail WHERE device_type_name= 'UPS设备' and DATE = '2025-09-30' LIMIT 10;



	

-- 全设备类型
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name 
	IN (SELECT device_type FROM overdue_device_type_dict GROUP BY device_type);


-- 变压器类型
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='变压器';
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='变压器' AND site_type_name = '通信枢纽楼' ;
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='变压器' AND room_id LIKE "01-02%";
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='变压器' AND site_type_name = '通信枢纽楼' AND room_id LIKE "01-02%";
SELECT * FROM overdue_device_detail WHERE device_type_name='变压器' LIMIT 10;


SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='高压直流开关电源' AND room_id LIKE "01-07%" AND manufactor_name = '维谛技术有限公司';




-- 设备表
SELECT * FROM overdue_count_device LIMIT 10;
SELECT * FROM overdue_count_device GROUP BY precinct_id;
SELECT SUM(overdue1_num)+SUM(overdue2_num)+SUM(overdue3_num)+SUM(overdue4_num) FROM overdue_count_device WHERE  CHAR_LENGTH(precinct_id) = 5 and device_type_name = '变压器'   AND DATE = '2025-09-28'; 
SELECT SUM(overdue1_num)+SUM(overdue2_num)+SUM(overdue3_num)+SUM(overdue4_num) FROM overdue_count_device WHERE  CHAR_LENGTH(precinct_id) = 2 and device_type_name = '变压器'   AND DATE = '2025-09-28'; 
SELECT * FROM overdue_count_device WHERE  CHAR_LENGTH(precinct_id) = 2 and device_type_name = '变压器'   AND DATE = '2025-09-28'; 
SELECT * FROM overdue_count_device WHERE  CHAR_LENGTH(precinct_id) = 5 and device_type_name = '变压器'   AND DATE = '2025-09-28'; 



SELECT SUM(total_device_num) FROM overdue_count_device WHERE device_type_name = '变压器'   AND DATE = '2025-09-28' and precinct_id = '01-02';
SELECT SUM(overdue1_num) FROM overdue_count_device WHERE device_type_name = '变压器'   AND DATE = '2025-09-28';
SELECT DATE FROM overdue_count_device WHERE sub_precinct_id GROUP BY DATE;
SELECT SUM(overdue1_num)+SUM(overdue2_num)+SUM(overdue3_num)+SUM(overdue4_num) FROM overdue_count_device WHERE device_type_name = '变压器'  AND DATE = '2025-09-28';



-- 设备表分类，份时间
SELECT * FROM overdue_count_device WHERE device_type_name = '高压直流配电'   AND DATE = '2025-09-30' GROUP BY update_time;






--   ----------------------------------  厂家统计分析表   统计一致性  ----------------------------------
SELECT * FROM overdue_device_detail LIMIT 10;

-- 全省厂家 - 类型
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND manufactor_name = '株洲变压器厂';
SELECT * FROM overdue_device_detail WHERE device_type_name = '变压器' AND manufactor_name = '华为' AND CHAR_LENGTH(city_name) IN (3,4) AND date = '2025-09-30' AND site_type_name IS NOT NULL;

SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND manufactor_name = '华为' AND date = '2025-09-30' AND site_type_name IS NOT null;
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND manufactor_name = '华为' AND CHAR_LENGTH(city_name) IN (3,4) AND date = '2025-09-30';

SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND manufactor_name = '华为' AND date = '2025-09-30' AND site_type_name IS NOT null;
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND manufactor_name = '华为' AND CHAR_LENGTH(city_name) IN (3,4) AND date = '2025-09-30';


SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '变压器' AND manufactor_name = '华为';
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '高压直流配电' AND manufactor_name = '中兴';


-- 单省厂家 - 类型
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '高压直流配电' AND manufactor_name = '北京动力源科技股份有限公司' AND room_id LIKE "01-02%";


-- 单市厂家 - 类型
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name = '高压直流配电' AND manufactor_name = '北京动力源科技股份有限公司' AND room_id LIKE "01-02-11%";



-- 统计分组
SELECT overdue_type,COUNT(*) FROM overdue_device_detail 
	WHERE device_type_name = '变压器' AND manufactor_name = '华为' AND room_id LIKE "01-02%"
	GROUP BY overdue_type; 


SELECT overdue_type,COUNT(*) FROM overdue_device_detail 
	WHERE device_type_name = '变压器' AND manufactor_name = '华为' AND site_type_name IS NOT null
	GROUP BY overdue_type; 


-- 统计分组，去除无站点信息的


SELECT sum(total_device_num) FROM overdue_count_manufactor where precinct_id = '01-02' and device_type_name = '变压器' and DATE = '2025-09-29' GROUP BY update_time;









--   ----------------------------------  地市统计分析表   统计一致性  ----------------------------------
SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM t_cfg_precinct WHERE precinct_name = '宁夏';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '阜阳市';


SELECT * FROM overdue_count_city ORDER BY DATE DESC  LIMIT 10;


-- 省级别
SELECT COUNT(*) FROM overdue_device_detail WHERE room_id LIKE '01-20%';
select COUNT(*) FROM overdue_device_detail WHERE room_id LIKE '01-20%' AND device_type_name IN 
	(
		SELECT device_type FROM overdue_device_type_dict GROUP BY device_type
	);
SELECT COUNT(*) FROM overdue_device_detail WHERE room_id LIKE '01-20%' and device_type_name='变压器';



-- 市级别
SELECT COUNT(*) FROM overdue_device_detail WHERE city_name = '安庆市'
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='变压器';
SELECT COUNT(*) FROM overdue_device_detail WHERE city_name = '滁州市' and device_type_name='变压器';


-- 区级别
SELECT COUNT(*) FROM overdue_device_detail WHERE city_name = '安庆市'
SELECT COUNT(*) FROM overdue_device_detail WHERE device_type_name='变压器';
SELECT COUNT(*) FROM overdue_device_detail WHERE city_name = '滁州市' and device_type_name='变压器';













--   ----------------------------------  超期服役设备详情   贵州（动环） - 广州（综资）地区  设备关联告警 ----------------------------------
SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM overdue_device_alert_monthly LIMIT 10;
SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州贵阳市贵安新区1104数据中心0438楼栋机房1';





-- 统计 power_device_id不为空的【重点】
-- 贵州 device_id：00751006000005629510
SELECT * FROM t_cfg_device WHERE device_name = '高压直流配电'
SELECT * FROM t_cfg_device WHERE device_name = '高压直流电源配电'
SELECT * FROM overdue_device_detail WHERE sys_device_id IS NOT NULL LIMIT 100;
SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-01-02-01-01';
SELECT * FROM t_cfg_device WHERE device_id = '00751006000005629510';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002844404';
SELECT * FROM t_cfg_device WHERE device_id = '00751006000005629507';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002844391';



-- 广西 device_id：00751006000005629510
SELECT * FROM t_cfg_device WHERE device_name = '高压直流配电'
SELECT * FROM t_cfg_device WHERE device_name = '高压直流电源配电'
SELECT * FROM overdue_device_detail WHERE power_device_id IS NOT NULL LIMIT 100;
SELECT * FROM overdue_device_detail WHERE sys_device_id IS NOT NULL LIMIT 100;
SELECT * FROM t_cfg_device WHERE precinct_id = '01-07-07-04-02-08';
SELECT * FROM t_cfg_device WHERE device_id = '00451006000004650625';


-- 东莞  04492006000005096123
SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州贵阳市贵安新区1104数据中心0438楼栋机房1';
SELECT * FROM t_cfg_device WHERE power_device_id  = '04492006000005096123'



-- 综资id：00000898390656
-- 动环model：00001008000002844404
SELECT * FROM t_cfg_precinct WHERE precinct_name = '广东';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '广东广州市黄埔区0603数据中心0301楼栋0113机房';
SELECT * FROM t_cfg_device WHERE device_id = '04489006000003662404';
SELECT * FROM t_cfg_device WHERE precinct_id = '01-01-17-06-03-01-13';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002844404';  -- 换成陕西的看看



SELECT * FROM t_cfg_precinct WHERE precinct_name = '广东';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州贵阳市贵安新区1104数据中心0438楼栋机房1';
SELECT * FROM t_cfg_device WHERE device_id = '04489006000003662404';
SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-01-02-01-01';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002844404';




SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州贵阳市贵安新区1104数据中心0438楼栋机房1';
SELECT * FROM t_cfg_device WHERE device_id = '04489006000003662404';
SELECT * FROM t_cfg_device WHERE precinct_id = '01-08-08-01-02-01-01';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002844404';
SELECT * FROM overdue_device_detail WHERE room_name LIKE  '贵州贵阳市贵安新区1104数据中心0438楼栋%' LIMIT 10;




-- ups设备 类型的【重点】
SELECT * FROM overdue_device_detail WHERE device_type_name LIKE  'UPS设备%' and room_name LIKE  '贵州贵阳市贵安新区1104数据中心0438楼栋%' LIMIT 10;


SELECT * FROM t_cfg_device LIMIT 10;
SELECT * FROM t_cfg_mete LIMIT 10;
SELECT * FROM t_cfg_metemodel LIMIT 10;
SELECT * FROM t_cfg_metemodel_detail LIMIT 10;




-- 找sys_device_id 大于10长度的
SELECT * FROM overdue_device_detail WHERE char_length(sys_device_id)>8 AND city_name = '广州市';





-- 高压直流配电
SELECT * FROM t_cfg_device WHERE device_name = '高压直流配电';
SELECT * FROM t_cfg_device WHERE device_name = '高压直流电源配电';
SELECT * FROM t_cfg_metemodel_detail where mete_code = '087040' LIMIT 10;





-- 查看告警情况
SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM overdue_device_detail where alert_times > 1 LIMIT 10;


-- 查看生命周期-总分析是否有告警了
SELECT * FROM overdue_count_total LIMIT 10;
SELECT * FROM overdue_count_total WHERE overdue1_alert_times>=1 OR overdue2_alert_times>=1 OR overdue3_alert_times>=1 OR overdue4_alert_times>=1
AND DATE = '2025-09-27';


























-- 最新查看语句
SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM overdue_device_alert_monthly LIMIT 10;

SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-25-01-09-02-06';
SELECT * FROM t_cfg_precinct WHERE precinct_name = '贵州贵阳市贵安新区1104数据中心0438楼栋机房1';
SELECT * FROM overdue_device_detail WHERE site_name IN ('广东东莞市东莞市0109数据中心0902楼栋0206机房') LIMIT 10;





SELECT * FROM t_cfg_device WHERE device_id = '00751006000005629507';
SELECT * FROM t_cfg_device WHERE device_id = '04492006000005096123';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002827788';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-25-01-09-02-06';



SELECT * FROM t_cfg_device WHERE char_length(power_device_id) >8 ;
SELECT * FROM overdue_device_detail where alert_times > 0 LIMIT 10;














-- 实验   【拿随意直流的】
SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM overdue_device_alert_monthly LIMIT 10;


SELECT * FROM t_cfg_device WHERE char_length(power_device_id) >8 ;
SELECT * FROM overdue_device_detail where alert_times > 0 LIMIT 10;
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-07-04-02-08';
SELECT * FROM t_cfg_device WHERE device_id = '00451006000004650625';
SELECT * FROM t_cfg_device WHERE device_id = '7312001006000005625007';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000003560162';
SELECT * FROM overdue_device_detail WHERE sys_device_id = '7312001006000005625007';



SELECT * FROM t_cfg_device WHERE device_name like '变压器%' LIMIT 100;    -- 第1条
SELECT * FROM t_cfg_device WHERE device_model = '00001008000002843345' LIMIT 10;
SELECT * FROM t_cfg_device WHERE device_id = '7312001006000005625007';
SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000002843345' LIMIT 10;
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-12-05-05-37-01';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-12-05-05-37-01';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-12-05-05-37-01';
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-12';



SELECT * FROM t_cfg_metemodel_detail where model_id IN 
	(SELECT device_model FROM t_cfg_device WHERE device_name like '变压器%' LIMIT 1000);




SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM overdue_device_detail  WHERE  device_type_name LIKE '变压器%'  LIMIT 10;
SELECT * FROM overdue_device_detail  WHERE  device_code  =  '-1125009106';

SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-26';


SELECT * FROM t_cfg_device a
	JOIN overdue_device_detail b ON a.power_device_id  = b.sys_device_id LIMIT 10;


SELECT * FROM t_cfg_device a
	JOIN overdue_device_detail b ON a.device_id  = b.sys_device_id LIMIT 10;
	
	
SELECT * FROM overdue_device_detail  WHERE sys_device_id IS NOT NULL LIMIT 10;



SELECT * FROM overdue_device_detail  WHERE sys_device_id IS NOT NULL;








--  从0开始
SELECT * FROM overdue_device_detail LIMIT 10;
SELECT * FROM overdue_count_total LIMIT 10;
SELECT * FROM overdue_count_device LIMIT 10;
SELECT * FROM overdue_count_manufactor LIMIT 10;
SELECT * FROM overdue_count_city LIMIT 10;
SELECT * FROM overdue_device_type_dict;

SELECT * FROM overdue_count_total LIMIT 10;





SELECT * FROM m_area LIMIT 10;




SELECT * FROM t_cfg_monitordevice LIMIT 10


spider