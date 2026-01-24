from spider_tools.project_tools.JT.ZZ.zz_match_new6.zzmatchspider import ZZMatchSpider

# ============ 命令行入口 ================= #
if __name__ == '__main__':
    # 示例：完全沿用原来调用方式   01-08-08-01-11
    spider = ZZMatchSpider(precinct_id='01-08-08', batch_num='20200223', force_create=False,
                           mains_nature='用于电费分析', power_site_level='传输节点',
                           power_room_type='汇聚机房', power_supply_mode='双电源双回路供电',
                           cutin_date='2025-01-02', province_id='520000', city_id='520400',
                           match_mode=0, irms_province_code='GZ', county_id='520404',
                           site_type='汇聚站点')
    # spider.name_match_site()
    spider.name_match_site_room()
    # spider.name_match_site_room_device()
