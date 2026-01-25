# 参数验证配置文件
# 定义各接口的参数验证规则

param_validation = {
    # 接收门禁开启信息接口
    '/v1/external/ywgl/pushAccessControlInfo': {
        'method': 'POST',
        'required': ['workOrdNum', 'room', 'openDoorTime', 'openDoorResult'],
        'type_map': {
            'workOrdNum': str,
            'room': str,
            'openDoorTime': str,
            'openDoorResult': int,
            'personName': str,
            'personId': str,
            'deviceId': str,
            'doorNum': str
        }
    },
    # 底层人脸操作结果同步接口
    '/v1/external/ywgl/syncFaceOperationResult': {
        'method': 'POST',
        'required': ['workOrdNum', 'operationResult', 'operationTime'],
        'type_map': {
            'workOrdNum': str,
            'operationResult': int,
            'operationTime': str,
            'errorMsg': str,
            'deviceId': str,
            'personId': str
        }
    }
}