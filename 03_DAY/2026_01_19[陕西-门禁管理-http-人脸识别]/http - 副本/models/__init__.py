# 数据模块初始化文件

from .device import device_data
from .person import person_data
from .face import face_data
from .record import record_data
from .device_status import device_status

__all__ = ['device_data', 'person_data', 'face_data', 'record_data', 'device_status']