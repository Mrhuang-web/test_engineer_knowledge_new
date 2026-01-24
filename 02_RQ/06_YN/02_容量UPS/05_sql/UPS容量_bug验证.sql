# 已用造数（一个系统，多个设备）
	
	# 查找设备（可以直接在设备中查找已经有关联的）
	SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
	SELECT * FROM t_cfg_device WHERE device_name = '四楼电力室1#艾默生(EMERSON UPS)(NXR)';
	SELECT * FROM t_cfg_device WHERE device_id IN ('00531006000005759877','37261006000000079739');
	SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000010762';
	# 删除曾经已经产生的数据
	SELECT * FROM device_es_mete WHERE device_id IN ('00531006000005759877','37261006000000079739');
	DELETE FROM device_es_mete WHERE device_id IN ('00531006000005759877','37261006000000079739');
	# 建立关联设备并准备数据（三相输出电流计算逻辑）   ---- 设备与系统关联
	SELECT * FROM t_cfg_devicesys_detail WHERE sub_id IN ('00531006000005759877','37261006000000079739');
	SELECT * FROM t_cfg_devicesys_detail WHERE devicesys_id IN ('da8ed141-a97b-4b28-aa2b-0127ea952e5e');
	INSERT INTO  t_cfg_devicesys_detail (devicesys_id,sub_id,scc_index,cell_index,cell_num) VALUE ('da8ed141-a97b-4b28-aa2b-0127ea952e5e','37261006000000079739',NULL,NULL,NULL);
	# ups定义
	SELECT * FROM t_cfg_devicesys where devicesys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';	
	# 设备系统所属precinct_id要存在precinct表中
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01-03';
	SELECT * FROM t_cfg_precinct WHERE precinct_name = 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房(test)';


	# 容量历史数据
	SELECT * from device_es_mete LIMIT 10;
	SELECT * from device_es_mete WHERE sys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';
	
	
	# 容量实时数据
	SELECT * from t_current_capacity;
	SELECT * from t_current_capacity WHERE sys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';










#   -------------------------------------------同机房同系统，负载详情和当前负载计算的‘额定容量’取值不一样------------------------------------------------



建立数据：
	#  同楼栋 -- 同机房 -- 同设备系统 -- 同设备类型
	#  先到 配置 - 批量维护  -> 系统中任意选择一个站点进行系统创建（滑倒最左侧有编辑功能，编辑好就算创建成功）
		# 选择数据：
			昭阳区电信局  KJ-DL-ZHT0002_昭阳区全球通大楼五楼动力机房  五楼1#艾默生UPS(NXR)
			昭阳区电信局  KJ-DL-ZHT0002_昭阳区全球通大楼五楼动力机房  五楼2#艾默生UPS(NXR)
			系统名称：测试容量系统2
	#  紧接 配置 - 批量维护 -> 设备中找到刚刚建立机房下两个系统下的设备，进行编辑子系统等配置
		# 选择数据：
			昭阳区电信局  KJ-DL-ZHT0002_昭阳区全球通大楼五楼动力机房  五楼1#艾默生UPS(NXR)  一体化高频UPS 200
			昭阳区电信局  KJ-DL-ZHT0002_昭阳区全球通大楼五楼动力机房  五楼2#艾默生UPS(NXR)  一体化高频UPS 300
	#  紧接 确保设备有测点模板
	#  紧接 触发接口
		# 接口数据
			curl 'http://10.12.7.157:3105/v1/capacity/statisticCapacityByDateAndPrecinctId?precinctId=01-32-01-02-09&date=2025-12-05&namespace=alauda'

	#查看设备所属省市区站点信息
	select province.precinct_name,city.precinct_name,county.precinct_name,site.precinct_id from t_cfg_precinct site 
		join t_cfg_precinct county on site.up_precinct_id = county.precinct_id
		join t_cfg_precinct city on county.up_precinct_id = city.precinct_id
		join t_cfg_precinct province on city.up_precinct_id = province.precinct_id
		where 
			site.precinct_name = "昭阳区电信局"; 



	# 查找设备（可以直接在设备中查找已经有关联的）
	SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
	SELECT * FROM t_cfg_device WHERE device_name IN ('五楼1#艾默生UPS(NXR)','五楼2#艾默生UPS(NXR)');
	SELECT * FROM t_cfg_device WHERE device_id IN ('00531006000003792725','00531006000003792726');
	SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000010762';
	
	
	# 设备系统所属precinct_id要存在precinct表中
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01-03';
	SELECT * FROM t_cfg_precinct WHERE precinct_name = 'KJ-DL-ZHT0002_昭阳区全球通大楼五楼动力机房';
	
	
	
	# 查看容量统计数据
	SELECT * FROM device_es_mete WHERE device_id IN ('00531006000003792725','00531006000003792726');

	






#   -------------------------------------------同机房同系统，负载详情和当前负载计算的‘额定容量’取值不一样------------------------------------------------



建立数据：
	#  同楼栋 -- 不同机房 -- 同设备系统 -- 同设备类型
	#  先到 配置 - 批量维护  -> 系统中任意选择一个站点进行系统创建（滑倒最左侧有编辑功能，编辑好就算创建成功）
		# 选择数据：
			昭阳区电信局 KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房 四楼电力室2#艾默生(EMERSON UPS)(NXR) 	   	测试容量系统1
			昭阳区电信局 KJ-DL-ZHT0005_昭阳区全球通大楼四楼新增动力机房 四楼新增电力室2#UPS主机1(中达GES20     测试容量系统1
			系统名称：测试容量系统2
	#  紧接 配置 - 批量维护 -> 设备中找到刚刚建立机房下两个系统下的设备，进行编辑子系统等配置
		# 选择数据：
			昭阳区电信局 KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房 四楼电力室2#艾默生(EMERSON UPS)(NXR) 	     一体化高频UPS 
			昭阳区电信局 KJ-DL-ZHT0005_昭阳区全球通大楼四楼新增动力机房 四楼新增电力室2#UPS主机1(中达GES204DS)     一体化高频UPS
	#  紧接 确保设备有测点模板
	#  紧接 触发接口
		# 接口数据
			curl 'http://10.12.7.157:3105/v1/capacity/statisticCapacityByDateAndPrecinctId?precinctId=01-32-01-02-09&date=2025-12-05&namespace=alauda'

	#查看设备所属省市区站点信息
	select province.precinct_name,city.precinct_name,county.precinct_name,site.precinct_id from t_cfg_precinct site 
		join t_cfg_precinct county on site.up_precinct_id = county.precinct_id
		join t_cfg_precinct city on county.up_precinct_id = city.precinct_id
		join t_cfg_precinct province on city.up_precinct_id = province.precinct_id
		where 
			site.precinct_name = "昭阳区电信局"; 



	# 查找设备（可以直接在设备中查找已经有关联的）
	SELECT * FROM t_cfg_dict WHERE col_name = 'device_type';
	SELECT * FROM t_cfg_device WHERE device_name IN ('四楼电力室2#艾默生(EMERSON UPS)(NXR)','四楼新增电力室2#UPS主机1(中达GES204DS)');
	SELECT * FROM t_cfg_device WHERE device_id IN ('00531006000003792648','00531006000005759880');
	SELECT * FROM t_cfg_metemodel_detail WHERE model_id = '00001008000000010762';
	
	
	# 设备系统所属precinct_id要存在precinct表中
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01';
	SELECT * FROM t_cfg_precinct WHERE precinct_id = '01-32-01-02-01-03';
	SELECT * FROM t_cfg_precinct WHERE precinct_name = 'KJ-DL-ZHT0003_昭阳区全球通大楼四楼动力机房';
	SELECT * FROM t_cfg_precinct WHERE precinct_name = 'KJ-DL-ZHT0005_昭阳区全球通大楼四楼新增动力机房';
	
	
	
	# 查看容量统计数据
	SELECT * FROM device_es_mete WHERE device_id IN ('00531006000003792648','00531006000005759880');























	
	
	
	# -------------- 这一块要确认下 --------------
	
	
	# 建立关联设备并准备数据（三相输出电流计算逻辑）   ---- 设备与系统关联
	SELECT * FROM t_cfg_devicesys_detail WHERE sub_id IN ('00531006000005759877','37261006000000079739');
	SELECT * FROM t_cfg_devicesys_detail WHERE devicesys_id IN ('da8ed141-a97b-4b28-aa2b-0127ea952e5e');
	INSERT INTO  t_cfg_devicesys_detail (devicesys_id,sub_id,scc_index,cell_index,cell_num) VALUE ('da8ed141-a97b-4b28-aa2b-0127ea952e5e','37261006000000079739',NULL,NULL,NULL);
	
	# ups定义
	SELECT * FROM t_cfg_devicesys where devicesys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';	
	
	

	# 容量历史数据
	SELECT * from device_es_mete LIMIT 10;
	SELECT * from device_es_mete WHERE sys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';
	
	
	# 容量实时数据
	SELECT * from t_current_capacity;
	SELECT * from t_current_capacity WHERE sys_id = 'da8ed141-a97b-4b28-aa2b-0127ea952e5e';