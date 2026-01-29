#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
import signal
import sys
from kafka import KafkaConsumer
from kafka.errors import KafkaError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('kafka_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('kafka_monitor')

class KafkaMonitor:
    def __init__(self, bootstrap_servers, topic, group_id='kafka_monitor_group'):
        """
        初始化 Kafka 监听器
        :param bootstrap_servers: Kafka 服务器地址，格式为 'host:port'
        :param topic: 要监听的 topic 名称
        :param group_id: 消费者组 ID
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
        self.group_id = group_id
        self.consumer = None
        self.running = False
        
        # 注册信号处理
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """
        信号处理函数，用于优雅退出
        """
        logger.info('接收到退出信号，正在关闭消费者...')
        self.running = False
        if self.consumer:
            self.consumer.close()
        sys.exit(0)
    
    def create_consumer(self):
        """
        创建 Kafka 消费者
        """
        max_retries = 3
        retry_interval = 5  # 秒
        
        try:
            for attempt in range(max_retries):
                try:
                    logger.info(f'尝试连接 Kafka 服务器 (第 {attempt + 1}/{max_retries} 次): {self.bootstrap_servers}')
                    
                    # 尝试使用不同的连接配置
                    self.consumer = KafkaConsumer(
                        self.topic,
                        bootstrap_servers=[self.bootstrap_servers],
                        group_id=self.group_id,
                        auto_offset_reset='earliest',  # 从最早的消息开始消费
                        enable_auto_commit=True,       # 自动提交偏移量
                        auto_commit_interval_ms=1000,  # 自动提交间隔
                        value_deserializer=lambda m: json.loads(m.decode('utf-8')) if m else None,
                        key_deserializer=lambda m: m.decode('utf-8') if m else None,
                        request_timeout_ms=60000,      # 请求超时时间（必须大于会话超时）
                        session_timeout_ms=30000,      # 会话超时时间
                        heartbeat_interval_ms=10000,    # 心跳间隔
                        max_in_flight_requests_per_connection=1,  # 减少并发请求
                        retry_backoff_ms=1000,  # 重试间隔
                        metadata_max_age_ms=300000,  # 元数据更新间隔
                        api_version=(0, 10, 2),  # 显式指定 API 版本
                        connections_max_idle_ms=600000,  # 连接最大空闲时间
                        max_poll_records=500,  # 每次 poll 的最大记录数
                        max_poll_interval_ms=300000  # 最大 poll 间隔
                    )
                    
                    logger.info(f'成功连接到 Kafka 服务器: {self.bootstrap_servers}')
                    logger.info(f'成功订阅 topic: {self.topic}')
                    logger.info(f'消费者组: {self.group_id}')
                    
                    # 获取分区信息（添加异常处理）
                    try:
                        partitions = self.consumer.partitions_for_topic(self.topic)
                        if partitions:
                            logger.info(f'分区信息: {partitions}')
                            logger.info(f'分区数量: {len(partitions)}')
                        else:
                            logger.warning(f'未找到 topic {self.topic} 的分区信息')
                    except Exception as e:
                        logger.error(f'获取分区信息时发生错误: {e}')
                        logger.warning('继续运行，但可能无法获取分区信息')
                    
                    logger.info('消费者创建成功，准备开始监听消息...')
                    return True
                    
                except KafkaError as e:
                    logger.error(f'第 {attempt + 1} 次连接失败: {e}')
                    
                    if attempt < max_retries - 1:
                        logger.info(f'等待 {retry_interval} 秒后重试...')
                        import time
                        time.sleep(retry_interval)
                    else:
                        logger.error(f'创建 Kafka 消费者失败: {e}')
                        logger.error(f'请检查以下几点:')
                        logger.error(f'1. Kafka 服务器是否运行在 {self.bootstrap_servers}')
                        logger.error(f'2. 网络连接是否正常')
                        logger.error(f'3. Topic 是否存在')
                        logger.error(f'4. 防火墙是否允许连接')
                        logger.error(f'5. Kafka 服务是否正常运行')
                        return False
            return False
        except Exception as e:
            logger.error(f'create_consumer 方法中发生未捕获的异常: {e}')
            import traceback
            logger.error(f'错误堆栈: {traceback.format_exc()}')
            return False
    
    def start_monitoring(self):
        """
        开始监听 Kafka 消息
        """
        logger.info('进入 start_monitoring 方法')
        self.running = True
        
        logger.info(f'当前 consumer 状态: {self.consumer}')
        
        if not self.consumer:
            logger.info('消费者不存在，尝试创建...')
            success = self.create_consumer()
            logger.info(f'创建消费者结果: {success}')
            if not success:
                logger.error('无法创建 Kafka 消费者，退出程序')
                return
        
        logger.info('开始监听 Kafka 消息...')
        logger.info('正在等待接收消息...')
        logger.info('按 Ctrl+C 退出监听')
        
        try:
            # 持续监听消息
            while self.running:
                try:
                    logger.info('准备调用 poll 方法获取消息...')
                    # 使用 poll 方法获取消息，设置较长的超时时间
                    messages = self.consumer.poll(timeout_ms=60000)
                    logger.info(f'poll 方法返回结果: {messages}')
                    
                    if messages:
                        for tp, msgs in messages.items():
                            logger.info(f'从分区 {tp} 收到 {len(msgs)} 条消息')
                            for message in msgs:
                                self.process_message(message)
                    else:
                        # 定期打印日志，确保脚本仍在运行
                        logger.info('未收到消息，继续监听...')
                        # 等待一段时间后再次尝试
                        import time
                        time.sleep(10)
                        
                except KafkaError as e:
                    logger.error(f'消费消息时发生错误: {e}')
                    logger.info('尝试重新连接...')
                    # 重新创建消费者
                    try:
                        if self.consumer:
                            self.consumer.close()
                    except Exception as close_error:
                        logger.error(f'关闭消费者时发生错误: {close_error}')
                    
                    self.consumer = None
                    success = self.create_consumer()
                    if not success:
                        logger.error('重新连接失败，退出程序')
                        return
                    logger.info('重新连接成功，继续监听...')
                    
        except KeyboardInterrupt:
            logger.info('接收到退出信号，正在关闭消费者...')
        except Exception as e:
            logger.error(f'发生未知错误: {e}')
            import traceback
            logger.error(f'错误堆栈: {traceback.format_exc()}')
        finally:
            logger.info('进入 finally 块，准备关闭消费者...')
            if self.consumer:
                try:
                    self.consumer.close()
                    logger.info('消费者已关闭')
                except Exception as close_error:
                    logger.error(f'关闭消费者时发生错误: {close_error}')
            logger.info('监听程序已退出')
    
    def process_message(self, message):
        """
        处理接收到的消息
        :param message: Kafka 消息对象
        """
        try:
            logger.info(f'接收到消息:')
            logger.info(f'  Topic: {message.topic}')
            logger.info(f'  Partition: {message.partition}')
            logger.info(f'  Offset: {message.offset}')
            logger.info(f'  Key: {message.key}')
            logger.info(f'  Value: {json.dumps(message.value, ensure_ascii=False, indent=2)}')
            logger.info('-' * 80)
        except Exception as e:
            logger.error(f'处理消息时发生错误: {e}')

def main():
    """
    主函数
    """
    # 配置参数
    bootstrap_servers = '10.1.203.120:9095'
    
    # 提示用户输入要监听的 topic
    # topic = input('请输入要监听的 topic 名称（例如：test_topic）: ')
    topic = 'entrance_raw_data'
    if not topic:
        logger.error('Topic 名称不能为空')
        return
    
    # 创建并启动监听器
    monitor = KafkaMonitor(bootstrap_servers, topic)
    monitor.start_monitoring()

if __name__ == '__main__':
    main()
