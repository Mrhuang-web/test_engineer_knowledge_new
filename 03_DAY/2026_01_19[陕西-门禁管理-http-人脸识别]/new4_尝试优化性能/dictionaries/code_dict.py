# 返回码字典映射文件
# 定义所有返回码和对应的说明

code_mapping = {
    # 成功返回码
    'LAN_SUS-0': {
        'result': 1,
        'success': True,
        'msg': '操作成功'
    },
    
    # 通用错误返回码
    'LAN_EXP-1000': {
        'result': 0,
        'success': False,
        'msg': '未知异常'
    },
    
    'LAN_EXP-1001': {
        'result': 0,
        'success': False,
        'msg': '密码错误，请检查密码正确性'
    },
    
    'LAN_EXP-1002': {
        'result': 0,
        'success': False,
        'msg': 'pass参数异常'
    },
    
    'LAN_EXP-1003': {
        'result': 0,
        'success': False,
        'msg': '接口服务未设置密码，请先设置密码'
    },
    
    'LAN_EXP-1004': {
        'result': 0,
        'success': False,
        'msg': '设备已被禁用，请先启用再做其它操作'
    },
    
    'LAN_EXP-1005': {
        'result': 0,
        'success': False,
        'msg': '设备正忙，请稍后再试'
    },
    
    'LAN_EXP-1006': {
        'result': 0,
        'success': False,
        'msg': 'The XX method is not supported.'
    },
    
    # 设备管理类错误返回码
    'LAN_EXP-2001': {
        'result': 0,
        'success': False,
        'msg': 'oldPass参数异常'
    },
    
    'LAN_EXP-2002': {
        'result': 0,
        'success': False,
        'msg': 'newPass参数异常'
    },
    
    'LAN_EXP-2003': {
        'result': 0,
        'success': False,
        'msg': '密码不允许为空或空格'
    },
    
    'LAN_EXP-2004': {
        'result': 0,
        'success': False,
        'msg': '新密码不允许为空或空格'
    },
    
    'LAN_EXP-2005': {
        'result': 0,
        'success': False,
        'msg': '旧密码错误'
    },
    
    'LAN_EXP-2006': {
        'result': 0,
        'success': False,
        'msg': '初次设置密码时，请确保oldPass、newPass相同'
    },
    
    'LAN_EXP-2049': {
        'result': 0,
        'success': False,
        'msg': 'timestamp参数异常'
    },
    
    'LAN_EXP-2050': {
        'result': 0,
        'success': False,
        'msg': 'timestamp时间格式错误'
    },
    
    'LAN_EXP-2188': {
        'result': 0,
        'success': False,
        'msg': 'languageType参数异常'
    },
    
    'LAN_EXP-2189': {
        'result': 0,
        'success': False,
        'msg': '不支持的语言类型'
    },
    
    'LAN_EXP-2201': {
        'result': 0,
        'success': False,
        'msg': 'timezone参数异常'
    },
    
    'LAN_EXP-2200': {
        'result': 0,
        'success': False,
        'msg': 'timezone参数不合法'
    },
    
    'LAN_EXP-2063': {
        'result': 0,
        'success': False,
        'msg': 'callbackUrl参数异常'
    },
    
    'LAN_EXP-2099': {
        'result': 0,
        'success': False,
        'msg': '请输入正确格式的callbackUrl地址'
    },
    
    'LAN_EXP-2061': {
        'result': 0,
        'success': False,
        'msg': 'url参数异常'
    },
    
    'LAN_EXP-2064': {
        'result': 0,
        'success': False,
        'msg': '请输入正确格式的url地址'
    },
    
    # 人员管理类错误返回码
    'LAN_EXP-3001': {
        'result': 0,
        'success': False,
        'msg': 'person参数异常'
    },
    
    'LAN_EXP-3002': {
        'result': 0,
        'success': False,
        'msg': 'person类json格式错误'
    },
    
    'LAN_EXP-3003': {
        'result': 0,
        'success': False,
        'msg': '人员ID(id)只允许数字0~9和英文字母，且最大长度为255'
    },
    
    'LAN_EXP-3004': {
        'result': 0,
        'success': False,
        'msg': 'name参数不能为空'
    },
    
    'LAN_EXP-3005': {
        'result': 0,
        'success': False,
        'msg': '人员ID已存在，请调用人员删除或者更新接口'
    },
    
    'LAN_EXP-3006': {
        'result': 0,
        'success': False,
        'msg': '数据库异常，人员注册失败'
    },
    
    'LAN_EXP-3007': {
        'result': 0,
        'success': False,
        'msg': 'id参数异常'
    },
    
    'LAN_EXP-3008': {
        'result': 0,
        'success': False,
        'msg': 'id参数不能为空'
    },
    
    'LAN_EXP-3009': {
        'result': 0,
        'success': False,
        'msg': '人员ID不存在，请先调用人员注册接口'
    },
    
    'LAN_EXP-3010': {
        'result': 0,
        'success': False,
        'msg': '数据库异常，人员删除失败'
    },
    
    'LAN_EXP-3011': {
        'result': 0,
        'success': False,
        'msg': 'facePermission参数不合法'
    },
    
    'LAN_EXP-3012': {
        'result': 0,
        'success': False,
        'msg': 'idCardPermission参数不合法'
    },
    
    'LAN_EXP-3013': {
        'result': 0,
        'success': False,
        'msg': 'faceAndCardPermission参数不合法'
    },
    
    'LAN_EXP-3015': {
        'result': 0,
        'success': False,
        'msg': 'personId参数异常'
    },
    
    'LAN_EXP-3016': {
        'result': 0,
        'success': False,
        'msg': 'personId参数不能为空'
    },
    
    'LAN_EXP-3017': {
        'result': 0,
        'success': False,
        'msg': '人员ID(personId)只允许数字-1，0~9和英文字母，且最大长度为255'
    },
    
    'LAN_EXP-3018': {
        'result': 0,
        'success': False,
        'msg': '每页显示数量length要求为(0,1000]的正整数'
    },
    
    'LAN_EXP-3019': {
        'result': 0,
        'success': False,
        'msg': '页码index为从0开始计数的整数，必须小于总页码'
    },
    
    'LAN_EXP-3031': {
        'result': 0,
        'success': False,
        'msg': 'startTime参数异常'
    },
    
    'LAN_EXP-3032': {
        'result': 0,
        'success': False,
        'msg': 'endTime参数异常'
    },
    
    'LAN_EXP-3033': {
        'result': 0,
        'success': False,
        'msg': 'startTime时间格式错误'
    },
    
    'LAN_EXP-3034': {
        'result': 0,
        'success': False,
        'msg': 'endTime时间格式错误'
    },
    
    'LAN_EXP-3035': {
        'result': 0,
        'success': False,
        'msg': 'endTime应大于startTime'
    },
    
    'LAN_EXP-3039': {
        'result': 0,
        'success': False,
        'msg': '人员ID(id)只允许数字-1，0~9和英文字母，且最大长度为255'
    },
    
    'LAN_EXP-3040': {
        'result': 0,
        'success': False,
        'msg': '设备人员数量过多，请使用分页查询'
    },
    
    # 照片管理类错误返回码
    'LAN_EXP-4002': {
        'result': 0,
        'success': False,
        'msg': 'faceId参数异常'
    },
    
    'LAN_EXP-2024': {
        'result': 0,
        'success': False,
        'msg': 'imgBase64参数异常'
    },
    
    'LAN_EXP-4005': {
        'result': 0,
        'success': False,
        'msg': '人员ID(personId)只允许数字0~9和英文字母，且最大长度为255'
    },
    
    'LAN_EXP-4006': {
        'result': 0,
        'success': False,
        'msg': '照片ID(faceId)只允许数字0~9和英文字母，且最大长度为255'
    },
    
    'LAN_EXP-4007': {
        'result': 0,
        'success': False,
        'msg': '照片ID已存在，请先调用删除或更新接口'
    },
    
    'LAN_EXP-4008': {
        'result': 0,
        'success': False,
        'msg': 'imgBase64不能为空'
    },
    
    'LAN_EXP-4009': {
        'result': 0,
        'success': False,
        'msg': 'isEasyWay参数不合法'
    },
    
    'LAN_EXP-4010': {
        'result': 0,
        'success': False,
        'msg': '提供的图片文件不完整或格式不正确'
    },
    
    'LAN_EXP-4011': {
        'result': 0,
        'success': False,
        'msg': '图片解析异常'
    },
    
    'LAN_EXP-4012': {
        'result': 0,
        'success': False,
        'msg': '注册照片已达到最大数量限定(3张)'
    },
    
    'LAN_EXP-4013': {
        'result': 0,
        'success': False,
        'msg': '数据库异常，照片注册失败'
    },
    
    'LAN_EXP-4016': {
        'result': 0,
        'success': False,
        'msg': 'faceId参数不能为空'
    },
    
    'LAN_EXP-4017': {
        'result': 0,
        'success': False,
        'msg': '照片ID不存在，请先调用照片注册接口'
    },
    
    'LAN_EXP-4018': {
        'result': 0,
        'success': False,
        'msg': '数据库异常，照片删除失败'
    },
    
    'LAN_EXP-4020': {
        'result': 0,
        'success': False,
        'msg': '数据库异常，照片更新失败'
    },
    
    'LAN_EXP-4025': {
        'result': 0,
        'success': False,
        'msg': '数据库异常'
    },
    
    'LAN_EXP-4030': {
        'result': 0,
        'success': False,
        'msg': '设备存储空间已满'
    },
    
    'LAN_EXP-4031': {
        'result': 0,
        'success': False,
        'msg': '该人员没有这个照片ID，请先调用照片注册接口'
    },
    
    'LAN_EXP-4032': {
        'result': 0,
        'success': False,
        'msg': 'imgBase64不能为gif图'
    },
    
    'LAN_EXP-4035': {
        'result': 0,
        'success': False,
        'msg': '提供的图片文件不完整或格式不正确'
    },
    
    'LAN_EXP-2218': {
        'result': 0,
        'success': False,
        'msg': '图片格式不支持'
    },
    
    'LAN_EXP-2241': {
        'result': 0,
        'success': False,
        'msg': '图片分辨率大于1080p'
    },
    
    # 算法报错
    'LAN_EXP-8006': {
        'result': 0,
        'success': False,
        'msg': '未检测到面部'
    },
    
    'LAN_EXP-8007': {
        'result': 0,
        'success': False,
        'msg': '检测到多个面部'
    },
    
    'LAN_EXP-8010': {
        'result': 0,
        'success': False,
        'msg': '人像过小'
    },
    
    'LAN_EXP-8013': {
        'result': 0,
        'success': False,
        'msg': '面部过大或面部不完整'
    },
    
    'LAN_EXP-8011': {
        'result': 0,
        'success': False,
        'msg': 'FaceSDK无法从照片中提到特征'
    },
    
    'LAN_EXP-8012': {
        'result': 0,
        'success': False,
        'msg': 'FaceSDK提取特征异常'
    },
    
    'LAN_EXP-8014': {
        'result': 0,
        'success': False,
        'msg': '人像偏转角度过大'
    },
    
    'LAN_EXP-8015': {
        'result': 0,
        'success': False,
        'msg': '人像面部太暗或太亮'
    },
    
    'LAN_EXP-8016': {
        'result': 0,
        'success': False,
        'msg': '人像清晰度过低'
    },
    
    'LAN_EXP-8017': {
        'result': 0,
        'success': False,
        'msg': '人像面部光线不均匀'
    },
    
    # 识别记录类错误返回码
    'LAN_EXP-5007': {
        'result': 0,
        'success': False,
        'msg': 'model参数不合法'
    },
    
    'LAN_EXP-5013': {
        'result': 0,
        'success': False,
        'msg': '数据库异常，识别记录删除失败'
    }
}