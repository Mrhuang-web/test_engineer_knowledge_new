import os
import json

class EventCenter:
    def __init__(self, config_path=None):
        self.events = {}  # 事件列表，键为事件指令
        self.current_event_index = {}  # 当前轮询的事件索引，键为事件指令
        self.protocol_configs = {}  # 不同协议的配置
        
        # 如果没有指定配置路径，使用默认路径
        if config_path is None:
            self.config_path = os.path.join(
                os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                "config", "event", "event.json"
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
                    self.events = config.get('events', {})
                    # 初始化每个事件指令的当前索引
                    for event_key in self.events:
                        self.current_event_index[event_key] = 0
                print(f"事件配置加载成功: {len(self.events)} 个事件指令")
            else:
                # 配置文件不存在，使用空配置
                self.events = {}
                self.current_event_index = {}
                print(f"事件配置文件不存在，使用空配置")
        except Exception as e:
            print(f"加载事件配置失败: {e}")
            # 使用空配置
            self.events = {}
            self.current_event_index = {}
    
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
    
    def get_next_event(self, event_key):
        """获取下一个事件，如果所有事件都返回完毕，则重新开始新一轮"""
        if event_key not in self.events:
            return None
        
        event_list = self.events[event_key]
        if not event_list:
            return None
        
        # 初始化索引如果不存在
        if event_key not in self.current_event_index:
            self.current_event_index[event_key] = 0
        
        event = event_list[self.current_event_index[event_key]]
        self.current_event_index[event_key] = (self.current_event_index[event_key] + 1) % len(event_list)
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
        data_frame_type = through_sdu.get('data_frame_type', '')
        
        # 组合判断键
        # 直接根据cid2、group、type组合生成command_key
        command_key = cid2 + group + type_
        
        # 尝试不同的组合方式查找协议配置
        # 1. 完整组合：cid2 + group + type_
        # 2. data_frame_type（适用于邦讯协议）
        command_keys = [command_key, data_frame_type]
        
        # 查找匹配的协议配置
        matched_config = None
        final_command_key = command_key
        
        # 遍历所有可能的command_keys
        for key in command_keys:
            for protocol_name, config in self.protocol_configs.items():
                if config.get('command_key') == key:
                    matched_config = config
                    final_command_key = key
                    break
            if matched_config:
                break
        
        # 如果没有匹配的协议配置，返回原始数据
        if not matched_config:
            return rule_response
        
        # 检查协议配置是否启用
        if not matched_config.get('enabled', False):
            return rule_response
        
        # 获取事件数据
        event_data = self.get_event_data(matched_config, final_command_key)
        if not event_data:
            return rule_response
        
        # 更新响应数据
        if 'data' in rule_response:
            # 根据事件数据中实际存在的字段来更新响应
            if 'remark' in event_data:
                rule_response['data']['remark'] = event_data.get('remark', '00')
            if 'status' in event_data:
                rule_response['data']['status'] = event_data.get('status', '00')
            if 'event_source' in event_data:
                rule_response['data']['event_source'] = event_data.get('event_source', '0000000000')
        
        return rule_response
    
    def get_event_data(self, protocol_config=None, command_key=None):
        """
        获取事件数据
        根据协议配置获取对应的事件数据
        """
        # 如果没有协议配置或command_key，返回None
        if not protocol_config or not command_key:
            return None
        
        # 使用command_key作为事件指令获取事件
        return self.get_next_event(command_key)
    
    

# 创建全局事件中心实例
event_center = EventCenter()