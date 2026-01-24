#-*- coding:utf-8 -*-
import time
import requests
from lxml import etree
from utils.logger import logger
import module
import config

def send_dev_conf(fsuid):
    root = etree.Element('Request')
    pk_type = etree.SubElement(root, 'PK_Type')
    info = etree.SubElement(root, 'Info')
    name_ = etree.SubElement(pk_type, 'Name')
    name_.text = 'SEND_DEV_CONF_DATA'
    fsuid_et = etree.SubElement(info, 'FSUID')
    values_et = etree.SubElement(info, 'Values')
    fsuid_et.text = fsuid.encode('utf-8')

    devices = module.query_devices_by_fsu(fsuid)
    for device in devices:
        device_et = etree.SubElement(values_et, 'Device')
        device_et.set('DeviceID', device.deviceid or '')
        device_et.set('DeviceName', device.devicename or '')
        #logger.info(type(device.devicename))
        #logger.info(device.devicename)
        device_et.set('SiteID', device.siteid or '')
        device_et.set('SiteName', device.sitename or '')
        device_et.set('RoomName', device.roomname or '')
        device_et.set('DeviceType', device.devicetype or '')
        device_et.set('DeviceSubType', device.devicesubtype or '')
        device_et.set('Model', device.model or '')
        device_et.set('Brand', device.brand or '')
        device_et.set('RatedCapacity', device.ratedcapacity or '')
        device_et.set('Version', device.version or '')
        device_et.set('BeginRunTime', device.beginruntime or '')
        device_et.set('DevDescribe', device.devdescribe or '')
        device_et.set('ConfRemark', device.confremark or '')
        signals = module.query_signals_by_device(fsuid,device.deviceid,all_record=True)
        sgl_count = len(signals or '')
        signals_et = etree.SubElement(device_et, 'Signals')
        signals_et.set('Count', str(sgl_count))
        for signal in signals:
            signal_et = etree.SubElement(signals_et, 'Signal')
            signal_et.set('Type', signal.type or '')
            signal_et.set('ID', signal.signalsid or '')
            signal_et.set('SignalName', signal.signalname or '')
            signal_et.set('SignalNumber', signal.signalnumber or '')
            signal_et.set('AlarmLevel', signal.alarmlevel or '')
            signal_et.set('threshold', signal.threshold or '')
            signal_et.set('NMAlarmID', signal.nmalarmid or '')

    send_dev_conf_content = etree.tostring(root, xml_declaration=True, encoding='utf-8', pretty_print=True)
    send_dev_conf_content = send_dev_conf_content.decode('utf-8')
    data =  '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:lsc="http://LSCService.chinamobile.com">
   <soapenv:Header/>
   <soapenv:Body>
      <lsc:invoke>
         <!--Optional:-->
         <xmlData><![CDATA[%s]]></xmlData>
      </lsc:invoke>
   </soapenv:Body>
</soapenv:Envelope>''' % send_dev_conf_content
    logger.info('上报动环设备的配置数据，请求包为:\n%s' % data)
    #open('c:/send_dev_conf_content.xml','w+').write(send_dev_conf_content)
    r = requests.post(config.G_B_INF_WSDL,data.encode('utf-8'))
    response = r.text
    logger.info(u'上报动环设备的配置数据，返回包为:\n%s' % response)

####### FSU注册上报
def send_login(fsuid):
    fsu_obj = module.queryFsu(fsuid)
    login_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>LOGIN</Name>
    </PK_Type>
    <Info>
        <UserName>%s</UserName>
        <PassWord>%s</PassWord>
        <FSUID>%s</FSUID>
        <FSUIP>%s</FSUIP>
        <FSUMAC>%s</FSUMAC>
        <FSUVER>%s</FSUVER>
    </Info>
</Request>''' % (
            fsu_obj.username,
            fsu_obj.password,
            fsu_obj.fsuid,
            fsu_obj.fsuip,
            fsu_obj.fsumac,
            fsu_obj.fsuver
   
)
    data = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:lsc="http://LSCService.chinamobile.com">
   <soapenv:Header/>
   <soapenv:Body>
      <lsc:invoke>
         <!--Optional:-->
         <xmlData><![CDATA[%s]]></xmlData>
      </lsc:invoke>
   </soapenv:Body>
</soapenv:Envelope>''' % login_content
    r=requests.post(config.G_B_INF_WSDL,data.encode('utf-8'))
    logger.info(dir(r))
    response = r.text
    logger.info(u'FSU注册，请求包为:\n%s' % data)
    logger.info(u'FSU注册，返回包为:\n%s' % response)


#######  发送告警
def send_alarm(fsuid,deviceid,signalid,alarmflag=u"BEGIN"):
    fsuid = fsuid.encode('utf-8')
    deviceid = deviceid.encode('utf-8')
    signalid = signalid.encode('utf-8')
    signal_obj = module.querySignal(fsuid, deviceid,signalid)
    # serialno = module.query_alarm_next_serialno(fsuid,deviceid,signalid)                #这个应该是监控点的告警顺序号
    mete_code = signal_obj.signalsid.encode('utf-8')      #mete_code,6位, 直接从数据库中取吧
    nmalarmid = signal_obj.nmalarmid    #直接取表
    if nmalarmid == None:
        nmalarmid = ""
    alarmtime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime() )
    alarmlevel = signal_obj.alarmlevel.encode('utf-8')  #直接取表
    if alarmlevel == '0':
        alarmlevel = '1'
    #logger.error(alarmflag)
    #logger.error(type(alarmflag))
    if alarmflag != u"END":
        alarmflag = "BEGIN"
        serialno = module.query_alarm_begin_serialno(fsuid,deviceid,signalid)
    else:
        alarmflag = "END"
        serialno = module.query_alarm_end_serialno(fsuid,deviceid,signalid)
    #alarmdesc = "告警描述"      # 这个从哪里取？可以从配置表中读， 我们先写死
    alarmdesc = module.query_alarm_desc_by_deviceid_signalid(fsuid,deviceid,signalid,alarmflag)
    eventvalue = "0.2"          # 值是监控点上报的当前值，这个随意填吧
    signalnumber = str(signal_obj.signalnumber)        #signalnumber实际上挂在某个设备下的传感器序号，设备+传感器确定一个监控点
    #alarmremark = "TestConsumeFailKey1"
    alarmremark = ""
    alarm_xml_content = '''<?xml version="1.0" encoding="UTF-8"?>
<Request>
    <PK_Type>
        <Name>SEND_ALARM</Name>
    </PK_Type>
    <Info>
        <FSUID>%s</FSUID>
        <Values>
            <TAlarmList>
                <TAlarm>
                    <SerialNo>%s</SerialNo>
                    <ID>%s</ID>
                    <DeviceID>%s</DeviceID>
                    <NMAlarmID>%s</NMAlarmID>
                    <AlarmTime>%s</AlarmTime>
                    <AlarmLevel>%s</AlarmLevel>
                    <AlarmFlag>%s</AlarmFlag>
                    <AlarmDesc>%s</AlarmDesc>
                    <EventValue>%s</EventValue>
                    <SignalNumber>%s</SignalNumber>
                    <AlarmRemark>%s</AlarmRemark>
                </TAlarm>
            </TAlarmList>
        </Values>
    </Info>
</Request>''' % (fsuid.decode('utf-8'),
                serialno,
                mete_code.decode('utf-8'),
                deviceid.decode('utf-8'), 
                nmalarmid, 
                alarmtime,
                alarmlevel.decode('utf-8'),
                alarmflag,
                alarmdesc,
                eventvalue,
                signalnumber,
                alarmremark,
                )
    #from suds.client import Client
    #client = Client (G_B_INF_WSDL)
    #element = etree.Element('xmlData')
    #element.text = etree.CDATA(alarm_xml_content)
    #result = client.service.invoke(element)
    data = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:lsc="http://LSCService.chinamobile.com">
   <soapenv:Header/>
   <soapenv:Body>
      <lsc:invoke>
         <!--Optional:-->
         <xmlData><![CDATA[%s]]></xmlData>
      </lsc:invoke>
   </soapenv:Body>
</soapenv:Envelope>''' % alarm_xml_content
    r=requests.post(config.G_B_INF_WSDL,data.encode('utf-8'))
    #logger.info(dir(r))
    response = r.text
    logger.info(u'发送告警，请求包为:\n%s' % data)
    logger.info(u'发送告警，返回包为:\n%s' % response)
    alarm_obj = module.Alarm()
    alarm_obj.fsuid = fsuid
    alarm_obj.serialno = serialno
    alarm_obj.signalid = signalid
    alarm_obj.deviceid = deviceid
    alarm_obj.nmalarmid = nmalarmid
    alarm_obj.alarmtime = alarmtime    #直接根据数据库的时间生成吧
    alarm_obj.alarmlevel = alarmlevel
    alarm_obj.alarmflag = alarmflag
    alarm_obj.alarmdesc = alarmdesc
    alarm_obj.eventvalue = eventvalue
    alarm_obj.signalnumber = signalnumber
    alarm_obj.alarmremark = alarmremark
    module.session.add(alarm_obj)
    module.session.commit()
    module.session.close()
