# -*- coding: utf-8 -*-
'''
Created on 2021-3-31
@author: xiecs
'''
import os

ServerConfig = {
    # "PasAddr": "http://10.12.3.79:28129",
    "PasAddr": "http://10.12.7.220:4908",
    "PasAddr_big_screen": "http://10.1.203.38:18580",
    "PasAddr_gd_northmanage": "http://10.1.203.121:28020",
    "db_pas": "host=10.1.4.177,port=2883,user=spider_test@dh,passwd=G$SGp!8L3O,db=spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",

    "PasAddr_sx": "http://10.1.203.120:8480/spider/web",  # "http://10.12.12.184:28129",
    "PasAddr_sx_energy": "http://10.1.203.120:8480/spider/web",  # "http://10.12.12.184:9988",
    "PasAddr_sx_report": "http://10.1.203.120:8480/spider/web",  # "http://10.12.12.184:8338",
    "PasAddr_sx_cabinet": "http://10.1.203.120:8480/spider/web",  # "http://10.12.12.184:9991",
    "PasAddr_sx_": "http://10.12.12.184:2345",
    "PasAddr_sx_external": "http://10.12.12.184:8806",
    # "PasAddr_external": "http://test.spider.composite.com:38982:28085",
    "PasAddr_external": "http://10.12.7.87:20854",  # external端口变化需要修改

    # nZ0qJ8kA1aI9
    "db_pas_sx": "host=10.12.12.186,port=3306,user=root,passwd=2oLYLnC-1*y7lub5hX$h,db=spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",
    "db_pas_sh": "host=10.1.203.120,port=3306,user=root,passwd=GPGAErA%ZkhMk59*jaD,db=sc-spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",
    "mpp_pas_jt": "host=10.1.4.114,port=9030,user=dh,passwd=1qaz!QAZ,db=dh,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",


    "WebBaseAddr": "ttp://10.12.70.60:0000",
    "PpsAddr": "http://10.12.7.120:18081",
    "MockAddr": "http://10.12.70.196:10080",
    "rsUrlPrefix": "http://183.233.87.197:12634",
    "previewUrl": "http://183.233.87.197:12634/mp_oms_portal/html/yxpt-h5/index.html?preview=1&pageId=%s",
    "previewUrl4Tmpl": "http://183.233.87.197:12634/mp_oms_portal/html/yxpt-h5/index.html?preview=1&templateId=%s",
    "redisNodes": {"host": "10.12.7.120", "port": "6399"},
    "redisPasswd": "Llyy_2021",

    # 云南连接配置
    "PasAddr_yunnan": "http://10.1.203.120:8580/spider/web",
    "db_pas_yunnan": "host=10.1.203.120,port=3306,user=root,passwd=GPGAErA%ZkhMk59*jaD,db=yn-spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",

    # 广西连接配置
    "PasAddr_guangxi": "http://10.1.203.120:8380/spider/web",
    "db_pas_guangxi": "host=10.12.12.186,port=3306,user=root,passwd=2oLYLnC-1*y7lub5hX$h,db=gx-spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",

    # 内蒙DCIM连接配置
    "PasAddr_dcim": "http://10.1.203.120:8980/spider/web",
    "db_pas_dcim": "host=10.12.12.186,port=3306,user=root,passwd=2oLYLnC-1*y7lub5hX$h,db=nmg_spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",

    # 贵州连接配置
    "PasAddr_guizhou": "http://10.1.203.120:8780/spider/web",
    "db_pas_guizhou": "host=10.1.203.120,port=3306,user=root,passwd=GPGAErA%ZkhMk59*jaD,db=gz-spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",

    # 广东连接配置
    "PasAddr_guangdong": "http://10.1.203.120:8680/spider/web",
    "db_pas_guangdong": "host=10.1.203.120,port=3306,user=root,passwd=GPGAErA%ZkhMk59*jaD,db=gd-spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",

    # 重庆sc连接配置
    "PasAddr_chongqing": "http://10.1.203.120:9080/spider/web",
    "db_pas_chongqing": "host=10.1.203.120,port=3306,user=root,passwd=GPGAErA%ZkhMk59*jaD,db=sc-spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",

    # 广东sc连接配置
    "PasAddr_guangdong_sc": "http://10.1.203.120:9080/spider/web",
    "db_pas_guangdong_sc": "host=10.1.203.120,port=3306,user=root,passwd=GPGAErA%ZkhMk59*jaD,db=sc-spider,charset=utf8,maxconnections=70,mincached=2,maxcached=100,maxshared=100,blocking=1,maxusage=100",

}

LogConfig = {
    "LOG_LEVEL": "INFO",
    "LOG_OPEN_MODE": "a",
    "PROJECT_LABEL": "OpsPaas",
    "LOG_FORMAT": "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"
}

# 登录用户 'webbas':"8GrZPxjT&",
# 测试用户 'autotest_high':高权限用户，有所有功能菜单
# 测试用户 'autotest_low': 垂直低权限用户，只有首页功能菜单
# 测试用户 'autotest_flat':水平低权限用户，只有部分市级数据权限
users = {
    "mpoms": "Mpoms_2021",
    "autotest_high": "GXu8kp0*4az3Eg8emLM7",
    "autotest_low": "GXu8kp0*4az3Eg8emLM7",
    "autotest_flat": "GXu8kp0*4az3Eg8emLM7",

}
# 集团测试账号
users_spider = {"zgyd_autotest_highquanxian": "GXu8kp0*4az3Eg8emLM7",
                "zgyd_autotest_lowquanxian": "GXu8kp0*4az3Eg8emLM7",
                "zgyd_auto_partziyuan_2": "GXu8kp0*4az3Eg8emLM7"}

apiUsers = {"13828825781": 'ATAPP001'}

token = 'tokeninfo.txt'

PAS_USER_PREFIX = 'USER'
API_USER_PREFIX = 'API'

exeFilter = ""
casePriority = "blocker"

appKey = '1qaz2wsx'

# amsadmin使用
SuccessCodeInProject = '200'
resultCode = {
    "200": "成功",
    "1": "系统内部错误",
    "010001": "页面创建失败",
    "000001": "请求参数{0}错误",
    "000002": "文件上传失败，状态码",
    "000003": "无权操作数据",
    "010004": "页面删除失败",
    "010007": "页面信息查询失败",
    "010008": "页面名称重复",
    "010002": "页面信息更新失败",
    "010003": "页面发布失败",
    "010101": "模板创建失败",
    "010102": "模板信息更新失败",
    "010104": "模板删除失败",
    "010103": "模板发布失败",
    "010105": "模板上下线失败",
    "010106": "模板信息查询失败",
    "010107": "模板名称重复",
    "010006": "页面上下线失败",
    "010201": "请求参数客群ID为空",
    "010202": "客群不存在",
    "010203": "客群存在重复记录",
    "010204": "客群已经删除，不能重复删除",
    "010206": "请求参数操作类型参数错误",
    "010207": "客群已经删除，不能上线",
    "010208": "客群已经删除，不能下线",
    "010209": "客群已经是上线状态，不能重复上线",
    "010210": "客群已经是下线状态，不能重复下线",
    "010212": "请求参数客群名称为空",
    "010213": "请求参数失效时间为空",
    "010214": "请求参数客群类型为空",
    "010215": "实例不存在或无权限查看",
    "010215": "实例不存在或无权限查看",
    "010216": "请求参数客群策略表达式为空",
    "010217": "请求参数各策略实例间的关系为空",
    "010223": "请求参数生效时间格式有误",
    "010205": "请求参数操作类型为空",
    "090001": "弹窗名字重复",
    "090003": "state枚举值参数错误",
    "090006": "弹窗已删除,无法修改",
    "401": "Full authentication is required to access this resource"
}

# Platform使用，开发规范性差，不同的模块规范不一
SuccessCode4PlatForm = '0'
Code4PlatForm = {
    "0": "成功",
    "1": "系统内部错误",
    "5": "ERROR_SIGN_INVALID",
    "9": "通用请求参数错误",
    "002001": "页面不存在",
    "000001": "请求参数错误",
    "002002": " 页面未上线",
    "002003": "该版本不是发布版本",
    "080014": "未中奖",
    "080001": "指定活动不存在",
    "002005": "策略校验不通过，无订购权限",
    "002007": "产品不存在",
    "101001": "业务平台返回订购失败消息",
}


def load_all_scripts(prefix, root):
    '''
    迭代搜索指定目录及其子目录下的所有jar文件，使用时不见从根目录开始遍历，要修改
    '''
    lpath = []
    file_list = os.listdir(os.path.abspath(root))
    for file in file_list:
        path = os.path.join(os.path.abspath(root), file)
        if os.path.isdir(path):
            #             lpath.extend(load_all_jars(prefix, path))
            pass
        else:
            if path.endswith('.py'):
                print('pytest -v ' + root + '\\' + file)
    #                 lpath.append('pytest -v '+prefix + file)

    return lpath


#
# if __name__ == '__main__':
#     print(os.getcwd())
#     lpath = load_all_scripts('', 'testcase\\knowledge')
#     lpath = load_all_scripts('', 'testcase\\ops')

#     conn_obj = MySQLHelper(ServerConfig['db_pas'])
#     aspbatis.generate_table_req_mapper(conn_obj, 'mp_strategy_usergroup,mp_strategy_instance')

if __name__ == '__main__':
    print(os.getcwd())
    lpath = load_all_scripts('', 'testcase\\knowledge')
    lpath = load_all_scripts('', 'testcase\\ops')

#     conn_obj = MySQLHelper(ServerConfig['db_pas'])
#     aspbatis.generate_table_req_mapper(conn_obj, 'mp_strategy_usergroup,mp_strategy_instance')
