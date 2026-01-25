# 参数校验配置文件
# 定义每个接口的参数类型和必填项

param_validation = {
    # 设备管理类接口
    '/setPassWord': {
        'method': 'POST',
        'required': ['oldPass', 'newPass'],
        'type_map': {
            'oldPass': str,
            'newPass': str
        }
    },
    
    '/device/information': {
        'method': 'GET',
        'required': ['pass'],
        'type_map': {
            'pass': str
        }
    },
    
    '/setTime': {
        'method': 'POST',
        'required': ['pass', 'timestamp'],
        'type_map': {
            'pass': str,
            'timestamp': str
        }
    },
    
    '/device/setLanguage': {
        'method': 'POST',
        'required': ['pass', 'languageType'],
        'type_map': {
            'pass': str,
            'languageType': str
        }
    },
    
    '/device/setTimeZone': {
        'method': 'POST',
        'required': ['pass', 'timeZone'],
        'type_map': {
            'pass': str,
            'timeZone': str
        }
    },
    
    '/restartDevice': {
        'method': 'POST',
        'required': ['pass'],
        'type_map': {
            'pass': str
        }
    },
    
    '/setIdentifyCallBack': {
        'method': 'POST',
        'required': ['pass', 'callbackUrl'],
        'type_map': {
            'pass': str,
            'callbackUrl': str,
            'base64Enable': int
        }
    },
    
    '/setImgRegCallBack': {
        'method': 'POST',
        'required': ['pass', 'url'],
        'type_map': {
            'pass': str,
            'url': str,
            'base64Enable': int
        }
    },
    
    '/device/openDoorControl': {
        'method': 'POST',
        'required': ['pass'],
        'type_map': {
            'pass': str,
            'type': int
        }
    },
    
    '/device/setSignalInput': {
        'method': 'POST',
        'required': ['pass', 'config'],
        'type_map': {
            'pass': str,
            'config': dict
        }
    },
    
    '/meetAndWarnSet': {
        'method': 'POST',
        'required': ['pass'],
        'type_map': {
            'pass': str,
            'meetEnable': bool,
            'meetFreeTime': int,
            'doorWarnEnable': bool,
            'doorCloseTime': int
        }
    },
    
    '/cardInfoSet': {
        'method': 'POST',
        'required': ['pass', 'readDataEnable', 'readSector', 'readBlock', 'readShift', 'readKeyA', 'wgOutType'],
        'type_map': {
            'pass': str,
            'readDataEnable': bool,
            'readSector': int,
            'readBlock': int,
            'readShift': int,
            'readKeyA': str,
            'wgOutType': int
        }
    },
    
    '/device/eventCallBack': {
        'method': 'POST',
        'required': ['pass', 'url'],
        'type_map': {
            'pass': str,
            'url': str
        }
    },
    
    '/getDoorSensor': {
        'method': 'GET',
        'required': ['pass'],
        'type_map': {
            'pass': str
        }
    },
    
    # 人员管理类接口
    '/person/create': {
        'method': 'POST',
        'required': ['pass', 'person'],
        'type_map': {
            'pass': str,
            'person': dict
        }
    },
    
    '/person/delete': {
        'method': 'POST',
        'required': ['pass', 'id'],
        'type_map': {
            'pass': str,
            'id': str
        }
    },
    
    '/person/update': {
        'method': 'POST',
        'required': ['pass', 'person'],
        'type_map': {
            'pass': str,
            'person': dict
        }
    },
    
    '/person/find': {
        'method': 'GET',
        'required': ['pass', 'id'],
        'type_map': {
            'pass': str,
            'id': str
        }
    },
    
    '/person/findByPage': {
        'method': 'GET',
        'required': ['pass', 'personId'],
        'type_map': {
            'pass': str,
            'personId': str,
            'length': int,
            'index': int
        }
    },
    
    # 照片管理类接口
    '/face/create': {
        'method': 'POST',
        'required': ['pass', 'personId', 'imgBase64'],
        'type_map': {
            'pass': str,
            'personId': str,
            'faceId': str,
            'imgBase64': str,
            'isEasyWay': bool
        }
    },
    
    '/face/delete': {
        'method': 'POST',
        'required': ['pass', 'faceId'],
        'type_map': {
            'pass': str,
            'faceId': str
        }
    },
    
    '/face/update': {
        'method': 'POST',
        'required': ['pass', 'personId', 'faceId', 'imgBase64'],
        'type_map': {
            'pass': str,
            'personId': str,
            'faceId': str,
            'imgBase64': str,
            'isEasyWay': bool
        }
    },
    
    '/face/find': {
        'method': 'POST',
        'required': ['pass', 'personId'],
        'type_map': {
            'pass': str,
            'personId': str
        }
    },
    
    '/face/takeImg': {
        'method': 'POST',
        'required': ['pass', 'personId'],
        'type_map': {
            'pass': str,
            'personId': str
        }
    },
    
    '/face/deletePerson': {
        'method': 'POST',
        'required': ['pass', 'personId'],
        'type_map': {
            'pass': str,
            'personId': str
        }
    },
    
    # 识别记录接口
    '/newFindRecords': {
        'method': 'GET',
        'required': ['pass', 'personId', 'startTime', 'endTime'],
        'type_map': {
            'pass': str,
            'personId': str,
            'startTime': str,
            'endTime': str,
            'length': int,
            'model': int,
            'order': str,
            'index': int
        }
    },
    
    '/newDeleteRecords': {
        'method': 'POST',
        'required': ['pass', 'personId', 'startTime', 'endTime'],
        'type_map': {
            'pass': str,
            'personId': str,
            'startTime': str,
            'endTime': str,
            'model': int
        }
    }
}