# -*- coding: utf-8 -*-
"""
@Time ： 2024/12/18 10:07
@Auth ： sunzhonghua
@File ：test02.py.py
@IDE ：PyCharm
"""
import time

import Showitems
from Showitems import pk_difference
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
import shutil

if __name__ == '__main__':
    """
    内蒙
    #现网环境当前的菜单,只需修改dcim_prod.json内容，即为接口响应/v1/roleOrganization/listRoleResourceTree
    Showitems.get_items('dcim_prod1.xlsx','dcim_prod.json')
    
    #测试环境当前的菜单,只需修改dcim_test.json内容，
    #从测试环境【角色列表-点击权限-/v1/roleOrganization/listRoleResourceTree】接口响应json数据
    
    Showitems.get_items('dcim_test.xlsx','dcim_test.json')
    pk_difference(file1="dcim_test.xlsx", file2="dcim_prod1.xlsx")
    
    dcim_prod.xlsx颜色标识如下
    绿色：测试环境和现网都存在的会标记绿色---一般升级后应该是一致的
    白色：没有颜色标识的是测试环境没有但是现网确有的---测试环境缺的菜单或者按钮
    红色：测试环境有但是现网不存在的---应该是新增或者修改的菜单或者按钮
    
    #贵州
    Showitems.get_items('gz_prod.xlsx','gz_prod.json')
    Showitems.get_items('gz_test.xlsx','gz_test.json')
    pk_difference(file1="gz_test.xlsx", file2="gz_prod.xlsx")
    
    #云南
    Showitems.get_items('yn_prod.xlsx', 'yn_prod.json')
    Showitems.get_items('yn_test.xlsx', 'yn_test.json')
    pk_difference(file1="yn_test.xlsx", file2="yn_prod.xlsx")
    
    Showitems.get_items('gx_prod.xlsx', 'gx_prod.json')
    Showitems.get_items('gx_test.xlsx', 'gx_test.json')
    pk_difference(file1="gx_test.xlsx", file2="gx_prod.xlsx")
    """
    Showitems.get_items(r'./XlsxFile/gx_prod.xlsx', r'./JsonFile/gx_prod.json')
    Showitems.get_items(r'./XlsxFile/gx_test.xlsx', r'./JsonFile/gx_test.json')
    # pk_difference(file1=r'./XlsxFile/gx_test.xlsx', file2=r'./XlsxFile/gx_prod.xlsx')
    pk_difference(file1=r'./XlsxFile/gx_test.xlsx', file2=r'./XlsxFile/gx_prod.xlsx')
