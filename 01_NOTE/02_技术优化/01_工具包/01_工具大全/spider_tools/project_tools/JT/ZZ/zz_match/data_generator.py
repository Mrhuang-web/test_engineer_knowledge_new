# data_generator.py
import random
import datetime


class DataGenerator:
    @staticmethod
    def generate_device_data(index_type, count):
        data_list = []
        for _ in range(count):
            data = {
                "device_type": index_type,
                "estimated_retirement_time": (
                            datetime.datetime.now() + datetime.timedelta(days=random.randint(1, 1000))).strftime(
                    '%Y-%m-%d'),
                "county_id": str(random.randint(100000, 999999)),
                "device_code": f"device_code_{random.randint(1, 1000)}",
                "device_number": f"device_number_{random.randint(1, 1000)}",
                "device_subclass": f"device_subclass_{random.randint(1, 1000)}",
                "batch_num": datetime.datetime.now().strftime('%Y%m%d'),
                "product_name": f"product_name_{random.randint(1, 1000)}",
                "res_code": f"res_code_{random.randint(1, 1000)}",
                "zh_label": f"zh_label_{random.randint(1, 1000)}",
                "start_time": datetime.datetime.now().strftime('%Y-%m-%d'),
                "province_id": str(random.randint(100000, 999999)),
                "city_id": str(random.randint(100000, 999999)),
                "vendor_id": f"vendor_id_{random.randint(1, 1000)}",
                "maintainor": f"maintainor_{random.randint(1, 1000)}",
                "lifecycle_status": "现网",
                "qualitor": f"qualitor_{random.randint(1, 1000)}",
                "collect_time": datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "related_room": f"related_room_{random.randint(1, 1000)}",
                "related_site": f"related_site_{random.randint(1, 1000)}",
            }
            data_list.append(data)
        return data_list
