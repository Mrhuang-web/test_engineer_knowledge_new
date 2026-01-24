# 01_mpp描述

## 概念

```
数据库 MPP（Massively Parallel Processing）

作用：
	一张表水平切分（Shard）到多台机器，SQL 查询被优化器拆成很多“子计划”，
	各节点并行计算 → 汇总结果，PB 级也能秒级返回

简单操作：
	 装集群（至少 3 节点：1 gcluster + 2 data node）
	 
	 建库建表时指定 DISTRIBUTED BY
	 CREATE DATABASE db1;
     USE db1;
     CREATE TABLE t_order(
       id bigint,
       amt decimal(12,2),
       shop_id int,
       primary key(id)
     )  DISTRIBUTED BY('shop_id');   -- 按店铺分片
     
     跑 SQL，优化器自动选 MPP 执行计划
     SELECT shop_id, SUM(amt) FROM t_order
		WHERE dt BETWEEN '2025-10-01' AND '2025-10-27'
		GROUP BY shop_id;
	
	 并行度 / 代价策略可手动干预：
	 SET gcluster_mpp_max_threads = 32;
	 SET gcluster_mpp_broadcast_threshold = 1048576;


说明
    表本身已经“分片”（也叫分布、shard）。
    建表时没写 DISTRIBUTED BY (col) / DISTRIBUTED REPLICATED 之类，整张表就默认落在一个节点，后续所有 SQL 都不会并行。
    语句里用到的对象都是分片表，或者优化器能把维表广播。
    如果你 JOIN 了一张本地单节点临时表，优化器往往把整个计划拉到单节点跑，避免反复网络 shuffle。
    当前 SQL 类型支持并行。
    绝大部分 SELECT/INSERT/UPDATE/DELETE/CREATE TABLE AS SELECT 都能并行，但像
```



## 区分

MySQL = 高并发短事务、强一致、单节点计算

MPP = 把表拆开、多台机器一起算，专杀“大表扫描+复杂 JOIN”，但牺牲事务与部分语法

简单 CRUD、订单/支付核心——继续 MySQL

报表、日志、数据仓库——上 MPP，但重新设计表结构和分片键，别指望“零改代码”

| 维度        | MySQL（单机或传统主从）                       | MPP 数据库（GBase 8a/TiDB-OLAP/StarRocks …）                 |
| ----------- | --------------------------------------------- | ------------------------------------------------------------ |
| 1. 数据切分 | 没有，整张表在一个实例                        | 建表时必须指定 DISTRIBUTED BY 分片键，数据被水平拆到多台节点 |
| 2. 执行模型 | 单线程（或 InnoDB 的线程）处理整张表          | 优化器把 SQL 拆成若干“分片计划”，各节点并行算 → 汇总         |
| 3. 事务隔离 | 完整 ACID、MVCC、行锁，支持高并发短事务       | 多数 MPP 为了 OLAP 牺牲部分隔离级别，只保证“最终一致”或快照读；高并发小事务反而慢 |
| 4. 语法兼容 | 90% 的 DQL/DML 相同                           | ① 支持窗口函数、ROLLUP、WITH 递归（MySQL 8 才有）<br>② 没有 `FOR UPDATE`、不支持外键、触发器、存储过程语法差异大 |
| 5. 性能拐点 | 单表 2~5 千万行、复杂 JOIN 3 张以上就明显下降 | PB 级、事实表 100 亿行 + 星型模型 20 张维表，秒级返回        |
| 6. 运维操作 | 一条 `mysqldump` 就能导出整库                 | 必须按“分片”并行导出/导入，单表 `ALTER` 会锁全集群，需要滚动重建 |





## 基础语法

```
分片键只能选一次，后期改=重建表

常见 DDL
    ALTER TABLE t_order ADD COLUMN pay_type tinyint
      AFTER amt;
    ALTER TABLE t_order SHRINK SPACE FULL;   -- 回收删除空洞
    
注释三种写法：#、--、/* */ 
```



## 验证

```
-- 1. 看表分片方式
SHOW CREATE TABLE t_order\G

-- 2. 看执行计划（GBase 8a 语法）
EXPLAIN SELECT …  -- 若计划里出现 “Data Redistribution”、“Gather” 字样，说明走了 MPP；  
                  -- 只有 “Single Node” 就是单节点。
```

