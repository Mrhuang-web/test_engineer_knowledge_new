#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
人脸门禁一体机Mock Server
使用Python原生库实现，支持主要的门禁功能
"""

import http.server
import json
import urllib.parse
from datetime import datetime
from business.device_service import DeviceService
from business.person_service import PersonService
from business.face_service import FaceService
from business.record_service import RecordService
from business.logger import global_logger

class FaceAccessControlHandler(http.server.BaseHTTPRequestHandler):
    """HTTP请求处理器"""
    
    # 初始化业务服务
    device_service = DeviceService()
    person_service = PersonService()
    face_service = FaceService()
    record_service = RecordService()
    logger = global_logger
    
    def send_response_json(self, result=1, success=True, msg="操作成功", code="LAN_SUS-0", data=None):
        """发送JSON响应"""
        response = {
            "result": result,
            "success": success,
            "msg": msg,
            "code": code,
            "data": data or {}
        }
        
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
    
    def parse_post_data(self):
        """解析POST请求数据"""
        content_length = int(self.headers.get("Content-Length", 0))
        post_data = self.rfile.read(content_length).decode("utf-8")
        return urllib.parse.parse_qs(post_data)
    
    def get_param(self, params, key, default=None):
        """获取参数值"""
        values = params.get(key)
        if values:
            return values[0]
        return default
    
    def do_POST(self):
        """处理POST请求"""
        start_time = datetime.now()
        
        try:
            # 解析POST数据
            post_params = self.parse_post_data()
            
            # 记录请求日志
            self.logger.log_request(self.command, self.path, self.client_address[0], post_params)
            
            # 设备管理类接口
            if self.path == "/setPassWord":
                self.handle_set_password(post_params)
            elif self.path == "/device/openDoorControl":
                self.handle_open_door(post_params)
            elif self.path == "/setIdentifyCallBack":
                self.handle_set_identify_callback(post_params)
            elif self.path == "/setImgRegCallBack":
                self.handle_set_img_reg_callback(post_params)
            elif self.path == "/device/eventCallBack":
                self.handle_set_event_callback(post_params)
            elif self.path == "/restartDevice":
                self.handle_restart_device(post_params)
            elif self.path == "/setTime":
                self.handle_set_time(post_params)
            elif self.path == "/device/setLanguage":
                self.handle_set_language(post_params)
            elif self.path == "/device/setTimeZone":
                self.handle_set_timezone(post_params)
            elif self.path == "/device/setSignalInput":
                self.handle_set_signal_input(post_params)
            elif self.path == "/meetAndWarnSet":
                self.handle_meet_warn_set(post_params)
            elif self.path == "/cardInfoSet":
                self.handle_card_info_set(post_params)
            
            # 人员管理类接口
            elif self.path == "/person/create":
                self.handle_person_create(post_params)
            elif self.path == "/person/delete":
                self.handle_person_delete(post_params)
            elif self.path == "/person/update":
                self.handle_person_update(post_params)
            
            # 照片管理类接口
            elif self.path == "/face/create":
                self.handle_face_create(post_params)
            elif self.path == "/face/delete":
                self.handle_face_delete(post_params)
            elif self.path == "/face/update":
                self.handle_face_update(post_params)
            elif self.path == "/face/find":
                self.handle_face_find(post_params)
            elif self.path == "/face/takeImg":
                self.handle_face_take_img(post_params)
            elif self.path == "/face/deletePerson":
                self.handle_face_delete_person(post_params)
            
            # 识别记录类接口
            elif self.path == "/newDeleteRecords":
                self.handle_delete_records(post_params)
            
            else:
                self.send_response_json(result=0, success=False, msg="接口不存在", code="LAN_EXP-1006")
        
        except Exception as e:
            self.logger.error(f"请求处理异常：{str(e)}", exc_info=True)
            self.send_response_json(result=0, success=False, msg=f"服务器内部错误: {str(e)}", code="LAN_EXP-1000")
        
        # 记录响应日志
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        self.logger.log_response(self.command, self.path, 200, response_time)
    
    def do_GET(self):
        """处理GET请求"""
        start_time = datetime.now()
        
        try:
            # 解析查询参数
            if "?" in self.path:
                path, query_string = self.path.split("?", 1)
                get_params = urllib.parse.parse_qs(query_string)
            else:
                path = self.path
                get_params = {}
            
            # 记录请求日志
            self.logger.log_request(self.command, self.path, self.client_address[0], get_params)
            
            # 设备管理类接口
            if path == "/device/information":
                self.handle_get_device_info(get_params)
            elif path == "/getDoorSensor":
                self.handle_get_door_sensor(get_params)
            
            # 人员管理类接口
            elif path == "/person/find":
                self.handle_person_find(get_params)
            elif path == "/person/findByPage":
                self.handle_person_find_by_page(get_params)
            
            # 识别记录类接口
            elif path == "/newFindRecords":
                self.handle_find_records(get_params)
            
            else:
                self.send_response_json(result=0, success=False, msg="接口不存在", code="LAN_EXP-1006")
        
        except Exception as e:
            self.logger.error(f"请求处理异常：{str(e)}", exc_info=True)
            self.send_response_json(result=0, success=False, msg=f"服务器内部错误: {str(e)}", code="LAN_EXP-1000")
        
        # 记录响应日志
        response_time = (datetime.now() - start_time).total_seconds() * 1000
        self.logger.log_response(self.command, self.path, 200, response_time)
    
    # 设备管理类接口处理
    def handle_set_password(self, params):
        """处理设置密码请求"""
        old_pass = self.get_param(params, "oldPass")
        new_pass = self.get_param(params, "newPass")
        
        if not old_pass or not new_pass:
            self.send_response_json(result=0, success=False, msg="密码不能为空", code="LAN_EXP-2003")
            return
        
        success, msg = self.device_service.set_password(old_pass, new_pass)
        if success:
            self.send_response_json(msg=msg, data=f"password is : {new_pass}")
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-2005")
    
    def handle_get_device_info(self, params):
        """处理获取设备信息请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        device_info = self.device_service.get_device_info()
        self.send_response_json(data=device_info, msg="查询成功")
    
    def handle_open_door(self, params):
        """处理远程开门请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        success, msg = self.device_service.open_door()
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg)
    
    def handle_get_door_sensor(self, params):
        """处理获取门磁状态请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        door_sensor = self.device_service.get_door_sensor()
        self.send_response_json(data={"status": door_sensor}, msg="获取成功")
    
    def handle_set_identify_callback(self, params):
        """处理设置识别回调请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        callback_url = self.get_param(params, "callbackUrl")
        success, msg = self.device_service.set_callback("identify", callback_url)
        self.send_response_json(msg=msg)
    
    def handle_set_img_reg_callback(self, params):
        """处理设置照片注册回调请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        url = self.get_param(params, "url")
        success, msg = self.device_service.set_callback("img_reg", url)
        self.send_response_json(msg=msg)
    
    def handle_set_event_callback(self, params):
        """处理设置事件回调请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        url = self.get_param(params, "url")
        success, msg = self.device_service.set_callback("event", url)
        self.send_response_json(msg=msg)
    
    def handle_restart_device(self, params):
        """处理重启设备请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        success, msg = self.device_service.restart_device()
        self.send_response_json(msg=msg)
    
    def handle_set_time(self, params):
        """处理设置时间请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        success, msg = self.device_service.set_time()
        self.send_response_json(msg=msg)
    
    def handle_set_language(self, params):
        """处理设置语言请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        language_type = self.get_param(params, "languageType")
        success, msg = self.device_service.set_language(language_type)
        self.send_response_json(msg=msg)
    
    def handle_set_timezone(self, params):
        """处理设置时区请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        timezone = self.get_param(params, "timeZone")
        success, msg = self.device_service.set_timezone(timezone)
        self.send_response_json(msg=msg)
    
    def handle_set_signal_input(self, params):
        """处理设置信号输入请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        config = self.get_param(params, "config")
        success, msg = self.device_service.set_signal_input(config)
        self.send_response_json(msg=msg)
    
    def handle_meet_warn_set(self, params):
        """处理会议与关门告警设置请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        success, msg = self.device_service.meet_warn_set(params)
        self.send_response_json(msg=msg)
    
    def handle_card_info_set(self, params):
        """处理卡片设置请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        success, msg = self.device_service.card_info_set(params)
        self.send_response_json(msg=msg)
    
    # 人员管理类接口处理
    def handle_person_create(self, params):
        """处理人员注册请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_json = self.get_param(params, "person")
        if not person_json:
            self.send_response_json(result=0, success=False, msg="人员信息不能为空", code="LAN_EXP-3002")
            return
        
        try:
            person_data = json.loads(person_json)
        except json.JSONDecodeError:
            self.send_response_json(result=0, success=False, msg="人员信息格式错误", code="LAN_EXP-3002")
            return
        
        success, msg = self.person_service.add_person(person_data)
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-3004")
    
    def handle_person_delete(self, params):
        """处理人员删除请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "id")
        if not person_id:
            self.send_response_json(result=0, success=False, msg="人员ID不能为空", code="LAN_EXP-3008")
            return
        
        success, msg = self.person_service.delete_person(person_id)
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-3009")
    
    def handle_person_update(self, params):
        """处理人员更新请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_json = self.get_param(params, "person")
        if not person_json:
            self.send_response_json(result=0, success=False, msg="人员信息不能为空", code="LAN_EXP-3002")
            return
        
        try:
            person_data = json.loads(person_json)
        except json.JSONDecodeError:
            self.send_response_json(result=0, success=False, msg="人员信息格式错误", code="LAN_EXP-3002")
            return
        
        success, msg = self.person_service.update_person(person_data)
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-3009")
    
    def handle_person_find(self, params):
        """处理人员查询请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "id", "-1")
        persons, msg = self.person_service.get_person(person_id)
        
        if persons is None:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-3009")
        else:
            self.send_response_json(data=persons, msg=msg)
    
    def handle_person_find_by_page(self, params):
        """处理人员分页查询请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "personId", "-1")
        persons, msg = self.person_service.get_person(person_id)
        
        if persons is None:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-3009")
        else:
            # 简单实现，实际应该分页
            self.send_response_json(data=persons, msg=msg)
    
    # 照片管理类接口处理
    def handle_face_create(self, params):
        """处理照片注册请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "personId")
        face_id = self.get_param(params, "faceId")
        img_base64 = self.get_param(params, "imgBase64")
        is_easy_way = self.get_param(params, "isEasyWay", "false").lower() == "true"
        
        face_data = {
            "personId": person_id,
            "faceId": face_id,
            "imgBase64": img_base64,
            "isEasyWay": is_easy_way
        }
        
        success, msg = self.face_service.add_face(face_data)
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-4008")
    
    def handle_face_delete(self, params):
        """处理照片删除请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        face_id = self.get_param(params, "faceId")
        if not face_id:
            self.send_response_json(result=0, success=False, msg="照片ID不能为空", code="LAN_EXP-4016")
            return
        
        success, msg = self.face_service.delete_face(face_id)
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-4017")
    
    def handle_face_update(self, params):
        """处理照片更新请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "personId")
        face_id = self.get_param(params, "faceId")
        img_base64 = self.get_param(params, "imgBase64")
        is_easy_way = self.get_param(params, "isEasyWay", "false").lower() == "true"
        
        face_data = {
            "personId": person_id,
            "faceId": face_id,
            "imgBase64": img_base64,
            "isEasyWay": is_easy_way
        }
        
        success, msg = self.face_service.update_face(face_data)
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-4031")
    
    def handle_face_find(self, params):
        """处理照片查询请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "personId")
        if not person_id:
            self.send_response_json(result=0, success=False, msg="人员ID不能为空", code="LAN_EXP-3016")
            return
        
        faces, msg = self.face_service.get_face(person_id)
        self.send_response_json(data=faces, msg=msg)
    
    def handle_face_take_img(self, params):
        """处理拍照注册请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "personId")
        if not person_id:
            self.send_response_json(result=0, success=False, msg="人员ID不能为空", code="LAN_EXP-3016")
            return
        
        success, msg = self.face_service.take_img(person_id)
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-3009")
    
    def handle_face_delete_person(self, params):
        """处理清空人员照片请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "personId")
        if not person_id:
            self.send_response_json(result=0, success=False, msg="人员ID不能为空", code="LAN_EXP-3016")
            return
        
        success, msg = self.face_service.clear_person_faces(person_id)
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-3009")
    
    # 识别记录类接口处理
    def handle_find_records(self, params):
        """处理识别记录查询请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "personId", "-1")
        start_time = self.get_param(params, "startTime", "0")
        end_time = self.get_param(params, "endTime", "9999-12-31 23:59:59")
        
        records, msg = self.record_service.get_records(person_id, start_time, end_time)
        if records is None:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-3009")
        else:
            self.send_response_json(data={"records": records}, msg=msg)
    
    def handle_delete_records(self, params):
        """处理识别记录删除请求"""
        passwd = self.get_param(params, "pass")
        if not self.device_service.verify_password(passwd):
            self.send_response_json(result=0, success=False, msg="密码错误", code="LAN_EXP-1001")
            return
        
        person_id = self.get_param(params, "personId")
        start_time = self.get_param(params, "startTime")
        end_time = self.get_param(params, "endTime")
        
        success, msg = self.record_service.delete_records(person_id, start_time, end_time)
        if success:
            self.send_response_json(msg=msg)
        else:
            self.send_response_json(result=0, success=False, msg=msg, code="LAN_EXP-5013")


def run_server(port=8090):
    """启动服务器"""
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, FaceAccessControlHandler)
    global_logger.info(f"人脸门禁Mock Server启动成功，监听端口: {port}")
    print(f"人脸门禁Mock Server启动成功，监听端口: {port}")
    print(f"接口根地址: http://localhost:{port}/")
    print("按 Ctrl+C 停止服务器")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        global_logger.info("服务器正在停止...")
        print("\n服务器正在停止...")
        httpd.server_close()
        global_logger.info("服务器已停止")
        print("服务器已停止")


if __name__ == "__main__":
    run_server()