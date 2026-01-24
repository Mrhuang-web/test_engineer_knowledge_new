# 01_kafka - offset explorer工具

前提：kafka的ip/域名加入到hosts文件中，hosts文件路径：C:\Windows\System32\drivers\etc

## 01_01_连接集群集群

```
启动`Offset Explorer`后，首先需要配置连接到您的Kafka集群：
	1. 打开`File`菜单，选择`New Connection...`或直接点击界面中的`+`按钮。
	2. 在弹出的对话框中输入Kafka集群的相关信息，包括：
        - **Name**: 给这个连接起一个易于识别的名字。
        - **Bootstrap Servers**: Kafka集群的地址，格式如 `host1:port1,host2:port2`。
        - **Security Settings**: 如有安全设置（如SASL认证），在此处配置。

点击`Test Connection`测试是否成功连接，无误后点击`Save`保存连接配置。

注意：可以同时输入多个ip:port，用;隔开即可
```

![image-20250818171313659](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818171313659.png)

![image-20250818172757019](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818172757019.png)

## 01_02_查看主题

```
成功连接后，Kafka的所有主题将会显示在左侧导航栏：
• 点击任一主题，右侧会列出该主题的所有分区及每个分区的offset信息。
• 可以通过搜索框快速查找特定主题。

brokers --节点信息   【即每个连接的ip和port信息】
topics -- 主题
consumers -- 消费者
```

![image-20250818171445823](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818171445823.png)

## 01_03_查看主题数据

```
要查看某个主题的消息内容：
1. 在左侧选择想要查看的主题。
```

![image-20250818171720748](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818171720748.png)

![image-20250818171730523](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818171730523.png)

## 01_04_查看主题数据过滤

```
数据量大，且需要查询比较久的数据

	kafka数据有时效性，一般设置3~7天
	
使用tools
	find messages
		选择对应topic
			通过key进行筛选
```

![image-20250818172013133](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818172013133.png)

![image-20250818172022770](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818172022770.png)

![image-20250818172030181](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818172030181.png)

![image-20250818172059547](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818172059547.png)

## 01_05_主题新增

```

```

![image-20250818172215777](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818172215777.png)

## 01_06_主题数据新增

```
目前，Offset Explorer主要用于查看和管理offset，直接在界面中添加消息的功能并不直接提供【mock数据】
	
	但可以使用Kafka的命令行工具kafka-console-producer.sh或
	集成的生产者工具（如许多开发环境中的生产者示例）来发送消息至指定主题。
	
注意：topic的数据mock，另一个topic或是其他topic是可能会接收到的
```

![image-20250818172354170](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818172354170.png)

![image-20250818172402227](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\image-20250818172402227.png)