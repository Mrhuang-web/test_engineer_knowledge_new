import requests as rq
import csv

header = {
    "authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1OTY3MDg1LCJpYXQiOjE3NjU4ODA2ODUsImp0aSI6ImJhZDE2MDM5YTA0YTQyOTdhZTc3NjAxMzFhZWYyOGI3IiwidXNlcl9pZCI6NjJ9.Co83SlyAyH0BPiMmYRx9geHiuyaiF2m7ikoYmQBEUEQ",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
}
url = "http://10.12.5.137:9002/api/files/"


with open('API.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f)
    writer.writerow(['file_path', 'file_name', 'file_status'])   # 表头

    for page in range(1, 26):        # 1~25 页
        params = {'page': page}      # 正确传参
        resp = rq.get(url, headers=header, params=params)
        resp.raise_for_status()
        json_data = resp.json()

        # 根据真实字段取，若接口返回的是 { results: [ {...}, ... ] }
        for item in json_data['results']:
            writer.writerow([
                item['file_path'],
                item['file_name'],
                item['status']
            ])