# -*- coding:utf-8 -*-
from lxml import etree
from utils.logger import logger
from module import *
import time
from datetime import datetime
import random

import config


def invoke_proxy(et):
    pk_type = et.xpath('/Request/PK_Type/Name')[0].text
    logger.info('pk_type:[%s]' % pk_type)
    logger.info('invoke proxy, pk_type: %s' % pk_type)
    try:
        # response = eval("on_%s(et)" % pk_type)
        response = eval("on_%s(et)" % pk_type).decode('utf-8')  # bytes转str
        # logger.info('response:\n{}'.format(response))
    except NameError:
        logger.error('未实现的接口，pk_type=%s, 连接关闭！ ' % pk_type)
        logger.error(' on_%s(et)' % pk_type)
        response = '<ERROR>Not Implement Interface!</ERROR>'
    return response


### actions
def on_GET_LOGININFO(req_et):
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    fsuobj = queryFsu(fsuid)
    Response, Info = __add_PK_Type('GET_LOGININFO_ACK')
    if fsuobj != None:
        etree.SubElement(Info, "UserName").text = fsuobj.username
        etree.SubElement(Info, "PassWord").text = fsuobj.password
        etree.SubElement(Info, "FSUID").text = fsuobj.fsuid
        etree.SubElement(Info, "FSUIP").text = fsuobj.fsuip
        etree.SubElement(Info, "FSUVER").text = fsuobj.fsuver
        etree.SubElement(Info, "SiteID").text = fsuobj.siteid
        etree.SubElement(Info, "SiteName").text = fsuobj.sitename
        etree.SubElement(Info, "RoomID").text = fsuobj.roomid
        etree.SubElement(Info, "RoomName").text = fsuobj.roomname
        __add_success_result_node(Info)
    else:
        __add_fail_result_node(Info, 'Fsu Not Found')
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_GET_DATA(req_et):
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    Response, Info = __add_PK_Type('GET_DATA_ACK')
    Values = etree.SubElement(Info, "Values")  # 失败时，Values节点为空
    Values.text = None
    if fsuid == None:  # fsu没有找到时，直接报错
        # __add_fail_result_node(Info, 'Fsu Not Found')
        pass
    else:
        __add_success_result_node(Info)
        DeviceList = etree.SubElement(Values, "DeviceList")
        DeviceList.text = None

        for req_device_node in req_et.xpath('/Request/Info/DeviceList/Device'):
            logger.info('req_device_node:%s' % req_device_node)
            device_id = req_device_node.get('ID')

            # todo 补充device_id输出点位  -- device_id 为 中间库中device_id
            logger.info('device_id:%s' % device_id)
            if device_id == None:  # 当为空，则返回该FSU所监控的所有设备的监控点的值；这种情况下，忽略IDs参数（即监控点ID列表)
                pass
            else:
                Device_Node = etree.SubElement(DeviceList, "Device")
                Device_Node.set('ID', device_id)
                tmp_list = []

                # todo 补充片段 - 绕过数据库直接返回包 - 默认通道号为0
                signalid_list = req_et.xpath('/Request/Info/DeviceList/Device[@ID="%s"]/ID' % device_id)
                logger.info('signalid_list: %s' % signalid_list)
                if signalid_list == []:
                    pass
                else:
                    for id in req_et.xpath('/Request/Info/DeviceList/Device[@ID="%s"]/ID' % device_id):
                        mete_ID = id.text
                        # for signalnumber in ['0', '1', '2', '3', '4']:
                        for signalnumber in ['0']:
                            sinalid_sianlnumber = '{}:{}'.format(mete_ID, signalnumber)
                            logger.info('current signalNumber: %s' % sinalid_sianlnumber)
                            # mete_kind = random.choice(['0', '1', '2'])
                            mete_kind = random.choice(['2'])
                            if signalnumber != None:
                                if signalnumber not in tmp_list:
                                    _add_TSemaphore_Node(Device_Node, signalnumber, mete_ID, mete_kind)
                                    tmp_list.append(sinalid_sianlnumber)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


# todo 更改不走sql
def _add_TSemaphore_Node(parent_node, signalnumber, mete_ID, mete_kind):
    Signalnumber = signalnumber  # 通道号
    if Signalnumber != None:
        TSemaphore_Node = etree.SubElement(parent_node, "TSemaphore")
        TSemaphore_Node.set('Type', mete_kind)
        TSemaphore_Node.set('ID', str(mete_ID))
        TSemaphore_Node.set('SignalNumber', Signalnumber.zfill(3))
        rand1 = str(float(random.randrange(1, 100)))
        rand2 = str(float(random.randrange(1, 100)))
        TSemaphore_Node.set('MeasuredVal', rand1)
        TSemaphore_Node.set('SetupVal', rand2)
        TSemaphore_Node.set('Status', '0')
        TSemaphore_Node.set('Time', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def __add_PK_Type(response_PK_Type):
    '''写xml头信息，指定PK_Type->Name即可，一直写到Info'''
    Response = etree.Element("Response")
    PK_Type = etree.SubElement(Response, "PK_Type")
    PK_Type_Name = etree.SubElement(PK_Type, "Name")
    PK_Type_Name.text = (response_PK_Type)
    Info = etree.SubElement(Response, "Info")
    return (Response, Info)


def on_SET_POINT(req_et):
    Response, Info = __add_PK_Type('SET_POINT_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    device_id_list = [li.get('ID') for li in req_et.xpath('/Request/Info/Value/DeviceList/Device')]
    DeviceList = etree.SubElement(Info, "DeviceList")
    etree.SubElement(Info, "FSUID").text = fsuid
    __add_success_result_node(Info)
    for device_id in device_id_list:
        TSemaphore_id_list = [li.get('ID') for li in
                              req_et.xpath('/Request/Info/Value/DeviceList/Device[@ID="%s"]/TSemaphore' % device_id)]
        Device = etree.SubElement(DeviceList, "Device")
        Device.set('ID', device_id)
        SuccessList = etree.SubElement(Device, "SuccessList")
        # 逻辑部分先不处理，全部当成成功返回
        for TSemaphore_id in TSemaphore_id_list:
            TSignalMeasurementId = etree.SubElement(SuccessList, "TSignalMeasurementId")
            TSignalMeasurementId.set('ID', TSemaphore_id)
            req_tsemaphore_node_list = req_et.xpath(
                '/Request/Info/Value/DeviceList/Device[@ID="%s"]/TSemaphore[@ID="%s"]' % (device_id, TSemaphore_id))
            if req_tsemaphore_node_list == []:
                req_SignalNumber = "NOT FOUND"
            else:
                req_SignalNumber = req_tsemaphore_node_list[0].get("SignalNumber")
                req_SignalID = req_tsemaphore_node_list[0].get("ID")
                # req_MeasuredVal = req_tsemaphore_node_list[0].get("MeasuredVal")
                req_SetupVal = req_tsemaphore_node_list[0].get("SetupVal")
            TSignalMeasurementId.set('SignalNumber', req_SignalNumber)
            updateSignal(fsuid, device_id, signalsid=req_SignalID, measuredval=req_SetupVal)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def __add_success_result_node(Info):
    etree.SubElement(Info, "Result").text = "1"
    etree.SubElement(Info, "FailureCause").text = None


def __add_fail_result_node(Info, msg='Some Error'):
    etree.SubElement(Info, "Result").text = "0"
    etree.SubElement(Info, "FailureCause").text = msg


def on_GET_THRESHOLD(req_et):
    Response, Info = __add_PK_Type('GET_THRESHOLD_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    fsuobj = queryFsu(fsuid)
    FSUID = etree.SubElement(Info, "FSUID")
    FSUID.text = fsuobj.fsuid  # 文档中此处未填
    Values = etree.SubElement(Info, "Values")  # 失败时，Values节点为空
    Values.text = None
    if fsuobj == None:  # fsu没有找到时，直接报错
        __add_fail_result_node(Info, 'Fsu Not Found')
    else:
        __add_success_result_node(Info)
        DeviceList = etree.SubElement(Values, "DeviceList")
        if DeviceList == None or DeviceList.text == None or len(DeviceList) == 0:
            logger.info('getFsuAllDeviceInfo:%s', fsuobj.fsuid)
        # device_obj_list = queryDeviceObjsByFsuid(fsuobj.fsuid)
        # for device_obj in device_obj_list:
        #     Device_Node = etree.SubElement(DeviceList, "Device")
        #     Device_Node.set('ID',device_obj.deviceid)
        #     for signal_obj in querySignalsObjsbyDeviceID(fsuid,device_id):
        #         _add_TThreshold_Node(Device_Node,signal_obj)
        # 如果deviceList这个节点为空的时候，获取这个fsu下的所有设备，并返回
        for req_device_node in req_et.xpath('/Request/Info/DeviceList/Device'):
            logger.info('req_device_node:%s' % req_device_node)
            device_id = req_device_node.get('ID')
            # 当device_id为空，则返回该FSU所监控的所有设备的监控点的值；这种情况下，忽略IDs参数（即监控点ID列表)
            if device_id == None:  # 全量查询还有问题，TODO
                device_obj_list = queryDeviceObjsByFsuid(fsuobj.fsuid)
                for device_obj in device_obj_list:
                    Device_Node = etree.SubElement(DeviceList, "Device")
                    Device_Node.set('ID', device_obj.deviceid)
                    for signal_obj in querySignalsObjsbyDeviceID(fsuid, device_id):
                        _add_TThreshold_Node(Device_Node, signal_obj)
            else:
                Device_Node = etree.SubElement(DeviceList, "Device")
                Device_Node.set('ID', device_id)
                signal_id_list = req_et.xpath('/Request/Info/DeviceList/Device[@ID="%s"]/ID' % device_id)
                # ID当为空，则返回该设备的所有监控点的值。
                if signal_id_list == []:
                    signal_obj_list = querySignalsObjsbyDeviceID(fsuid, device_id)
                    for signal_obj in signal_obj_list:
                        _add_TThreshold_Node(Device_Node, signal_obj)
                else:
                    for id in signal_id_list:
                        ID = id.text
                        if ID != None:
                            signal_obj = querySignal(fsuid, device_id, ID)
                            _add_TThreshold_Node(Device_Node, signal_obj)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def _add_TThreshold_Node(parent_node, signal_obj):
    TThreshold_Node = etree.SubElement(parent_node, "TThreshold")
    TThreshold_Node.set('Type', signal_obj.type)
    TThreshold_Node.set('ID', str(signal_obj.signalsid))
    TThreshold_Node.set('SignalNumber', signal_obj.signalnumber or '')
    TThreshold_Node.set('Threshold', signal_obj.threshold or '')
    TThreshold_Node.set('AlarmLevel', signal_obj.alarmlevel or '')
    TThreshold_Node.set('NMAlarmID', signal_obj.nmalarmid or '')


def on_SET_THRESHOLD(req_et):
    Response, Info = __add_PK_Type('SET_THRESHOLD_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    fsuobj = queryFsu(fsuid)
    deviceid_list = [li.get('ID') for li in req_et.xpath('/Request/Info/Value/DeviceList/Device')]
    logger.info('deviceid_list:%s' % deviceid_list)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
        return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")
    __add_success_result_node(Info)
    DeviceList = etree.SubElement(Info, 'DeviceList')
    for deviceid in deviceid_list:
        Device_Node = etree.SubElement(DeviceList, 'Device')
        Device_Node.set('ID', deviceid)
        SuccessList = etree.SubElement(Device_Node, 'SuccessList')
        threshold_node_list = req_et.xpath('/Request/Info/Value/DeviceList/Device[@ID="%s"]/TThreshold' % deviceid)
        logger.info('threshold_node_list %s' % threshold_node_list)
        for threshold_node in threshold_node_list:
            thresholdid = threshold_node.get('ID')
            type = threshold_node.get('Type')
            signalnumber = threshold_node.get('SignalNumber')
            threshold = threshold_node.get('Threshold')
            alarmlevel = threshold_node.get('AlarmLevel')
            nmalarmid = threshold_node.get('NMAlarmID')

            threshold_obj = queryTThreshold(fsuid, deviceid, thresholdid)
            if threshold_obj == None:
                threshold_obj = Threshold(deviceid=deviceid, thresholdid=thresholdid, type=type,
                                          signalnumber=signalnumber,
                                          threshold=threshold, alarmlevel=alarmlevel, nmalarmid=nmalarmid)
                session.add(threshold_obj)
                session.commit()
            else:
                session.query(Signals).filter_by(fsuid=fsuid).filter_by(deviceid=deviceid).filter_by(
                    signalsid=thresholdid).update({"type": type,
                                                   "deviceid": deviceid,
                                                   "signalnumber": signalnumber,
                                                   "threshold": threshold,
                                                   "alarmlevel": alarmlevel,
                                                   "nmalarmid": nmalarmid
                                                   })
                session.commit()
            TSignalMeasurementId_Node = etree.SubElement(SuccessList, 'TSignalMeasurementId')
            TSignalMeasurementId_Node.set('ID', thresholdid)
            TSignalMeasurementId_Node.set('SignalNumber', signalnumber)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_SET_LOGININFO(req_et):
    Response, Info = __add_PK_Type('SET_LOGININFO_ACK')
    username = req_et.xpath('/Request/Info/UserName')[0].text
    password = req_et.xpath('/Request/Info/PassWord')[0].text
    updateFsu('1', username, password)  # 直接把编号为1的FSU的数据进行修改
    __add_success_result_node(Info)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_GET_FTP(req_et):
    Response, Info = __add_PK_Type('GET_FTP_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    logger.info('request fsuid = %s' % fsuid)
    fsuobj = queryFsu(fsuid)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
    else:
        __add_success_result_node(Info)
        etree.SubElement(Info, "FSUID").text = fsuobj.fsuid
        etree.SubElement(Info, "UserName").text = fsuobj.username
        etree.SubElement(Info, "PassWord").text = fsuobj.password
    # open('e:/czw.xml','w+').write(etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8"))
    # return etree.tostring(Response)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_SET_FTP(req_et):
    Response, Info = __add_PK_Type('SET_FTP_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    username = req_et.xpath('/Request/Info/UserName')[0].text
    password = req_et.xpath('/Request/Info/PassWord')[0].text
    fsuobj = queryFsu(fsuid)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
    else:
        updateFsu(fsuid, username, password)
        __add_success_result_node(Info)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_TIME_CHECK(req_et):
    Response, Info = __add_PK_Type('TIME_CHECK_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    year = req_et.xpath('/Request/Info/Time/Year')[0].text
    month = req_et.xpath('/Request/Info/Time/Month')[0].text
    day = req_et.xpath('/Request/Info/Time/Day')[0].text
    hour = req_et.xpath('/Request/Info/Time/Hour')[0].text
    minute = req_et.xpath('/Request/Info/Time/Minute')[0].text
    second = req_et.xpath('/Request/Info/Time/Second')[0].text
    fsuobj = queryFsu(fsuid)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
    else:
        try:
            time.mktime((int(year), int(month), int(day), int(hour), int(minute), int(second), 0, 0, 0))
            __add_success_result_node(Info)
        except Exception:
            __add_fail_result_node(Info, "Time Error")
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_GET_FTP(req_et):
    Response, Info = __add_PK_Type('GET_FTP_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    fsuobj = queryFsu(fsuid)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
    else:
        etree.SubElement(Info, "UserName").text = fsuobj.username
        etree.SubElement(Info, "PassWord").text = fsuobj.password
        __add_success_result_node(Info)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_SET_FTP(req_et):
    Response, Info = __add_PK_Type('SET_FTP_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    username = req_et.xpath('/Request/Info/UserName')[0].text
    password = req_et.xpath('/Request/Info/PassWord')[0].text
    fsuobj = queryFsu(fsuid)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
    else:
        updateFsu(fsuid, username, password)
        __add_success_result_node(Info)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_GET_FSUINFO(req_et):
    Response, Info = __add_PK_Type('GET_FSUINFO_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    fsuobj = queryFsu(fsuid)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
    else:
        etree.SubElement(Info, "FSUID").text = fsuid
        TFSUStatus = etree.SubElement(Info, "TFSUStatus")
        # 确保即使状态字段为空，也能返回合理的默认值
        etree.SubElement(TFSUStatus, "CPUUsage").text = fsuobj.tfsustatus_cpuusage or "50"
        etree.SubElement(TFSUStatus, "MEMUsage").text = fsuobj.tfsustatus_memusage or "60"
        etree.SubElement(TFSUStatus, "HardDiskUsage").text = fsuobj.tfsustatus_harddiskusage or "40"
        __add_success_result_node(Info)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_UPDATE_FSUINFO_INTERVAL(req_et):
    Response, Info = __add_PK_Type('UPDATE_FSUINFO_INTERVAL_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    interval = req_et.xpath('/Request/Info/Interval')[0].text
    fsuobj = queryFsu(fsuid)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
    else:
        session.query(Fsu).filter_by(fsuid=fsuid).update({"interval": interval, })
        session.commit()
        __add_success_result_node(Info)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_SET_FSUREBOOT(req_et):
    Response, Info = __add_PK_Type('SET_FSUREBOOT_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    fsuobj = queryFsu(fsuid)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
    else:
        __add_success_result_node(Info)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_GET_DEV_CONF(req_et):
    Response, Info = __add_PK_Type('GET_DEV_CONF_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    deviceid = req_et.xpath('/Request/Info/DeviceID')[0].text
    fsuobj = queryFsu(fsuid)
    deviceobj = queryDevice(fsuid, deviceid)
    logger.info('start build info')
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
    elif deviceobj == None:
        Values = etree.SubElement(Info, 'Values')
        Device = etree.SubElement(Values, 'Device')
        __add_fail_result_node(Info, "DeviceID not Found")
    else:
        Values = etree.SubElement(Info, 'Values')
        Device = etree.SubElement(Values, 'Device')
        Device.set('DeviceID', deviceobj.deviceid or '')
        Device.set('DeviceName', deviceobj.devicename or '')
        Device.set('SiteID', deviceobj.siteid or '')
        Device.set('RoomID', deviceobj.roomid or '')
        Device.set('SiteName', deviceobj.sitename or '')
        Device.set('RoomName', deviceobj.roomname or '')
        Device.set('DeviceType', deviceobj.devicetype or '')
        Device.set('DeviceSubType', deviceobj.devicesubtype or '')
        Device.set('Model', deviceobj.model or '')
        Device.set('Brand', deviceobj.brand or '')
        Device.set('RatedCapacity', deviceobj.ratedcapacity or '')
        Device.set('Version', deviceobj.version or '')
        Device.set('BeginRunTime', deviceobj.beginruntime or '')
        Device.set('DevDescribe', deviceobj.devdescribe or '')
        Device.set('ConfRemark', deviceobj.confremark or '')
        signals_obj_list = query_signals_by_device(fsuid, deviceid)
        Signals_Node = etree.SubElement(Device, 'Signals')
        Signals_Node.set("Count", str(len(list(signals_obj_list) or '')))
        for signal_obj in signals_obj_list:
            Signal_Node = etree.SubElement(Signals_Node, 'Signal')
            Signal_Node.set('Type', signal_obj.type or '')
            Signal_Node.set('ID', signal_obj.signalsid or '')
            Signal_Node.set('SignalName', signal_obj.signalname or '')
            Signal_Node.set('SignalNumber', signal_obj.signalnumber or '')
            Signal_Node.set('AlarmLevel', signal_obj.alarmlevel or '')
            Signal_Node.set('Thresbhold', signal_obj.threshold or '')
            Signal_Node.set('NMAlarmID', signal_obj.nmalarmid or '')
        __add_success_result_node(Info)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_SET_DEV_CONF_DATA(req_et):
    Response, Info = __add_PK_Type('SET_DEV_CONF_DATA_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    fsuobj = queryFsu(fsuid)
    deviceid_list = [li.get('DeviceID') for li in req_et.xpath('/Request/Info/Values/Device')]
    logger.info('deviceid_list:%s' % deviceid_list)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
        return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")
    __add_success_result_node(Info)
    SuccessList = etree.SubElement(Info, 'SuccessList')
    for deviceid in deviceid_list:
        device_node = req_et.xpath('/Request/Info/Values/Device[@DeviceID="%s"]' % deviceid)[0]
        devicename = device_node.get('DeviceName')
        siteid = device_node.get('SiteID')
        roomid = device_node.get('RoomID')
        roomname = device_node.get('RoomName')
        devicetype = device_node.get('DeviceType')
        devicesubtype = device_node.get('DeviceSubType')
        model = device_node.get('Model')
        brand = device_node.get('Brand')
        ratedcapacity = device_node.get('RatedCapacity')
        version = device_node.get('Version')
        beginruntime = device_node.get('BeginRunTime')
        devdescribe = device_node.get('DevDescribe')
        confremark = device_node.get('ConfRemark')
        deviceobj = queryDevice(fsuid, deviceid)
        if deviceobj == None:
            deviceobj = Device(deviceid=deviceid, fsuid=fsuid, devicename=devicename, siteid=siteid, roomid=roomid,
                               roomname=roomname, devicetype=devicetype, devicesubtype=devicesubtype,
                               model=model, brand=brand, ratedcapacity=ratedcapacity, version=version,
                               beginruntime=beginruntime, devdescribe=devdescribe, confremark=confremark)
            session.add(deviceobj)
            session.commit()
        else:
            session.query(Device).filter_by(fsuid=fsuid).filter_by(deviceid=deviceid).update({"devicename": devicename,
                                                                                              "fsuid": fsuid,
                                                                                              "siteid": siteid,
                                                                                              "roomid": roomid,
                                                                                              "roomname": roomname,
                                                                                              "devicetype": devicetype,
                                                                                              "devicesubtype": devicesubtype,
                                                                                              "model": model,
                                                                                              "brand": brand,
                                                                                              "ratedcapacity": ratedcapacity,
                                                                                              "version": version,
                                                                                              "beginruntime": beginruntime,
                                                                                              "devdescribe": devdescribe,
                                                                                              "confremark": confremark,
                                                                                              })
            session.commit()
        etree.SubElement(SuccessList, 'Device').set('ID', deviceid)
        logger.info('update device success, start update signal')
        sinals_node_list = req_et.xpath('/Request/Info/Values/Device[@DeviceID="%s"]/Signals/Signal' % deviceid)
        for sinals_node in sinals_node_list:
            signalsid = sinals_node.get('ID')
            type = sinals_node.get('Type')
            signalname = sinals_node.get('SignalName')
            signalnumber = sinals_node.get('SignalNumber')
            alarmlevel = sinals_node.get('AlarmLevel')
            threshold = sinals_node.get('Threshold')
            nmalarmid = sinals_node.get('NMAlarmID')
            sinals_obj = queryTSemaphore(fsuid, deviceid, signalsid)
            if sinals_obj == None:
                signalsobj = Signals(signalsid=signalsid, deviceid=deviceid, type=type, signalname=signalname,
                                     signalnumber=signalnumber,
                                     alarmlevel=alarmlevel, thresbhold=thresbhold, nmalarmid=nmalarmid)
                session.add(signalsobj)
                session.commit()
            else:
                session.query(Signals).filter_by(fsuid=fsuid).filter_by(deviceid=deviceid).filter_by(
                    signalsid=signalsid).update({"type": type,
                                                 "deviceid": deviceid,
                                                 "signalname": signalname,
                                                 "signalnumber": signalnumber,
                                                 "alarmlevel": alarmlevel,
                                                 "nmalarmid": nmalarmid
                                                 })
                session.commit()
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def _add_TStorageRule_Node(parent_node, storage_obj):
    TStorageRule_Node = etree.SubElement(parent_node, "TStorageRule")
    TStorageRule_Node.set('Type', storage_obj.type)
    TStorageRule_Node.set('ID', str(storage_obj.storageid))
    TStorageRule_Node.set('SignalNumber', storage_obj.signalnumber or '')
    TStorageRule_Node.set('AbsoluteVal', storage_obj.absoluteval or '')
    TStorageRule_Node.set('RelativeVal', storage_obj.relativeval or '')
    TStorageRule_Node.set('StorageInterval', storage_obj.storageinterval or '')
    TStorageRule_Node.set('StorageRefTime', storage_obj.storagereftime or '')


def on_GET_STORAGERULE(req_et):
    Response, Info = __add_PK_Type('GET_STORAGERULE_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    fsuobj = queryFsu(fsuid)
    deviceid_list = [li.get('ID') for li in req_et.xpath('/Request/Info/DeviceList/Device')]
    logger.info('deviceid_list:%s' % deviceid_list)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
        return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")
    __add_success_result_node(Info)
    Values = etree.SubElement(Info, 'Values')
    DeviceList = etree.SubElement(Values, 'DeviceList')
    for deviceid in deviceid_list:
        tsignalmeasurementid_node_list = req_et.xpath(
            '/Request/Info/DeviceList/Device[@ID="%s"]/TSignalMeasurementId' % deviceid)
        Device_Node = etree.SubElement(DeviceList, 'Device')
        Device_Node.set('ID', deviceid)
        if tsignalmeasurementid_node_list == []:
            for storage_obj in queryStorageByDevice(fsuid, deviceid):
                _add_TStorageRule_Node(Device_Node, storage_obj)
    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")


def on_SET_STORAGERULE(req_et):
    Response, Info = __add_PK_Type('SET_STORAGERULE_ACK')
    fsuid = req_et.xpath('/Request/Info/FSUID')[0].text
    fsuobj = queryFsu(fsuid)
    deviceid_list = [li.get('ID') for li in req_et.xpath('/Request/Info/Value/DeviceList/Device')]
    logger.info('deviceid_list:%s' % deviceid_list)
    if fsuobj == None:
        __add_fail_result_node(Info, "FSUID not Found")
        return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")
    __add_success_result_node(Info)
    DeviceList = etree.SubElement(Info, 'DeviceList')
    for deviceid in deviceid_list:
        tstoragerule_node_list = req_et.xpath('/Request/Info/Value/DeviceList/Device[@ID="%s"]/TStorageRule' % deviceid)
        Device_Node = etree.SubElement(DeviceList, 'Device')
        Device_Node.set('ID', deviceid)
        SuccessList = etree.SubElement(Device_Node, 'SuccessList')
        for tstoragerule_node in tstoragerule_node_list:
            storageid = tstoragerule_node.get('ID')
            type = tstoragerule_node.get('Type')
            signalnumber = tstoragerule_node.get('SignalNumber')
            absoluteval = tstoragerule_node.get('AbsoluteVal')
            relativeval = tstoragerule_node.get('RelativeVal')
            storageinterval = tstoragerule_node.get('StorageInterval')
            storagereftime = tstoragerule_node.get('StorageRefTime')
            storage_obj = queryStorageBySignal(fsuid, deviceid, storageid)
            device_obj = queryDevice(fsuid, deviceid)
            TSignalMeasurementId = etree.SubElement(SuccessList, 'TSignalMeasurementId')
            TSignalMeasurementId.set('ID', storageid)
            TSignalMeasurementId.set('SignalNumber', signalnumber)
            if device_obj == None:
                pass
            else:
                if storage_obj == None:
                    storage_obj = Storage(storageid=storageid, fsuid=fsuid, deviceid=deviceid, type=type,
                                          signalnumber=signalnumber,
                                          absoluteval=absoluteval, relativeval=relativeval,
                                          storageinterval=storageinterval,
                                          storagereftime=storagereftime)
                    session.add(storage_obj)
                    session.commit()
                else:
                    session.query(Storage).filter_by(fsuid=fsuid).filter_by(deviceid=deviceid).filter_by(
                        storageid=storageid).update({
                        "type": type,
                        "fsuid": fsuid,
                        "deviceid": deviceid,
                        "signalnumber": signalnumber,
                        "absoluteval": absoluteval,
                        "relativeval": relativeval,
                        "storageinterval": storageinterval,
                        "storagereftime": storagereftime,
                    })
                    session.commit()

    return etree.tostring(Response, pretty_print=True, xml_declaration=True, encoding="utf-8")
