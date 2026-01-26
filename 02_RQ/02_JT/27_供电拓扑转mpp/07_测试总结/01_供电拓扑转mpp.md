# 01总结

```
涉及服务：scada-service,  mpp-service 

查看匹配的设备
特别说明：
	只有综资本身的任务，和之前一样，然后建立在mpp的综资数据上


1.页面可以手动刷新
2.每天自动触发 scada抽取任务
curl --location --request GET 'http://localhost:28020/v1/topuConfig/mappingResourceAll'
```

