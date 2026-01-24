# 01总结

```
本次提测内容：
1、综资的csv文件写入mpp

涉及服务：external-service

涉及脚本：
1、https://gitsz1.aspirecn.com/spider/kernel/-/blob/develop/master/bin/dbscript/3.0.27.0/ddl/综资数据写入mpp_ddl_20251223.sql
2、https://gitsz1.aspirecn.com/spider/kernel/-/blob/develop/master/bin/dbscript/3.0.27.0/dml/综资数据写入mpp_dml_20251223.sql

涉及配置：
1、external-service添加如下配置
starrocks:
  host: 10.1.4.115 #StarRocks的fe的LEADER节点ip
  port: 8030 #StarRocks的fe的http端口
  data-base: dh
  user-name: dh
  passcode: xxxx
  batch-size: 10000 #每批次写入StarRocks的行数
  label-flag: 0 #是否启用label(事务，避免重复导入), 0-不启用，1-启用



其它说明：
1、触发任务curl，ip和端口是cicd上external-service服务对应的ip和端口；
2、orderId参数的值可以对应修改；
3、batchNum格式为yyyyMMdd；saveEsOrMpp是es或mpp，es则是写入es，mpp则写入mpp
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000010,SSSP-20241031-000018,SSSP-20241031-000021,SSSP-20241031-000022,SSSP-20241031-000023,SSSP-20241031-000025,SSSP-20241031-000027,SSSP-20241031-000028,SSSP-20241031-000029,SSSP-20241031-000031,SSSP-20241031-000032,SSSP-20241031-000035,SSSP-20241031-000036,SSSP-20241031-000038,SSSP-20241031-000039,SSSP-20241031-000040,SSSP-20241031-000041,SSSP-20241031-000042,SSSP-20241031-000043,SSSP-20241031-000044,SSSP-20241031-000045,SSSP-20250110-000002,SSSP-20250110-000003,SSSP-20250110-000004&batchNum=20251210&saveEsOrMpp=mpp'

curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000010&batchNum=20251210&saveEsOrMpp=mpp'
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000029&batchNum=20251210&saveEsOrMpp=mpp'


# 站点动环属性
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000029&batchNum=20251210&saveEsOrMpp=mpp'
# 空间_站点
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000010&batchNum=20251210&saveEsOrMpp=mpp'
# 空间_机房
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000018&batchNum=20251210&saveEsOrMpp=mpp'
# 机房动环属性
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000021&batchNum=20251210&saveEsOrMpp=mpp'
# 动环专业内输出分路
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000045&batchNum=20251210&saveEsOrMpp=mpp'
# 站点映射关系
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20250110-000002&batchNum=20251210&saveEsOrMpp=mpp'
# 园区映射关系
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20250110-000003&batchNum=20251210&saveEsOrMpp=mpp'
# 机房映射关系
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20250110-000004&batchNum=20251210&saveEsOrMpp=mpp'

# 缺少 空间_数据中心
# 缺少 机架利用率
	这两个存数据的


# 变压器
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000022&batchNum=20251210&saveEsOrMpp=mpp'
# 变换设备
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000023&batchNum=20251210&saveEsOrMpp=mpp'
# 高压配电
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000025&batchNum=20251210&saveEsOrMpp=mpp'
# 高压直流电源
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000027&batchNum=20251210&saveEsOrMpp=mpp'
# 高压直流配电
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000028&batchNum=20251210&saveEsOrMpp=mpp'
# 低压交流配电
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000031&batchNum=20251210&saveEsOrMpp=mpp'
# 发电机组
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000032&batchNum=20251210&saveEsOrMpp=mpp'
# 开关电源
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000035&batchNum=20251210&saveEsOrMpp=mpp'
# 低压直流配电
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000036&batchNum=20251210&saveEsOrMpp=mpp'
# UPS设备
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000038&batchNum=20251210&saveEsOrMpp=mpp'
# 蓄电池
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000039&batchNum=20251210&saveEsOrMpp=mpp'
# 空调
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000040&batchNum=20251210&saveEsOrMpp=mpp'
# 节能设备
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000041&batchNum=20251210&saveEsOrMpp=mpp'
# 动环监控
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000042&batchNum=20251210&saveEsOrMpp=mpp'
# 智能电表
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000043&batchNum=20251210&saveEsOrMpp=mpp'
# 其它设备
curl --location --request GET 'http://10.1.202.8:31640/migration/v1/zzSyncData/startSyncZZData?orderId=SSSP-20241031-000044&batchNum=20251210&saveEsOrMpp=mpp'




涉及ftp：
	10.1.4.113
	/tmp/zzdata 目录下
	vsftpd	wccQKPbCmx8@r*6p
	
	进入方式：
		ftp  ip
			输入密码
			用户名
	目前cicd上
		只有8和193这两个能连到ftp


涉及表：
	mpp：
		SELECT * FROM  dim_zz_data_sync_info;  - 映射关系（字段在mpp_column字段）






----------------------------------------------------------




集团综资->mpp
	table_name
	也是在里面
		数据是分区

	原始数据：
		113 ->
		
			89,还是8,还是118？
			119 -> 
		原来数据表
			trun掉数据 （跟zz_data_sync_info） - 里面的es表明一致 -- mpp数据库中

	（每一个批次都要对）
	数据量对不对
	数据字段对不对
		数据字段（均增加下面两个字段）
			flowtime
			starttime

		接口传入时间必须大于同步表里面的batch_num
			执行后，表的时间会自动更正为接口传入的批次号（必须是晚于表中的时间）
			否则不进行插入




telnet 10.1.4.114 8030
telnet 10.1.4.115 8030

telnet 10.1.5.109 8040 
telnet 10.1.5.111 8040
telnet 10.1.5.112 8040 
telnet 10.1.5.113 8040

	在cicd上部署external服务的机器上面（也就是node节点里面），看看上面的ip端口通不通
	如果不通就加白名单，telnet 10.1.5.112 8040 估计是这个不通，不知道为啥，这个机器，每天都会变的

	
	如果有不通的，就用这个命令，修改ip，添加白名单
	iptables -I INPUT -p tcp --dport 8040 -s 10.1.202.8 -j ACCEPT

	说明：即有连接不上的ip，就到对应ip服务上，直接执行上面的命令，ip换成exter当前部署后的node ip即可



external服务配置中
	gw.url: "http://10.12.7.87:31640/migration/v1/api"
		ip改为目前external部署的cicd下的node ip和port


		label为1时，表里如果有数据了，那就不会再导入了
		label为0时，表里有数据，也会重复导入

		单次批次在10000 或 以内即可
```

