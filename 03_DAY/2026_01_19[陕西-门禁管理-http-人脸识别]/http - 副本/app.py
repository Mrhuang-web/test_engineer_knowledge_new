from flask import Flask, request, jsonify, render_template
import functools

# 引入自定义模块
from rules.response import base_response, ERROR_CODES
from models import device_data
from services import device_service, person_service, face_service, record_service

app = Flask(__name__)

# 配置最大请求实体大小，支持1080p照片，默认为50MB (50*1024*1024字节)
# 可根据需要调整此值，建议不超过设备内存限制
MAX_CONTENT_LENGTH = 50 * 1024 * 1024
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# 处理不支持的HTTP方法
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify(base_response(0, False, f'The {request.method} method is not supported.', ERROR_CODES['METHOD_NOT_SUPPORTED'])), 405

# 处理请求实体过大错误
@app.errorhandler(413)
def request_entity_too_large(e):
    return jsonify(base_response(0, False, 'imgBase64 参数异常', ERROR_CODES['IMG_BASE64_PARAM_ERROR'])), 413

# 密码验证装饰器
def require_password(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        # 检查设备是否有密码
        current_password = device_data.get_password()
        
        # 获取请求中的所有参数键名，用于检查参数名是否正确
        if request.method == 'GET':
            all_params = request.args
            all_param_names = list(request.args.keys())
        else:
            all_params = request.form
            all_param_names = list(request.form.keys())
        
        # 情况1：设备有密码，检查pass参数
        if current_password is not None:
            # 检查pass参数是否存在，处理参数名拼写错误情况
            has_pass_param = False
            for param_name in all_param_names:
                if param_name.strip().lower() == 'pass':
                    # 检查参数名是否包含空格或回车
                    if param_name != 'pass':
                        # 参数名带有空格或回车，返回参数异常
                        return jsonify(base_response(0, False, 'pass 参数异常', ERROR_CODES['PASS_PARAM_ERROR']))
                    has_pass_param = True
                    break
            
            if not has_pass_param:
                # pass参数漏传或拼写错误
                return jsonify(base_response(0, False, 'pass 参数异常', ERROR_CODES['PASS_PARAM_ERROR']))
            
            # 获取pass参数值
            if request.method == 'GET':
                passwd = request.args.get('pass')
            else:
                passwd = request.form.get('pass')
            
            # 检查pass参数值是否异常
            if (passwd is None or 
                not isinstance(passwd, str) or 
                '\n' in passwd or 
                '\r' in passwd or 
                passwd.strip() == '' or
                ' ' in passwd.strip()):  # 检查密码值是否包含空格
                return jsonify(base_response(0, False, 'pass 参数异常', ERROR_CODES['PASS_PARAM_ERROR']))
            
            # 检查密码是否正确
            if passwd != current_password:
                return jsonify(base_response(0, False, '密码错误，请检查密码正确性', ERROR_CODES['PASSWORD_ERROR']))
        # 情况2：设备无密码
        else:
            # 只有设置密码接口(/setPassWord)需要检查oldPass和newPass参数
            # 其他接口直接允许访问
            if request.path == '/setPassWord':
                # 检查是否传入了oldPass和newPass参数
                required_params = ['oldPass', 'newPass']
                for param in required_params:
                    if param not in all_params:
                        return jsonify(base_response(0, False, '密码参数异常', ERROR_CODES['PASS_PARAM_ERROR']))
                    
                    # 检查参数名是否正确（没有空格或回车）
                    for param_name in all_param_names:
                        if param_name.strip() == param and param_name != param:
                            return jsonify(base_response(0, False, '密码参数异常', ERROR_CODES['PASS_PARAM_ERROR']))
                
                # 获取密码参数值
                if request.method == 'GET':
                    old_pass = request.args.get('oldPass')
                    new_pass = request.args.get('newPass')
                else:
                    old_pass = request.form.get('oldPass')
                    new_pass = request.form.get('newPass')
                
                # 检查密码参数值是否异常
                for pwd in [old_pass, new_pass]:
                    if (pwd is None or 
                        not isinstance(pwd, str) or 
                        '\n' in pwd or 
                        '\r' in pwd or 
                        pwd.strip() == '' or
                        ' ' in pwd.strip()):
                        return jsonify(base_response(0, False, '密码参数异常', ERROR_CODES['PASS_PARAM_ERROR']))
                
                # 检查oldPass和newPass是否相同且为12345678
                if old_pass != new_pass or old_pass != '12345678':
                    return jsonify(base_response(0, False, '密码错误，请检查密码正确性', ERROR_CODES['PASSWORD_ERROR']))
        
        return f(*args, **kwargs)
    return decorated

# 设备管理类接口

# 设置设备密码
@app.route('/setPassWord', methods=['POST'])
def set_password():
    old_pass = request.form.get('oldPass')
    new_pass = request.form.get('newPass')
    return jsonify(device_service.set_password(old_pass, new_pass))

# 设备信息查询
@app.route('/device/information', methods=['GET'])
@require_password
def get_device_info():
    return jsonify(device_service.get_device_info())

# 设置设备时间
@app.route('/setTime', methods=['POST'])
@require_password
def set_time():
    timestamp = request.form.get('timestamp')
    return jsonify(device_service.set_time(timestamp))

# 语言切换
@app.route('/device/setLanguage', methods=['POST'])
@require_password
def set_language():
    language_type = request.form.get('languageType')
    return jsonify(device_service.set_language(language_type))

# 设置时区
@app.route('/device/setTimeZone', methods=['POST'])
@require_password
def set_timezone():
    time_zone = request.form.get('timeZone')
    return jsonify(device_service.set_timezone(time_zone))

# 设备重启
@app.route('/restartDevice', methods=['POST'])
@require_password
def restart_device():
    return jsonify(device_service.restart_device())

# 识别回调
@app.route('/setIdentifyCallBack', methods=['POST'])
@require_password
def set_identify_callback():
    callback_url = request.form.get('callbackUrl')
    base64_enable = request.form.get('base64Enable', 1)
    return jsonify(device_service.set_identify_callback(callback_url, base64_enable))

# 注册照片回调
@app.route('/setImgRegCallBack', methods=['POST'])
@require_password
def set_img_reg_callback():
    url = request.form.get('url')
    base64_enable = request.form.get('base64Enable', 1)
    return jsonify(device_service.set_img_reg_callback(url, base64_enable))

# 远程控制输出
@app.route('/device/openDoorControl', methods=['POST'])
@require_password
def open_door():
    type_ = request.form.get('type', 1)
    return jsonify(device_service.open_door(type_))

# 获取门磁状态
@app.route('/getDoorSensor', methods=['GET'])
@require_password
def get_door_status():
    return jsonify(device_service.get_door_status())

# 事件回调
@app.route('/device/eventCallBack', methods=['POST'])
@require_password
def set_event_callback():
    url = request.form.get('url')
    return jsonify(device_service.set_event_callback(url))

# 重置设备
@app.route('/resetDevice', methods=['POST'])
@require_password
def reset_device():
    return jsonify(device_service.reset_device())

# 获取设备状态
@app.route('/device/status', methods=['GET'])
@require_password
def get_device_status():
    return jsonify(device_service.get_device_status())

# 信号输入设置
@app.route('/device/setSignalInput', methods=['POST'])
@require_password
def set_signal_input():
    config = request.form.get('config')
    return jsonify(device_service.set_signal_input(config))

# 会议与关门告警设置
@app.route('/meetAndWarnSet', methods=['POST'])
@require_password
def set_meet_and_warn():
    meet_enable = request.form.get('meetEnable')
    meet_free_time = request.form.get('meetFreeTime')
    door_warn_enable = request.form.get('doorWarnEnable')
    door_close_time = request.form.get('doorCloseTime')
    return jsonify(device_service.set_meet_and_warn(meet_enable, meet_free_time, door_warn_enable, door_close_time))

# 卡片设置
@app.route('/cardInfoSet', methods=['POST'])
@require_password
def set_card_info():
    read_data_enable = request.form.get('readDataEnable')
    read_sector = request.form.get('readSector')
    read_block = request.form.get('readBlock')
    read_shift = request.form.get('readShift')
    read_key_a = request.form.get('readKeyA')
    wg_out_type = request.form.get('wgOutType')
    return jsonify(device_service.set_card_info(read_data_enable, read_sector, read_block, read_shift, read_key_a, wg_out_type))

# 人员管理类接口

# 人员注册
@app.route('/person/create', methods=['POST'])
@require_password
def create_person():
    person_data = request.form.get('person')
    return jsonify(person_service.create_person(person_data))

# 人员删除
@app.route('/person/delete', methods=['POST'])
@require_password
def delete_person():
    id_ = request.form.get('id')
    return jsonify(person_service.delete_person(id_))

# 人员更新
@app.route('/person/update', methods=['POST'])
@require_password
def update_person():
    person_data = request.form.get('person')
    return jsonify(person_service.update_person(person_data))

# 人员查询
@app.route('/person/find', methods=['GET'])
@require_password
def find_person():
    id_ = request.args.get('id')
    return jsonify(person_service.find_person(id_))

# 人员分页查询
@app.route('/person/findByPage', methods=['GET'])
@require_password
def find_person_by_page():
    person_id = request.args.get('personId', '-1')
    length = int(request.args.get('length', 1000))
    index = int(request.args.get('index', 0))
    return jsonify(person_service.find_person_by_page(person_id, index, length))

# 照片管理类接口

# 照片注册
@app.route('/face/create', methods=['POST'])
@require_password
def create_face():
    # 检查 faceId 参数是否存在
    if 'faceId' not in request.form:
        # faceId 参数未上传，返回参数异常
        from rules.response import base_response
        from rules.response import ERROR_CODES
        return jsonify(base_response(0, False, 'faceId 参数异常', ERROR_CODES['FACE_ID_PARAM_ERROR']))
    
    person_id = request.form.get('personId')
    face_id = request.form.get('faceId', '')
    img_base64 = request.form.get('imgBase64')
    
    # 验证 isEasyWay 参数
    is_easy_way_value = request.form.get('isEasyWay')
    if is_easy_way_value is not None:
        is_easy_way_value = is_easy_way_value.lower()
        if is_easy_way_value not in ['true', 'false']:
            # isEasyWay 参数不合法，返回错误
            from rules.response import base_response
            from rules.response import ERROR_CODES
            return jsonify(base_response(0, False, 'isEasyWay 参数不合法', ERROR_CODES['IS_EASY_WAY_ILLEGAL']))
    
    # 转换 is_easy_way 为布尔值
    is_easy_way = is_easy_way_value.lower() == 'true' if is_easy_way_value is not None else False
    
    return jsonify(face_service.create_face(person_id, face_id, img_base64, is_easy_way))

# 照片删除
@app.route('/face/delete', methods=['POST'])
@require_password
def delete_face():
    face_id = request.form.get('faceId')
    return jsonify(face_service.delete_face(face_id))

# 照片更新
@app.route('/face/update', methods=['POST'])
@require_password
def update_face():
    person_id = request.form.get('personId')
    face_id = request.form.get('faceId')
    img_base64 = request.form.get('imgBase64')
    is_easy_way = request.form.get('isEasyWay', 'false').lower() == 'true'
    return jsonify(face_service.update_face(person_id, face_id, img_base64, is_easy_way))

# 照片查询
@app.route('/face/find', methods=['POST'])
@require_password
def find_face():
    person_id = request.form.get('personId')
    return jsonify(face_service.find_face(person_id))

# 拍照注册
@app.route('/face/takeImg', methods=['POST'])
@require_password
def take_img():
    person_id = request.form.get('personId')
    return jsonify(face_service.take_img(person_id))

# 清空人员注册照片
@app.route('/face/deletePerson', methods=['POST'])
@require_password
def delete_person_faces():
    person_id = request.form.get('personId')
    return jsonify(face_service.delete_person_faces(person_id))

# 识别记录接口

# 识别记录查询
@app.route('/newFindRecords', methods=['GET'])
@require_password
def find_records():
    # 获取参数
    person_id = request.args.get('personId', '-1')
    model = request.args.get('model', -1)
    order = request.args.get('order', 'desc')
    index = request.args.get('index', 0)
    length = request.args.get('length', 1000)
    start_time = request.args.get('startTime', 0)
    end_time = request.args.get('endTime', 0)
    
    # 转换参数类型（只转换明确需要整数的参数）
    try:
        model = int(model)
        index = int(index)
        length = int(length)
    except ValueError:
        # 参数格式错误，返回对应的错误码
        from rules.response import base_response, ERROR_CODES
        return jsonify(base_response(0, False, '参数异常', ERROR_CODES['PARAMETER_ERROR']))
    
    # 调用服务层方法（服务层会处理start_time和end_time的格式转换）
    return jsonify(record_service.find_records(person_id, model, order, index, length, start_time, end_time))

# 识别记录删除
@app.route('/newDeleteRecords', methods=['POST'])
@require_password
def delete_records():
    # 获取参数
    person_id = request.form.get('personId', '-1')
    model = request.form.get('model', -1)
    start_time = request.form.get('startTime', 0)
    end_time = request.form.get('endTime', 0)
    
    # 转换参数类型
    try:
        model = int(model)
    except ValueError:
        # 参数格式错误，返回对应的错误码
        from rules.response import base_response, ERROR_CODES
        return jsonify(base_response(0, False, '参数异常', ERROR_CODES['PARAMETER_ERROR']))
    
    # 调用服务层方法
    return jsonify(record_service.delete_records(person_id, model, start_time, end_time))

# 模拟识别记录生成
@app.route('/simulateIdentify', methods=['POST'])
@require_password
def simulate_identify():
    person_id = request.form.get('personId')
    return jsonify(record_service.simulate_identify(person_id))

# Web操作页面
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8090, debug=True)