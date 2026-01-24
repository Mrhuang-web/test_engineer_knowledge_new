## 一、消息队列性能问题排查详解（L18-30）

### 1. 监控消息堆积

#### 什么是消息堆积？
消息堆积是指消息队列中未被消费者处理的消息数量持续增加的情况。这通常意味着生产者发送消息的速度超过了消费者处理消息的速度。

#### 如何查看队列长度？

##### Kafka 示例：


# 查看指定主题的分区信息和消息数量
kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test-topic --time -1

# 输出示例：
test-topic:0:10000
# 含义：test-topic主题的0号分区有10000条消息
```

##### RabbitMQ 示例：
1. 登录 RabbitMQ 管理界面（默认 http://localhost:15672）
2. 点击 "Queues" 标签
3. 查看 "Ready" 列，显示的是待处理的消息数量

#### 如何监控消费速率和生产速率？

##### Kafka 示例：
1. 使用 Kafka Manager 或 Kafka Eagle 等可视化工具
2. 查看 "Produced Messages/Sec" 和 "Consumed Messages/Sec" 指标
3. 如果消费速率持续低于生产速率，说明存在消息堆积

##### RabbitMQ 示例：
1. 登录 RabbitMQ 管理界面
2. 点击 "Queues" 标签
3. 查看 "Incoming" 和 "Deliver/Get" 指标
4. "Incoming" 是生产速率，"Deliver/Get" 是消费速率

### 2. 分析延迟

#### 什么是消息延迟？
消息延迟是指消息从生产者发送到消费者接收并处理的总时间。

#### 如何使用消息队列自带的监控工具？



# 启用 Kafka 监控指标
# 在 server.properties 中添加
exporter.type=kafka_metrics
```

使用 Prometheus + Grafana 监控：
1. 安装并配置 Kafka Exporter
2. 配置 Prometheus 抓取 Kafka Exporter 指标
3. 在 Grafana 中导入 Kafka 监控面板，查看 "Message Latency" 指标

##### RabbitMQ 示例：
1. 登录 RabbitMQ 管理界面
2. 点击 "Queues" 标签
3. 查看 "Message rate" 图表，分析消息处理延迟
4. 或使用 RabbitMQ Delayed Message Plugin 专门监控延迟

#### 如何检查网络延迟和 broker 性能？

##### 检查网络延迟：
1. 使用 ping 命令测试 broker 节点之间的延迟
2. 检查防火墙设置，确保允许 broker 节点之间的通信

##### 检查 broker 性能：
1. 查看 broker 节点的 CPU、内存、磁盘 I/O 等资源使用情况
2. 检查 broker 节点的网络带宽，确保足够支持消息流量


# 使用 ping 命令检查网络延迟
ping kafka-broker-ip

# 使用 traceroute 命令检查网络路径
traceroute kafka-broker-ip

# 使用 iperf 命令测试网络带宽
iperf -c kafka-broker-ip -p 5201
```

##### 检查 broker 性能：
# 查看 broker CPU 使用率
top -p $(pgrep -f kafka)

# 查看 broker 内存使用率
free -h

# 查看 broker 磁盘 I/O
iostat -x 1
```

### 3. 检查配置

#### Kafka 分区数设置
- **分区数的作用**：Kafka 的分区数决定了最大并行处理能力，每个分区只能由一个消费者组中的一个消费者消费
- **如何确定合理的分区数**：
  - 分区数 ≥ 消费者组中的消费者数量
  - 分区数 = 预期峰值吞吐量 / 单分区吞吐量
  - 示例：预期峰值吞吐量为 100,000 条/秒，单分区吞吐量为 10,000 条/秒，则需要 10 个分区

##### 查看 Kafka 主题分区数：
```bash
# 查看指定主题的分区数
kafka-topics.sh --bootstrap-server localhost:9092 --topic test-topic --describe
```




# 查看 broker CPU 使用率
top -p $(pgrep -f kafka)

# 查看 broker 内存使用率
free -h

# 查看 broker 磁盘 I/O
iostat -x 1
```

### 3. 检查配置

#### Kafka 分区数设置
- **分区数的作用**：Kafka 的分区数决定了最大并行处理能力，每个分区只能由一个消费者组中的一个消费者消费
- **如何确定合理的分区数**：
  - 分区数 ≥ 消费者组中的消费者数量
  - 分区数 = 预期峰值吞吐量 / 单分区吞吐量
  - 示例：预期峰值吞吐量为 100,000 条/秒，单分区吞吐量为 10,000 条/秒，则需要 10 个分区

##### 查看 Kafka 主题分区数：
```bash
# 查看指定主题的分区数
kafka-topics.sh --bootstrap-server localhost:9092 --topic test-topic --describe
```


kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic test-topic
```

#### 消费者组数量设置
- **消费者组的作用**：每个消费者组独立消费主题的所有消息
- **合理设置消费者组数量**：
  - 根据业务需求，每个需要独立消费消息的业务设置一个消费者组
  - 避免过多消费者组导致资源浪费

##### 查看 Kafka 消费者组：

kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list


#### 批量发送/消费配置优化

##### Kafka 生产者批量配置：
```properties
# 在 producer.properties 中设置
batch.size=16384  # 批量大小，默认 16KB
linger.ms=5       # 等待时间，默认 0ms
# 含义：当消息大小达到 batch.size 或等待时间达到 linger.ms 时，才发送消息
```

##### Kafka 消费者批量配置：
```properties
# 在 consumer.properties 中设置
fetch.min.bytes=1  # 单次拉取的最小字节数，默认 1B
fetch.max.wait.ms=500  # 单次拉取的最大等待时间，默认 500ms
# 含义：当拉取到的消息达到 fetch.min.bytes 或等待时间达到 fetch.max.wait.ms 时，才返回消息
```

### 4. 查看日志

#### Kafka 日志位置
- **Broker 日志**：默认在 `kafka-logs` 目录下
- **生产者/消费者日志**：由应用程序配置决定，通常在应用日志目录下

#### 查看 Kafka Broker 日志：

tail -f kafka-logs/server.log | grep ERROR


# 默认日志位置
tail -f /var/log/rabbitmq/rabbit@hostname.log | grep ERROR
```

## 二、缓存系统性能问题排查详解（L44-63）

### 1. 监控命中率

#### 什么是缓存命中率？
缓存命中率是指缓存命中次数占总请求次数的比例。命中率越高，说明缓存的效果越好，能有效减少数据库压力。

#### 如何计算缓存命中率？
```
缓存命中率 = (缓存命中次数 / 总请求次数) × 100%
```

#### Redis 如何查看命中率？
```bash
# 连接 Redis
redis-cli

# 查看 Redis 统计信息
info stats

# 查找以下指标
keyspace_hits:10000  # 缓存命中次数
keyspace_misses:2000  # 缓存未命中次数

# 计算命中率
命中率 = (10000 / (10000 + 2000)) × 100% = 83.33%
```



#### 命中率过低的原因和解决方法：
| 原因 | 解决方法 |
|------|----------|
| 缓存键设计不合理 | 优化缓存键，使用更通用的键设计 |
| 缓存失效策略不当 | 调整 TTL（生存时间），使用更合理的失效策略 |
| 缓存容量不足 | 增加缓存容量或使用更高效的缓存淘汰策略 |
| 热点数据频繁变化 | 考虑使用本地缓存或调整缓存更新策略 |

### 2. 检查内存使用率

#### Redis 如何查看内存使用率？



# 连接 Redis
redis-cli

# 查看内存使用情况
info memory

# 关键指标
used_memory:1073741824  # 使用的内存，单位字节
used_memory_human:1.00G  # 人类可读格式
maxmemory:2147483648     # 最大内存限制
maxmemory_human:2.00G    # 人类可读格式

# 计算内存使用率
内存使用率 = (1073741824 / 2147483648) × 100% = 50%



#### 如何监控缓存淘汰策略和淘汰率？

# 查看 Redis 统计信息
info stats

# 查找以下指标
evicted_keys:1000  # 被淘汰的键数量

# 计算淘汰率
淘汰率 = evicted_keys / (keyspace_hits + keyspace_misses) × 100%
```



#### 常见的 Redis 淘汰策略：
| 策略 | 含义 |
|------|------|
| noeviction | 不淘汰任何键，内存不足时返回错误 |
| allkeys-lru | 淘汰最近最少使用的键 |
| allkeys-random | 随机淘汰键 |
| volatile-lru | 淘汰设置了过期时间的最近最少使用的键 |
| volatile-random | 随机淘汰设置了过期时间的键 |
| volatile-ttl | 淘汰设置了过期时间且剩余时间最短的键 |

### 3. 分析响应时间

#### 如何查看 Redis 慢查询日志？


# 连接 Redis
redis-cli

# 设置慢查询日志阈值（单位：微秒）
config set slowlog-log-slower-than 10000  # 记录超过 10ms 的查询

# 设置慢查询日志长度
config set slowlog-max-len 1000

# 查看慢查询日志
slowlog get

# 输出示例：
1) 1) (integer) 1  # 日志 ID
   2) (integer) 1620000000  # 时间戳
   3) (integer) 20000  # 执行时间（微秒）
   4) 1) "KEYS"  # 命令
      2) "*"


#### 缓存响应时间突然增加的原因：
1. **网络问题**：
   - 检查 Redis 服务器和应用服务器之间的网络延迟
   - 使用 ping 命令或网络监控工具

2. **缓存服务器负载过高**：
   - 检查 Redis 服务器的 CPU、内存、磁盘 I/O 使用率
   - 查看 Redis 连接数是否过多

### 4. 检查连接数

#### Redis 如何查看连接数？





# 连接 Redis
redis-cli

# 查看当前连接数
info clients

# 关键指标
connected_clients:100  # 当前连接数
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0
```

#### 如何监控连接创建和关闭频率？


# 查看 Redis 统计信息
info stats

# 查找以下指标
total_connections_received:10000  # 总连接数
rejected_connections:0  # 被拒绝的连接数

# 计算连接频率
连接频率 = (total_connections_received / 运行时间)  # 单位：连接/秒
```

#### 连接数过多的解决方法：
1. **使用连接池**：
   - 应用程序中使用 Redis 连接池，避免频繁创建和关闭连接
   - 调整连接池参数，如最大连接数、最小空闲连接数等

2. **优化应用程序**：
   - 检查应用程序是否存在连接泄漏
   - 确保每次使用完连接后正确关闭

3. **调整 Redis 配置**：
   ```bash
   # 在 redis.conf 中设置
   maxclients 10000  # 最大连接数，默认 10000



### 示例 1：解决 Kafka 消息堆积问题

1. **发现问题**：
   - 通过 Kafka Manager 发现 test-topic 主题的消息数量持续增加
   - 生产速率为 10,000 条/秒，消费速率为 5,000 条/秒

2. **分析问题**：
   - 查看主题分区数：只有 2 个分区
   - 查看消费者组：只有 2 个消费者
   - 单分区吞吐量约为 2,500 条/秒

3. **解决问题**：

  # 增加主题分区数到 4 个
   kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic test-topic --partitions 4
   ```
   - 增加消费者组中的消费者数量到 4 个
   - 调整生产者批量配置：batch.size=32768，linger.ms=10

4. **验证结果**：
   - 消费速率提升到 10,000 条/秒
   - 消息堆积逐渐减少，最终恢复正常

### 示例 2：解决 Redis 命中率低问题

1. **发现问题**：
   - 通过 Prometheus + Grafana 发现 Redis 命中率仅为 60%
   - 慢查询日志中大量 KEYS * 命令

2. **分析问题**：
   - 应用程序中使用了 KEYS * 命令遍历所有键
   - 缓存键设计不合理，没有使用前缀
   - 缓存 TTL 设置过短，只有 10 秒

3. **解决问题**：
   - 优化应用程序，避免使用 KEYS * 命令，改用 SCAN 命令
   - 统一缓存键前缀，如 "user:123"、"order:456"
   - 调整缓存 TTL 为 300 秒（5 分钟）

4. **验证结果**：
   - Redis 命中率提升到 90%
   - 慢查询日志中不再有 KEYS * 命令
   - 应用程序响应时间明显降低