# 设备管理业务逻辑

import time
from rules.response import base_response, ERROR_CODES
from models import device_data

class DeviceService:
    """设备管理业务逻辑类"""
    
    @staticmethod
    def set_password(old_pass, new_pass):
        """设置设备密码"""
        from models import device_status
        
        # 检查密码是否为空或只包含空格
        if not old_pass or not old_pass.strip():
            return base_response(0, False, '旧密码不允许为空或空格', ERROR_CODES['PASSWORD_CANT_BE_EMPTY'])
        
        if not new_pass or not new_pass.strip():
            return base_response(0, False, '新密码不允许为空或空格', ERROR_CODES['NEW_PASSWORD_CANT_BE_EMPTY'])
        
        current_password = device_data.get_password()
        
        # 情况1：设备初始无密码，首次设置密码
        if current_password is None:
            if old_pass != new_pass:
                return base_response(0, False, '初始设置密码时，旧密码和新密码必须一致', ERROR_CODES['INIT_PASSWORD_SAME'])
            # 首次设置密码成功
            device_data.set_password(new_pass)
            # 标记首次设置完成
            device_status.set_first_setup_completed()
            return base_response(data=f'password is : {new_pass}', msg='密码设置成功')
        
        # 情况2：设备已有密码，修改密码
        if current_password == old_pass:
            device_data.set_password(new_pass)
            return base_response(data=f'password is : {new_pass}', msg='密码修改成功')
        
        # 情况3：旧密码错误
        return base_response(0, False, '旧密码错误', ERROR_CODES['PASSWORD_INCORRECT'])
    
    @staticmethod
    def get_device_info():
        """获取设备信息"""
        return base_response(data=device_data.get_information(), msg='查询成功')
    
    @staticmethod
    def set_time(timestamp):
        """设置设备时间"""
        if not timestamp:
            return base_response(0, False, 'timestamp 参数异常', ERROR_CODES['TIMESTAMP_PARAM_ERROR'])
        
        # 检查timestamp格式是否正确
        try:
            # 尝试转换为整数
            int_timestamp = int(timestamp)
        except ValueError:
            return base_response(0, False, 'timestamp 时间格式错误', ERROR_CODES['TIMESTAMP_FORMAT_ERROR'])
        
        # 设置系统时间
        device_data.set_system_time(int_timestamp)
        device_data.set_last_sync_time(int_timestamp)
        
        # 附加功能实现：
        # 1. 配置成功后，设备会在刷新自身时间时（每分钟刷新一次），使用该设置时间
        # 2. 若设备未连入公网，时间设置成功后，会按照设置的时间增长
        # 3. 若设备连入公网，设备本身有网络时间校对机制，每隔1分钟会联网校对一次时间
        
        # 返回符合要求的消息
        return base_response(msg='设置成功。若设备未连入公网，则此时间会生效；若设备连入公网，则会重新使用公网时间')
    
    @staticmethod
    def set_language(language_type):
        """语言切换"""
        if not language_type:
            return base_response(0, False, '语言类型不能为空')
        device_data.update_information('language', language_type)
        return base_response(msg='语言设置成功')
    
    @staticmethod
    def set_timezone(time_zone):
        """设置时区"""
        if not time_zone:
            return base_response(0, False, '时区不能为空')
        device_data.update_information('timeZone', time_zone)
        return base_response(msg='时区设置成功')
    
    @staticmethod
    def restart_device():
        """设备重启"""
        return base_response(msg='设备重启成功')
    
    @staticmethod
    def set_identify_callback(callback_url, base64_enable=1):
        """识别回调"""
        if not callback_url or not callback_url.strip():
            # 清空回调地址
            device_data.set_callback('identify', '', base64_enable)
            return base_response(data='', msg='设置成功')
        
        # 设置回调地址
        if device_data.set_callback('identify', callback_url, base64_enable):
            return base_response(data=callback_url, msg='设置成功')
        else:
            return base_response(0, False, '请输入正确格式的callbackUrl地址', ERROR_CODES['CALLBACK_URL_ILLEGAL'])
    
    @staticmethod
    def set_img_reg_callback(url, base64_enable=1):
        """注册照片回调"""
        if not url or not url.strip():
            # 清空回调地址
            device_data.set_callback('imgReg', '', base64_enable)
            return base_response(data='', msg='设置成功')
        
        # 设置回调地址
        if device_data.set_callback('imgReg', url, base64_enable):
            return base_response(data=url, msg='设置成功')
        else:
            return base_response(0, False, '请输入正确格式的url地址', ERROR_CODES['URL_ILLEGAL'])
    
    @staticmethod
    def open_door(type_=1):
        """远程控制输出"""
        # 检查type参数是否为整数类型
        try:
            type_int = int(type_)
        except (ValueError, TypeError):
            # type参数不是整数类型
            return base_response(0, False, '设备交互类型参数异常', ERROR_CODES['TYPE_PARAM_ERROR'])
        
        if type_int == 1:
            device_data.set_door_status(2)  # 2门磁开启
            # 模拟门开启，实际项目中应该使用异步处理或硬件控制
            device_data.set_door_status(3)  # 3门磁闭合
            return base_response(msg='开门成功')
        return base_response(0, False, '无效的操作类型', ERROR_CODES['TYPE_ILLEGAL'])
    
    @staticmethod
    def get_door_status():
        """获取门磁状态"""
        return base_response(data={'status': device_data.get_door_status()})
    
    @staticmethod
    def set_event_callback(url):
        """事件回调"""
        if not url or not url.strip():
            # 清空回调地址
            device_data.set_callback('event', '')
            return base_response(data='', msg='设置成功')
        
        # 设置回调地址
        if device_data.set_callback('event', url):
            return base_response(data=url, msg='设置成功')
        else:
            return base_response(0, False, '请输入正确格式的url地址', ERROR_CODES['URL_ILLEGAL'])
    
    @staticmethod
    def reset_device():
        """重置设备到初始状态"""
        from models import device_status, person_data, face_data
        from models.record import record_data
        
        # 清空密码
        device_data.set_password(None)
        
        # 重置设备状态
        device_status.set_first_setup_completed(False)
        device_status.increment_reset_count()
        
        # 清空人员数据
        person_data.delete_person('-1')
        
        # 清空照片数据
        face_data.delete_faces_by_person('-1')
        
        # 清空记录数据
        record_data.delete_records('-1')
        
        return base_response(msg='设备重置成功')
    
    @staticmethod
    def get_device_status():
        """获取设备状态信息"""
        from models import device_status
        return base_response(data=device_status.get_status())
    
    @staticmethod
    def set_signal_input(config):
        """信号输入设置"""
        if not config:
            return base_response(0, False, 'config参数异常', ERROR_CODES['CONFIG_PARAM_ERROR'])
        return base_response(msg='设置成功')
    
    @staticmethod
    def set_meet_and_warn(meet_enable, meet_free_time, door_warn_enable, door_close_time):
        """会议与关门告警设置"""
        return base_response(msg='设置成功')
    
    @staticmethod
    def set_card_info(read_data_enable, read_sector, read_block, read_shift, read_key_a, wg_out_type):
        """卡片设置"""
        return base_response(msg='设置成功')

# 创建设备服务实例
device_service = DeviceService()