import json

from sqlalchemy import *

import aspire.JSONHelper as JsonUtil
import aspire.utilLibrary as StrLib
from Common import Assert
from Common import Request
from Common import TestEnv
from Common.Getmysqldata import CheckDBdate
from Common.Utils import *
from Conf.Config import Config
from Params.params import readYml

SKIP_SIGN = -1
VERID = 0
REQID = 1
AUTHOR = 2
CASE_TITLE = 3
# = 4
METHOD = 5
API_URL = 6
HEADER = 7
REQUEST_DATA = 8
REQUEST_PARTDATA = 9
RESPONSE_CODE = 10
RESPONSE_ASSERT = 11
BEFORE_SQL = 12
AFTER_SQL = 13
CHECK_SQL = 14


class BaseCaseAbout():
    test = Assert.Assertions()

    def __init__(self, env='release'):
        """
        用例初始化
        """
        # self.exsql=CheckDBdate()
        self.env = env
        self.headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "head_orgAccount": "alauda",
            "head_userName": "alauda",
            "Authorization": "59PWo5VanZqS8XcQEBBoiH5PR7I3iEYAENK25YXjxGZeJbmx77mGoTdHo5fMToMN"}
        self.requestObject = None
        self.responseObject = None
        self.urlPath = None
        self.method = 'POST'
        self.urlhostAport = 'http://' + Config().get_conf(self.env, 'host') + ':' + \
                            Config().get_conf(self.env, 'hostport')
        self.api_url = None
        self.urlPathParams = None
        conf = Config()
        self.dbip = conf.get_conf(self.env, 'dbip')
        self.dbport = conf.get_conf(self.env, 'dbport')
        self.dbname = conf.get_conf(self.env, 'dbname')
        self.dbuser = conf.get_conf(self.env, 'dbuser')
        self.dbpw = conf.get_conf(self.env, 'dbpw')
        self.url = conf.get_conf(self.env, 'esurl')
        engines = "mysql+pymysql://" + self.dbuser + ":" + self.dbpw + \
                  "@" + self.dbip + "/" + self.dbname + "?charset=utf8"
        engine = create_engine(engines, max_overflow=5)
        self.conn = engine.connect()

    def clrequest(self, redata):
        # 处理请求参数
        req_yml_file = ''
        params_num_d = None  # 请求参数模板
        # a1=time.clock()
        if (len(redata) >= 0) and redata.__contains__("yml|"):
            # post
            ymlfile = str(redata).split("|")
            num = int(ymlfile[1])
            req_yml_file = ymlfile[0]
            data = readYml(req_yml_file)
            params_num_d = (data.data)[num]
            # isget = 0
        elif redata.startswith("requestO="):
            # ab1 = time.clock()
            params_num_d = json.loads(redata.lstrip('requestO='))
            # ab = time.clock()
        elif redata == "":
            params_num_d = ""
            # ac = time.clock()
        else:
            pass
        return req_yml_file, params_num_d

    def setApi_url(self, urlPath):
        if ((not isinstance(urlPath, str)) & (len(urlPath) == 0)):
            return
        urlPath = urlPath.replace('\n', '')
        urlPath = urlPath.replace('\t', '')
        self.urlPath = urlPath
        self.api_url = self.urlhostAport + self.urlPath
        MyLog.info("self.api_url" + self.api_url)

    def afterexeDB(self, exesql):
        if len(str(exesql).strip()) > 0:
            CheckDBdate().exsqlex(exesql, self.env, '数据后置处理')
        else:
            pass
        MyLog.info("self.exesql" + exesql)

    def exeDB(self, exesql):
        if len(str(exesql).strip()) > 0:
            CheckDBdate().exsqlex(exesql, self.env, '数据预置处理')
        else:
            pass
        MyLog.info("self.exesql" + exesql)

    def exeDB_param(self, exesql, param=None):
        if len(str(exesql).strip()) > 0:
            if param:
                CheckDBdate().exsqlex02(exesql, self.env, '数据预置处理', param)
            else:
                CheckDBdate().exsqlex02(exesql, self.env, '数据预置处理')
        else:
            pass
        MyLog.info("self.exesql" + exesql)

    def setApi_urlencode(self, urlPath):
        if ((not isinstance(urlPath, str)) & (len(urlPath) == 0)):
            return
        urlPath = urlPath.replace('\n', '')
        urlPath = urlPath.replace('\t', '')
        self.urlPath = urlPath
        self.api_url = self.urlhostAport + self.urlPath
        # self.api_url = self.urlhostAport + parse.quote(self.urlPath)
        MyLog.info("self.api_url" + self.api_url)

    def setApi_url_ocm(self, urlPath):
        if ((not isinstance(urlPath, str)) & (len(urlPath) == 0)):
            return
        urlPath = urlPath.replace('\n', '')
        urlPath = urlPath.replace('\t', '')
        # self.api_url = self.urlhostAport + self.urlPath
        self.api_url = urlPath
        MyLog.info("self.setApi_url_ocm" + self.api_url)

    def setHeaderByStr(self, headerjsonStr):
        if ((not isinstance(headerjsonStr, str)) & (len(headerjsonStr) == 0)):
            return
        headerjsonStr = headerjsonStr.replace('\n', '')
        headerjsonStr = headerjsonStr.replace('\t', '')
        if (isinstance(headerjsonStr, str) & (len(headerjsonStr) > 0)):
            hearderdata = json.loads(headerjsonStr)
            self.headers = hearderdata
            self.headers.setdefault('Authorization', '59PWo5VanZqS8XcQEBBoiH5PR7I3iEYAENK25YXjxGZeJbmx77mGoTdHo5fMToMN')
        else:
            pass

    def setMethod(self, method):
        if (method in ('GET', 'POST', 'UPLOAD', 'DELETE')):
            self.method = method

    def updateRequest(self, requstdata, requestpart):
        """
        :param requstdata:yml中的请求数据模板
        :param requestpart: 需要修改的数据key=v1|key2=v2
        :return:
        """

        if self.method == "POST":
            if requestpart == "":
                self.requestObject = json.dumps(requstdata)
            else:
                requstdata = eval(json.dumps(requstdata))
                paramefromexcel = (requestpart).split("|")
                for p in paramefromexcel:
                    kv = p.split("=")
                    key = (kv[0])
                    # value = eval(kv[1])
                    value = kv[1]
                    print(value)
                    requstdata[key] = value
                    self.requestObject = json.dumps(requstdata)

        else:
            # get请求 请求数据就是这样的  precinctId=01&siteType=4&isHomePage=true  precinctId=01&siteType=4&isHomePage=true
            # self.requestObject="?"+requstdata
            self.api_url += "?" + requstdata
        print("self.requstObject=============", self.requestObject)

    def updateRequest_value_to_json(self, requstdata, requestpart):
        """
        :param requstdata:yml中的请求数据模板
        :param requestpart: 需要修改的数据jsonpath=v1|jsonpath=v2
        :return:
        """
        if self.method == "POST":

            if requestpart == "":
                self.requestObject = json.dumps(requstdata)
                MyLog.info("requstObject_不替换" + str(self.requestObject))
                pass
            else:
                requstdata = eval(json.dumps(requstdata))
                paramefromexcel = (requestpart).split("|")
                for p in paramefromexcel:
                    kv = p.split("=")
                    keyjsonpath = (kv[0])
                    # value = eval(kv[1])
                    newvalue = kv[1]
                    self.requestObject = json.dumps(
                        JsonUtil.update_value_by_jsonpath(
                            requstdata, keyjsonpath, newvalue))
            MyLog.info("requstObject_POST" + str(self.requestObject))
        else:
            if self.method == "GET":
                # get请求 请求数据 precinctId=01&siteType=4&isHomePage=true  precinctId=01&siteType=4&isHomePage=true
                # self.requestObject="?"+requstdata
                if requstdata == "":
                    # 参数直接从url传递
                    print("self.api_url--->", self.api_url)
                else:
                    self.api_url += "?" + requstdata
            else:
                pass
        MyLog.info("case.requstObject" + str(self.requestObject))

    def sendData_upload(self, requestpart, action):
        self.responseObject = Request.Request(action).post_request_uploadfile_byprecinct(
            self.api_url, requestpart, headers=self.headers)

    def sendData(self, action):
        """
        :param action:
        :return: {'code': 200, 'body': {'status': '200', 'message': None, 'data': {'si}}}
        """
        print("case.requestObject", str(self.requestObject))
        if self.method == "POST":
            self.responseObject = Request.Request(action).post_request_data(
                self.api_url, self.requestObject, self.headers)
        elif self.method == "GET":
            self.responseObject = Request.Request(
                action).get_request(self.api_url, "", self.headers)
        repr_responseObject_str = str(self.responseObject)
        if len(repr_responseObject_str) > 4096:
            repr_responseObject_str = str(self.responseObject)[:4096] + ' ...'
        MyLog.info("case.responseObject" + repr_responseObject_str)

    def loadToken(self, tmp_path_factory, userName, hKey='token'):
        try:
            self.userName = userName
            root_tmp_dir = tmp_path_factory.getbasetemp().parent
            fn = str(root_tmp_dir / TestEnv.token)
            info = ""
            with open(fn, "r+") as file:
                info += file.readline()
                obj = json.loads(info)
            self.headers[hKey] = JsonUtil.get_value_from_json(
                obj, TestEnv.PAS_USER_PREFIX + userName)
        except BaseException:
            raise

    def deduplication(self, srcList):
        if isinstance(srcList, list):
            dstList = []
            for x in srcList:
                if x not in dstList:
                    dstList.append(x)
        else:
            return srcList

    def updateRequestBody(self, Params):
        if (Params is None):
            return

        if (not isinstance(Params, str)):
            MyLog.debug('%s' % ('请求参数不是字符串类型'))
            return

        if len(Params) == 0:
            return

        Params = Params.replace('\n', '')

        paramList = JsonUtil.match_test_rule_value(Params)

        kvList = []
        for param in paramList:
            if param.lower().startswith('(fileobj)'):
                dataInFile = ""
                import os
                filePath = os.path.join(
                    os.path.abspath(""),
                    "resoure",
                    param.lstrip('(fileobj)'))
                with open(filePath, encoding='utf-8') as rfile:
                    tData = rfile.readlines()
                for t in tData:
                    t = t.replace('\n', '')
                    t = t.replace('\t', '')
                    dataInFile = dataInFile + t

                josnStr = JsonUtil.eval_re_in_string(dataInFile)
                self.reqObject = json.loads(josnStr)
            else:
                kvList.append(param)

        self.reqObject = JsonUtil.upadate_values_to_json(
            self.reqObject, kvList)

        self.reqObject = JsonUtil.match_node_rule_value(self.reqObject)

    def updateUrlPathSuffix(self, suffix):
        if (isinstance(suffix, str)):
            self.urlPathSuffix = suffix

    def updateUrlPathParamByStr(self, params):
        if (isinstance(params, str)):
            kvParams = params.split("|")
            if (self.urlPathParams is None):
                self.urlPathParams = {}
            for p in kvParams:
                kvParam = p.split("=")
                self.urlPathParams[kvParam[0]
                ] = StrLib.dataPreprocessing(kvParam[1])

    def updateUrlPathParams(self, params):
        if (isinstance(params, (list, tuple))):
            for p in params:
                if (self.urlPathParams is None):
                    self.urlPathParams = params
                else:
                    self.urlPathParams = self.urlPathParams + "&" + p

        elif (isinstance(params, (dict))):
            for k in params:
                if (self.urlPathParams is None):
                    self.urlPathParams = k + '=' + params[k]
                else:
                    self.urlPathParams = self.urlPathParams + \
                                         "&" + k + '=' + params[k]

    def assertRespons_True(self, redata):
        assert self.responseObject['body'] == redata

    def assertRespons(self, redata):
        if len(str(redata)) > 0:
            sstrpathStr = str(redata).split("|")
            for kv in sstrpathStr:
                aa = kv.split("=")
                print("aa[0]", aa[0], "---aa[1]", aa[1])
                if str(aa[0]) == "repectRespons":
                    # repectRespons={"message":"成功","result":"成功","date":null,"status":"200","data":null}
                    repectrespons_data = JsonUtil.load_json_from_str(aa[1])
                    assert self.test.assert_json_same(
                        self.responseObject['body'], repectrespons_data)
                    # assert self.assert_isinstance_src_dst(self.responseObject['body'], repectrespons_data)
                    # assert self.test.assert_in_text(self.responseObject['body'], repectrespons_data)
                elif aa[0].__contains__("self."):
                    MyLog.info(aa[0])
                    MyLog.info(aa[1])
                    try:
                        str(eval(aa[0]))
                    except IndexError:
                        MyLog.error('eval表达式有误,aa[0]为 %s' % aa[0])
                        assert aa[0] == aa[1]
                    else:
                        assert str(eval(aa[0])) == str(aa[1])
                else:
                    reponsepathdata = JsonUtil.get_value_from_json(
                        self.responseObject['body'], str(aa[0]))
                    if aa[1] == "None":
                        assert reponsepathdata is None
                    else:
                        assert self.test.assert_text_str(
                            reponsepathdata, aa[1])
        else:
            pass

    def assertResultCode(self, path, expectedCode='200'):
        if (len(expectedCode) > 0):
            JsonUtil.assert_value_to_jsonObj(
                self.respObject, path, expectedCode)
            if expectedCode.lower().startswith('(float)'):
                expectedCode = expectedCode.lstrip('(float)')
            elif expectedCode.lower().startswith('(int)'):
                expectedCode = expectedCode.lstrip('(int)')
            elif expectedCode.lower().startswith('(bool)'):
                expectedCode = expectedCode.lstrip('(bool)')
            JsonUtil.assert_value_to_jsonObj(
                self.respObject, 'message', TestEnv.resultCode[expectedCode])

        MyLog.info('\n返回码校验通过')

    def assertRespByKV(self, path, expected):
        JsonUtil.assert_value_to_jsonObj(self.respObject, path, expected)
        MyLog.info('\n键值对校验通过，Key=%s, Value=%' % (path, expected))

    def assertRespByKVS(self, kvList):
        for kv in kvList:
            kvInfo = kv.split("=")
            JsonUtil.assert_value_to_jsonObj(
                self.respObject, kvInfo[0], kvInfo[1])
            MyLog.info('\n键值对校验通过，Key=%s, Value=%s' % (kvInfo[0], kvInfo[1]))

    def assertRespByStr(self, verifyStr):
        verifyStr = verifyStr.replace('\n', '')
        verifyStr = verifyStr.replace('\t', '')
        kvList = JsonUtil.match_test_rule_value(verifyStr)

        self.assertRespByKVS(kvList)

    def getPageSize(self, total, defaultPage=1, defaultRows=10):
        actualPage = defaultPage
        keyPage = 'page'
        if (isinstance(defaultPage, int)):
            actualPage = defaultPage
        elif (isinstance(defaultPage, str)):
            page = defaultPage.split("=")
            if (len(page) == 1):
                actualPage = int(defaultPage)
            else:
                actualPage = int(page[1])
                keyPage = page[0]

        try:
            rPage = JsonUtil.get_value_from_json(self.reqObject, keyPage)
            if isinstance(rPage, str):
                actualPage = int(rPage)
            else:
                actualPage = rPage
        except BaseException:
            MyLog.info('请求中没有页码信息，采用默认值')

        if (actualPage < 1):
            actualPage = 1

        actualRows = defaultRows
        keyRows = 'rows'
        if (isinstance(defaultRows, int)):
            actualRows = defaultRows
        elif (isinstance(defaultRows, str)):
            rows = defaultRows.split("=")
            if (len(page) == 1):
                actualRows = int(defaultRows)
            else:
                actualRows = int(rows[1])
                keyRows = rows[0]

        try:
            rRows = JsonUtil.get_value_from_json(self.reqObject, keyRows)
            if isinstance(rRows, str):
                actualRows = int(rRows)
            else:
                actualRows = rRows
        except BaseException:
            MyLog.info('请求中没有每页条数信息，采用默认值')

        if (actualRows < 0):
            actualRows = 10

        import math
        if actualPage <= 0:
            actualPage = 1
        else:
            totalPages = int(math.ceil(total / actualRows))
            if totalPages > 0:
                if actualPage < totalPages:
                    pass
                else:
                    actualPage = totalPages

            else:
                actualPage = 1

        offset = (actualPage - 1) * actualRows

        ifLimit = ' limit %s, %s' % (offset, actualRows)

        return ifLimit

    def getSortInfo(
            self,
            defaultSortName='sortName',
            defaultOrder='order',
            tableAlias=None):
        '''处理排序规则
        :defaultSortName：不包含“=”，则表示请求排序字段路径，找不到不排序；如包含“=”，则Key为请求中排序字段路径，value为默认排序字段
        :defaultOrder:不包含“=”，则表示请求中排序方式路径，找不到默认升序；如包含“=”，则Key为请求中排序方式路径，value为默认排序方式
        '''
        ifSort = None
        sortName = None
        if (isinstance(defaultSortName, str)):
            kvSort = defaultSortName.split('=')
            if (len(kvSort) == 1):  # 排序路径
                try:
                    sortName = JsonUtil.get_value_from_json(
                        self.reqObject, defaultSortName)
                except BaseException:
                    pass
            elif (len(kvSort) == 2):  # 设置默认排序字段
                try:
                    sortName = JsonUtil.get_value_from_json(
                        self.reqObject, kvSort[0])
                except BaseException:
                    sortName = kvSort[1]

        order = 'desc'
        if (isinstance(defaultOrder, str)):
            kvOrder = defaultOrder.split('=')
            if (len(kvOrder) == 1):  # 排序路径
                try:
                    order = JsonUtil.get_value_from_json(
                        self.reqObject, kvOrder[0])
                except BaseException:
                    pass
            elif (len(kvOrder) == 2):  # 设置默认排序字段
                try:
                    order = JsonUtil.get_value_from_json(
                        self.reqObject, kvOrder[0])
                except BaseException:
                    order = kvOrder[1]

        if (isinstance(sortName, str)):
            if (tableAlias is None):
                ifSort = ' order by %s %s' % (sortName, order)
            else:
                ifSort = ' order by %s.%s %s' % (tableAlias, sortName, order)

        return ifSort

    def whereByList(self, statement, ifList):
        if (not isinstance(ifList, list)):
            statement = statement + ";"
        elif (len(ifList) == 0):
            statement = statement + ";"
        else:
            statement = statement + " where " + ifList[0]
            for s in ifList[1:]:
                statement = statement + ' and ' + s
            statement = statement + ";"

        MyLog.info('组装后的SQL语句是：\n%s' % (statement))
        return statement

    def ListToString(self, src, splitChar=','):
        MyLog.info(src)
        if isinstance(src, str):
            return src

        if isinstance(src, (list, tuple)):
            if (len(src) >= 1):
                rValue = src[0]
                for val in src[1:]:
                    rValue = rValue + splitChar + str(val)
                return rValue
            else:
                return None


class BaseJsonBody4Req(object):
    '''
    : 通过封装的方式统一测试用例处理模式，从而减少代码编写工作量
    '''

    def __init__(self, reqSchema):
        '''
        Constructor
        '''
        self.reqJsonObject = JsonUtil.load_json_from_file(reqSchema)

    def getJsonStr(self):
        jsonStr = json.dumps(self.reqJsonObject)
        #         logger.info('\n请求内容是: %s' % jsonStr)
        return jsonStr

    def getJsonObj(self):
        #         logger.info('\n请求内容是: %s' % json.dumps(self.reqJsonObject))
        return self.reqJsonObject

    def setJsonObject(self, newReqPath):
        self.reqJsonObject = JsonUtil.load_json_from_file(newReqPath)

    def getValueByXPath(self, json_path):
        return JsonUtil.get_value_from_json(self.reqJsonObject, json_path)

    def updateByKVList(self, kvList):
        JsonUtil.upadate_values_to_json(self.reqJsonObject, kvList)

    def updateByKeyValue(self, path, value):
        JsonUtil.update_value_to_json(self.reqJsonObject, path, value)

    def preReqParams(self, reqParams):
        if (reqParams is None):
            return

        if (not isinstance(reqParams, str)):
            MyLog.debug('%s' % ('请求参数不是字符串类型'))
            return

        if len(reqParams) == 0:
            return

        reqParams = reqParams.replace('\n', '')

        paramList = JsonUtil.match_test_rule_value(reqParams)

        kvList = []
        for param in paramList:
            if param.lower().startswith('(fileobj)'):
                dataInFile = ""
                import os
                filePath = os.path.join(
                    os.path.abspath(""),
                    "resoure",
                    param.lstrip('(fileobj)'))
                with open(filePath, encoding='utf-8') as rfile:
                    tData = rfile.readlines()
                for t in tData:
                    t = t.replace('\n', '')
                    t = t.replace('\t', '')
                    dataInFile = dataInFile + t

                josnStr = JsonUtil.eval_re_in_string(dataInFile)
                self.reqJsonObject = json.loads(josnStr)
            else:
                kvList.append(param)

        self.reqJsonObject = JsonUtil.upadate_values_to_json(
            self.reqJsonObject, kvList)

        self.reqJsonObject = JsonUtil.match_node_rule_value(self.reqJsonObject)


class BaseHeaders(object):

    def __init__(self):
        self.headers = {
            "Content-Type": "application/json; charset=UTF-8"
        }

    def readToken(self, tmp_path_factory, UserName):
        try:
            root_tmp_dir = tmp_path_factory.getbasetemp().parent
            fn = str(root_tmp_dir / TestEnv.token)
            info = ""
            with open(fn, "r+") as file:
                info += file.readline()
                obj = json.loads(info)
            self.headers['Cookie'] = JsonUtil.get_value_from_json(
                obj, TestEnv.PAS_USER_PREFIX + UserName)
        except BaseException:
            raise

    def setKeyValue(self, k, v):
        self.headers[k] = v

    def getHeaderD(self):
        #         logger.info('请求头是：%s' % (self.headers))
        return self.headers

    def setHeaderByStr(self, params):
        if ((not isinstance(params, str)) & (len(params) == 0)):
            return
        params = params.replace('\n', '')
        params = params.replace('\t', '')
        headerList = JsonUtil.match_test_rule_value(params)
        for headerInfo in headerList:
            kv = headerInfo.split("=")
            self.headers[kv[0]] = kv[1]


class BaseJsonBody4Resp(object):

    def __init__(self, req=None, resp=None, userName=None):
        if (not isinstance(req, str)):
            self.reqJsonObj = None
        else:
            self.reqJsonObj = json.loads(req)

        if (not isinstance(resp, str)):
            self.respJsonObj = None
        else:
            self.respJsonObj = json.loads(resp)

        if (not isinstance(userName, str)):
            self.userName = None
        else:
            self.userName = userName

    def setResponse(self, resp):
        if (not isinstance(resp, str)):
            self.respJsonObj = None
        else:
            self.respJsonObj = json.loads(resp)

    def assertdefaultResultCode(self, expectedCode='200'):
        if (len(expectedCode) > 0):
            self.assertResultCode('status', expectedCode)

    def assertResultCode(self, path, expectedCode='200'):
        if (len(expectedCode) > 0):
            JsonUtil.assert_value_to_jsonObj(
                self.respJsonObj, path, expectedCode)
            if expectedCode.lower().startswith('(float)'):
                expectedCode = expectedCode.lstrip('(float)')
            elif expectedCode.lower().startswith('(int)'):
                expectedCode = expectedCode.lstrip('(int)')
            elif expectedCode.lower().startswith('(bool)'):
                expectedCode = expectedCode.lstrip('(bool)')
            JsonUtil.assert_value_to_jsonObj(
                self.respJsonObj, 'message', TestEnv.resultCode[expectedCode])

        MyLog.info('\n返回码校验通过')

    def assertRespByKV(self, path, expected):
        JsonUtil.assert_value_to_jsonObj(self.respJsonObj, path, expected)
        MyLog.info('\n键值对校验通过，Key=%s, Value=%' % (path, expected))

    def assertRespByKVS(self, kvList):
        for kv in kvList:
            kvInfo = kv.split("=")
            JsonUtil.assert_value_to_jsonObj(
                self.respJsonObj, kvInfo[0], kvInfo[1])
            MyLog.info('\n键值对校验通过，Key=%s, Value=%s' % (kvInfo[0], kvInfo[1]))

    def assertRespByStr(self, verifyStr):
        verifyStr = verifyStr.replace('\n', '')
        verifyStr = verifyStr.replace('\t', '')
        kvList = JsonUtil.match_test_rule_value(verifyStr)

        self.assertRespByKVS(kvList)
