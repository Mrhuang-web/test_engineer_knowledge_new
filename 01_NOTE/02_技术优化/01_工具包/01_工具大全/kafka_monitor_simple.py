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
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('kafka_monitor_simple')

class KafkaMonitor:
    def __init__(self, bootstrap_servers, topic):
        """
        初始化 Kafka 监听器
        :param bootstrap_servers: Kafka 服务器地址，格式为 'host:port'
        :param topic: 要监听的 topic 名称
        """
        self.bootstrap_servers = bootstrap_servers
        self.topic = topic
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
    
    def start(self):
        """
        开始监听 Kafka 消息
        """
        self.running = True
        
        try:
            # 创建最简单的消费者
            logger.info(f'尝试连接到 Kafka 服务器: {self.bootstrap_servers}')
            logger.info(f'尝试订阅 topic: {self.topic}')
            
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=[self.bootstrap_servers],
                auto_offset_reset='earliest'
            )
            
            logger.info('成功创建 Kafka 消费者')
            logger.info('开始监听消息...')
            logger.info('按 Ctrl+C 退出')
            
            # 持续监听消息
            for message in self.consumer:
                if not self.running:
                    break
                
                logger.info(f'接收到消息:')
                logger.info(f'  Topic: {message.topic}')
                logger.info(f'  Partition: {message.partition}')
                logger.info(f'  Offset: {message.offset}')
                logger.info(f'  Key: {message.key}')
                logger.info(f'  Value: {message.value}')
                logger.info('-' * 80)
                
        except KafkaError as e:
            logger.error(f'Kafka 错误: {e}')
        except Exception as e:
            logger.error(f'未知错误: {e}')
            import traceback
            logger.error(f'错误堆栈: {traceback.format_exc()}')
        finally:
            if self.consumer:
                self.consumer.close()
                logger.info('消费者已关闭')
            logger.info('程序已退出')

if __name__ == '__main__':
    # 配置参数
    bootstrap_servers = '10.1.203.120:9095'
    topic = 'entrance_raw_data'
    
    # 创建并启动监听器
    monitor = KafkaMonitor(bootstrap_servers, topic)
    monitor.start()
