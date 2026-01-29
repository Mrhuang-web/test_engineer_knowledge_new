#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from kafka import KafkaAdminClient
from kafka.errors import KafkaError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('kafka_test')

def test_kafka_connection():
    """
    测试 Kafka 连接和服务状态
    """
    bootstrap_servers = '10.1.203.120:9095'
    
    try:
        # 尝试创建 admin 客户端来测试连接
        admin_client = KafkaAdminClient(
            bootstrap_servers=[bootstrap_servers],
            client_id='kafka_test',
            request_timeout_ms=30000
        )
        
        logger.info(f'成功连接到 Kafka 服务器: {bootstrap_servers}')
        
        # 获取所有可用的 topic
        topics = admin_client.list_topics()
        logger.info(f'可用的 topic 列表: {topics}')
        
        # 关闭 admin 客户端
        admin_client.close()
        logger.info('测试完成，连接正常')
        return True
        
    except KafkaError as e:
        logger.error(f'Kafka 连接测试失败: {e}')
        logger.error('请检查以下几点:')
        logger.error(f'1. Kafka 服务是否运行在 {bootstrap_servers}')
        logger.error('2. 网络连接是否正常')
        logger.error('3. 防火墙是否允许连接')
        logger.error('4. 端口号是否正确')
        return False

if __name__ == '__main__':
    test_kafka_connection()
