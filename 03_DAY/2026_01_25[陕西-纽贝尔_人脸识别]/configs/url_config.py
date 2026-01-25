# URL配置文件
# 定义所有接口的URL和对应的处理函数映射

url_mapping = {
    # 动环发给运维管理的接口
    '/v1/external/ywgl/pushAccessControlInfo': {'method': 'POST', 'handler': 'external.push_access_control_info'},
    '/v1/external/ywgl/syncFaceOperationResult': {'method': 'POST', 'handler': 'external.sync_face_operation_result'}
}

# 服务器配置
server_config = {
    'host': '0.0.0.0',
    'port': 8090,
    'debug': True
}

# 热启动配置
hot_restart_config = {
    # 是否启用热启动
    'enabled': True,
    # 检测间隔，单位：秒
    'check_interval': 2,
    # 监控的目录列表，相对于项目根目录
    'monitored_dirs': ['business_logic', 'datastore', 'dictionaries', 'configs'],
    # 监控的文件扩展名
    'monitored_extensions': ['.py'],
    # 重启延迟，单位：秒，确保文件完全写入
    'restart_delay': 0.5
}