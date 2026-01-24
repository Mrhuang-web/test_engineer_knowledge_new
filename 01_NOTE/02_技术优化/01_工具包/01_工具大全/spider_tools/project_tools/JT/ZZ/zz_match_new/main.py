# ==================== 使用示例 ====================
if __name__ == '__main__':
    # 示例2: 运行业务逻辑（保留原始调用方式）
    # 珠海 440400 汕头 440500  佛山 440600  韶关 440200
    # main_nature:市电直供、市电转供、其他（风力发电、太阳能发电、风光互补，用于电费分析）
    spider = ZZMatchSpider(precinct_id='01-01-11', batch_num='20240101', force_create=False,
                           mains_nature='用于电费分析', power_site_level='传输节点', power_room_type='汇聚机房',
                           power_supply_mode='双电源双回路供电', cutin_date='2025-01-02', province_id='440000',
                           city_id='440200', match_model=0, irms_province_code='GD', county_id='440511',
                           site_type='汇聚站点')
    spider.name_match_site()
    # spider.name_match_site_room()

    # spider = ZZMatchSpider(precinct_id='01-08-08-04-03-01', batch_num='20250104', force_create=False, match_mode=2)
    # spider.name_match_site_room_device()
