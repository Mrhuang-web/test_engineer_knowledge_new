#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多维度性能测试脚本
使用Python内置库进行不同并发级别的性能测试
"""

import http.client
import json
import threading
import time
import random
import string

class MultiConcurrencyTest:
    def __init__(self, host="localhost", port=8090, total_requests=100):
        self.host = host
        self.port = port
        self.total_requests = total_requests
        self.results = []
        self.lock = threading.Lock()
        
        # 初始化测试数据
        self.passwd = "123456"
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
    
    def _run_test(self, test_func, name, concurrency):
        """运行单个测试"""
        self.results = []
        requests_per_worker = self.total_requests // concurrency
        threads = []
        
        start_time = time.time()
        
        # 创建并启动线程
        for _ in range(concurrency):
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
        
        if success_count > 0:
            avg_latency = sum(r["latency"] for r in self.results if r["success"]) / success_count
            min_latency = min(r["latency"] for r in self.results if r["success"])
            max_latency = max(r["latency"] for r in self.results if r["success"])
        else:
            avg_latency = 0
            min_latency = 0
            max_latency = 0
        
        tps = self.total_requests / total_time
        
        return {
            "name": name,
            "concurrency": concurrency,
            "total_time": total_time,
            "success_count": success_count,
            "failure_count": failure_count,
            "avg_latency": avg_latency,
            "min_latency": min_latency,
            "max_latency": max_latency,
            "tps": tps
        }
    
    # 测试用例
    def test_get_device_info(self, concurrency):
        """测试获取设备信息接口"""
        def func():
            return self._make_request(
                "GET",
                f"/device/information?pass={self.passwd}"
            )
        return self._run_test(func, "获取设备信息接口", concurrency)
    
    def test_create_person(self, concurrency):
        """测试创建人员接口"""
        def func():
            person_id = "test_" + ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            return self._make_request(
                "POST",
                f"/person/create",
                {"pass": self.passwd, "person": {"id": person_id, "name": "Test Person"}}
            )
        return self._run_test(func, "创建人员接口", concurrency)
    
    def test_main_flow(self, concurrency):
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
        return self._run_test(func, "主流程接口", concurrency)
    
    def run_all_tests(self, concurrency_levels=[50, 100, 200, 400, 600]):
        """运行所有测试"""
        print("=== 多维度性能测试开始 ===")
        print(f"测试配置: 总请求数={self.total_requests}")
        print(f"并发级别: {concurrency_levels}")
        print("=" * 60)
        
        all_results = []
        
        for concurrency in concurrency_levels:
            print(f"\n--- 开始 {concurrency} 并发测试 ---")
            
            # 测试主要接口
            device_info_result = self.test_get_device_info(concurrency)
            all_results.append(device_info_result)
            
            create_person_result = self.test_create_person(concurrency)
            all_results.append(create_person_result)
            
            # 测试主流程
            main_flow_result = self.test_main_flow(concurrency)
            all_results.append(main_flow_result)
        
        # 打印详细结果
        print("\n=== 详细测试结果 ===")
        print(f"{'接口名称':<15} {'并发数':<8} {'总耗时(秒)':<12} {'成功数':<8} {'失败数':<8} {'平均响应(ms)':<15} {'TPS':<10} {'成功率':<8}")
        print("-" * 90)
        
        for result in all_results:
            success_rate = (result['success_count'] / self.total_requests) * 100
            print(f"{result['name']:<15} {result['concurrency']:<8} {result['total_time']:<12.2f} {result['success_count']:<8} {result['failure_count']:<8} {result['avg_latency']:<15.2f} {result['tps']:<10.2f} {success_rate:<8.1f}%")
        
        # 打印汇总结果
        print("\n=== 性能测试汇总 ===")
        print(f"{'并发数':<8} {'设备信息TPS':<15} {'创建人员TPS':<15} {'主流程TPS':<15} {'平均成功率':<15}")
        print("-" * 70)
        
        for concurrency in concurrency_levels:
            device_info_tps = next(r['tps'] for r in all_results if r['name'] == "获取设备信息接口" and r['concurrency'] == concurrency)
            create_person_tps = next(r['tps'] for r in all_results if r['name'] == "创建人员接口" and r['concurrency'] == concurrency)
            main_flow_tps = next(r['tps'] for r in all_results if r['name'] == "主流程接口" and r['concurrency'] == concurrency)
            
            concurrency_results = [r for r in all_results if r['concurrency'] == concurrency]
            total_success = sum(r['success_count'] for r in concurrency_results)
            total_requests = len(concurrency_results) * self.total_requests
            avg_success_rate = (total_success / total_requests) * 100
            
            print(f"{concurrency:<8} {device_info_tps:<15.2f} {create_person_tps:<15.2f} {main_flow_tps:<15.2f} {avg_success_rate:<15.1f}%")
        
        # 生成优化建议
        self._generate_optimization_suggestions(all_results)
        
        print("\n=== 多维度性能测试完成 ===")
    
    def _generate_optimization_suggestions(self, results):
        """生成优化建议"""
        print("\n=== 性能优化建议 ===")
        
        # 分析每个接口在不同并发下的表现
        interfaces = set(r['name'] for r in results)
        
        for interface in interfaces:
            interface_results = [r for r in results if r['name'] == interface]
            interface_results.sort(key=lambda x: x['concurrency'])
            
            # 检查是否有性能下降趋势
            has_performance_drop = False
            for i in range(1, len(interface_results)):
                # 如果TPS下降超过20%，则认为性能下降
                if interface_results[i]['tps'] < interface_results[i-1]['tps'] * 0.8:
                    has_performance_drop = True
                    break
            
            if has_performance_drop:
                print(f"1. {interface}: 在高并发下性能有所下降，建议优化相关代码")
        
        # 检查成功率
        for result in results:
            if result['failure_count'] > 0:
                print(f"2. {result['name']}在{result['concurrency']}并发下有{result['failure_count']}个失败请求，建议检查错误原因")
        
        # 检查响应时间
        for result in results:
            if result['avg_latency'] > 100:
                print(f"3. {result['name']}在{result['concurrency']}并发下平均响应时间为{result['avg_latency']:.2f}ms，建议优化")
        
        # 通用建议
        print("\n4. 通用优化建议：")
        print("   - 考虑使用多进程或异步IO提升并发处理能力")
        print("   - 优化数据存储结构，减少内存占用")
        print("   - 添加缓存机制，减少重复计算")
        print("   - 优化线程调度，减少上下文切换开销")
        print("   - 考虑使用更高效的HTTP服务器，如uvicorn或gunicorn")

if __name__ == "__main__":
    # 创建测试实例
    tester = MultiConcurrencyTest(
        host="localhost",
        port=8090,
        total_requests=100
    )
    
    # 运行不同并发级别的测试
    tester.run_all_tests(concurrency_levels=[50, 100, 200, 400, 600])
