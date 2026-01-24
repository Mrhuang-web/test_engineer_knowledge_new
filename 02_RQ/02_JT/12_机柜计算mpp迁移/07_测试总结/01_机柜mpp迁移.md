# 01总结

```

```





# 02补充

```
6、集团
	涉及服务：
		composite、cabinet（接口都在这里执行）、mpp
		composite-service、mpp-service、cabinet-service
				（  机柜列和机柜都在路由1和路由2的电能和功率配置测点数据  ）
				（  机房内已接入FSU）
		注意：接口传入的参数，及统计参数日期的（如传入 20251010，那能量的就会计算1009 00：00：00  到 1010 00：00：00 离零点前后一小时最近的两条数据进行求差值）
		


	机柜管理mpp（mpp相当于fsu -- 落入fact）
		(机柜和机柜列配置测点，不受限制)

		机柜管理（机柜和机柜列都需要配置用电关系）
			机柜(必须配置支路1和支路2的功率和电能，才能触发)：
			机柜列：
		
			
		机柜报表分析(分别执行机柜，机柜列的，执行后便会统计到机柜报表分析中  -- 根据机柜管理机柜列和机柜用电关系配置来生成)
			生成逻辑：
				电量：当日零点值-昨日零点值(如传入 20251010，那能量的就会计算1009 00：00：00  到 1010 00：00：00 离零点前后一小时最近的两条数据进行求差值)
				功率：取最接近0点的数（比如传入的是20251010，那么10号的报表，取的就是里11号00:00最近的一条）
			报表：
				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetReport?dayDate=2025-11-24&roomId=01-08-08-03-07-02-01"
				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetColumnReport?dayDate=2025-11-24&roomId=01-08-08-03-07-02-01"

				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetReport?dayDate=2025-11-24&roomId=01-08-08-01-11-01-01"
				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetColumnReport?dayDate=2025-11-24&roomId=01-08-08-01-11-01-01"
			
				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetReport?dayDate=2025-11-26&roomId=01-08-08-01-11-01-04"
				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetColumnReport?dayDate=2025-11-26&roomId=01-08-08-01-11-01-04"

				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetReport?dayDate=2025-09-29&roomId=01-08-08-01-11-01-04"
				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetColumnReport?dayDate=2025-09-29&roomId=01-08-08-01-11-01-04"

				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetReport?dayDate=2025-09-02&roomId=01-08-08-01-11-01-04"

				curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetColumnReport?dayDate=2025-09-01&roomId=01-08-08-01-11-01-04"
		

		
			
		机柜视图配置（简单的展示而已  -- 需要先配置机柜视图，才能进行机柜可视化的查看）
			排序：
				energy_cabinet_column_view
		
		
		
		
		
		机柜可视化
			(可以根据报表已经配置机柜的机房--即机房报表    -- 找到对应机房)


			涉及表：energy_cabinet_daily_report
			
			电力容量统计（取最近2小时的）
				整体电力容量：机柜管理中-机房下对应机柜列的额定功率之和
				已用电力容量：机柜管理中-机房下对应机柜列的用电关系 -- 支路功率之和（如果有多个机柜列，那就统计多个机柜列之和 -- 只有1和2路）  --> 需求中（是机柜1和2支路功率之和）
				未用电力容量：整体-已用
			
			机房用电量
				昨日用电量：（计算为：昨日零点最近的1条数据，与今天零点最近的一条数据的差值  -- 需要相差整点24小时）
					eg：
						2025-11-24  10.09
						2025-11-24 01:00:00			28.48
						2025-11-25 01:00:00			38.57
						
				上月用电量：（应该也是一样的逻辑，只不过取得是月初和月底）
					eg：
			
			机房温湿度：
				取实时数据 -- 017302、017301测点
			
			
			机柜能耗（测试机柜数据）：
				能耗管理-机柜报表分析-机柜报表-机柜总电量（kWh）
				触发机柜既有数据：curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetReport?dayDate=2025-11-24&roomId=01-08-08-01-11-01-04"
				
			
			pue：
				配置：
					用电关系（主要）：配置it电流和总电流,必须是以下测点
					
					实时（前端自动轮询接口）：
						计算实时PUE：取用机房能耗用电关系的总个IT的，找到8类设备替换成功对应功率测点系数复用，计算实时PUE（每小时计算一次，取最近2小时的fsu，存储在redis->energy:roomPue01-32-07-01-08-01）
						第二、三位（设备类型编码） 设备类型 信号标准名 信号编码ID 单位
						01 高压配电 总有功功率P 001325 kW
						02 低压交流配电 总有功功率P 002345 kW
						04 低压直流配电 直流功率 004304 kW
						08 UPS设备 输出总有功功率P 008342 kW
						09 UPS配电 输入xx总有功功率P 009331 kW
						88 高压直流电源配电 主路总功率 088306 kW
						92 智能电表 总有功功率 092330 kW
						96 交流母线配电 始端XX总有功功率 096314 kW
						
						pue计算规则为总用电/it用电
					
					配置后，在用电关系（主要）对应站点，点击数据刷新，即可触发，进行计算 ( 只计算昨天的pue，上个月不知道会不会 ) -- 开发说只会刷新近3天的数据

						
				昨日：
					取自能耗机房的总用电量（能耗报表-机房能耗）
				上月：
					取自能耗机房的总用电量（能耗报表-机房能耗）
			
			

			涉及能耗（机房pue和用电量：重点）：
					curl --location 'http://10.12.7.160:32458/v1/energy/executeStationEleBetweenTime?stationIdStr=01-08-08-01-11&startTime=2025-09-01&endTime=2025-11-30'
					curl --location 'http://10.12.7.160:32458/v1/energy/executeStationEleBetweenTime?stationIdStr=01-08-07-11-04&startTime=2025-10-01&endTime=2025-11-30'
					curl -X POST 
					curl -X GET "http://10.12.8.147:30917/v1/energy/scheduleCabinetReport?dayDate=2025-09-29&roomId=01-08-08-01-11-01-04"
					curl "http://10.12.8.147:30917/v1/energy/scheduleCabinetColumnReport?dayDate=2025-09-29&roomId=01-08-08-01-11-01-04"




		
				没有查询到，缓存数据会计算
					Closing non transactional SqlSession [org.apache.ibatis.session.defaults.DefaultSqlSession@5018b7ec]
					2024-04-15 14:38:48.736 INFO 7 —- [ool-14-thread-5] c.a.g.e.s.s.ComplexEnergyConfigSchedule : 机房01-32-13-10-31-01生成计算公式：总用电- (1212001006000000006587088306_01)+(1212001006000000006584092330_01)+(1212001006000000006563008342_01)+(1212001006000000006567008342_01)，it用电- (1212001006000000006563008342_00.8)+(1212001006000000006567008342_00.8)+(1212001006000000006584092330_0*0.8)
					2024-04-15 14:38:48.743 INFO 7 —- [ool-14-thread-5] c.a.g.e.s.s.ComplexEnergyConfigSchedule : 机房01-32-13-10-31-01计算实时pue成功
					2024-04-15 14:38:51.045 INFO 7 —- [nio-9988-exec-3] c.a.g.e.s.s.ComplexEnergyConfigSchedule : 查询机房01-32-13-10-31-01从redis的缓存值成功

			

			现网
				curl "http://localhost:30917/v1/energy/scheduleCabinetReport?dayDate=2025-11-27&roomId=01-08-07-11-04-39-21"
				curl "http://localhost:30917/v1/energy/scheduleCabinetColumnReport?dayDate=2025-11-27&roomId=01-08-07-11-04-39-21"
				curl --location 'http://localhost32458/v1/energy/executeStationEleBetweenTime?stationIdStr=01-08-07-11-04&startTime=2025-10-01&endTime=2025-11-30'






			

```

