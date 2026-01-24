class WriterFactory:
    """写入器工厂"""

    @staticmethod
    def create_writer(index_category: str, **kwargs) -> BaseWriter:
        """
        创建写入器实例 - 保持原始接口不变
        :param index_category: 索引类别字符串
        """
        # 设备类 - 通过 device_type 参数传递
        if index_category in ['air', 'battery', 'low_ac_distribution', 'switch_power',
                              'energy_save', 'high_dc_distribution', 'high_distribution',
                              'high_power', 'smart_meter', 'transform', 'transform_device', 'ups']:
            return DeviceWriter(device_type=index_category, **kwargs)

        # 房间类
        elif index_category == 'room':
            return RoomWriter(**kwargs)
        elif index_category == 'room_property':
            return RoomPropertyWriter(**kwargs)

        # 站点类
        elif index_category == 'site':
            return SiteWriter(**kwargs)
        elif index_category == 'site_property':
            return SitePropertyWriter(**kwargs)

        # 映射类
        elif index_category.startswith('irms_') and index_category.endswith('_map'):
            # 提取映射类型，如 'dc', 'rom', 'site'
            map_type = index_category.split('_')[1]
            return IrmsMapWriter(map_type=map_type, **kwargs)

        # 连接类
        elif index_category == 'link_pe_in':
            return BaseWriter(index_type=index_category, **kwargs)

        else:
            raise ValueError(f"不支持的索引类别: {index_category}")
