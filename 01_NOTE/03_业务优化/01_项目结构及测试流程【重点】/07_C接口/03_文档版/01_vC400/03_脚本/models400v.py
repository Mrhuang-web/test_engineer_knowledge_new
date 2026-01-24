# coding: utf-8
from logging.handlers import RotatingFileHandler
import random
from sqlalchemy import CHAR, Column, DateTime, Float, Index, String, Table
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Float,create_engine, MetaData,PrimaryKeyConstraint,text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import cast
from sqlalchemy import Integer, DateTime, ForeignKey, Sequence,VARCHAR,FLOAT,BigInteger
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.pool import NullPool
from sqlalchemy import and_,or_
import os,sys, struct, logging, time, hashlib, threading,copy
from datetime import datetime, date, timedelta
import config
Base = declarative_base()
metadata = Base.metadata

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
# 初始化数据库连接:
engine = create_engine(config.MYSQL_CONN_STR, pool_recycle=3600, pool_size=5, pool_pre_ping=True, pool_timeout=5,
                       max_overflow=50, echo=False)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)
serialno=0

class ActiveAlarmSendRecord(Base):
    __tablename__ = 'active_alarm_send_record'

    Id = Column(BIGINT(20), primary_key=True, comment='涓婚敭鑷??')
    AlarmId = Column(BIGINT(20), unique=True, comment='瀹炴椂鍛婅?id')
    SCID = Column(String(20), comment='涓嬬骇SCID')
    SiteID = Column(String(20), comment='绔欑偣id')
    DeviceID = Column(String(20), comment='璁惧?id')
    Type = Column(INTEGER(11), comment='鏁版嵁绫诲瀷')
    SignalID = Column(String(20), comment='娴嬬偣缂栧彿')
    SignalNumber = Column(String(20), comment='娴嬬偣搴忓彿')
    SignalName = Column(String(200), comment='淇″彿鍚嶇О')
    NMAlarmID = Column(String(100), comment='缃戠?鍛婅?id')
    SerialNo = Column(BIGINT(20), comment='鍛婅?搴忓彿')
    AlarmTime = Column(DateTime, comment='鍛婅?鍙戠敓鏃堕棿')
    AlarmLevel = Column(INTEGER(11), comment='鍛婅?绛夌骇d')
    AlarmStatus = Column(INTEGER(20), comment='鍛婅?鐘舵? 0:寮??,1:纭??,2:缁撴潫')
    AlarmDesc = Column(String(200), comment='鍛婅?鍐呭?鎻忚堪')
    AlarmValue = Column(Float, comment='鍛婅?瑙﹀彂鍊')
    SynNo = Column(INTEGER(20), comment='鍛婅?娴佹按鍙')
    AlarmRemark = Column(String(200), comment='棰勭暀瀛楁?')
    rAlertId = Column(String(200), comment='宸ョ▼鏍囪瘑 缂虹渷涓?:闈炲伐绋嬬姸鎬?1:宸ョ▼鐘舵?')
    SendStatus = Column(INTEGER(11), comment='鍙戦?鐘舵? 0:鏈?彂閫?1:鍙戦?鎴愬姛,2:鍙戦?澶辫触,3:宸叉帴鏀')
    SendTime = Column(DateTime, comment='鍙戦?鏃堕棿')
    PacketSerialNo = Column(BIGINT(20), comment='鎶ユ枃搴忓彿')
    CreateTime = Column(DateTime, comment='鍏ュ簱鏃堕棿')
    RetryCount = Column(INTEGER(11), comment='閲嶈瘯娆℃暟')


class ActiveAlarmSerialno(Base):
    __tablename__ = 'active_alarm_serialno'

    serial_no = Column(BIGINT(20), primary_key=True)
    index_seq = Column(BIGINT(20), nullable=False)
    alert_id = Column(String(200), nullable=False, unique=True)


class AlarmRecordSendfail(Base):
    __tablename__ = 'alarm_record_sendfail'

    alert_id = Column(String(200), nullable=False)
    create_time = Column(DateTime)
    alert_status = Column(String(2))
    index_seq = Column(BIGINT(20), primary_key=True)
    last_retry = Column(DateTime)
    retry = Column(INTEGER(11))
    status = Column(String(2))
    alert_json = Column(String(10240))
    remark = Column(String(400))


class DActivealarm(Base):
    __tablename__ = 'd_activealarm'

    Id = Column(BIGINT(20), primary_key=True)
    SCID = Column(String(20))
    SiteID = Column(String(20))
    DeviceID = Column(String(20))
    Type = Column(INTEGER(11))
    SignalID = Column(String(20))
    SignalNumber = Column(String(20))
    SignalName = Column(String(200))
    NMAlarmID = Column(String(100))
    SerialNo = Column(BIGINT(20))
    AlarmTime = Column(DateTime)
    AlarmLevel = Column(INTEGER(11))
    AlarmStatus = Column(INTEGER(20))
    AlarmDesc = Column(String(2000))
    AlarmValue = Column(Float)
    SynNo = Column(INTEGER(20))
    AlarmRemark = Column(String(200))
    # LscInTime = Column(DateTime)
    # CscInTime = Column(DateTime)
    rAlertId = Column(String(200), index=True)


class DActivealarmDel(Base):
    __tablename__ = 'd_activealarm_del'

    delid = Column(INTEGER(11), primary_key=True)


class DSignalh(Base):
    __tablename__ = 'd_signalh'

    Id = Column(BIGINT(20), primary_key=True)
    SCID = Column(String(20))
    SiteID = Column(String(20))
    DeviceID = Column(String(20))
    Type = Column(INTEGER(11))
    SignalID = Column(String(20))
    SignalNumber = Column(String(20))
    Value = Column(Float(asdecimal=True))
    UpdateTime = Column(DateTime)
    SignalDesc = Column(String(200), comment='信号描述')


class GetpointFilterRule(Base):
    __tablename__ = 'getpoint_filter_rule'

    rule_type = Column(String(50), primary_key=True)
    rule_detail = Column(String(400), comment='规则详细')


class MArea(Base):
    __tablename__ = 'm_area'

    SCID = Column(String(50), nullable=False)
    AreaID = Column(BIGINT(20), primary_key=True)
    LastAreaID = Column(BIGINT(20))
    AreaName = Column(String(255))


class MDevice(Base):
    __tablename__ = 'm_device'

    SCID = Column(String(50))
    DeviceID = Column(BIGINT(50), primary_key=True)
    RoomID = Column(String(100))
    SiteID = Column(String(100))
    DeviceName = Column(String(255))
    DeviceDesc = Column(String(2000))
    DeviceType = Column(INTEGER(11))
    Productor = Column(String(255))
    Version = Column(String(255))
    BeginRunTime = Column(DateTime)
    DeviceModel = Column(String(255))
    LocateNeStatus = Column(INTEGER(11))
    ModelId = Column(String(100), comment='测点模板id')


class MIdRelate(Base):
    __tablename__ = 'm_id_relate'
    __table_args__ = (
        Index('idx_cid_type', 'cId', 'dataType'),
    )

    id = Column(BIGINT(20), primary_key=True)
    scId = Column(INTEGER(11), nullable=False)
    configId = Column(String(50), nullable=False, index=True, comment='配置管理主键')
    cId = Column(String(50), nullable=False, comment='中间库主键')
    dataType = Column(INTEGER(11))


class MRoom(Base):
    __tablename__ = 'm_room'

    SCID = Column(String(50))
    RoomID = Column(INTEGER(11), primary_key=True)
    SiteID = Column(String(100))
    RoomType = Column(TINYINT(4))
    RoomName = Column(String(255))
    RoomDesc = Column(String(2000))

# class MSignal(Base):
#     __tablename__ = 'm_signal'
#
#     SCID=Column('SCID', String(50))
#     SiteID=Column('SiteID', String(100)),
#     DeviceID=Column('DeviceID', String(50), index=True),
#     Type=Column('Type', INTEGER(11)),
#     SignalID=Column('SignalID', String(50)),
#     SignalNumber=Column('SignalNumber', String(50)),
#     SignalName=Column('SignalName', String(255)),
#     AlarmLevel=Column('AlarmLevel', INTEGER(11)),
#     Threshold=Column('Threshold', Float),
#     StoragePeriod=Column('StoragePeriod', Float),
#     AbsoluteVal=Column('AbsoluteVal', Float),
#     RelativeVal=Column('RelativeVal', Float),
#     StaticVal=Column('StaticVal', String(255)),
#     Describe=Column('Describe', String(2000)),
#     NMAlarmID=Column('NMAlarmID', String(255)),

t_m_signal = Table(
    'm_signal', metadata,
    Column('SCID', String(50)),
    Column('SiteID', String(100)),
    Column('DeviceID', String(50), index=True),
    Column('Type', INTEGER(11)),
    Column('SignalID', String(50)),
    Column('SignalNumber', String(50)),
    Column('SignalName', String(255)),
    Column('AlarmLevel', INTEGER(11)),
    Column('Threshold', Float),
    Column('StoragePeriod', Float),
    Column('AbsoluteVal', Float),
    Column('RelativeVal', Float),
    Column('StaticVal', String(255)),
    Column('Describe', String(2000)),
    Column('NMAlarmID', String(255)),
    Index('idx_siteid_deviceid', 'SCID', 'SiteID', 'DeviceID', 'SignalID')
)



class MSite(Base):
    __tablename__ = 'm_site'

    SCID = Column(String(50))
    SiteID = Column(INTEGER(11), primary_key=True)
    SiteName = Column(String(50))
    SiteDesc = Column(String(2000))
    Longitude = Column(Float(asdecimal=True))
    Latitude = Column(Float(asdecimal=True))
    NodeFeatures = Column(TINYINT(4))
    SiteType = Column(TINYINT(4))
    AreaId = Column(String(255))


class Nodemodify(Base):
    __tablename__ = 'nodemodify'

    Id = Column(BIGINT(20), primary_key=True)
    Type = Column(INTEGER(11))
    SiteID = Column(CHAR(255))
    DeviceID = Column(CHAR(255))
    SignalID = Column(CHAR(255))
    SignalNumber = Column(INTEGER(11))
    ModifyType = Column(INTEGER(11))
    ModifyTime = Column(DateTime)

#
# t_t_precinct_id_map = Table(
#     't_precinct_id_map', metadata,
#     Column('old_id', String(255), comment='旧ID'),
#     Column('new_id', String(255), comment='新ID'),
#     Column('precinct_name', String(1000), comment='站点名称')
# )



def queryDeviceMax():

    with engine.connect() as connection:
        cursor = connection.execute(text("SELECT  max(DeviceID) FROM  m_device" ))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def queryDevicecount(roomid):
    with engine.connect() as connection:
        cursor = connection.execute(text(
            "SELECT  count(*)  FROM    m_device where RoomID = {}".format(
                int(roomid))))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def queryMArea(sCID,areaID):
    result = session.query(MArea).filter_by(SCID=sCID,AreaID=areaID).first()
    session.rollback()
    return result

def queryMRoomfist(sCID,roomID,siteID):
    result = session.query(MRoom).filter_by(SCID=sCID,RoomID=roomID,SiteID=siteID).first()
    session.rollback()
    return result

def queryMSitefist(sCID,siteID):
    result = session.query(MSite).filter_by(SCID=sCID,SiteID=siteID).first()
    session.rollback()
    return result

def queryMSite(siteId):
    result = session.query(MSite.SiteID).order_by(SiteID=siteId).all()
    session.rollback()
    return result

def queryRoom(siteID="2005"):
    # result = session.query(MRoom).filter_by(SiteID=siteID).all()
    result = session.query(MRoom).all()
    # result = session.query(MRoom).filter_by(SiteID=siteID).first()
    session.rollback()
    return result


def queryRoombyID(roomID):
    result = session.query(MRoom).filter_by(RoomID=roomID).first()
    # result = session.query(MRoom).all()
    # result = session.query(MRoom).filter_by(SiteID=siteID).first()
    session.rollback()
    return result

def queryDevice(roomid):
    ##  "
    "select NodeId,AlarmDeviceType,NodeName from M_Device where NodeId >= {} and NodeId <= {} order by NodeId,AlarmDeviceType"
    # device_start_id = int(roomid) + 2048
    # device_end_id = int(roomid) + 524288
    with engine.connect() as connection:
        cursor = connection.execute(text(
            "SELECT  SCID,DeviceID,RoomID,SiteID,DeviceName,DeviceDesc,DeviceType,Productor,Version,BeginRunTime,DeviceModel,LocateNeStatus  FROM    m_device where RoomID = {}".format(
                int(roomid))))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def queryDevicebyID(deviceid):
    result = session.query(MDevice).filter_by(DeviceID=deviceid).first()
    session.rollback()
    return result

def query_signal_by_deviceid(deviceid):
    ''' '''
    sql = '''select SCID,SiteID,DeviceID,Type,SignalID,SignalNumber,SignalName,AlarmLevel,Threshold,StoragePeriod,AbsoluteVal,RelativeVal,StaticVal, NMAlarmID from m_signal where DeviceID = {}    order by AlarmLevel desc  '''
    with engine.connect() as connection:
        cursor = connection.execute(text(sql.format(deviceid)))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def query_signal_by_siteandtype(siteid,datatypes):
    ''' type 非告警 [1,2,3,4]      告警编码 [0]'''
    sql = '''select SCID,SiteID,DeviceID,Type,SignalID,SignalNumber,SignalName,AlarmLevel,Threshold,StoragePeriod,AbsoluteVal,RelativeVal,StaticVal, NMAlarmID from m_signal where SiteID = {}  and  Type in  {}  order by AlarmLevel desc  '''
    with engine.connect() as connection:
        cursor = connection.execute(text(sql.format(siteid,datatypes)))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result



def query_signal_by_deviceidandtype(deviceid,datatypes):
    ''' type 非告警 [1,2,3,4]      告警编码 [0]'''
    sql = '''select SCID,SiteID,DeviceID,Type,SignalID,SignalNumber,SignalName,AlarmLevel,Threshold,StoragePeriod,AbsoluteVal,RelativeVal,StaticVal, NMAlarmID from m_signal where DeviceID = {}  and  Type in  {}  order by AlarmLevel desc  '''
    with engine.connect() as connection:
        cursor = connection.execute(text(sql.format(deviceid,datatypes)))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result



def query_signal_by_signalidandnoandtype(deviceid,signalid,signalnumber,datatypes):
    ''' type 非告警 [1,2,3,4]      告警编码 [0]'''
    sql = '''select SCID,SiteID,DeviceID,Type,SignalID,SignalNumber,SignalName,AlarmLevel,Threshold,StoragePeriod,AbsoluteVal,RelativeVal,StaticVal, NMAlarmID from m_signal where DeviceID = {}  and  SignalID ={} and SignalNumber={} and  Type in  {}  order by AlarmLevel desc  '''
    with engine.connect() as connection:
        cursor = connection.execute(text(sql.format(deviceid,signalid,signalnumber,datatypes)))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def query_signal_by_signalidandno(deviceid,signalid,signalnumber):
    ''' '''
    # sql = '''select SCID,SiteID,DeviceID,Type,SignalID,SignalNumber,SignalName,AlarmLevel,Threshold,StoragePeriod,AbsoluteVal,RelativeVal,StaticVal, NMAlarmID from m_signal where DeviceID = {}   and  SignalID={}   '''
    # with engine.connect() as connection:
    #     cursor = connection.execute(text(sql.format(deviceid,signalid)))
    # result = cursor.fetchall()
    # cursor.close()
    # connection.close()
    # return result
    result = session.query(t_m_signal).filter_by(DeviceID=deviceid,SignalID=signalid,SignalNumber=signalnumber).first()
    session.rollback()
    return result



#
# def queryAlert(nodeid):
#     sql = '''select  Id,SCID,SiteID,DeviceID,Type,SignalID,SignalNumber,SignalName,NMAlarmID,SerialNo,AlarmTime,AlarmLevel,AlarmStatus,AlarmDesc,AlarmValue,SynNo,AlarmRemark  from d_activealarm where nodeid = {} and m_dic.`Describe` LIKE "%-%" ORDER BY signalid'''
#     with engine.connect() as connection:
#         cursor = connection.execute(text(sql.format(nodeid)))
#     result = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     return result


def  addsignalh(signal,mete_value,mete_value_min,mete_value_max):
    global  serialno
    with engine.connect() as connection:
        cursor = connection.execute(text('SELECT  MAX(Id)   FROM  d_signalh '))
    id = cursor.fetchone()[0]
    if serialno  is None:
        #告警表为空的时候
        serialno=id

    "signal--> SCID,SiteID,DeviceID,Type,SignalID,SignalNumber,SignalName,AlarmLevel,Threshold,StoragePeriod,AbsoluteVal,RelativeVal,StaticVal, NMAlarmID"
    "INSERT INTO `d_signalh` (`Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `Value`, `UpdateTime`, `SignalDesc`) VALUES (20206, '1', '2006', '42628', 2, '087309', '0', 26.6, '2024-05-25 15:50:56', NULL);"
    "查询中间库-signal--->     ('1', '2005', '42406', 4, '001001', '1', 'AB�ߵ�ѹ���߸澯', 4, 1.0, 1.0, 1.0, 1.0, None, 'A', '601-001-1-001001')"

    signalh_obj = DSignalh()
    signalh_obj.Id = serialno
    signalh_obj.SCID = signal[0]
    signalh_obj.SiteID = signal[1]
    signalh_obj.DeviceID = signal[2]
    signalh_obj.Type =  signal[3]
    signalh_obj.SignalID =  signal[4]
    signalh_obj.SignalNumber = signal[5]
    if  signalh_obj.Type in ['1', '4']:# 对于数字量
        signalh_obj.Value = '1'
    else:
        if  mete_value_min <= mete_value_max:
            maxval=mete_value_max
            minval=mete_value_min
            signalh_obj.Value = round(random.uniform(float(minval), float(maxval)), 8)
        else:
            signalh_obj.Value = mete_value
    signalh_obj.UpdateTime = datetime.now()
    signalh_obj.SignalDesc ="SignalDesc"
    logger.info("signalh_obj=")
    logger.info(signalh_obj.Value)
    logger.info(signalh_obj)
    session.add(signalh_obj)
    session.commit()


def add_alert(roomid,deviceid,signal,alarmflag=0):
    with engine.connect() as connection:
        cursor = connection.execute(text('SELECT MAX(id)+1 FROM d_activealarm'))
    alert_id = cursor.fetchone()[0]
    with engine.connect() as connection:
        cursor = connection.execute(text('SELECT MAX(SerialNo)+1 FROM d_activealarm'))
    serialno = cursor.fetchone()[0]
    if serialno  is None:
        #告警表为空的时候
        serialno=1001

    "signal--> SCID,SiteID,DeviceID,Type,SignalID,SignalNumber,SignalName,AlarmLevel,Threshold,StoragePeriod,AbsoluteVal,RelativeVal,StaticVal, NMAlarmID"
    "DActivealarm `Id`, `SCID`, `SiteID`, `DeviceID`, `Type`, `SignalID`, `SignalNumber`, `SignalName`, `NMAlarmID`, `SerialNo`, `AlarmTime`, `AlarmLevel`, `AlarmStatus`, `AlarmDesc`, `AlarmValue`, `SynNo`, `AlarmRemark`"

    "查询中间库-signal--->('1', '2005', '42406', 4, '001001', '1', 'AB�ߵ�ѹ���߸澯', 4, 1.0, 1.0, 1.0, 1.0, None, 'A', '601-001-1-001001')"

    alert_obj = DActivealarm()
    alert_obj.Id = alert_id
    alert_obj.SCID = signal[0]
    alert_obj.SiteID = signal[1]#signal.SiteID
    alert_obj.DeviceID = signal[2]#deviceid
    alert_obj.Type =  signal[3]# signal.Type
    alert_obj.SignalID =  signal[4]#signal.SignalID
    alert_obj.SignalNumber = signal[5]#signal.SignalNumber
    alert_obj.SignalName = signal[6]# signal.SignalName
    alert_obj.NMAlarmID = signal[4] #  signal[13]
    alert_obj.SerialNo =serialno   #消警要跟告警的一致
    alert_obj.AlarmTime =  datetime.now()
    alert_obj.AlarmLevel =  signal[7] #signal.AlarmLevel
    alert_obj.AlarmStatus = alarmflag
    alert_obj.AlarmDesc = "下限告警-触发值169.5V"
    alert_obj.AlarmValue =  "500"
    alert_obj.SynNo =  24545837
    alert_obj.AlarmRemark =None
    # alert_obj.LscInTime = datetime.now()
    # alert_obj.CscInTime = datetime.now()
    session.add(alert_obj)
    session.commit()


def cancel_alert(roomid,deviceid,signal,alarmflag=2):
    with engine.connect() as connection:
        cursor = connection.execute(text('SELECT MAX(id)+1 FROM d_activealarm'))
    alert_id = cursor.fetchone()[0]
    with engine.connect() as connection:
        cursor = connection.execute(text(
            'SELECT da.SerialNo    from d_activealarm da WHERE da.DeviceID={} AND da.SignalID={} AND da.SignalNumber={} AND da.AlarmStatus ={}  ORDER BY da.AlarmTime DESC    LIMIT 1'.format(
                deviceid,signal[4],signal[5],0)))
    serialno = cursor.fetchone()[0]
    if serialno == None:
        logger.error('not exists seriano')
        return

    alert_obj = DActivealarm()
    alert_obj.Id = alert_id
    alert_obj.SCID = signal[0]
    alert_obj.SiteID = signal[1]  # signal.SiteID
    alert_obj.DeviceID = signal[2]  # deviceid
    alert_obj.Type = signal[3]  # signal.Type
    alert_obj.SignalID = signal[4]  # signal.SignalID
    alert_obj.SignalNumber = signal[5]  # signal.SignalNumber
    alert_obj.SignalName = signal[6]  # signal.SignalName
    alert_obj.NMAlarmID =  signal[4]  # 601-006-1-006001   V版本接出只识别后六位006001；集团的接入是不需要这个字段的
    alert_obj.SerialNo = serialno  # 消警要跟告警的一直
    alert_obj.AlarmTime = datetime.now()
    alert_obj.AlarmLevel = signal[7]  # signal.AlarmLevel
    alert_obj.AlarmStatus = alarmflag
    alert_obj.AlarmDesc = "下限告警-触发值169.5V"
    alert_obj.AlarmValue = "500"
    alert_obj.SynNo = 24545837
    alert_obj.AlarmRemark = None
    # alert_obj.LscInTime = datetime.now()
    # alert_obj.CscInTime = datetime.now()
    session.add(alert_obj)
    session.commit()


def test():
    print(queryDevicebyID('42406'))
    pass

if __name__=="__main__":
    test()
