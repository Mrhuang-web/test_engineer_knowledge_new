# URL配置文件
# 定义所有接口的URL和对应的处理函数映射

url_mapping = {
    # 设备管理类接口
    '/setPassWord': {'method': 'POST', 'handler': 'device.set_password'},
    '/device/information': {'method': 'GET', 'handler': 'device.get_device_info'},
    '/setTime': {'method': 'POST', 'handler': 'device.set_time'},
    '/device/setLanguage': {'method': 'POST', 'handler': 'device.set_language'},
    '/device/setTimeZone': {'method': 'POST', 'handler': 'device.set_timezone'},
    '/restartDevice': {'method': 'POST', 'handler': 'device.restart_device'},
    '/setIdentifyCallBack': {'method': 'POST', 'handler': 'device.set_identify_callback'},
    '/setImgRegCallBack': {'method': 'POST', 'handler': 'device.set_img_reg_callback'},
    '/device/openDoorControl': {'method': 'POST', 'handler': 'device.open_door_control'},
    '/device/setSignalInput': {'method': 'POST', 'handler': 'device.set_signal_input'},
    '/meetAndWarnSet': {'method': 'POST', 'handler': 'device.set_meet_warn'},
    '/cardInfoSet': {'method': 'POST', 'handler': 'device.set_card_info'},
    '/device/eventCallBack': {'method': 'POST', 'handler': 'device.set_event_callback'},
    '/getDoorSensor': {'method': 'GET', 'handler': 'device.get_door_sensor'},
    
    # 人员管理类接口
    '/person/create': {'method': 'POST', 'handler': 'person.create_person'},
    '/person/delete': {'method': 'POST', 'handler': 'person.delete_person'},
    '/person/update': {'method': 'POST', 'handler': 'person.update_person'},
    '/person/find': {'method': 'GET', 'handler': 'person.find_person'},
    '/person/findByPage': {'method': 'GET', 'handler': 'person.find_person_by_page'},
    
    # 照片管理类接口
    '/face/create': {'method': 'POST', 'handler': 'face.create_face'},
    '/face/delete': {'method': 'POST', 'handler': 'face.delete_face'},
    '/face/update': {'method': 'POST', 'handler': 'face.update_face'},
    '/face/find': {'method': 'POST', 'handler': 'face.find_face'},
    '/face/takeImg': {'method': 'POST', 'handler': 'face.take_img'},
    '/face/deletePerson': {'method': 'POST', 'handler': 'face.delete_person_faces'},
    
    # 识别记录接口
    '/newFindRecords': {'method': 'GET', 'handler': 'record.find_records'},
    '/newDeleteRecords': {'method': 'POST', 'handler': 'record.delete_records'}
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