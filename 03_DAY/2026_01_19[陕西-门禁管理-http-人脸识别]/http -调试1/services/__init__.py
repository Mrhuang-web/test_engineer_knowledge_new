# 业务逻辑模块初始化文件

from .device_service import device_service
from .person_service import person_service
from .face_service import face_service
from .record_service import record_service

__all__ = ['device_service', 'person_service', 'face_service', 'record_service']