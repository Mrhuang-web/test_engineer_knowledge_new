#!/usr/bin/env python3
# 动环接口客户端模块
# 用于调用动环平台的接口

import requests
import json
import logging
from configs.url_config import external_config

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DonghuanClient:
    """动环接口客户端"""
    
    def __init__(self, env=None):
        """
        初始化动环客户端
        
        Args:
            env (str): 环境名称，可选值：test/prod，默认使用配置文件中的current_env
        """
        # 获取配置
        self.env = env or external_config['current_env']
        env_config = external_config[self.env]
        
        self.server_root = env_config['server_root']
        self.secret_key = env_config['secret_key']
        self.use_https = env_config['use_https']
        self.base_url = f"{'https' if self.use_https else 'http'}://{self.server_root}"
        
        logger.info(f"动环客户端初始化成功，环境: {self.env}，服务器: {self.server_root}")
        
    def _request(self, path, data):
        """
        发送请求到动环接口
        
        Args:
            path (str): 接口路径，例如：/v1/external/ywgl/addFace
            data (dict): 请求数据
            
        Returns:
            dict: 响应结果
        """
        url = f"{self.base_url}{path}"
        
        logger.info(f"调用动环接口: {url}")
        logger.info(f"请求数据: {data}")
        
        try:
            # 准备form-data格式的请求数据
            form_data = {}
            
            # 将data转换为JSON字符串，放入form-data的data字段
            form_data['data'] = json.dumps(data)
            
            # 添加密钥到form-data
            form_data['secret_key'] = self.secret_key
            
            logger.info(f"form-data请求数据: {form_data}")
            
            # 发送POST请求，使用form-data格式
            response = requests.post(url, data=form_data, verify=False)  # verify=False 用于测试环境，生产环境建议开启
            
            # 解析响应
            response.raise_for_status()  # 检查HTTP状态码
            response_data = response.json()
            
            logger.info(f"接口响应: {response_data}")
            return response_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"请求异常: {e}")
            return {
                'code': '21',
                'desc': f'接口异常: {str(e)}',
                'data': ''
            }
        except json.JSONDecodeError as e:
            logger.error(f"响应解析异常: {e}")
            return {
                'code': '21',
                'desc': f'响应解析异常: {str(e)}',
                'data': ''
            }
    
    def add_face(self, face_data):
        """
        调用动环addFace接口，推送工单及人脸照片
        
        Args:
            face_data (dict): 人脸数据，必须包含以下字段：
                - workOrdNum: 工单号（必填）
                - name: 姓名（必填）
                - account: 账号（必填）
                - phone: 联系方式（必填）
                - city: 城市（必填）
                - site: 站点名称列表（必填）
                - room: 进入机房名称列表（必填）
                - deviceId: 门禁设备ID列表（必填）
                - picture: 人脸照片base64字符串（必填）
                - startDate: 登记时间，格式：YYYY-MM-DD（必填）
                
        Returns:
            dict: 响应结果，包含以下字段：
                - code: 返回编码，00表示成功，21为接口异常，22为安全校验不通过，23为请求参数错误
                - desc: 返回描述
                - data: 业务数据信封
        """
        # 直接调用接口，_request方法会处理form-data格式转换
        return self._request('/v1/external/ywgl/addFace', face_data)

# 单例模式，方便全局使用
def get_donghuan_client(env=None):
    """
    获取动环客户端实例
    
    Args:
        env (str): 环境名称，可选值：test/prod
        
    Returns:
        DonghuanClient: 动环客户端实例
    """
    return DonghuanClient(env)

if __name__ == '__main__':
    # 示例用法1：使用默认环境（配置文件中current_env指定）
    client1 = get_donghuan_client()
    
    # 示例用法2：指定环境
    # client2 = get_donghuan_client(env='prod')
    
    # 示例数据
    face_data = {
        "workOrdNum": "JF-20251222-0313",
        "name": "测试用户",
        "account": "testuser",
        "phone": "13800001111",
        "city": "咸阳市",
        "site": ["安康白河庆华化工厂站点"],
        "room": ["咸阳秦都应急楼一楼综合机房"],
        "deviceId": ["20231201996901"],
        "picture": "test_base64_string",
        "startDate": "2025-12-26"
    }
    
    # 调用接口
    result = client1.add_face(face_data)
    print(f"调用结果: {result}")
