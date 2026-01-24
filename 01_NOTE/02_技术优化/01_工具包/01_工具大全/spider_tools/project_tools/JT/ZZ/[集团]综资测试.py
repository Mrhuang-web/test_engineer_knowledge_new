# 测试2
from spider_tools.project_tools.JT.ZZ.common_zz_match import ZZMatchSpider

if __name__ == '__main__':
    # 目前从市开始匹配（可修改selectForESlist更改层级的匹配）
    # force_create目前使用False,替换为True会清空索引重新创建
    # spider = ZZMatchSpider(precinct_id='01-01-08', batch_num='20250104', force_create=False,
    #                        mains_nature='市电转供', power_site_level='传输节点', power_room_type='汇聚机房',
    #                        power_supply_mode='双电源双回路供电', cutin_date='2024-11-01', province_id='440000',
    #                        city_id='440500', match_model=0, irms_province_code='GD')
    # spider.name_match_site()

    #
    spider = ZZMatchSpider(precinct_id='01-08-08-04-03-01-01', batch_num='20250104', force_create=False, match_model=2)
    spider.name_match_site_room_device()
