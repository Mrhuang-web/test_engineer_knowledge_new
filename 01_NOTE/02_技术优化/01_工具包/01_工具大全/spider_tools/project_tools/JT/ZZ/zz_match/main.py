# main.py
from spider import ZZMatchSpider

if __name__ == '__main__':
    spider = ZZMatchSpider(precinct_id='01-01-11', batch_num='20250101', index_suffix='YYYYMMm', site_type='核心站点',
                           irms_province_code='GZ', province_id='520000', city_id='520400', county_id='000000')
    spider.name_match_site()
