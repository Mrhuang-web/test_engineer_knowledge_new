业务说明：
	注意：
		映射关系一定要存在，不然映射不起来（比如动环是1，那么就要有1的映射，同时综资的也要存在）
	1、在视图监控中配置关系
	2、同步执行后（就是把综资的市电配置，同步到site表中的，oil级别里面），就会根据页面配置的关系回显综资的市电配置到监控视图上
		补充逻辑：
			这里会先通过site的站点名字，匹配t_zz_power_specialty的zh_label,拿到rescode
			拿到rescode后，会到t_zz_site_property 找到对应的mains_configuration_level -- (综资的都是中文的  -- 然后的规则会匹配到)、
			匹配到之后，会把这里的mains_configuration_level，更新到site表中的zz_es_oil_machine_level上
			site的property，修改为1
		补充逻辑2：
			所有的数据都共用一份zz_power_dict_mapping表
				用于映射关系
			
	3、其他地方则取站点表中的，动环的配置
	4、t_zz_power_specialty 中 某个为0来着才是动环属性里面有的     
	
	5、回显是config/zzMappingPower/get接口返回的，因此没有返回打开编辑后，就不会展示综资的市电配置信息
	                               
其余：                                                         
	1、验证同步
	2、验证视图展示的是综资
	3、其他地方展示的是动环
	SELECT * from t_zz_power_specialty LIMIT 10;
	SELECT * from t_zz_site_property LIMIT 10;
	SELECT * from t_cfg_site LIMIT 10;
	SELECT * from  zz_power_dict_mapping;
	SELECT * from t_cfg_dict WHERE col_name = 'es_oil_machine_level';
	SELECT * from t_scheduled_task;
	






# 前置梳理
SELECT * from t_zz_power_specialty LIMIT 10;
SELECT * from t_zz_site_property LIMIT 10;
SELECT * from t_cfg_site LIMIT 10;
SELECT * from  zz_power_dict_mapping LIMIT 10;
SELECT * from t_scheduled_task LIMIT 10;




# 用已有用例举例说明
	SELECT * from t_cfg_dict WHERE col_name = 'es_oil_machine_level';
	SELECT * from t_cfg_dict WHERE col_name = 'zz_es_oil_machine_level';
	
	SELECT * from t_cfg_site WHERE zz_es_oil_machine_level IS NOT NULL;
	SELECT * from t_cfg_site WHERE es_oil_machine_level IS NOT NULL;
	SELECT * from zz_power_dict_mapping LIMIT 10;
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-07-05-02-41';
	SELECT * from t_cfg_site WHERE site_id = '01-07-05-02-41' LIMIT 10;
	SELECT * from t_zz_power_specialty WHERE zh_label = '百色测试数据to传输节点';
	SELECT * from t_zz_site_property WHERE res_code = 'SITE--0c3e-42a9-8713-fda5dd93894a';   # 2市电1油机   原来：1市电无油机

	SELECT * FROM t_cfg_precinct WHERE precinct_name = '百色测试数据to传输节点';
	SELECT * from t_cfg_site WHERE site_id = '01-07-05-02-41' LIMIT 10;
	SELECT * from t_zz_power_specialty LIMIT 10;
	SELECT * from t_zz_power_specialty WHERE zh_label = '百色测试数据to传输节点';
	SELECT * from t_zz_site_property LIMIT 10;
	SELECT * from t_zz_site_property WHERE res_code = 'SITE--0c3e-42a9-8713-fda5dd93894a';
	SELECT * from t_scheduled_task LIMIT 10;
	
	
	SELECT * FROM t_cfg_precinct WHERE precinct_name = '北海测试数据区25邮局2';
	SELECT * from t_cfg_site WHERE site_id = '01-07-07-01-34' LIMIT 10;
	SELECT * from t_zz_power_specialty LIMIT 10;
	SELECT * from t_zz_power_specialty WHERE zh_label = '北海测试数据区25邮局2';
	SELECT * from t_zz_site_property LIMIT 1000;
	SELECT * from t_zz_site_property WHERE res_code = 'SITE-8a381782202387a2012030cd988c51ac'; 
	
	UPDATE t_cfg_site SET zz_es_oil_machine_level = NULL WHERE site_id = '01-07-07-01-34';

	SELECT * from t_scheduled_task LIMIT 10;








# 广西市电
	# 综资市电油机配置的枚举值 -- mains_configuration_level字段内容
	SELECT * FROM t_zz_site_property where res_code = 'SITE--0c3e-42a9-8713-fda5dd93894a' LIMIT 10;
	
		# 综资对应信息
		SELECT * FROM t_zz_space_resources LIMIT 10;
		SELECT * FROM t_zz_space_resources where zh_label = '百色测试数据to传输节点' LIMIT 10;
		SELECT * FROM t_zz_power_specialty where zh_label = '百色测试数据to传输节点'  LIMIT 10;
	
	
	
	# 动环市电油机配置的枚举值 -- mains_configuration_level字段内容
	select * FROM t_cfg_site LIMIT 10;
	SELECT * FROM t_cfg_dict WHERE col_name = 'es_oil_machine_level';
		
		# 查看站点
		SELECT * FROM t_cfg_precinct WHERE precinct_name = '百色测试数据to传输节点';
		SELECT site_id,es_oil_machine_level,zz_es_oil_machine_level FROM t_cfg_site WHERE site_id = '01-07-05-02-41';
	









	# 手工造关联
		# 取 t_zz_space_resources  SITE-8a381782202387a2012030cd988c51ac      柳州鱼峰区金利达 修改为  北海测试数据区25邮局2
		# 取 t_zz_site_property     0001f582bf1b499f842219b5596da65f   改为    SITE-8a381782202387a2012030cd988c51ac
		# 取 t_zz_space_resources  TRAPH-8a380d9d454a8ced014603dd617153a1 和 zh_label 改为  SITE-8a381782202387a2012030cd988c51ac 和 北海测试数据区25邮局2
		# 取 t_zz_power_specialty   SITE-8a381782202387a2012030cd988c51ac   device_type_id 原本为   5 
		SELECT * FROM t_zz_space_resources	 LIMIT 10;
		SELECT * FROM t_zz_site_property LIMIT 10;
		SELECT * FROM t_zz_power_specialty LIMIT 10;
		SELECT * FROM t_zz_space_resources WHERE int_id = 'SITE-8a381782202387a2012030cd988c51ac' LIMIT 10;
		SELECT * FROM t_zz_site_property where res_code = 'SITE-8a381782202387a2012030cd988c51ac' LIMIT 10;
		SELECT * FROM t_zz_power_specialty where zh_label = '北海测试数据区25邮局2'  LIMIT 10;

		SELECT * FROM t_cfg_precinct WHERE precinct_name = '北海测试数据区25邮局2';
		
		
		
		SELECT dict_id, dict_code, dict_note, col_name, up_dict FROM t_cfg_dict WHERE col_name = 'zz_es_voltage_level' order by dict_code;
		
		
		
		
		
		
		SELECT * from t_cfg_dict WHERE col_name = 'es_oil_machine_level';
		SELECT * from t_cfg_dict WHERE col_name = 'zz_es_oil_machine_level';
		
		SELECT * FROM  t_cfg_precinct a
			JOIN t_cfg_site site ON a.precinct_id = site.site_id
			WHERE a.precinct_name = '南宁测试数据8厂第二生产楼';
		
		SELECT * FROM t_zz_power_specialty where zh_label = '南宁测试数据8厂第二生产楼'  LIMIT 10;
		

		
		
		
		
		
		
		
		
		



	# 日志
		SELECT 
			a.precinct_id precinctId,
			b.site_id siteId,
			a.precinct_name siteName,
			b.site_type siteType,
			b.property property, 
			b.es_sum_ways esSumWays, 
			b.es_voltage_level esVoltageLevel, 
			b.es_capacity esCapacity, 
			b.es_nature esNature, 
			b.backup_method backupMethod, 
			b.is_from_differ_trans_site is_fromDifferTransSite, 
			b.es_oil_machine_level esOilMachineLevel, 
			b.design_pue designPue 
		FROM t_cfg_precinct a 
			LEFT  JOIN t_cfg_site b  ON a.precinct_id = b.site_id 
			WHERE a.precinct_kind = 2  AND a.isdel= 0;
		
		
		
		

		
		SELECT distinct mains_voltage_level FROM t_zz_site_property order by mains_voltage_level;
		SELECT dict_id, dict_code, dict_note, col_name, up_dict FROM t_cfg_dict WHERE col_name = 'zz_es_voltage_level' order by dict_code;
		
		
		SELECT dict_id, dict_code, dict_note, col_name, up_dict FROM t_cfg_dict WHERE col_name = 'zz_property' order by dict_code;