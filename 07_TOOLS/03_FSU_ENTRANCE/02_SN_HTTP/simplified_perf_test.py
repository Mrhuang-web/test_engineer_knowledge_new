#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简化的性能测试脚本，用于测试不同并发级别的性能表现
"""

import http.client
import json
import threading
import time
import random
import string

class SimplifiedPerfTest:
    def __init__(self, host="localhost", port=8090, total_requests=50):
        self.host = host
        self.port = port
        self.total_requests = total_requests
        self.results = []
        self.lock = threading.Lock()
        
        # 初始化测试数据
        self.passwd = "123456"
        self.test_img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    def _make_request(self, method, path, body=None):
        """发送HTTP请求并返回结果"""
        start_time = time.time()
        try:
            conn = http.client.HTTPConnection(self.host, self.port, timeout=10)
            headers = {"Content-Type": "application/json"}
            
            if body:
                body = json.dumps(body)
            
            conn.request(method, path, body, headers)
            response = conn.getresponse()
            response.read().decode()
            conn.close()
            
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # 毫秒
            return True, latency
        except Exception as e:
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # 毫秒
            return False, latency
    
    def _worker(self, test_func, requests_per_worker):
        """测试工作线程"""
        for _ in range(requests_per_worker):
            success, latency = test_func()
            with self.lock:
                self.results.append((success, latency))
    
    def run_test(self, test_name, concurrency):
        """运行单个测试"""
        self.results = []
        requests_per_worker = self.total_requests // concurrency
        threads = []
        
        start_time = time.time()
        
        # 创建并启动线程
        for _ in range(concurrency):
            if test_name == "device_info":
                def func():
                    return self._make_request("GET", f"/device/information?pass={self.passwd}")
            elif test_name == "create_person":
                def func():
                    person_id = "test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                    return self._make_request("POST", f"/person/create", {"pass": self.passwd, "person": {"id": person_id, "name": "Test"}})
            elif test_name == "main_flow":
                def func():
                    person_id = "test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                    face_id = "face_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
                    
                    # 创建人员
                    self._make_request("POST", f"/person/create", {"pass": self.passwd, "person": {"id": person_id, "name": "Test"}})
                    
                    # 创建照片
                    self._make_request("POST", f"/face/create", {"pass": self.passwd, "personId": person_id, "faceId": face_id, "imgBase64": self.test_img_base64})
                    
                    # 查询人员
                    self._make_request("GET", f"/person/find?id={person_id}&pass={self.passwd}")
                    
                    # 查询照片
                    self._make_request("POST", f"/face/find", {"pass": self.passwd, "personId": person_id})
                    
                    # 删除照片
                    self._make_request("POST", f"/face/delete", {"pass": self.passwd, "faceId": face_id})
                    
                    # 删除人员
                    return self._make_request("POST", f"/person/delete", {"pass": self.passwd, "id": person_id})
            
            thread = threading.Thread(target=self._worker, args=(func, requests_per_worker))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 统计结果
        success_count = sum(1 for success, _ in self.results if success)
        failure_count = self.total_requests - success_count
        
        if success_count > 0:
            avg_latency = sum(latency for success, latency in self.results if success) / success_count
            min_latency = min(latency for success, latency in self.results if success)
            max_latency = max(latency for success, latency in self.results if success)
        else:
            avg_latency = 0
            min_latency = 0
            max_latency = 0
        
        tps = self.total_requests / total_time
        
        return {
            "test_name": test_name,
            "concurrency": concurrency,
            "total_time": total_time,
            "success_count": success_count,
            "failure_count": failure_count,
            "avg_latency": avg_latency,
            "min_latency": min_latency,
            "max_latency": max_latency,
            "tps": tps
        }

if __name__ == "__main__":
    tester = SimplifiedPerfTest(total_requests=50)
    concurrency_levels = [50, 100, 200, 400, 600]
    test_names = ["device_info", "create_person", "main_flow"]
    
    print("=== 性能测试开始 ===")
    print(f"总请求数: {tester.total_requests}")
    print(f"并发级别: {concurrency_levels}")
    print("=" * 60)
    
    all_results = []
    
    for test_name in test_names:
        print(f"\n--- 测试 {test_name} ---")
        for concurrency in concurrency_levels:
            result = tester.run_test(test_name, concurrency)
            all_results.append(result)
            
            success_rate = (result['success_count'] / tester.total_requests) * 100
            print(f"  并发 {concurrency}: TPS={result['tps']:.2f}, 平均响应={result['avg_latency']:.2f}ms, 成功率={success_rate:.1f}%")
    
    # 打印汇总结果
    print("\n=== 性能测试汇总 ===")
    print(f"{'测试名称':<12} {'并发数':<8} {'TPS':<10} {'平均响应(ms)':<15} {'成功率':<10}")
    print("-" * 60)
    
    for result in all_results:
        success_rate = (result['success_count'] / tester.total_requests) * 100
        print(f"{result['test_name']:<12} {result['concurrency']:<8} {result['tps']:<10.2f} {result['avg_latency']:<15.2f} {success_rate:<10.1f}%")
    
    print("\n=== 性能测试完成 ===")
