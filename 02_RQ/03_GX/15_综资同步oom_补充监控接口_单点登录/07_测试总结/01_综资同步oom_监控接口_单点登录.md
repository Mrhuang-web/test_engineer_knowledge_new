# 01总结

## 综资数据同步oom

```
涉及服务：external

涉及配置：external中
	csvSplitChar: ^
		ftpIp: 10.1.4.113
		ftpPort: 21
		ftpUser: vsftpd
		ftpPwd: wccQKPbCmx8@r*6p
		ftpBasePath: /tmp/zongzi
		threadNum: 1
		backDataDay: 7
		ftpFileName: 
			RM_SITE_PROPERTY_yyyymmdd.csv,
			RM_ROOM_PROPERTY_yyyymmdd.csv,
			RM_AREA_SITE_yyyymmdd.csv,
			RM_AREA_RESPOINT_yyyymmdd.csv,
			RM_AREA_ROOM_yyyymmdd.csv,
			RM_AREA_RACKPOS_yyyymmdd.csv,
			PHYSICAL_STATION_yyyymmdd.csv
			CE_DEVICE_PE_TRANSFORM_yyyymmdd.csv,
			CE_DECIVE_PE_TRANSFORM_DEVICE_yyyymmdd.csv,
			CE_NET_PE_HIGH_DISTRIBUTION_yyyymmdd.csv,
			CE_DEVICE_PE_HIGH_DISTRIBUTION_yyyymmdd.csv,
			CE_NET_PE_HIGH_POWER_yyyymmdd.csv,
			CE_DEVICE_PE_HIGH_POWER_yyyymmdd.csv,
			CE_DEVICE_PE_HIGH_DC_DISTRIBUTION_yyyymmdd.csv,
			CE_NET_PE_LOW_DISTRIBUTION_yyyymmdd.csv,
			CE_DEVICE_PE_LOW_AC_DISTRIBUTION_yyyymmdd.csv,
			CE_DEVICE_PE_UPS_AC_DISTRIBUTION_yyyymmdd.csv,
			CE_NET_PE_SWITCH_POWER_yyyymmdd.csv,
			CE_DEVICE_PE_POWER_GENERATION_yyyymmdd.csv,
			CE_NET_PE_OPEN_POWER_yyyymmdd.csv,
			CE_DEVICE_PE_SWITCH_POWER_yyyymmdd.csv,
			CE_DEVICE_PE_LOW_DC_DISTRIBUTION_yyyymmdd.csv,
			CE_NET_PE_UPS_yyyymmdd.csv,
			CE_DEVICE_PE_UPS_yyyymmdd.csv,
			CE_DEVICE_PE_BATTERY_LA_yyyymmdd.csv,
			CE_DEVICE_PE_BATTERY_LI_yyyymmdd.csv,
			CE_DEVICE_PE_CACH_yyyymmdd.csv,
			CE_DEVICE_PE_CACH_END_yyyymmdd.csv,
			CE_DEVICE_PE_HIROSS_yyyymmdd.csv,
			CE_DEVICE_PE_NA_yyyymmdd.csv,
			CE_DEVICE_PE_BB_yyyymmdd.csv,
			CE_DEVICE_PE_HES_yyyymmdd.csv,
			CE_DEVICE_PE_WPC_yyyymmdd.csv,
			CE_DEVICE_PE_MONITOR_yyyymmdd.csv,
			CE_DEVICE_PE_ROOM_ENVIRONMENT_yyyymmdd.csv,
			CE_DEVICE_PE_IAC_yyyymmdd.csv,
			CE_DEVICE_PE_SMART_METER_yyyymmdd.csv,
			CE_LINK_PE_IN_yyyymmdd.csv,
			CE_LINK_PE_OUT_yyyymmdd.csv,
			CE_DEVICE_PE_OTHER_yyyymmdd.csv,
			CE_DEVICE_PE_ESS_yyyymmdd.csv,
			CE_NET_PE_CACH_yyyymmdd.csv,
			
		ftpWay: ftp
		deviceTypeId: 101,102,1,2,3,4,5,6,8,14,15,19,76,87,92,103,106,201,202,203,205,206,207,208,209

涉及表：
	综资映射表：t_sync_field_config
	其中device_type_id，用于区分为哪一种类型（站点、机房、还是设备等类别）
```



```
逻辑：
	综资映射表：t_sync_field_config
	
	1、csv->es(原始数据存放在/tmp/zongzi/yyyymmdd/目录下,然后读取时会保存到服务本地临时文件夹中用于写入es，写入完后就删除)
		调用接口：
		dataDate：为zongzi目录下，文件目录的时间批次命名
		fileName：为具体的综资csv文件
		isDelldName：为true()，为false()
		curl --location --request GET 'http://10.12.5.125:31272/v1/schedule/shareCenterDataSync?dataDate=20260121&fileName=CE_DEVICE_PE_BATTERY_LI_20260121.csv&isDelIdxName=true'
		
	2、es—>mysql
		调用接口：
			dataDate：批次号日期
			deviceid：类别（即站点、机房、设备等 - sync表中有对应关系  -- 可以一次传入多个）
			curl --location --request GET 'http://10.12.5.125:31272/v1/schedule/shareCenterEsDataSync?dataDate=20250910&deviceId=0%2C101%2C102%2C103%2C1%2C2%2C3%2C4%2C5%2C6%2C7%2C8%2C9%2C11%2C12%2C13%2C14%2C15%2C16%2C17%2C18%2C68%2C76%2C77%2C78%2C87%2C88%2C92%2C93%2C201%2C202%2C203'\'' \   --header '\''Cookie: JSESSIONID=2DD70EF295EF79B61E5CD5CC12FE8DD3'\'''
            | device\_type\_id | device\_type | 开发串对应 deviceId（URL 片段） | es\_index\_name                              |
            | ---------------- | ------------ | ---------------------- | -------------------------------------------- |
            | 0                | 站点动环属性       | 0%2C                   | ods\_ftp\_site\_property                     |
            | 1                | 高压配电         | 1%2C                   | ods\_ftp\_device\_pe\_high\_distribution     |
            | 2                | 低压交流配电       | 2%2C                   | ods\_ftp\_device\_pe\_low\_ac\_distribution  |
            | 3                | 变压器          | 3%2C                   | ods\_ftp\_device\_pe\_transform              |
            | 4                | 低压直流配电       | 4%2C                   | ods\_ftp\_device\_pe\_low\_dc\_distribution  |
            | 5                | 发电机组         | 5%2C                   | ods\_ftp\_device\_pe\_power\_generation      |
            | 6                | 开关电源         | 6%2C                   | ods\_ftp\_device\_pe\_switch\_power          |
            | 7                | 铅酸电池         | 7%2C                   | ods\_ftp\_device\_pe\_battery\_la            |
            | 8                | UPS设备        | 8%2C                   | ods\_ftp\_device\_pe\_ups                    |
            | 9                | UPS配电        | 9%2C                   | ods\_ftp\_device\_pe\_ups\_ac\_distribution  |
            | 11               | 机房专用空调       | 11%2C                  | ods\_ftp\_device\_pe\_hiross                 |
            | 12               | 中央空调末端       | 12%2C                  | ods\_ftp\_device\_pe\_cach\_end              |
            | 13               | 中央空调主机       | 13%2C                  | ods\_ftp\_device\_pe\_cach                   |
            | 14               | 变换设备         | 14%2C                  | ods\_ftp\_device\_pe\_transform\_device      |
            | 15               | 普通空调         | 15%2C                  | ods\_ftp\_device\_pe\_na                     |
            | 16               | 极早期烟感        | 16%2C                  | ods\_ftp\_device\_pe\_ess                    |
            | 17               | 机房环境         | 17%2C                  | ods\_ftp\_device\_pe\_room\_environment      |
            | 18               | 电池恒温箱        | 18%2C                  | ods\_ftp\_device\_pe\_bb                     |
            | 68               | 锂电池          | 68%2C                  | ods\_ftp\_device\_pe\_battery\_li            |
            | 76               | 动环监控         | 76%2C                  | ods\_ftp\_device\_pe\_monitor                |
            | 77               | 智能通风换热       | 77%2C                  | ods\_ftp\_device\_pe\_hes                    |
            | 78               | 风光设备         | 78%2C                  | ods\_ftp\_device\_pe\_wpc                    |
            | 87               | 高压直流电源       | 87%2C                  | ods\_ftp\_device\_pe\_high\_power            |
            | 88               | 高压直流配电       | 88%2C                  | ods\_ftp\_device\_pe\_high\_dc\_distribution |
            | 92               | 智能电表         | 92%2C                  | ods\_ftp\_device\_pe\_smart\_meter           |
            | 93               | 智能门禁         | 93%2C                  | ods\_ftp\_device\_pe\_iac                    |
            | 101              | 站点           | 101%2C                 | ods\_ftp\_area\_site                         |
            | 102              | 机房           | 102%2C                 | ods\_ftp\_area\_room                         |
            | 103              | 资源点          | 103%2C                 | ods\_ftp\_area\_respoint                     |
            | 201              | UPS系统        | 201%2C                 | ods\_ftp\_net\_pe\_ups                       |
            | 202              | 开关电源系统       | 202%2C                 | ods\_ftp\_net\_pe\_open\_power               |
            | 203              | 动环专业内输出分路    | 203                    | ods\_ftp\_link\_pe\_in                       |
            | 204              | 高压配电系统       | —                      | ods\_ftp\_net\_pe\_high\_distribution        |
            | 205              | 高压直流电源系统     | —                      | ods\_ftp\_net\_pe\_high\_power               |
            | 206              | 低压配电系统       | —                      | ods\_ftp\_net\_pe\_low\_distribution         |
            | 207              | 发电系统         | —                      | ods\_ftp\_net\_pe\_switch\_power             |
            | 208              | 节能设备         | —                      | ods_ftp_device_pe_energy_save    |


	3、全链路执行（默认跑昨天的全链路）
			curl --location --request GET 'http://10.12.5.125:31272/v1/schedule/shareCenterDataSync/all'
```



```
补充点：
	是否启用非标准文件处理
		enableNotStandardFile: true
	
	这个蓄电池分铅酸电池和锂电池，这里配置全部写入到锂电池
        CE_DEVICE_PE_AIR: VE_PET_AIRCONDITION_13
        CE_DEVICE_PE_ENERY_SAVE: VE_PET_ENERGYSAVINGDEVICE_6
        CE_DEVICE_PE_POWER_MONITOR: VE_PET_MONITORINGDEVICE_13
        CE_DEVICE_PE_SMART_METER: VE_PET_AMMETER_9
        CE_LINK_PE_IN: VE_PET_POWERLINEIN_7
        CE_LINK_PE_OUT: VE_PET_POWERLINEOUT_7

	触发写入es,如果提示java.io.FileNotFoundException: /tmp/shareCenterData/VE_PET_AMMETER_9_20250717.CSV 
		(No such file or directory)cicd需要进入容器内部。进入/tmp/目录下 mkdir shareCenterData后再执行 ftp写入es
		
	映射表（综资各设备文件映射关系）：es映射、mysql映射
		t_sync_field_config
		t_zz_field_mapping

        记得看下产品给的最新的标准映射表.xlsx,如果发现es上面的字段少了或者es上面对应字段值不对，
        直接检查上面es对应索引表的字段之间映射关系是否准确。

	这个直接触两个操作（读取FTP文件写入ES索引，持久化到mysql,所以直接执行这个就可以）
		curl —location —request GET ‘http://10.188.99.5:21530/v1/schedule/shareCenterDataSync/all‘ &
		以上同步只会读取上一天的文件夹日期综资数据/home/vsftpd/tmp/zongzi/ 下的，有则执行，没有跳过直接结束同步。
        修改日期：复制旧一天全量数据的那个的文件夹，改成上一天的日期。
        执行我以下这个脚步，记得改下对应文件目录的日期，脚本路径在：重新写一个即可
        
        # 使用mv命令的替代方案（如：把20250807/文件夹下的包含 "*20250806*"格式的.csv文件名的日期，遍历全部改成new_base的目标日期20250807）
        src_dir="/home/vsftpd/tmp/zongzi/20260121"
        dst_dir="/home/vsftpd/tmp/zongzi/20260124"
        old_date=20260121
        new_date=20260124

        mkdir -p "$dst_dir"

        # 1. 复制 + 文件名替换
        find "$src_dir" -type f -name "*${old_date}*" -print0 |
          while IFS= read -r -d '' file; do
              new_name=$(basename "${file//${old_date}/${new_date}}")
              cp -- "$file" "$dst_dir/$new_name"
          done

        # 2. 改文件内容
        find "$dst_dir" -type f -exec sed -i "s/${old_date}/${new_date}/g" {} +

        # 3. 刷时间戳为“现在”
        find "$dst_dir" -type f -exec touch {} +
```



```
测试方式：
	先在/tmp/zongzi，建立对应批次日期文件夹，存入综资原始数据
	触发接口，检查csv数据是否入库到es，是否存在乱码，是否存在数据缺失，数据行缺失，字段缺失（目标处理服务器是否能够自动建立目录并处理数据入es后删除）
		同批次数据重复执行是否会重复写入
	接着触发入库mysql接口，检查es中的数据与mysql中，是否存在乱码，是否存在数据缺失，数据行缺失，字段缺失，同批次数据重复执行是否会重复写入
	
	目前已经生成了一个比较统计函数，获取字段归档的脚本
		使用方法-把脚本放置到数据目录的统计，执行即可
		会生成一个比较文件，即可比较数量和字段是否满足
	后续优化：
		可以直接执行流程，然后判断es的数据和mysql的数据，是否与脚本中输出的文件行数一致
        然后比较首行数据是否字段一致，数据是否匹配
```



```
待确认：
	服务中临时读取文件夹，是脚本触发后会自己创建的吗，还是手动先创建好的？
	目前写入es后，数据乱码，存在数据丢失
	同步mysql中也是
```



```
问题：
	1、目前导入后，自建值出现乱码
	2、触发接口后，服务就重启了（全链路，或是站点动环属性表）
```



## external服务补充监控接口

```
涉及服务：external
	触发接口：curl --location --request GET 'http://localhost:21530/v1/monitorapi/curlApi'
	回显success即可
```



# 单点登录

```
需要现网验证
```

