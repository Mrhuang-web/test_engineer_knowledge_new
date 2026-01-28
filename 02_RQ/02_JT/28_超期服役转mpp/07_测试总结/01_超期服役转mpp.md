# 01总结



```
前置准备：
	
	集团动环数据库：
		进入zz_data_sync_info,将站点、机房、设备等table_name有值的,改其batch_num为想跑验证的批次
		已拉取现网precinct表和site表及device表(或脚本造数) -- 都有对应的批次号
		进入纵横：http://10.1.5.111:12345/wizdata/ui/projects/15930069689600/workflow/instances
		执行工作流-工作流定义-综资匹配-稽核-超期服役（补数-当前日期即可）,如果下线手工点击上线即可
	
	mpp数据源中：
		要根据batch_num来判断批次号，从而修改动环的同步表的batch_num
		只取最新stat_time的批次（无论是手工造数还是同步造数，都要确保跟最新stat_time一致，不然会导致其他数据都同步不到了）
```

