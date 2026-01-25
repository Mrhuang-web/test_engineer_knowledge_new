# 设备管理类接口业务逻辑
from datastore.data_store import data_store
from dictionaries.code_dict import code_mapping

class DeviceService:
    def __init__(self):
        self.data_store = data_store
    
    def set_password(self, params):
        """设置设备密码"""
        old_pass = params.get('oldPass')
        new_pass = params.get('newPass')
        
        # 验证参数
        if not old_pass or not new_pass:
            return self._get_response('LAN_EXP-2001')
        
        # 检查密码是否为空或空格
        if not old_pass.strip() or not new_pass.strip():
            return self._get_response('LAN_EXP-2003')
        
        current_pass = self.data_store.get_password()
        
        if current_pass is None:
            # 初次设置密码，需要oldPass和newPass相同
            if old_pass != new_pass:
                return self._get_response('LAN_EXP-2006')
            self.data_store.set_password(new_pass)
            return self._get_response('LAN_SUS-0', msg='密码设置成功', data=f'password is : {new_pass}')
        else:
            # 修改密码，需要验证旧密码
            if old_pass != current_pass:
                return self._get_response('LAN_EXP-2005')
            self.data_store.set_password(new_pass)
            return self._get_response('LAN_SUS-0', msg='密码修改成功', data=f'password is : {new_pass}')
    
    def get_device_info(self, params):
        """获取设备信息"""
        passwd = params.get('pass')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 获取当前时间（毫秒级）
        import time
        current_time = int(time.time() * 1000)
        
        # 返回设备信息，按照要求的格式补充
        device_info = {
            "SDKVersion": "109",
            "cpuTemperature": "48",
            "cpuUsageRate": "37%",
            "deviceKey": "E03C1CB214AC1801",
            "faceCount": str(len(self.data_store.faces)),
            "fingerCount": "0",
            "freeDiskSpace": "5624M",
            "ip": "192.168.1.89",
            "languageType": "zh_CN",
            "memoryUsageRate": "50%",
            "personCount": str(len(self.data_store.persons)),
            "time": str(current_time),
            "timeZone": "",
            "version": "GD-V216.2130"
        }
        
        return self._get_response('LAN_SUS-0', data=device_info, msg='查询成功')
    
    def set_time(self, params):
        """设置设备时间
        timestamp: Unix毫秒级时间戳，String类型
        配置成功后，设备会在刷新自身时间时（每分钟刷新一次）使用该设置时间
        若设备未连入公网，时间设置成功后，会按照设置的时间增长
        若设备连入公网，设备本身有网络时间校对机制，每隔1分钟会联网校对一次时间，将设备时间调整与公网时间一致
        """
        passwd = params.get('pass')
        timestamp = params.get('timestamp')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证timestamp参数是否存在
        if 'timestamp' not in params:
            return self._get_response('LAN_EXP-1002', msg='timestamp参数异常')
        
        # 验证timestamp参数值
        if not timestamp:
            return self._get_response('LAN_EXP-2049')
        
        # 验证并处理时间戳
        try:
            # 尝试将timestamp转换为整数时间戳
            timestamp_int = int(timestamp)
            
            # 处理毫秒级时间戳（将其转换为秒级）
            # 如果是毫秒级时间戳（超过10位），转换为秒级
            if timestamp_int > 2147483647:  # 超过32位秒级时间戳最大值，说明是毫秒级
                timestamp_sec = timestamp_int // 1000
            else:
                timestamp_sec = timestamp_int
            
            # 验证时间戳是否在合理范围内（1970-01-01 到 2100-01-01）
            min_timestamp = 0  # 1970-01-01 00:00:00 UTC
            max_timestamp = 4102444800  # 2100-01-01 00:00:00 UTC
            
            if timestamp_sec < min_timestamp or timestamp_sec > max_timestamp:
                return self._get_response('LAN_EXP-2050', msg='timestamp时间范围错误')
            
            # 转换时间戳为可读时间格式
            import time
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_sec))
            
            # 保存设置的时间戳（毫秒级）和转换后的时间
            self.data_store.set_device_time(formatted_time)
            self.data_store.set_device_timestamp(timestamp_int)  # 保存原始毫秒级时间戳
            
        except ValueError:
            # 如果转换失败，返回时间格式错误
            return self._get_response('LAN_EXP-2050', msg='timestamp时间格式错误，应为整数毫秒级时间戳')
        
        # 返回成功响应
        return self._get_response('LAN_SUS-0', msg='设置成功。设备会在每分钟刷新时间时使用该设置时间；若未连入公网，将按照设置时间增长；若连入公网，将定期校对为网络时间')
    
    def set_language(self, params):
        """语言切换"""
        passwd = params.get('pass')
        language_type = params.get('languageType')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证languageType参数是否存在
        if 'languageType' not in params:
            return self._get_response('LAN_EXP-2188', msg='languageType参数异常')
        
        # 验证languageType参数值是否有效
        if language_type not in ['zh_CN', 'en']:
            return self._get_response('LAN_EXP-2189')
        
        return self._get_response('LAN_SUS-0', msg='设置成功')
    
    def set_timezone(self, params):
        """设置时区"""
        passwd = params.get('pass')
        timezone = params.get('timeZone')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证timeZone参数是否存在
        if 'timeZone' not in params:
            return self._get_response('LAN_EXP-2201', msg='timezone参数异常')
        
        # 验证timeZone参数值是否有效
        if not timezone or not isinstance(timezone, str):
            return self._get_response('LAN_EXP-2200')
        
        # 简化处理，直接返回成功
        return self._get_response('LAN_SUS-0', msg='设置成功')
    
    def restart_device(self, params):
        """设备重启"""
        passwd = params.get('pass')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        return self._get_response('LAN_SUS-0', msg='操作成功，设备即将重启')
    
    def set_identify_callback(self, params):
        """识别回调设置"""
        passwd = params.get('pass')
        callback_url = params.get('callbackUrl')
        base64_enable = params.get('base64Enable')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证callbackUrl参数
        if not callback_url:
            return self._get_response('LAN_EXP-2063')
        
        # 验证base64Enable参数，如果存在则必须为int类型
        if 'base64Enable' in params:
            if not isinstance(base64_enable, int):
                return self._get_response('LAN_EXP-1002', msg='base64Enable参数异常')
        
        # 简化处理，直接保存回调地址
        self.data_store.set_identify_callback(callback_url)
        return self._get_response('LAN_SUS-0', msg='设置成功')
    
    def set_img_reg_callback(self, params):
        """注册照片回调设置"""
        passwd = params.get('pass')
        callback_url = params.get('url')
        base64_enable = params.get('base64Enable')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证url参数
        if not callback_url:
            return self._get_response('LAN_EXP-2061')
        
        # 验证base64Enable参数，如果存在则必须为int类型
        if 'base64Enable' in params:
            if not isinstance(base64_enable, int):
                return self._get_response('LAN_EXP-1002', msg='base64Enable参数异常')
        
        # 简化处理，直接保存回调地址
        self.data_store.set_img_reg_callback(callback_url)
        return self._get_response('LAN_SUS-0', msg='设置成功')
    
    def open_door_control(self, params):
        """远程控制输出（开门）"""
        passwd = params.get('pass')
        control_type = params.get('type')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证type参数，如果存在则必须为int类型且值为1
        if 'type' in params:
            if not isinstance(control_type, int) or control_type != 1:
                return self._get_response('LAN_EXP-1002', msg='type参数异常')
        
        # 简化处理，直接返回开门成功
        return self._get_response('LAN_SUS-0', msg='开门成功')
    
    def set_signal_input(self, params):
        """信号输入设置"""
        passwd = params.get('pass')
        config = params.get('config')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证config参数是否存在
        if 'config' not in params:
            return self._get_response('LAN_EXP-2007', msg='config参数异常')
        
        # 验证config参数是否为空
        if not config:
            return self._get_response('LAN_EXP-2013', msg='config参数不能为空')
        
        # 验证config是否为dict类型
        if not isinstance(config, dict):
            return self._get_response('LAN_EXP-2008', msg='config类json格式错误')
        
        # 验证config参数的必填字段
        required_fields = ['inputNo', 'isEnable', 'type']
        for field in required_fields:
            if field not in config:
                return self._get_response('LAN_EXP-2009', msg='config参数不合法')
        
        # 验证inputNo参数
        input_no = config.get('inputNo')
        # 支持float类型的整数
        if isinstance(input_no, (int, float)) and input_no == int(input_no):
            input_no = int(input_no)
        if not isinstance(input_no, int):
            return self._get_response('LAN_EXP-2208', msg='inputNo参数异常')
        if input_no not in [1, 2]:
            return self._get_response('LAN_EXP-2209', msg='inputNo参数不合法')
        
        # 验证isEnable参数
        is_enable = config.get('isEnable')
        # 支持字符串和数字类型的布尔值
        if isinstance(is_enable, (int, float)):
            is_enable = bool(is_enable)
        elif isinstance(is_enable, str):
            is_enable = is_enable.lower() in ['true', '1']
        if not isinstance(is_enable, bool):
            return self._get_response('LAN_EXP-2210', msg='isEnable参数异常')
        # 布尔值没有不合法的情况，只要类型正确即可
        
        # 验证type参数
        type_param = config.get('type')
        # 支持float类型的整数
        if isinstance(type_param, (int, float)) and type_param == int(type_param):
            type_param = int(type_param)
        if not isinstance(type_param, int):
            return self._get_response('LAN_EXP-2212', msg='type参数异常')
        if type_param not in [1, 2, 3]:
            return self._get_response('LAN_EXP-2213', msg='type参数不合法')
        
        # 验证name参数（如果存在）
        if 'name' in config:
            name = config.get('name')
            # name参数不合法的情况，这里简化处理
            if not isinstance(name, str):
                return self._get_response('LAN_EXP-2214', msg='name参数不合法')
        
        # 保存设置
        # 这里简化处理，实际项目中应该保存到数据存储中
        self.data_store.set_signal_input_config(input_no, config)
        
        return self._get_response('LAN_SUS-0', msg='设置成功')
    
    def set_meet_warn(self, params):
        """会议与关门告警设置"""
        passwd = params.get('pass')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 简化处理，直接返回成功
        return self._get_response('LAN_SUS-0', msg='设置成功')
    
    def set_card_info(self, params):
        """卡片设置"""
        passwd = params.get('pass')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 简化处理，直接返回成功
        return self._get_response('LAN_SUS-0', msg='设置成功')
    
    def set_event_callback(self, params):
        """事件回调设置"""
        passwd = params.get('pass')
        callback_url = params.get('url')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 验证url参数
        if not callback_url:
            return self._get_response('LAN_EXP-2061')
        
        # 简化处理，直接保存回调地址
        self.data_store.set_event_callback(callback_url)
        return self._get_response('LAN_SUS-0', msg='设置成功')
    
    def get_door_sensor(self, params):
        """获取门磁状态"""
        passwd = params.get('pass')
        
        # 验证pass参数是否存在
        if 'pass' not in params:
            return self._get_response('LAN_EXP-1002', msg='pass参数异常')
        
        # 验证设备是否已设置密码
        if self.data_store.get_password() is None:
            return self._get_response('LAN_EXP-1003')
        
        # 验证密码是否正确
        if not self.data_store.verify_password(passwd):
            return self._get_response('LAN_EXP-1001')
        
        # 简化处理，返回默认状态
        return self._get_response('LAN_SUS-0', data={'status': 2})  # 2门磁开启
    
    def _get_response(self, code, msg=None, data=None):
        """生成统一格式的响应，确保返回参数顺序为code、data、msg、result、success
        如果data为None，则从响应中移除data字段"""
        base_response = code_mapping.get(code, code_mapping['LAN_EXP-1000'])
        
        # 构建响应字典，确保顺序正确
        response = {
            'code': code,
            'msg': msg if msg is not None else base_response['msg'],
            'result': base_response['result'],
            'success': base_response['success']
        }
        
        # 只有当data不为None时，才添加到响应中
        if data is not None:
            # 将data插入到code之后
            response = {
                'code': code,
                'data': data,
                'msg': response['msg'],
                'result': response['result'],
                'success': response['success']
            }
        elif base_response.get('data', None) is not None:
            # 如果base_response中有data，也添加到响应中
            response = {
                'code': code,
                'data': base_response['data'],
                'msg': response['msg'],
                'result': response['result'],
                'success': response['success']
            }
        
        return response

# 创建全局实例
device_service = DeviceService()