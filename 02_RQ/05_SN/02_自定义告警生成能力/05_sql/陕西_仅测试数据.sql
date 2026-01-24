# ---------------------------------------------------------------------------------------------
# 数据中心
# id:00811006000001788141		动环设备id

# 通信机楼		陕西测试_通信机楼
# id:00811006000001788180		动环设备id

# 传输节点
# id:00811006000001788182		动环设备id

# 数据中心
# id:00811006000001788181		动环设备id

SELECT * FROM t_cfg_dict where col_name = 'site_level';



# 时间配置——原始：  采集间隔（collect_delay：60000毫秒-1分钟），采集时间段（collect_length：86400000毫秒-24小时）
UPDATE alert_generate_conf SET collect_length = '180000' WHERE id IN (2,4,6,8)
UPDATE alert_generate_conf SET collect_length = '86400000' WHERE id IN (2,4,6,8)





# -------------------------------------------------------------------超高温度-----------------------------------------------------------------------------------------
#	alert_generate_conf					触发告警配置  -- 【start测点为触发条件、触发后会调用reteled_handler、然后采集collect测点值、根据条件判断是否generate】
#	alert_generate_threshold			门限值配置和告警等级表    -> 017096，006099	  
#	alert_generate_collect_task		自定义告警采集表-->

SELECT * FROM alert_generate_conf;
SELECT * FROM alert_generate_threshold;
SELECT * FROM alert_generate_collect_task;
SELECT * FROM alert_alerts LIMIT 10;
SELECT * FROM alert_alerts WHERE precinct_name LIKE '%陕西测试%';
SELECT * FROM alert_alerts order BY 'alert_start_time' desc LIMIT 500;









# --------------------------------------------------------------------电压极低-------------------------------------------------------------------------------------

#	alert_generate_conf					触发告警配置  -- 【start测点为触发条件、触发后会调用reteled_handler、然后采集collect测点值、根据条件判断是否generate】
#	alert_generate_threshold			门限值配置和告警等级表    -> 017096，006099	  
#	alert_generate_collect_task		自定义告警采集表-->

SELECT * FROM alert_generate_conf;
SELECT * FROM alert_generate_threshold;
SELECT * FROM alert_generate_collect_task;
SELECT * FROM alert_alerts LIMIT 10;


SELECT * FROM sn_zz_ce_device_pe_switch_power;
SELECT * FROM sn_zz_ce_device_pe_battery;



# 数据中心	——		开关、铅酸电池、锂电池		【阈值47  --门限校验47		1级告】
# 						单一   —— 开关				00811006000001788148
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788148';

#						单一   —— 铅酸电池		 00811006000001788149	
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788149';


#						单一   —— 锂电池	  		00811006000001788160
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788160';

# 						单一   —— 开关				00811006000001788148			已配置
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788148';

#						组合   —— 三者









# 通信机楼	——		开关、铅酸电池、锂电池	【阈值47		-- 存在错误  --门限校验47		1级告警】
# 						单一   —— 开关				00811006000001788262
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788262';
INSERT INTO `sn_zz_ce_device_pe_switch_power` (`Id`, `CreateTime`, `DataDate`, `res_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `related_system`, `rated_output_voltage`, `monitoring_module_model`, `total_rack_loading_modules_number`, `total_rack_match_modules_number`, `signal_output_rated_capacity`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `related_rackpos`, `qr_code_no`, `native_ems_id`, `native_ems_name`, `power_device_id`, `power_device_name`, `project_code`) 
VALUES (3, '2025-08-04 17:43:52', '20250804', 'hjj_test_switch_power2', '陕西省', '安康市', '白河区', '陕西测试_通信机楼', '陕西测试_通信机楼', '开关电源', '分立开关电源', '陕西测试_通信机楼-开关电源', '1#', 'ZHE486KG', '中恒', 'T_PHY_COM_POWER_SMPS_SYS-ff808081798e648001799d7ff0805103', '-48V', 'ZHM09LS', '20', '20', '100', '2018-11-22', '2030-11-21', '现网', '黄佳杰', '黄佳杰', '', '', '00811006000001788262', '开关电源', '00811006000001788262', '开关电源', '');



#						单一   —— 铅酸电池		 00811006000001788149		
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788149';

INSERT INTO `sn_zz_ce_device_pe_battery` (`Id`, `CreateTime`, `DataDate`, `res_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `ralated_power_device`, `reted_capacity`, `cell_voltage_level`, `total_monomers_number`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `qr_code_no`, `backup_time`, `native_ems_id`, `native_ems_name`, `power_device_id`, `power_device_name`, `project_code`) 
VALUES (11, '2025-08-04 17:40:51', '20250804', 'hjj_test_battery3', '陕西省', '安康市', '白河区', '陕西测试_通信机楼', '陕西测试_通信机楼', '铅酸电池', '开关电源铅酸电池', '陕西测试_通信机楼-铅酸电池', '1', '6-GFM-150M', '南都', 'hjj_test_switch_power2', '150', '12V', '4', '2019-01-10', '2025-01-08', '现网', '黄佳杰', '黄佳杰', '00811006000001788263', '', '', '', '00811006000001788263', '', '');


#						单一   —— 锂电池		 00811006000001788274				开关电源zh为错误的--不触发采集任务
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788274';

INSERT INTO `sn_zz_ce_device_pe_battery` (`Id`, `CreateTime`, `DataDate`, `res_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `ralated_power_device`, `reted_capacity`, `cell_voltage_level`, `total_monomers_number`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `qr_code_no`, `backup_time`, `native_ems_id`, `native_ems_name`, `power_device_id`, `power_device_name`, `project_code`) 
VALUES (11, '2025-08-04 17:40:51', '20250804', 'hjj_test_battery7', '陕西省', '安康市', '白河区', '陕西测试_通信机楼', '陕西测试_通信机楼', '锂电池', '开关电源锂电池', '陕西测试_通信机楼-锂电池', '1', '6-GFM-150M', '南都', 'hjj_test_switch_power6', '150', '12V', '4', '2019-01-10', '2025-01-08', '现网', '黄佳杰', '黄佳杰', '00811006000001788274', '', '', '', '00811006000001788274', '', '');


#						单一   —— 开关电源		 00811006000001788262			未配置对应锂电池综资表里  --直接进行告警测试
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788262';



#						单一   —— 铅酸电池		 00811006000001788263			修改挂载的开关设备label、看是否同步
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788263';
UPDATE sn_zz_ce_device_pe_battery SET ralated_power_device = 'hjj_test_switch_power4' WHERE zh_label = '陕西测试_通信机楼-铅酸电池';		#改为传输节点的
UPDATE sn_zz_ce_device_pe_battery SET ralated_power_device = 'hjj_test_switch_power2' WHERE zh_label = '陕西测试_通信机楼-铅酸电池';		#恢复









# 传输节点	——		开关、铅酸电池、锂电池	【阈值46		-- 存在错误  --门限校验46		3级告警】
# 						单一   —— 开关				00811006000001788225
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788225';
INSERT INTO `sn_zz_ce_device_pe_switch_power` (`Id`, `CreateTime`, `DataDate`, `res_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `related_system`, `rated_output_voltage`, `monitoring_module_model`, `total_rack_loading_modules_number`, `total_rack_match_modules_number`, `signal_output_rated_capacity`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `related_rackpos`, `qr_code_no`, `native_ems_id`, `native_ems_name`, `power_device_id`, `power_device_name`, `project_code`) 
VALUES (4, '2025-08-04 17:43:52', '20250804', 'hjj_test_switch_power4', '陕西省', '安康市', '白河区', '陕西测试_传输节点', '陕西测试_传输节点', '开关电源', '分立开关电源', '陕西测试_传输节点-开关电源', '1#', 'ZHE486KG', '中恒', 'T_PHY_COM_POWER_SMPS_SYS-ff808081798e648001799d7ff0805103', '-48V', 'ZHM09LS', '20', '20', '100', '2018-11-22', '2030-11-21', '现网', '黄佳杰', '黄佳杰', '', '', '00811006000001788225', '开关电源', '00811006000001788225', '开关电源', '');



#						单一   —— 铅酸电池		 00811006000001788226		插入错误的检测
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788226';

INSERT INTO `sn_zz_ce_device_pe_battery` (`Id`, `CreateTime`, `DataDate`, `res_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `ralated_power_device`, `reted_capacity`, `cell_voltage_level`, `total_monomers_number`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `qr_code_no`, `backup_time`, `native_ems_id`, `native_ems_name`, `power_device_id`, `power_device_name`, `project_code`) 
VALUES (17, '2025-08-04 17:40:51', '20250804', 'hjj_test_battery5', '陕西省', '安康市', '白河区', '陕西测试_传输节点', '陕西测试_传输节点', '铅酸电池', '开关电源铅酸电池', '陕西测试_传输节点-铅酸电池', '1', '6-GFM-150M', '南都', 'hjj_test_switch_power4', '150', '12V', '4', '2019-01-10', '2025-01-08', '现网', '黄佳杰', '黄佳杰', '00811006000001788226', '', '', '', '00811006000001788226', '', '');








# 通信基站	——		开关、铅酸电池、锂电池	【阈值46		-- 存在错误  --门限校验46		3级告警】
# 						单一   —— 开关				00811006000001788188
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788188';
INSERT INTO `sn_zz_ce_device_pe_switch_power` (`Id`, `CreateTime`, `DataDate`, `res_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `related_system`, `rated_output_voltage`, `monitoring_module_model`, `total_rack_loading_modules_number`, `total_rack_match_modules_number`, `signal_output_rated_capacity`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `related_rackpos`, `qr_code_no`, `native_ems_id`, `native_ems_name`, `power_device_id`, `power_device_name`, `project_code`) 
VALUES (5, '2025-08-04 17:43:52', '20250804', 'hjj_test_switch_power3', '陕西省', '安康市', '白河区', '陕西测试_通信基站', '陕西测试_通信基站', '开关电源', '分立开关电源', '陕西测试_通信机楼-开关电源', '1#', 'ZHE486KG', '中恒', 'T_PHY_COM_POWER_SMPS_SYS-ff808081798e648001799d7ff0805103', '-48V', 'ZHM09LS', '20', '20', '100', '2018-11-22', '2030-11-21', '现网', '黄佳杰', '黄佳杰', '', '', '00811006000001788188', '开关电源', '00811006000001788188', '开关电源', '');



#						单一   —— 铅酸电池		 00811006000001788189		插入错误的检测
SELECT * FROM t_cfg_device WHERE device_id = '00811006000001788189';

INSERT INTO `sn_zz_ce_device_pe_battery` (`Id`, `CreateTime`, `DataDate`, `res_code`, `province_id`, `city_id`, `county_id`, `related_site`, `related_room`, `device_type`, `device_subclass`, `zh_label`, `device_code`, `product_name`, `vendor_id`, `ralated_power_device`, `reted_capacity`, `cell_voltage_level`, `total_monomers_number`, `start_time`, `estimated_retirement_time`, `lifecycle_status`, `maintainor`, `qualitor`, `qr_code_no`, `backup_time`, `native_ems_id`, `native_ems_name`, `power_device_id`, `power_device_name`, `project_code`) 
VALUES (16, '2025-08-04 17:40:51', '20250804', 'hjj_test_battery6', '陕西省', '安康市', '白河区', '陕西测试_通信基站', '陕西测试_通信基站', '铅酸电池', '开关电源铅酸电池', '陕西测试_通信机楼-铅酸电池', '1', '6-GFM-150M', '南都', 'hjj_test_switch_power3', '150', '12V', '4', '2019-01-10', '2025-01-08', '现网', '黄佳杰', '黄佳杰', '00811006000001788189', '', '', '', '00811006000001788189', '', '');






