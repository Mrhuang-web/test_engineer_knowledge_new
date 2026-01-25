#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能测试脚本
使用Python内置库进行并发性能测试
"""

import http.client
import json
import threading
import time
import random
import string

class PerformanceTest:
    def __init__(self, host="localhost", port=8090, concurrency=10, total_requests=100):
        self.host = host
        self.port = port
        self.concurrency = concurrency
        self.total_requests = total_requests
        self.results = []
        self.lock = threading.Lock()
        
        # 初始化测试数据
        self.passwd = "123456"
        self.test_person_id = "test_perf_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        self.test_face_id = "test_face_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        
        # 模拟base64图片数据（简化版）
        self.test_img_base64 = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    
    def _make_request(self, method, path, body=None, headers=None):
        """发送HTTP请求并返回结果"""
        start_time = time.time()
        try:
            conn = http.client.HTTPConnection(self.host, self.port, timeout=10)
            
            if headers is None:
                headers = {
                    "Content-Type": "application/json"
                }
            
            if body:
                body = json.dumps(body)
            
            conn.request(method, path, body, headers)
            response = conn.getresponse()
            response_data = response.read().decode()
            response_json = json.loads(response_data)
            
            conn.close()
            
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # 毫秒
            
            return {
                "success": True,
                "status_code": response.status,
                "latency": latency,
                "path": path,
                "method": method
            }
        except Exception as e:
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # 毫秒
            
            return {
                "success": False,
                "status_code": 0,
                "latency": latency,
                "path": path,
                "method": method,
                "error": str(e)
            }
    
    def _worker(self, test_func, requests_per_worker):
        """测试工作线程"""
        for _ in range(requests_per_worker):
            result = test_func()
            with self.lock:
                self.results.append(result)
    
    def _run_test(self, test_func, name):
        """运行单个测试"""
        self.results = []
        requests_per_worker = self.total_requests // self.concurrency
        threads = []
        
        print(f"\n=== 开始测试 {name} ===")
        print(f"并发数: {self.concurrency}, 总请求数: {self.total_requests}")
        
        start_time = time.time()
        
        # 创建并启动线程
        for _ in range(self.concurrency):
            thread = threading.Thread(target=self._worker, args=(test_func, requests_per_worker))
            threads.append(thread)
            thread.start()
        
        # 等待所有线程完成
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # 统计结果
        success_count = sum(1 for r in self.results if r["success"])
        failure_count = self.total_requests - success_count
        avg_latency = sum(r["latency"] for r in self.results) / self.total_requests
        min_latency = min(r["latency"] for r in self.results)
        max_latency = max(r["latency"] for r in self.results)
        tps = self.total_requests / total_time
        
        # 打印结果
        print(f"=== 测试 {name} 结果 ===")
        print(f"总耗时: {total_time:.2f} 秒")
        print(f"成功请求: {success_count}")
        print(f"失败请求: {failure_count}")
        print(f"平均响应时间: {avg_latency:.2f} 毫秒")
        print(f"最小响应时间: {min_latency:.2f} 毫秒")
        print(f"最大响应时间: {max_latency:.2f} 毫秒")
        print(f"TPS: {tps:.2f}")
        print("=" * 50)
        
        return {
            "name": name,
            "total_time": total_time,
            "success_count": success_count,
            "failure_count": failure_count,
            "avg_latency": avg_latency,
            "min_latency": min_latency,
            "max_latency": max_latency,
            "tps": tps
        }
    
    # 测试用例
    def test_set_password(self):
        """测试设置密码接口"""
        def func():
            return self._make_request(
                "POST",
                f"/setPassWord",
                {"pass": self.passwd, "oldPass": self.passwd, "newPass": self.passwd}
            )
        return self._run_test(func, "设置密码接口")
    
    def test_get_device_info(self):
        """测试获取设备信息接口"""
        def func():
            return self._make_request(
                "GET",
                f"/device/information?pass={self.passwd}"
            )
        return self._run_test(func, "获取设备信息接口")
    
    def test_create_person(self):
        """测试创建人员接口"""
        def func():
            person_id = "test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            return self._make_request(
                "POST",
                f"/person/create",
                {"pass": self.passwd, "person": {"id": person_id, "name": "Test Person"}}
            )
        return self._run_test(func, "创建人员接口")
    
    def test_create_face(self):
        """测试创建照片接口"""
        def func():
            face_id = "test_face_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            person_id = "test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            # 先创建人员
            self._make_request(
                "POST",
                f"/person/create",
                {"pass": self.passwd, "person": {"id": person_id, "name": "Test Person"}}
            )
            return self._make_request(
                "POST",
                f"/face/create",
                {"pass": self.passwd, "personId": person_id, "faceId": face_id, "imgBase64": self.test_img_base64}
            )
        return self._run_test(func, "创建照片接口")
    
    def test_main_flow(self):
        """测试主流程接口"""
        def func():
            # 1. 创建人员
            person_id = "test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            self._make_request(
                "POST",
                f"/person/create",
                {"pass": self.passwd, "person": {"id": person_id, "name": "Test Person"}}
            )
            
            # 2. 创建照片
            face_id = "test_face_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            self._make_request(
                "POST",
                f"/face/create",
                {"pass": self.passwd, "personId": person_id, "faceId": face_id, "imgBase64": self.test_img_base64}
            )
            
            # 3. 查询人员
            self._make_request(
                "GET",
                f"/person/find?id={person_id}&pass={self.passwd}"
            )
            
            # 4. 查询照片
            self._make_request(
                "POST",
                f"/face/find",
                {"pass": self.passwd, "personId": person_id}
            )
            
            # 5. 删除照片
            self._make_request(
                "POST",
                f"/face/delete",
                {"pass": self.passwd, "faceId": face_id}
            )
            
            # 6. 删除人员
            result = self._make_request(
                "POST",
                f"/person/delete",
                {"pass": self.passwd, "id": person_id}
            )
            return result
        return self._run_test(func, "主流程接口")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=== 性能测试开始 ===")
        print(f"测试配置: 并发数={self.concurrency}, 总请求数={self.total_requests}")
        print("=" * 50)
        
        all_results = []
        
        # 测试主要接口
        all_results.append(self.test_get_device_info())
        all_results.append(self.test_create_person())
        all_results.append(self.test_create_face())
        
        # 测试主流程
        all_results.append(self.test_main_flow())
        
        # 打印汇总结果
        print("\n=== 性能测试汇总 ===")
        print(f"{'测试名称':<20} {'总耗时(秒)':<15} {'成功数':<10} {'失败数':<10} {'平均响应(ms)':<15} {'TPS':<10}")
        print("-" * 85)
        for result in all_results:
            print(f"{result['name']:<20} {result['total_time']:<15.2f} {result['success_count']:<10} {result['failure_count']:<10} {result['avg_latency']:<15.2f} {result['tps']:<10.2f}")
        
        print("\n=== 性能测试完成 ===")

if __name__ == "__main__":
    # 创建测试实例
    tester = PerformanceTest(
        host="localhost",
        port=8090,
        concurrency=10,
        total_requests=100
    )
    
    # 运行所有测试
    tester.run_all_tests()
