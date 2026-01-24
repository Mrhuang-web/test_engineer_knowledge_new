class DeviceTypeMapper:
    """设备类型到索引类型的映射器"""

    # 用户提供的映射关系
    DEVICE_TYPE_MAP = {
        # 高压配电
        '1': 'high_distribution',
        # 低压交流配电
        '2': 'low_ac_distribution',
        '96': 'low_ac_distribution',
        # 变压器
        '3': 'transform',
        # 低压直流配电
        '4': 'low_dc_distribution',  # 原配置中未包含，需补充
        # 发电机组
        '5': 'power_generation',  # 注意：原配置中未包含，需补充
        # 开关电源
        '6': 'switch_power',
        # 蓄电池
        '68': 'battery',
        '7': 'battery',
        # ups设备
        '8': 'ups',
        # 空调设备
        '11': 'air',
        '12': 'air',
        '13': 'air',
        '15': 'air',
        # 变换设备
        '14': 'transform_device',
        # 动环监控
        '17': 'power_monitor',  # 原配置中未包含，需补充
        '76': 'power_monitor',  # 原配置中未包含，需补充
        '93': 'power_monitor',  # 原配置中未包含，需补充
        # 节能设备
        '18': 'energy_save',
        '77': 'energy_save',
        '78': 'energy_save',
        # 高压直流电源
        '87': 'high_power',
        # 高压直流配电
        '88': 'high_dc_distribution',
        # 智能电表
        '92': 'smart_meter',
        # 其他设备
        '16': 'other',  # 原配置中未包含，需补充
        '94': 'other',  # 原配置中未包含，需补充
    }

    @staticmethod
    def get_index_type(device_type_str: str) -> str:
        """
        根据设备类型字符串返回对应的索引类型
        :param device_type_str: 如 'CDU', '空调', 'UPS设备'
        :return: 如 'air', 'ups', 'battery'
        """
        # 先尝试直接匹配
        index_type = DeviceTypeMapper.DEVICE_TYPE_MAP.get(device_type_str)
        if index_type:
            return index_type
        # 默认返回 other
        print(f"未找到设备类型 '{device_type_str}' 的映射，使用默认索引类型 'other'")
        return 'other'
