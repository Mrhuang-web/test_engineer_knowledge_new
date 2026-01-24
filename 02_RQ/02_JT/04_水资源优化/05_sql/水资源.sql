# 字典
SELECT * FROM water_mete;
SELECT * FROM t_cfg_precinct LIMIT 100;
SELECT * FROM t_cfg_precinct WHERE precinct_name = '山西测试核心机楼2006中心' LIMIT 100;
SELECT * FROM t_cfg_dict where dict_note = '生产楼' LIMIT 100;
SELECT * FROM t_cfg_dict where col_name = 'precinct_kind' LIMIT 100;
# 用水字典配置
SELECT * FROM water_second_type;
# 设备测点取值
SELECT * FROM water_device_mete_day WHERE precinct_id = '01-01-25-01-09-02';
SELECT * FROM water_device_mete_month WHERE precinct_id = '01-01-25-01-09-02';
# 用水关系配置  -- 删除后执行日月刷新 -- 除了历史配置，其他都会被删除
SELECT * FROM water_formula_config WHERE precinct_id = '01-01-25-01-09-02'; 
SELECT * FROM water_formula_config_his WHERE precinct_id = '01-01-25-01-09-02';
SELECT * FROM water_formula_config_total WHERE precinct_id = '01-01-25-01-09-02';
# 用水类型中运算类型为手动填报
SELECT * FROM water_manual_month_config;
# 用水类型中运算类型为手动填报的月水量
SELECT * FROM water_manual_month_cost; 
SELECT * FROM water_precinct_project_device;
# 日水量 -删除后日刷新，记录还是会在，只是清空而已
SELECT * FROM water_station_building_day LIMIT 100; 
# 各种用水类型的月水量（月差值不是用日累加）  -删除后月刷新，记录还是会在，只是清空而已
SELECT * FROM water_station_building_month WHERE precinct_id = '01-01-25-01-09-02'; 
# 站点对应
SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-01-25-01-09-02';










# 冷却侧用水求和（冷却水补水、冷却塔排污、冷却水蒸发、应急补水）  -- 配置项
SELECT SUM(cool_water)+SUM(cool_tower_discharge_water)+SUM(cool_evaporation_water)+SUM(emergency_water) 
FROM water_formula_config_total;
# 冷却侧用水求和（冷却水补水、冷却塔排污、冷却水蒸发、应急补水）  -- 计算值  -- 只计算生产楼
SELECT SUM(a.cool_water)+SUM(a.cool_tower_discharge_water)+SUM(a.cool_evaporation_water)+SUM(a.emergency_water)  
FROM water_station_building_day a  
INNER JOIN t_cfg_precinct b on a.precinct_id=b.precinct_id
WHERE b.building_type=1; 
# 冷却侧用水
SELECT SUM(cool_side_water) FROM water_station_building_day;
SELECT * FROM  water_formula_config WHERE belong_station = '01-19-05-07-08' 
AND update_time > '2025-06-03 00:00:00' AND update_time < '2025-06-03 23:59:59';
# 站点水量查看  山西测试核心机楼2006中心 01-23-07-01-06-01
SELECT * FROM water_station_building_day WHERE precinct_id = '01-23-07-01-06-01';
SELECT * FROM water_station_building_month WHERE precinct_id = '01-23-07-01-06-01';



