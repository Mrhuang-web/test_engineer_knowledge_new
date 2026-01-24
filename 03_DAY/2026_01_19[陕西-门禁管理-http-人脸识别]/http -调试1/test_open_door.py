import requests
import json

def test_open_door():
    """测试远程开门功能"""
    url = "http://127.0.0.1:8091/device/openDoorControl"
    data = {"type": 1, "pass": "12345678"}
    
    try:
        response = requests.post(url, data=data, timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Testing remote door opening...")
    test_open_door()