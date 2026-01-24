#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能测试脚本
使用Python内置库进行并发性能测试（优化版）
"""

import http.client
import json
import threading
import time
import random
import string
import argparse

class PerformanceTest:
    def __init__(self, host="localhost", port=8093, concurrency=10, total_requests=100):
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
        """发送HTTP请求并返回结果（优化版，减少内存分配）"""
        start_time = time.time()
        conn = None
        try:
            conn = http.client.HTTPConnection(self.host, self.port, timeout=5)
            
            if headers is None:
                headers = {
                    "Content-Type": "application/json"
                }
            
            if body:
                body = json.dumps(body, separators=(',', ':'), ensure_ascii=False)
            
            conn.request(method, path, body, headers)
            response = conn.getresponse()
            response_data = response.read().decode()
            
            end_time = time.time()
            latency = (end_time - start_time) * 1000  # 毫秒
            
            # 简化响应处理，只检查状态码
            success = 200 <= response.status < 300
            
            return {
                "success": success,
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
        finally:
            if conn:
                conn.close()
    
    def _worker(self, test_func, requests_per_worker):
        """测试工作线程（优化版，减少锁竞争）"""
        local_results = []
        for _ in range(requests_per_worker):
            result = test_func()
            local_results.append(result)
        
        with self.lock:
            self.results.extend(local_results)
    
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
    def test_get_device_info(self):
        """测试获取设备信息接口（优化版，减少内存分配）"""
        url = f"/device/information?pass={self.passwd}"
        def func():
            return self._make_request("GET", url)
        return self._run_test(func, "获取设备信息接口")
    
    def test_create_person(self):
        """测试创建人员接口（优化版，减少内存分配）"""
        def func():
            person_id = "test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            body = {
                "pass": self.passwd,
                "person": {
                    "id": person_id,
                    "name": "Test Person"
                }
            }
            return self._make_request("POST", "/person/create", body)
        return self._run_test(func, "创建人员接口")
    
    def run_all_tests(self):
        """运行所有测试"""
        print("=== 性能测试开始 ===")
        print(f"测试配置: 并发数={self.concurrency}, 总请求数={self.total_requests}")
        print("=" * 50)
        
        all_results = []
        
        # 只测试核心接口，减少测试时间
        all_results.append(self.test_get_device_info())
        all_results.append(self.test_create_person())
        
        # 打印汇总结果
        print("\n=== 性能测试汇总 ===")
        print(f"{'测试名称':<20} {'总耗时(秒)':<15} {'成功数':<10} {'失败数':<10} {'平均响应(ms)':<15} {'TPS':<10}")
        print("-" * 85)
        for result in all_results:
            print(f"{result['name']:<20} {result['total_time']:<15.2f} {result['success_count']:<10} {result['failure_count']:<10} {result['avg_latency']:<15.2f} {result['tps']:<10.2f}")
        
        print("\n=== 性能测试完成 ===")

if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description="性能测试脚本")
    parser.add_argument("--host", default="localhost", help="测试目标主机")
    parser.add_argument("--port", type=int, default=8093, help="测试目标端口")
    parser.add_argument("--concurrency", type=int, default=10, help="并发数")
    parser.add_argument("--total-requests", type=int, default=100, help="总请求数")
    args = parser.parse_args()
    
    # 创建测试实例
    tester = PerformanceTest(
        host=args.host,
        port=args.port,
        concurrency=args.concurrency,
        total_requests=args.total_requests
    )
    
    # 运行所有测试
    tester.run_all_tests()
