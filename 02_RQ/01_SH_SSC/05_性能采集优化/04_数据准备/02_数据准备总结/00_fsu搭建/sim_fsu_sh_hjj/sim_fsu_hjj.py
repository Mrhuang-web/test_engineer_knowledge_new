# -*- coding:utf-8 -*-
'''
sim_fsu_spyne.py返回时会有soapenv11的字样，可能被测系统无法识别
另外spyne中定义的xmlData一定会带上namespace,无法去掉。
因此，这里自定义soap信封
'''

import signal
import os, time
from lxml import etree

import tornado.ioloop
import tornado.web
import tornado.httpserver
import tornado.options
from tornado.concurrent import run_on_executor
from tornado import gen
from concurrent.futures import ThreadPoolExecutor

from control import invoke_proxy
from utils.logger import logger
import module
import client_action
import config
from utils import udpserver
is_closing = False


# 加认证
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class LoginHandler(BaseHandler):
    def get(self):
        # self.write('<html><body><form action="/login" method="post">'
        #           '<h5> user: <input type="text" name="user">'
        #           '<h5> password: <input type="password" name="password">'
        #           '<h5> <input type="submit" value="登录">'
        #           '</form></body></html>')
        self.set_secure_cookie("user", "admin", expires_days=0.0001)
        self.render("login.html")

    def post(self):
        user = self.get_argument("user")
        password = self.get_argument("password")
        if user == 'admin' and password == 'GXu8kp0*4az3Eg8emLM7':
            self.set_secure_cookie("user", self.get_argument("user"), expires_days=1)
            self.redirect("/")
        else:
            self.redirect("/login")


class MainHandler(BaseHandler):
    def get(self, wsdl):
        wsdl = open('./FSUService.wsdl', 'r+').read() % config.PORT
        self.set_header('content-type', 'text/xml; charset=utf-8')
        self.write(wsdl)

    def post(self):
        '''没有任何实现'''
        pass


class FSUHandler(BaseHandler):
    # @tornado.web.authenticated
    executor = ThreadPoolExecutor(20)

    # @gen.coroutine
    @run_on_executor
    def post(self, ):
        req_body = self.request.body
        logger.debug("req_body:%s" % req_body)
        root_et = etree.fromstring(req_body)
        namespaces = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
                      'fsus': 'http://FSUService.chinamobile.com'}
        et = etree.fromstring(root_et.xpath('//xmlData', namespaces=namespaces)[0].text.encode('utf-8'))
        pk_type = et.xpath('/Request/PK_Type/Name')[0].text
        # logger.info("et: %s" % et)
        logger.info('**************: %s' % pk_type)
        if pk_type == 'GET_DATA':
            import time
            # logger.info('***********: sleep 2')
            # time.sleep(5)
        response_data = invoke_proxy(et)
        response = add_soapenv_header(response_data)
        self.set_header('content-type', 'text/xml; charset=utf-8')
        self.write(response)
        # if not os.path.exists('./temp'):
        #    os.mkdir('./temp')
        # time_str = time.strftime('%Y%m%d_%H%M%S',time.localtime())
        # open(os.path.join('./temp','{}.{}.xml'.format(time_str,pk_type)),'w+').write(req_body.decode('utf-8'))
        # open(os.path.join('./temp','{}.{}.xml'.format(time_str,pk_type+'_ACK')),'w+').write(response)

    @gen.coroutine
    def get(self):
        wsdl = open('./FSUService.wsdl', 'r+').read() % config.PORT
        self.set_header('content-type', 'text/xml; charset=utf-8')
        self.write(wsdl)


def add_soapenv_header(xmldata):
    header = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
   <SOAP-ENV:Header/>
   <SOAP-ENV:Body SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
      <ns1:invokeResponse xmlns:ns1="http://FSUService.chinamobile.com">
         <invokeReturn><![CDATA['''
    tail = ''']]></invokeReturn>
      </ns1:invokeResponse>
   </SOAP-ENV:Body>
</SOAP-ENV:Envelope>'''
    resp = '{}{}{}'.format(header, xmldata, tail)
    logger.info('response:\n{}'.format(resp))
    return resp


# 创建视图类
class AlertFsuHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        fsu_obj_list = module.queryFsus()
        self.render("fsu.html", fsus=fsu_obj_list)


class AlertDeviceHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, fsuid):
        self.set_cookie('fsuid', fsuid, expires=time.time() + 900)
        devices = module.query_devices_by_fsu(fsuid)
        self.render("device.html", fsuid=fsuid, devices=devices)


class AlertDeviceSignalHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self, deviceid):
        # fsuid = self.get_cookie('fsuid')
        fsuid = self.get_argument('fsuid').strip()
        # self.set_cookie('deviceid', deviceid, expires=time.time()+900)
        signals = module.query_alert_signals_by_device(fsuid, deviceid, all_record=False)
        # fsuid = self.get_cookie('fsuid')
        self.render("signal.html", signals=signals, fsuid=fsuid, deviceid=deviceid)


class SendAlertHandler(BaseHandler):
    executor = ThreadPoolExecutor(20)  # 起线程池，由当前RequestHandler持有

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        fsuid = self.get_argument('fsuid').strip()
        deviceid = self.get_argument('deviceid').strip()
        signalid = self.get_argument('signalid').strip()
        alarmflag = self.get_argument('alarmflag').strip()
        signals = module.query_signals_by_device(fsuid, deviceid)
        # client_action.send_alarm(fsuid,deviceid,signalid,alarmflag)
        self.block_send_alarm(fsuid, deviceid, signalid, alarmflag)
        # self.render("signal.html", signals=signals, fsuid=fsuid, deviceid=deviceid)
        # self.redirect(r'/signal/{}'.format(deviceid)
        self.redirect(r'/signal/{}?fsuid={}'.format(deviceid, fsuid))

    @run_on_executor
    def block_send_alarm(self, fsuid, deviceid, signalid, alarmflag):
        client_action.send_alarm(fsuid, deviceid, signalid, alarmflag)


class SendLoginHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        fsuid = self.get_argument('fsuid').strip()
        client_action.send_login(fsuid)
        self.redirect(r'/fsu')


class SendDevConfHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        fsuid = self.get_argument('fsuid').strip()
        client_action.send_dev_conf(fsuid)
        self.redirect(r'/fsu')


class setMeteValueHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        config.METE_CODE = self.get_argument('mete_code').strip()
        config.METE_VALUE = self.get_argument('mete_value').strip()
        # self.redirect(r'.')
        self.render("set_mete_value.html", METE_CODE=config.METE_CODE, METE_VALUE=config.METE_VALUE)


class setMeteValuesHandler(BaseHandler):
    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        # 改成入库到fsu库，作为历史展示
        config.METE_CODE = self.get_argument('mete_code').strip()
        config.METE_VALUE = self.get_argument('mete_value').strip()
        deviceid = self.get_argument('deviceid').strip()
        fsuid = self.get_argument('fsuid').strip()
        mete_code = self.get_argument('mete_code').strip()
        # 將本次設置的metevalue 存儲到fsu庫
        module.updateSignal(fsuid, deviceid, signalsid=config.METE_CODE, measuredval=config.METE_VALUE)
        self.redirect(r'/signal/{}?fsuid={}'.format(deviceid, fsuid))
        signals1 = module.query_signalsid_list_by_metacode(fsuid, deviceid, mete_code)


class fsuUdpServer(udpserver.UDPServer):
    pass

####### tool functions， 用于tornado服务器接受ctrl+C的中止

def signal_handler(signum, frame):
    global is_closing
    is_closing = True


def try_exit():
    global is_closing
    if is_closing:
        tornado.ioloop.IOLoop.instance().stop()


#######################################################
# 路由配置，这是各种模拟器需要改的地方
#######################################################
sim_fsu = tornado.web.Application([
    (r"/login", LoginHandler),
    (r"/", AlertFsuHandler),
    (r"/services/FSUService", FSUHandler),
    (r"/fsu", AlertFsuHandler),
    (r"/device/(.*)", AlertDeviceHandler),
    (r"/signal/(.*)", AlertDeviceSignalHandler),
    (r"/send_alert", SendAlertHandler),
    (r"/send_dev_conf", SendDevConfHandler),
    (r"/send_login", SendLoginHandler),
    (r"/set", setMeteValueHandler),
    (r"/sets", setMeteValuesHandler),
    (r"/(.*)", MainHandler),
],
    # 项目配置信息
    # 网页模板
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    # 静态文件
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=False,
    autoreload=True,
    cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
    login_url="/login",
)

if __name__ == "__main__":
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)
    # http_server = tornado.httpserver.HTTPServer(sim_fsu)
    sim_fsu.listen(config.PORT)
    # http_server.bind(config.PORT,'0.0.0.0')
    # http_server.start(num_processes=1)
    tornado.ioloop.IOLoop.current().start()



# -*- coding:utf-8 -*-
# '''
# sim_fsu_spyne.py返回时会有soapenv11的字样，可能被测系统无法识别
# 另外spyne中定义的xmlData一定会带上namespace,无法去掉。
# 因此，这里自定义soap信封
# '''
#
# import signal
# import os, time
# from lxml import etree
#
# import tornado.ioloop
# import tornado.web
# import tornado.httpserver
# import tornado.options
# from tornado.concurrent import run_on_executor
# from tornado import gen
# from concurrent.futures import ThreadPoolExecutor
#
# from control import invoke_proxy
# from utils.logger import logger
# import module
# import client_action
# import config
# from utils import udpserver
#
# is_closing = False
#
#
# # 加认证
# class BaseHandler(tornado.web.RequestHandler):
#     def get_current_user(self):
#         return self.get_secure_cookie("user")
#
#
# class LoginHandler(BaseHandler):
#     def get(self):
#         # self.write('<html><body><form action="/login" method="post">'
#         #           '<h5> user: <input type="text" name="user">'
#         #           '<h5> password: <input type="password" name="password">'
#         #           '<h5> <input type="submit" value="登录">'
#         #           '</form></body></html>')
#         self.set_secure_cookie("user", "admin", expires_days=0.0001)
#         self.render("login.html")
#
#     def post(self):
#         user = self.get_argument("user")
#         password = self.get_argument("password")
#         if user == 'admin' and password == 'Dh@159_dev':
#             self.set_secure_cookie("user", self.get_argument("user"), expires_days=1)
#             self.redirect("/")
#         else:
#             self.redirect("/login")
#
#
# class MainHandler(BaseHandler):
#     def get(self, wsdl):
#         wsdl = open('./FSUService.wsdl', 'r+').read() % config.PORT
#         self.set_header('content-type', 'text/xml; charset=utf-8')
#         self.write(wsdl)
#
#     def post(self):
#         '''没有任何实现'''
#         pass
#
#
# class FSUHandler(BaseHandler):
#     # @tornado.web.authenticated
#     @gen.coroutine
#     def post(self, ):
#         req_body = self.request.body
#         logger.debug("req_body:%s" % req_body)
#         root_et = etree.fromstring(req_body)
#         namespaces = {'soapenv': 'http://schemas.xmlsoap.org/soap/envelope/',
#                       'fsus': 'http://FSUService.chinamobile.com'}
#         et = etree.fromstring(root_et.xpath('//xmlData', namespaces=namespaces)[0].text.encode('utf-8'))
#         pk_type = et.xpath('/Request/PK_Type/Name')[0].text
#         # logger.info("et: %s" % et)
#         response_data = invoke_proxy(et)
#         response = add_soapenv_header(response_data)
#         print("response:", response)
#         self.set_header('content-type', 'text/xml; charset=utf-8')
#         self.write(response)
#         # if not os.path.exists('./temp'):
#         #    os.mkdir('./temp')
#         # time_str = time.strftime('%Y%m%d_%H%M%S',time.localtime())
#         # open(os.path.join('./temp','{}.{}.xml'.format(time_str,pk_type)),'w+').write(req_body.decode('utf-8'))
#         # open(os.path.join('./temp','{}.{}.xml'.format(time_str,pk_type+'_ACK')),'w+').write(response)
#
#     @gen.coroutine
#     def get(self):
#         wsdl = open('./FSUService.wsdl', 'r+').read() % config.PORT
#         self.set_header('content-type', 'text/xml; charset=utf-8')
#         self.write(wsdl)
#
#
# def add_soapenv_header(xmldata):
#     header = '''<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
#    <SOAP-ENV:Header/>
#    <SOAP-ENV:Body SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
#       <ns1:invokeResponse xmlns:ns1="http://FSUService.chinamobile.com">
#          <invokeReturn><![CDATA['''
#     tail = ''']]></invokeReturn>
#       </ns1:invokeResponse>
#    </SOAP-ENV:Body>
# </SOAP-ENV:Envelope>'''
#     resp = '{}{}{}'.format(header, xmldata, tail)
#     logger.info('response:\n{}'.format(resp))
#     return resp
#
#
# # 创建视图类
# class AlertFsuHandler(BaseHandler):
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self):
#         fsu_obj_list = module.queryFsus()
#         self.render("fsu.html", fsus=fsu_obj_list)
#
#
# class AlertDeviceHandler(BaseHandler):
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self, fsuid):
#         self.set_cookie('fsuid', fsuid, expires=time.time() + 900)
#         devices = module.query_devices_by_fsu(fsuid)
#         self.render("device.html", fsuid=fsuid, devices=devices)
#
#
# class AlertDeviceSignalHandler(BaseHandler):
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self, deviceid):
#         # fsuid = self.get_cookie('fsuid')
#         fsuid = self.get_argument('fsuid').strip()
#         # self.set_cookie('deviceid', deviceid, expires=time.time()+900)
#         signals = module.query_alert_signals_by_device(fsuid, deviceid, all_record=False)
#         # fsuid = self.get_cookie('fsuid')
#         self.render("signal.html", signals=signals, fsuid=fsuid, deviceid=deviceid)
#
#
# class SendAlertHandler(BaseHandler):
#     executor = ThreadPoolExecutor(20)  # 起线程池，由当前RequestHandler持有
#
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self):
#         fsuid = self.get_argument('fsuid').strip()
#         deviceid = self.get_argument('deviceid').strip()
#         signalid = self.get_argument('signalid').strip()
#         alarmflag = self.get_argument('alarmflag').strip()
#         signals = module.query_signals_by_device(fsuid, deviceid)
#         # client_action.send_alarm(fsuid,deviceid,signalid,alarmflag)
#         self.block_send_alarm(fsuid, deviceid, signalid, alarmflag)
#         # self.render("signal.html", signals=signals, fsuid=fsuid, deviceid=deviceid)
#         # self.redirect(r'/signal/{}'.format(deviceid)
#         self.redirect(r'/signal/{}?fsuid={}'.format(deviceid, fsuid))
#
#     @run_on_executor
#     def block_send_alarm(self, fsuid, deviceid, signalid, alarmflag):
#         client_action.send_alarm(fsuid, deviceid, signalid, alarmflag)
#
#
# class SendLoginHandler(BaseHandler):
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self):
#         fsuid = self.get_argument('fsuid').strip()
#         client_action.send_login(fsuid)
#         self.redirect(r'/fsu')
#
#
# class SendDevConfHandler(BaseHandler):
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self):
#         fsuid = self.get_argument('fsuid').strip()
#         client_action.send_dev_conf(fsuid)
#         self.redirect(r'/fsu')
#
#
# class setMeteValueHandler(BaseHandler):
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self):
#         config.METE_CODE = self.get_argument('mete_code').strip()
#         config.METE_VALUE = self.get_argument('mete_value').strip()
#         # self.redirect(r'.')
#         self.render("set_mete_value.html", METE_CODE=config.METE_CODE, METE_VALUE=config.METE_VALUE)
#
#
# class setMeteValuesHandler(BaseHandler):
#     @tornado.web.authenticated
#     @gen.coroutine
#     def get(self):
#         # 改成入库到fsu库，作为历史展示
#         config.METE_CODE = self.get_argument('mete_code').strip()
#         config.METE_VALUE = self.get_argument('mete_value').strip()
#         deviceid = self.get_argument('deviceid').strip()
#         fsuid = self.get_argument('fsuid').strip()
#         mete_code = self.get_argument('mete_code').strip()
#         # 將本次設置的metevalue 存儲到fsu庫
#         module.updateSignal(fsuid, deviceid, signalsid=config.METE_CODE, measuredval=config.METE_VALUE)
#         self.redirect(r'/signal/{}?fsuid={}'.format(deviceid, fsuid))
#         signals1 = module.query_signalsid_list_by_metacode(fsuid, deviceid, mete_code)
#
#
# class fsuUdpServer(udpserver):
#
#     pass
#
# ####### tool functions， 用于tornado服务器接受ctrl+C的中止
#
# def signal_handler(signum, frame):
#     global is_closing
#     is_closing = True
#
#
# def try_exit():
#     global is_closing
#     if is_closing:
#         tornado.ioloop.IOLoop.instance().stop()
#
#
# #######################################################
# # 路由配置，这是各种模拟器需要改的地方
# #######################################################
# sim_fsu = tornado.web.Application([
#     (r"/login", LoginHandler),
#     (r"/", AlertFsuHandler),
#     (r"/services/FSUService", FSUHandler),
#     (r"/fsu", AlertFsuHandler),
#     (r"/device/(.*)", AlertDeviceHandler),
#     (r"/signal/(.*)", AlertDeviceSignalHandler),
#     (r"/send_alert", SendAlertHandler),
#     (r"/send_dev_conf", SendDevConfHandler),
#     (r"/send_login", SendLoginHandler),
#     (r"/set", setMeteValueHandler),
#     (r"/sets", setMeteValuesHandler),
#     (r"/(.*)", MainHandler),
# ],
#     # 项目配置信息
#     # 网页模板
#     template_path=os.path.join(os.path.dirname(__file__), "templates"),
#     # 静态文件
#     static_path=os.path.join(os.path.dirname(__file__), "static"),
#     debug=True,
#     autoreload=True,
#     cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
#     login_url="/login",
# )
#
# if __name__ == "__main__":
#     tornado.options.parse_command_line()
#     signal.signal(signal.SIGINT, signal_handler)
#     http_server = tornado.httpserver.HTTPServer(sim_fsu)
#     sim_fsu.listen(config.PORT)
#     http_server.bind(config.PORT,'0.0.0.0')
#     # http_server.start(num_processes=1)
#     tornado.ioloop.IOLoop.current().start()
