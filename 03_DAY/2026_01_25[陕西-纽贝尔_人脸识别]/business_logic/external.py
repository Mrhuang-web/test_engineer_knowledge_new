# 外部接口业务逻辑
# 处理动环发给运维管理的接口

class ExternalService:
    def push_access_control_info(self, params):
        """接收门禁开启信息接口"""
        # 处理门禁开启信息
        work_ord_num = params.get('workOrdNum', '')
        room = params.get('room', '')
        open_door_time = params.get('openDoorTime', '')
        open_door_result = params.get('openDoorResult', 0)
        person_name = params.get('personName', '')
        person_id = params.get('personId', '')
        device_id = params.get('deviceId', '')
        door_num = params.get('doorNum', '')
        
        # 记录日志或保存数据
        print(f"Received access control info: workOrdNum={work_ord_num}, room={room}, openDoorTime={open_door_time}, openDoorResult={open_door_result}")
        
        # 返回成功响应
        return {
            'code': '000000',
            'msg': 'Success',
            'result': 1,
            'success': True
        }
    
    def sync_face_operation_result(self, params):
        """底层人脸操作结果同步接口"""
        # 处理人脸操作结果
        work_ord_num = params.get('workOrdNum', '')
        operation_result = params.get('operationResult', 0)
        operation_time = params.get('operationTime', '')
        error_msg = params.get('errorMsg', '')
        device_id = params.get('deviceId', '')
        person_id = params.get('personId', '')
        
        # 记录日志或保存数据
        print(f"Received face operation result: workOrdNum={work_ord_num}, operationResult={operation_result}, operationTime={operation_time}")
        
        # 返回成功响应
        return {
            'code': '000000',
            'msg': 'Success',
            'result': 1,
            'success': True
        }

# 创建服务实例
external_service = ExternalService()