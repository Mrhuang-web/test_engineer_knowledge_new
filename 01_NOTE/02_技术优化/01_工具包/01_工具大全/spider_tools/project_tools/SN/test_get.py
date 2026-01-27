#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试GET请求（无body）的token生成
"""
import test

# 测试GET请求（无body）
print('GET请求测试结果:')
token = test.build_token('test_key', '')
print(f'Token: "{token}"')
print(f'Token长度: {len(token)}')

auth_header = test.build_auth_header('test_appid', 'test_key', '')
print(f'Authorization: {auth_header["Authorization"]}')

print('\n测试完成！')
