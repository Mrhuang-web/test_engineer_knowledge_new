import time

import requests as rq
from datetime import datetime, timedelta


class Cabinet:
    def __init__(self):
        self.url = 'http://10.12.8.147:30917/v1/energy/scheduleCabinetReport'
        self.headers = {
            'host': '10.12.8.147:30917',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36',
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }

    def pull_cabinet_report(self, date, roomId):
        data = {
            'dayDate': date,
            'roomId': roomId
        }
        info = rq.get(url=self.url, headers=self.headers, params=data)
        return info.status_code, info.text

    def pull_cabinet_column_report(self, date, roomId):
        self.url = 'http://10.12.8.147:30917/v1/energy/scheduleCabinetColumnReport'
        data = {
            'dayDate': date,
            'roomId': roomId
        }
        info = rq.get(url=self.url, headers=self.headers, params=data)
        return info.status_code, info.text


if __name__ == '__main__':
    cabinet = Cabinet()

    start_date = datetime(2025, 9, 1)
    end_date = datetime(2025, 11, 30)  # 举例结束日期
    print(start_date)

    current_date = start_date
    while current_date <= end_date:

        current_date_shift = current_date.strftime('%Y-%m-%d')
        roomId = '01-08-08-01-11-01-04'

        # cabinet_info = cabinet.pull_cabinet_report(current_date_shift, roomId)
        # print("机柜_current_date:", current_date, cabinet_info)
        # time.sleep(5)

        cabinet_column_info = cabinet.pull_cabinet_column_report(current_date_shift, roomId)
        print("机柜列_current_date:", current_date, cabinet_column_info)
        time.sleep(5)
        current_date += timedelta(days=1)
