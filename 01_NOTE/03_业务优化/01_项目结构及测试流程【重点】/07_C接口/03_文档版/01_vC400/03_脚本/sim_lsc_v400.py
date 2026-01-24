#!/usr/bin/env python
# -*- coding:utf8 -*-
"""
目的：模拟C接口3.5.1版本,实现下级LSC。cinterface的数据库配置和配置单文件需要配置为3.5版本。
分析：C接口分为2部分，一个是socket接口，还有一个是数据库接口；数据库接口可以直接采用中间库手工构造数据，但socket接口还是需要模拟
实现：采用tornado
备注：告警实时上报走的是数据库接口，所以socket上不用实现, 所以实际socket只用实现登录、登出、 心跳、获取实时数据
"""

import os, sys, struct, logging, random
import queue, signal
from logging.handlers import RotatingFileHandler

from tornado.tcpserver import TCPServer
from tornado import ioloop, gen, iostream
from tornado.ioloop import IOLoop
import tornado.web
import tornado.options

import config
import models400 as model

Header = 0x7E7C6B5A  # 报文开始包头标志 0x7E7C6B5A
SerialsNo = 1001  # 报文发送、应答过程中使用的序号，应答包的序号等于对应的发送包的序号

QUEUE_IN = queue.Queue()
QUEUE_OUT = queue.Queue()

is_closing = False
G_STREAM = None  # 注册后会只认这一个stream
ID, LSCID, NMAlarmID, Status, Description = 4859906, 1, 123, 1, "[0012345679	前置机中断	2008-05-20 11:04:23	021	0000.00.000	一级 开始	2]"

global G_Interface_List
is_realtimedata = 0  #是否能返回实时数据 1返回 0不返回
G_Interface_List = [
    {'name': 'LOGIN', 'id': 101, 'desc': '登录'},
    {'name': 'LOGIN_ACK', 'id': 102, 'desc': '登录响应'},
    {'name': 'LOGOUT', 'id': 103, 'desc': '登出'},
    {'name': 'LOGOUT_ACK', 'id': 104, 'desc': '登出响应'},

    {'name': 'SET_DYN_ACCESS_MODE', 'id': 401, 'desc': '设置实时数据的访问方式'},
    {'name': 'DYN_ACCESS_MODE_ACK', 'id': 402, 'desc': '返回访问方式及数据请求的结果'},

    {'name': 'SET_ALARM_MODE', 'id': 501, 'desc': '请求告警数据方式设置'},
    {'name': 'ALARM_MODE_ACK', 'id': 502, 'desc': '请求告警数据方式设置-返回设定成功与否'},
    {'name': 'SEND_ALARM', 'id': 503, 'desc': '实时告警发送'},
    {'name': 'SEND_ALARM_ACK', 'id': 504, 'desc': '实时告警发送确认'},
    {'name': 'SYNC_ALARM', 'id': 505, 'desc': '告警同步'},
    {'name': 'SYNC_ALARM_ACK', 'id': 506, 'desc': '告警同步确认'},
    {'name': 'SET_POINT', 'id': 1001, 'desc': '写数据请求'},
    {'name': 'SET_POINT_ACK', 'id': 1002, 'desc': '写数据响应'},

    {'name': 'MODIFY_PA', 'id': 1101, 'desc': '改口令请求'},
    {'name': 'MODIFY_PA_ACK', 'id': 1102, 'desc': '改口令响应'},

    {'name': 'HEART_BEAT', 'id': 1201, 'desc': '确认连接'},
    {'name': 'HEART_BEAT_ACK', 'id': 1202, 'desc': '回应连接'},

    {'name': 'TIME_CHECK', 'id': 1301, 'desc': '发送时钟消息'},
    {'name': 'TIME_CHECK_ACK', 'id': 1302, 'desc': '时钟同步响应'},
]



# ===============================================================================
# util functions
# ===============================================================================

def getNameByID(pkgid):
    '''从全局变量中，通过包PackageID返回PackageName
    '''
    global G_Interface_List
    a = [li for li in G_Interface_List if li['id'] == pkgid]
    if a == []:
        return None
    else:
        PackageName=a[0]['name']
        logger.info('[get PackageName ]\n%s' % PackageName)
        return PackageName


def getIDByName(pkgname):
    '''从全局变量中，通过包PackageName返回PackageID
    '''
    global G_Interface_List
    a = [li for li in G_Interface_List if li['name'] == pkgname]
    if a == []:
        return None
    else:
        return a[0]['id']


def getRespIDByReqID(reqid):
    return reqid + 1


# ===============================================================================
# Logger
# ===============================================================================
logger = logging.getLogger("sim_lsc")
formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s")
runtimelog = RotatingFileHandler("run.log", maxBytes=5 * 1024 * 1024, backupCount=3)
runtimelog.setFormatter(formatter)
logger.addHandler(runtimelog)
# 写屏功能，如不需要，则请注释下面三行
stdoutlog = logging.StreamHandler(sys.stdout)
stdoutlog.setFormatter(formatter)
logger.addHandler(stdoutlog)
logger.setLevel(logging.DEBUG)  # DEBUG, INFO, WARNING, ERROR, CRITICAL ...etc

class SocketServer(TCPServer):

    @gen.coroutine
    def handle_stream(self, stream, address):
        global QUEUE_IN, QUEUE_OUT, G_STREAM
        try:
            while True:
                G_STREAM = stream
                header = yield G_STREAM.read_bytes(16, partial=True) #每拿16个字节返回
                (self.Header, self.Length, self.SerialsNo, self.PK_Type) = struct.unpack('<llll', header)
                self.PK_Name = getNameByID(self.PK_Type)
                self.PK_Body = yield G_STREAM.read_bytes(self.Length - 16,
                                                         partial=True)  # PK_Body的内容，是不包含PK_Type的，即只包含Info和2位CRC
                logger.info('[orginal header]\n%s' % trans(header))
                logger.info('[orginal header]\n%s' % type(header))
                logger.debug(
                    '[unpack header]\n\tself.Header:%s\n\tself.Length:%s\n\tself.SerialsNo:%s\n\tself.PK_Type:%s -- [%s]' % \
                    (hex(self.Header), self.Length, self.SerialsNo, self.PK_Type, self.PK_Name))
                logger.info('[original body]\n%s' % trans(self.PK_Body))
                self.req_msg_name = getNameByID(self.PK_Type)
                yield self.sc_proxy(self.req_msg_name)
        except iostream.StreamClosedError:
            pass

    @gen.coroutine
    def sc_proxy(self, methodName):
        '''这一层的主要目的是进行proxy模式的分流，所有接口处理，均需要定义方法：on_接口请求包名()
        未实现的接口，直接关闭连接；
        这样处理的好处是，未来需要加入新的接口实现时，只需要增加方法: on_请求包名()
        '''
        # logger.info('sc_proxy' % self.PK_Type)
        # logger.info('sc_proxy' % self.Resp_PK_Type)
        # logger.info('sc_proxy' % self.PK_Body)

        try:
            logger.info('sc_proxy')
            getattr(self, "on_%s" % methodName)()
        except Exception:
            logger.error('未实现的接口，self.PK_Type=%s, 连接关闭！ ' % self.PK_Type)
            G_STREAM.close()

    @gen.coroutine
    def on_LOGIN(self):
        '''直接返回登录成功'''
        logger.info('on_LOGIN:%s')
        username, password, reqcrc = struct.unpack('<20s20sH', self.PK_Body)
        logger.info('登录请求, username=%s, password=%s' % (username, password))
        self.Resp_PK_Type = getIDByName('LOGIN_ACK')
        # self.Resp_Length = 16 + 4 + 2
        LOGIN_ACK_fmt = '<lllllH'
        self.Resp_Length = struct.calcsize(LOGIN_ACK_fmt)
        self.Resp_Info = config.EnumRightMode['LEVEL2']  # 返回权限给上级SC
        self.Resp_CRC16 = 0x00  # 目前未校验CRC
        logger.info('[LOGIN_ACK]回包,Resp_length:%s; SerialsNo:%s; Resp_PK_type:%s; Resp_Info:%s' % (
            self.Resp_Length, self.SerialsNo, self.Resp_PK_Type, self.Resp_Info))
        yield self.send_message(
            struct.pack(LOGIN_ACK_fmt, 0x7E7C6B5A, self.Resp_Length, self.SerialsNo, self.Resp_PK_Type, self.Resp_Info,
                        self.Resp_CRC16))

    @gen.coroutine
    def on_LOGOUT(self):
        '''
        :return: 退出登录成功，返回数据，关闭连接
        实际上对接动环的c接口，就没看到过这个请求
        '''
        self.Resp_PK_Type = getIDByName('LOGOUT_ACK')
        LOGOUT_ACK_fmt = '<llllH'
        self.Resp_Length = struct.calcsize(LOGOUT_ACK_fmt)
        self.Resp_Info = config.EnumResult['SUCCE']
        self.Resp_CRC16 = 0x00  # 目前未校验CRC
        logger.info('[LOGOUT_ACK]回包,Resp_length:%s; SerialsNo:%s; Resp_PK_type:%s; Resp_Info:%s' % (
            self.Resp_Length, self.SerialsNo, self.Resp_PK_Type, self.Resp_Info))
        yield self.send_message(
            struct.pack(LOGOUT_ACK_fmt, 0x7E7C6B5A, self.Resp_Length, self.SerialsNo, self.Resp_PK_Type, self.Resp_Info,
                        self.Resp_CRC16))
        logger.info("退出登录成功,关闭连接！")
        G_STREAM.close()

    @gen.coroutine
    def on_TIME_CHECK(self):
        '''
        5.1.10.7.时钟同步
        动环cservinfo表中的配置加上后，定期发起，每24小时；但目前还不能手工发起
        '''
        self.Resp_PK_Type = getIDByName('TIME_CHECK_ACK')
        TIME_CHECK_ACK_fmt = '<lllllH'
        self.Resp_Length = struct.calcsize(TIME_CHECK_ACK_fmt)
        self.Resp_Result = config.EnumResult['SUCCE']
        logger.info('[TIME_CHECK_ACK]回包,Resp_length:%s; SerialsNo:%s; Resp_PK_type:%s; Resp_Result:%s' % (
            self.Resp_Length, self.SerialsNo, self.Resp_PK_Type, self.Resp_Result))
        yield self.send_message(
            struct.pack(TIME_CHECK_ACK_fmt, 0x7E7C6B5A, self.Resp_Length, self.SerialsNo, self.Resp_PK_Type,
                        self.Resp_Result, 0x00))

    @gen.coroutine
    def on_HEART_BEAT(self):
        #5.1.10.6.确认连接的报文
        self.Resp_PK_Type = getIDByName('HEART_BEAT_ACK')
        HEART_BEAT_ACK_fmt = '<llllH'  #llll info是空不返回了。需要再返回空
        self.Resp_Length = struct.calcsize(HEART_BEAT_ACK_fmt)
        logger.info('[HEART_BEAT_ACK]回包,Resp_length:%s; SerialsNo:%s; Resp_PK_type:%s' % (
            self.Resp_Length, self.SerialsNo, self.Resp_PK_Type,))
        yield self.send_message(
            struct.pack('<llllH', 0x7E7C6B5A, self.Resp_Length, self.SerialsNo, self.Resp_PK_Type, 0x00))


    @gen.coroutine
    def on_SET_DYN_ACCESS_MODE(self):
        """
        #根据TID的数据类型判断，
        # 如果是站点类型，则判断SiteID,上送该站点下所有的设备的监控点信息，后续编号可以为空；
        # 如果是设备类型，则判断DeviceID，上送该设备下所有的监控点信息，后续编号可以为空；
        # 如果是监控点类型，则上送该点的信息，后续同类测点顺序号有效
        TID
        Type（EnumType）监控系统数据的种类-在集团C接口调试发现请求过来的TYPE是空的，就固定按照设备返回所有测点数据
        SiteID Char(SITEID_LEN)站点编号
        DeviceID Char(DEVICEID_LEN)设备编号
        SignalID Char(ID_LEN) 监控点编号
        SignalNumber Char(SIGNALNUM_LEN) 同类监控点顺序号
        """
        logger.info('处理实时数据on_SET_DYN_ACCESS_MODE')
        self.Resp_PK_Type = self.PK_Type + 1
        self.Resp_PK_Name = getNameByID(self.Resp_PK_Type)
        logger.info('[self.PK_Body]\n\t%s', type(self.PK_Body[:16]))
        #一个l:long 类型，即 64 位（8 字节）的有符号长整型
        (TerminalID, GroupID, Mode, PollingTime) = struct.unpack('<llll', self.PK_Body[:16])
        logger.info('T0erminalID, GroupID, Mode, PollingTime = %s, %s, %s, %s ' % (
            TerminalID, GroupID, Mode, PollingTime))
        Ids = self.PK_Body[16:-2]
        logger.debug('[original Ids]\n\t%s', Ids)
        logger.debug('[original type(Ids)]\n\t%s', type(Ids))
        logger.debug('[original  Ids-str]\n\t%s', str(Ids, encoding='utf-8'))
        tids_num = int(len(Ids) /(4+20+26+20+3))
        logger.debug('[len(Ids)]\n\t%s', tids_num)
        tid_list=[]
        for tid in  (struct.unpack('<' + tids_num * '73s', Ids)):
            tid_list.append(tid)
        logger.debug('[tid_list]\n\t%s', tid_list)
        for tiddata in tid_list:
            #'<'：表示使用小端字节序（little - endian）
            #4s20s26s20s3s：5个字段 s字节
            (Type,SiteID,DeviceID,SignalID,SignalNumber)=struct.unpack('<' + '4s20s26s20s3s', tiddata)
            logger.debug('[unpack tId-tidone=_]\n\t%s  %s %s %s %s', Type,SiteID,DeviceID,SignalID,SignalNumber)
            logger.debug('[unpack tId-tidone-DeviceID_]\n\t%s', str(DeviceID, encoding='utf-8'))
            logger.debug('[unpack tId-tidone-SiteID]\n\t%s ', str(SiteID, encoding='utf-8'))
            logger.debug('[unpack tId-tidone-Type_]\n\t%s ',str(Type, encoding='utf-8'))
            tidtype=str(Type, encoding='utf-8')
            siteid=str(SiteID, encoding='utf-8')
            deviceid=str(DeviceID, encoding='utf-8')
            # signalid=SignalID
            # signalnumber=SignalNumber
        tidtype = 6
        logger.debug('[unpack Info] [SET_DYN_ACCE_SC_MODE][%s]\n\tTerminalID:%s\n\tGroupID:%s\n\tMode:%s\n\tPollingTime:%s',
            self.PK_Name, TerminalID, GroupID, Mode, PollingTime)
        Result = 1
        signal_obj_list=[]
        datatypes=(1,2,3,4)
        signalid=0
        signalnumber=0
        is_realtimedata=1
        logger.debug('[unpack Ids-type(must in 5,6,7)]\n\t%s', tidtype)
        if tidtype == 5:
            signal_obj_list=model.query_signal_by_siteandtype(siteid,datatypes)
        elif tidtype == 6:
            signal_obj_list=model.query_signal_by_deviceidandtype(deviceid, datatypes)
        elif tidtype == 7:
            signal_obj_list=model.query_signal_by_signalidandnoandtype(deviceid,signalid,signalnumber,datatypes)
        else:
            logger.debug('[unpack Ids-tidtype not in  [5,6,7]  \n\t')
        signallen = len(signal_obj_list)
        SET_DYN_ACCE_SC_MODE_ACK_fmt = '<llllllll'
        args_listd = []
        for signal_obj in signal_obj_list:
            [SCID,SiteID,DeviceID,Type,SignalID,SignalNumber,SignalName,AlarmLevel,Threshold,StoragePeriod,AbsoluteVal,RelativeVal,StaticVal, NMAlarmID] = signal_obj
            logger.info('实时数据 [SignalNumber:%s]', SignalNumber)
            if Type in ['1', '4']:  # 对于数字量
                Value = 1
                SET_DYN_ACCE_SC_MODE_ACK_fmt += '20s26s20s3sli'
            else:
                # 模拟量中有整数或者小数 比如电压就是整数，温度就是小数，后续可再优化
                maxval = 50.333
                minval = 25.22
                Value = round(random.uniform(minval, maxval), 2)
                SET_DYN_ACCE_SC_MODE_ACK_fmt += '20s26s20s3sfi'
            logger.info("Value 字段类型类型1 long 数字量 %s", type(Value))
            Status=1
            logger.info('实时数据 [SiteID:%s, DeviceID:%s, SignalID:%s, SignalNumber:%s, Value:%s,  Status:%s]', SiteID, DeviceID, SignalID, SignalNumber, Value ,Status)
            logger.info([str(SiteID).encode('utf-8'), str(DeviceID).encode('utf-8'), str(SignalID).encode('utf-8'),str(SignalNumber).encode('utf-8'),Value, str('0').encode('utf-8')])
            SiteID_bytes=str(SiteID).encode('utf-8').ljust(20, b'\x00')
            DeviceID_bytes=str(DeviceID).encode('utf-8').ljust(26, b'\x00')
            SignalID_bytes=str(SignalID).encode('utf-8').ljust(26, b'\x00')
            SignalNumber_by = str(SignalNumber).encode('utf-8').ljust(3, b'\x00')
            SignalNumber_bytes = struct.pack('<3s', SignalNumber_by)
            args_listd+=([SiteID_bytes, DeviceID_bytes,SignalID_bytes,SignalNumber_bytes,Value,int(Status)])
        SET_DYN_ACCE_SC_MODE_ACK_fmt += 'l'  # 最后需要补一个H
        SET_DYN_ACCE_SC_MODE_ACK_fmt += 'H'  # 最后需要补一个H
        Cnt1=signallen #返回正确数据值得数量
        Cnt2=int(0) # 返回无效监控点ID的数量，如果返回0则所有数据有效，Values2为空
        Values1=args_listd
        logger.info("Values1Values1Values1Values1Values1Values1Values1Values1Values1Values1Values1Values1Values1 %s", Values1)
        args_list =  [SET_DYN_ACCE_SC_MODE_ACK_fmt, 0x7E7C6B5A, struct.calcsize(SET_DYN_ACCE_SC_MODE_ACK_fmt),
                      self.SerialsNo, self.Resp_PK_Type, TerminalID, GroupID, Result,Cnt1]+ Values1 +[Cnt2] + [0x00]
        # logger.info('args_list:%s', args_list)
        resp_body = struct.pack(args_list[0], *args_list[1:])
        yield self.send_message(resp_body)
        logger.info("实时数据回包信息: %s" % resp_body)



    @gen.coroutine
    def on_SEND_ALARM_ACK(self):
        '''直接发送告警，这个方法以后不再使用了，需要改'''
        logger.info('SEND_ALARM_ACK PK_Body:%s' % trans(self.PK_Body))
        pass


    @gen.coroutine
    def send_message(self, data):
        global QUEUE_OUT, G_STREAM
        QUEUE_OUT.put(data)
        # G_STREAM.write( data )


# 加认证
class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")


class LoginHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user", "admin", expires_days=0.0001)
        self.render("login.html")

    def post(self):
        user = self.get_argument("user")
        password = self.get_argument("password")
        if user == 'admin' and password == 'Dh@159_dev':
            self.set_secure_cookie("user", self.get_argument("user"), expires_days=1)
            self.redirect("/")
        else:
            self.redirect("/login")


class MainHandler(BaseHandler):
    '''机房列表'''

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        room_obj_list = model.queryRoom()
        logger.info('room_obj_list:%s' % room_obj_list)

        self.render("room.html", rooms=room_obj_list)


class DeviceListHandler(BaseHandler):
    '''设备列表'''

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        roomid = self.get_argument('roomid').strip()
        roomname = model.queryRoombyID(roomid).RoomName
        device_obj_list = model.queryDevice(roomid=roomid)
        self.render("device.html", devices=device_obj_list, roomname=roomname, roomid=roomid)


class SignalListHandler(BaseHandler):
    '''信号列表'''

    @tornado.web.authenticated
    @gen.coroutine
    def get(self):
        roomid = self.get_argument('roomid').strip()
        deviceid = self.get_argument('deviceid').strip()
        roomname = model.queryRoombyID(roomid).RoomName
        devicename = model.queryDevicebyID(deviceid).DeviceName
        signal_obj_list = model.query_signal_by_deviceid(deviceid=deviceid)
        self.render("signal.html", signals=signal_obj_list, roomname=roomname, roomid=roomid, deviceid=deviceid,
                    devicename=devicename)


class SendAlarmHandler(tornado.web.RequestHandler):
    """
    INSERT INTO `d_activealarm` (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `NMAlarmID`, `SerialNo`,
    `AlarmTime`, `AlarmLevel`, `AlarmStatus`, `AlarmDesc`, `AlarmValue`, `SynNo`, `AlarmRemark`)
    VALUES (140327, '1', '620402009', '40001', 4, '001001', '1', 'AB线电压过高告警', '001001', 140327, '2024-04-09 11:24:39', 4, 0, '下限告警-触发值169.5V', 500, 24545837, NULL);

    """
    @gen.coroutine
    def get(self):
        roomid = self.get_argument('roomid').strip()
        deviceid = self.get_argument('deviceid').strip()
        roomname = self.get_argument('roomname').strip()
        devicename = self.get_argument('devicename').strip()
        alarmflag = self.get_argument('alarmflag').strip()
        signalid = self.get_argument('signalid').strip()
        signalnumber = self.get_argument('signalnumber').strip()
        signal = model.query_signal_by_signalidandno(deviceid,signalid,signalnumber)
        # 如果是告警
        if alarmflag == '0':
            pass
            model.add_alert(roomid,deviceid,signal,alarmflag)
            self.redirect(r'/signals_list?roomid={}&deviceid={}'.format(roomid, deviceid))
        # 如果是2，则为消警
        else:
            pass
            model.cancel_alert(roomid,deviceid,signal,alarmflag=2)
            self.redirect(r'/signals_list?roomid={}&deviceid={}'.format(roomid, deviceid))



class sendValueHandler(tornado.web.RequestHandler):
    """

    """
    @gen.coroutine
    def get(self):
        ##roomid=20005&deviceid=42582&mete_code=001328&mete_value=
        roomid = self.get_argument('roomid').strip()
        deviceid = self.get_argument('deviceid').strip()
        # mete_code = self.get_argument('mete_code').strip()
        signalid = self.get_argument('signalid').strip()
        signalnumber = self.get_argument('signalnumber').strip()
        mete_value = self.get_argument('mete_value').strip()
        mete_value_min = self.get_argument('mete_value_min').strip()
        mete_value_max = self.get_argument('mete_value_max').strip()
        signal = model.query_signal_by_signalidandno(deviceid,signalid,signalnumber)
        print("写入的signal=",signal)
        model.addsignalh(signal,mete_value,mete_value_min,mete_value_max)
        self.redirect(r'/signals_list?roomid={}&deviceid={}'.format(roomid, deviceid))


####### tool functions， 用于tornado服务器接受ctrl+C的中止
def signal_handler(signum, frame):
    global is_closing
    is_closing = True


def try_exit():
    global is_closing
    if is_closing:
        tornado.ioloop.IOLoop.instance().stop()


httpserver = tornado.web.Application([
    (r"/login", LoginHandler),
    (r"/", MainHandler),
    (r"/device_list", DeviceListHandler),
    (r"/signals_list", SignalListHandler),
    (r"/send_alert", SendAlarmHandler),
    (r"/send_value", sendValueHandler),
    (r"/(.*)", MainHandler),
],
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    debug=True,
    autoreload=True,
    cookie_secret="61oETzKXQAGaYdghdhgfhfhfg",
    login_url="/login",
)


# def CRC16(s):
#    h='0'
#    for i in range(len(s)/2):
#        h=hex(int(h,16)+int(s[2*i:2*i+2],16))

#    h=h.replace('0x','')
#    if len(h)<=1:
#        h='00'+h
#    return h.upper()[-2:]

def CRC16(data):
    import binascii
    if type(data) != type(b'0'):
        data_bytes = data.encode('utf-8')
    else:
        data_bytes = data
    crc = binascii.crc_hqx(data_bytes, 0)
    crc_hex = hex(crc)[2:].upper()
    crc_hex = crc_hex.zfill(0)
    return crc_hex


def on_Q():
    global QUEUE_OUT, G_STREAM
    while QUEUE_OUT.qsize() > 0:
        # logger.info( 'Q_out not empty' )
        # item = QUEUE_OUT.get( block = False )
        item = QUEUE_OUT.get_nowait()
        logger.debug('Send Queue item:%s' % trans(item))
        # yield stream.write( item.encode('utf-8') )
        G_STREAM.write(item)


def trans(s):
    return "%s" % '-'.join('%.2x' % x for x in s)


# ===============================================================================
# main方法
# ===============================================================================
if __name__ == '__main__':
    tornado.options.parse_command_line()
    signal.signal(signal.SIGINT, signal_handler)

    socket_server = SocketServer()
    socket_server.listen(config.SOCKET_PORT)
    socket_server.start()
    httpserver.listen(config.HTTP_PORT)  # 暂时先关http，后续有空了再写页面触发告警和消警, 以及测点历史数据
    ioloop.PeriodicCallback(on_Q, 200).start()
    logger.info('\nSocket Interface Listening on Port : %s\nHTTP Server Listening on Port: %s' % (
        config.SOCKET_PORT, config.HTTP_PORT))
    IOLoop.instance().start()
