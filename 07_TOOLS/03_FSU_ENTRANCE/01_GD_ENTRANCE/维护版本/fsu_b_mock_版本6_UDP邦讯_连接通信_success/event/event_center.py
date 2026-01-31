import os
import json

class EventCenter:
    def __init__(self, config_path=None):
        self.events = []  # 事件列表
        self.current_event_index = 0  # 当前轮询的事件索引
        self.protocol_configs = {}  # 不同协议的配置
        
        # 如果没有指定配置路径，使用默认路径
        if config_path is None:
            self.config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config", "liwei", "event_rules", "events.json"
            )
        else:
            self.config_path = config_path
        
        # 协议配置文件路径
        self.protocol_config_path = os.path.join(
            os.path.dirname(self.config_path),
            "protocol_configs.json"
        )
        
        self.init_events()
        self.init_protocol_configs()
    
    def init_events(self):
        # 从配置文件初始化事件配置
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.events = config.get('events', [])
                print(f"事件配置加载成功: {len(self.events)} 个事件")
            else:
                # 配置文件不存在，使用空配置
                self.events = []
                print(f"事件配置文件不存在，使用空配置")
        except Exception as e:
            print(f"加载事件配置失败: {e}")
            # 使用空配置
            self.events = []
    
    def init_protocol_configs(self):
        # 从配置文件初始化协议配置
        try:
            if os.path.exists(self.protocol_config_path):
                with open(self.protocol_config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.protocol_configs = config.get('protocol_configs', {})
                print(f"协议配置加载成功: {len(self.protocol_configs)} 个协议")
            else:
                # 配置文件不存在，使用空配置
                self.protocol_configs = {}
                print(f"协议配置文件不存在，使用空配置")
        except Exception as e:
            print(f"加载协议配置失败: {e}")
            # 使用空配置
            self.protocol_configs = {}
    
    def get_next_event(self):
        """获取下一个事件，如果所有事件都返回完毕，则重新开始新一轮"""
        if not self.events:
            return None
        
        event = self.events[self.current_event_index]
        self.current_event_index = (self.current_event_index + 1) % len(self.events)
        return event
    
    def check_and_update_response(self, parsed_data, rule_response):
        """
        检查并更新响应数据
        根据cid2、group、type组合判断是否需要处理
        """
        # 提取cid2、group、type
        through_pdu = parsed_data.get('through_pdu', {})
        through_sdu = parsed_data.get('through_sdu', {})
        
        cid2 = through_pdu.get('cid2', '')
        group = through_sdu.get('group', '')
        type_ = through_sdu.get('type', '')
        
        # 组合判断键
        command_key = cid2 + group + type_
        
        # 查找匹配的协议配置
        matched_config = None
        for protocol_name, config in self.protocol_configs.items():
            if config.get('command_key') == command_key:
                matched_config = config
                break
        
        # 如果没有匹配的协议配置，返回原始数据
        if not matched_config:
            return rule_response
        
        # 检查协议配置是否启用
        if not matched_config.get('enabled', False):
            return rule_response
        
        # 获取事件数据
        event_data = self.get_event_data(matched_config)
        if not event_data:
            return rule_response
        
        # 更新响应数据
        if 'data' in rule_response:
            rule_response['data']['remark'] = event_data.get('remark', '00')
            rule_response['data']['status'] = event_data.get('status', '00')
            rule_response['data']['event_source'] = event_data.get('event_source', '0000000000')
        
        return rule_response
    
    def get_event_data(self, protocol_config=None):
        """
        获取事件数据
        根据协议配置获取对应的事件数据
        """
        # 如果没有协议配置，使用默认事件轮询
        if not protocol_config:
            return self.get_next_event()
        
        # 从协议配置中获取事件文件路径
        event_file = protocol_config.get('event_file')
        if not event_file:
            return self.get_next_event()
        
        # 构建事件文件的完整路径
        event_file_path = os.path.join(
            os.path.dirname(self.config_path),
            event_file
        )
        
        # 读取事件文件
        try:
            if os.path.exists(event_file_path):
                with open(event_file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    events = config.get('events', [])
                    if events:
                        # 轮询获取事件
                        event = events[self.current_event_index % len(events)]
                        self.current_event_index += 1
                        return event
        except Exception as e:
            print(f"读取事件文件失败: {e}")
        
        # 如果读取失败，使用默认事件轮询
        return self.get_next_event()
    
    

# 创建全局事件中心实例
event_center = EventCenter()