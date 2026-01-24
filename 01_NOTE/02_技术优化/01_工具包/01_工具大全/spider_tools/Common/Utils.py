import xlrd3
import os
import uuid
import hashlib
import json
# from Common.Log import MyLog
import time
from datetime import datetime, timedelta
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode

from asptest.common.jsonutil import get_value_from_json,convert_data_to_unicode_escape
import asptest.common.constant as constant


from asptest.common import xutils

def get_excel_data(service, funcname):
    #dataFile = os.path.join(os.path.abspath("."), "testdata", "energy_puetestdata.xlsx")
    dataFile = str(
        os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                os.pardir))) + "/Params/testdata/" + "energy_puetestdata.xlsx"
    # print(dataFile)
    book = xlrd3.open_workbook(dataFile)
    sheet_data = book.sheet_by_name(service)
    case_data = []
    d = []
    # funcname='告警上报'
    # print(sheet_data.nrows)
    for i in range(1, sheet_data.nrows):
        d = sheet_data.row_values(i)
        # print(d[4])
        if(d[4] == funcname):
            # print(d)
            case_data.append(d)
    # MyLog.debug(case_data)
    return case_data


def get_need_uuid4():
    # 对应java import java.util.UUID; UUID.randomUUID().toString().replace("-",
    # "")
    uid4 = uuid.uuid4()
    uid = str(uid4).replace("-", "")
    return uid

def md5_encrypt(text):
    """
    # 调用函数进行加密
    plaintext = "Hello World"
    encrypted_text = md5_encrypt(plaintext)
    print("原始文本：", plaintext)
    print("加密结果：", encrypted_text)
    """
    # 创建md5对象
    md5 = hashlib.md5()
    # 将文本转换为字节类型并更新到md5对象中
    md5.update(text.encode('utf-8'))
    # 获取加密后的结果（16位小写）
    encrypted_result = md5.hexdigest()[:32]
    return encrypted_result

def get_sqllist(sqlfile):
    """
    读取到预设的sql
    :return:
    """
    data_file = os.path.join(os.path.dirname(__file__), "../Params/SqlScript/", sqlfile)

    f = open(str(data_file), encoding='utf-8')
    print("sql文件位置--------------,", f)
    line = f.readline()
    sqlall = ''
    while line:
        sqlall = sqlall + line.strip("\n").strip("\t")
        line = f.readline()
    sqlalllist = sqlall.split(';')
    return sqlalllist


### chenzw
def last_month_str():
    now = datetime.now()
    first_day_of_current_month = now.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    previous_year = str(last_day_of_previous_month.year)
    previous_month = str(last_day_of_previous_month.month).rjust(2,'0')
    last_month_str = previous_year+'-'+previous_month
    return last_month_str

def last_month_compact_str():
    now = datetime.now()
    first_day_of_current_month = now.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    previous_year = str(last_day_of_previous_month.year)
    previous_month = str(last_day_of_previous_month.month).rjust(2, '0')
    last_month_compact_str = previous_year+previous_month
    return last_month_compact_str

def last_day_str():
    today = time.time()
    yesterday = today - 86400
    last_day_str = time.strftime('%Y-%m-%d', time.localtime(yesterday))
    return last_day_str

def last_day_compact_str():
    today = time.time()
    yesterday = today - 86400
    last_day_compact_str = time.strftime('%Y%m%d', time.localtime(yesterday))
    return last_day_compact_str


def encrypt(data):
    # 定义密钥和初始化向量, 动环项目当前如下
    AES_KEY = b'W6Mzcjb7hQOdq0305m7RAbuywXHpfNKn'
    IV = b'AEEocbLFuazMreUp'
    # 创建 AES cipher 对象
    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    # 对数据进行填充
    padded_data = pad(data.encode('utf-8'), AES.block_size)
    # 加密数据
    encrypted_data = cipher.encrypt(padded_data)
    # 将加密后的数据编码为 Base64 字符串
    return b64encode(encrypted_data).decode('utf-8')


def decrypt(data):
    # 定义密钥和初始化向量, 动环项目当前如下
    AES_KEY = b'W6Mzcjb7hQOdq0305m7RAbuywXHpfNKn'
    IV = b'AEEocbLFuazMreUp'
    # 解码 Base64 编码的数据
    encrypted_data = b64decode(data)
    # 创建 AES Cipher 对象
    cipher = AES.new(AES_KEY, AES.MODE_CBC, IV)
    # 解密数据
    decrypted_data = cipher.decrypt(encrypted_data)
    # 移除填充
    unpadded_data = unpad(decrypted_data, AES.block_size)
    # 返回解密后的字符串
    return unpadded_data.decode('utf-8')

def convert_datatype_by_flag_dh(src_value):
    '''根据数据开头的标志将字符串转换为制定类型的数据，一般放在变量替换之后调用
    : 参数:
      - src_value: 需要转换的字符串原始值
    : 返回值：转换后的数据
    动环扩展： 加入(encrypt)模式的传输层关键字段加解密的校验，例如手机号、邮箱等
    '''

    if isinstance(src_value, str) == False:
        return src_value

    src_value = src_value.lstrip()

    if src_value.lower().startswith('(int)'):
        src_value = int(src_value[5:])
    elif src_value.lower().startswith('(float)'):
        src_value = float(src_value[7:])
    elif src_value.lower().startswith('(bool)'):
        if 'true' in src_value.lower():
            src_value = True
        else:
            src_value = False
    elif src_value.lower().startswith('(list)'):
        data = src_value[6:]
        if (len(data) == 0):
            src_value = []
        elif data.lower().startswith('['):
            # src_value = eval(data)
            src_value = json.loads(data)
        else:
            src_value = data.split(",")
    elif src_value.lower().startswith('(dict)'):
        data = src_value[6:]
        #         src_value = eval(data)
        src_value = json.loads(data)
    elif src_value.lower().startswith('(jfile)'):
        path = os.path.abspath(src_value[7:])
        # 需要外层代码处理好路径
        #         path = os.path.join(os.path.abspath(".") , "resoure", src_value.lstrip('(jfile)'))
        with open(path, encoding='utf-8') as rfile:
            data = rfile.readlines()
        src_value = data[0]
        src_value = xutils.handle_regx_in_text(src_value)
    elif src_value.lower().startswith('{') & src_value.lower().endswith('}'):
        src_value = eval(src_value)
    elif src_value.lower().startswith('[') & src_value.lower().endswith(']'):
        src_value = eval(src_value)
    elif src_value.lower().startswith('(encrypt)'):
        data = src_value[9:]
        src_value = encrypt(data)
    else:
        pass
    if src_value == u"None":
        src_value = None

    return src_value

def convert_dictInlist_values_to_str(data):
    """
    将字典列表中的所有值转换为字符串格式。
    接口响应数据皆为字符串类型，sql查询结果则不一定，目的是将sql查询出的字典结果转化为字符串类型

    :param data: 包含字典的列表
    :return: 转换后的字典列表
    """
    def convert_value(value):
        if value is None:
            return None
        elif isinstance(value, list):
            return [str(item) for item in value]
        else:
            return str(value)

    return [{k: convert_value(v) for k, v in dicta.items()} for dicta in data]


def comparison_value_in_dicts(obj1, obj2, excludes=None):
    """ 在一些测试场景中，需要用到数据库查询结果与消息体中的部分字段进行比较，其逻辑要求如下：
    : 1)消息字段与数据表字段定义符合驼峰规则映射，即消息按大小写驼峰，数据库表字段为下划线驼峰
    : 2)校验逻辑以消息体为基础，即遍历消息体的所有字段，数据表多余字段不处理
    : 3)可以指定不需要校验的字段列表
    : 4)对于数据库查询结果为时间类型的，需要进行字符串转换后比较
    : 5）测试用例数据中一般不直接调用，由业务层二次封装后调用

    : 参数:
        - obj1: 比较对象1，通常响应消息某个节点的值
        - obj2: 比较对象2，某个表中记录查询结果
        - excludes: 对象1中某些不不校验的特殊字段

    : 返回值：无，存在键值不相等时，直接校验失败.
    : 方法使用实例:
        # 查询站点下的所有模组，模组名称和模组ID
        sql = '''
        SELECT
          config_id AS systemId,
          NAME AS systemName
        FROM
          cold_source_config
        WHERE
          parent_id  = 'b0eb65b7-29cd-4bfa-9256-6e7b1ec57e3e'
          AND TYPE = '1';
        '''

        expected = conn_obj.select(sql, isdict=True)

        for i, j in zip(action.resp_body['data'], expected):
            comparison_value_in_dicts(i, j)
    """
    if excludes is None:
        excludes = []

    if not (isinstance(obj1, dict) and isinstance(obj2, dict)):
        assert False, '比较类型不正确'

    for key in obj1:
        if key in excludes:
            continue

        if key not in obj2:
            assert False, f'数据库sql结果中缺少对应字段：{key}'

        obj1_value = obj1[key]
        obj2_value = obj2[key]

        if isinstance(obj2_value, datetime):
            obj2_value = obj2_value.strftime('%Y-%m-%d %H:%M:%S')

        assert obj1_value == obj2_value, f'字段 {key} 的值不匹配：{obj1_value} != {obj2_value}'


def assert_values_to_json_obj_dh(json_obj, kvs, params=None):
    """通过键值对校验一个字典对象的中某些xpath路径的值，可以处理参数.

    : 参数:
        - json_obj: 待校验的字典对象，如响应消息
        - kvs: 字符串或列表对象，字符串通过‘|’分割；每一个值是一个键值对，其值会进行数据转换，如(del)开头将会删除，(int)开头会转为int值
        - params: 当kvs是字符串时，会替换其中的正则表达式

    : 返回值，无
    动环扩展： key=value中的value为*时，不对值进行校验（即只校验字段存在）
    """
    if isinstance(kvs, str):
        kvs = xutils.handle_regx_in_text(kvs, params)
        kvs = kvs.split(constant.DATA_SPLIT)

    if isinstance(kvs, (list, tuple)) is False:
        raise Exception("请输入正确的期望数据")

    for kv in kvs:
        expected = kv.split('=')

        expect_value = expected[1].lstrip()

        expect_value = xutils.convert_datatype_by_flag(expect_value)

        actual_value = get_value_from_json(json_obj, expected[0].strip())

        if expect_value != '*':
            assert actual_value == expect_value, "resp=%s,json_path=%s, expect=%s, real=%s" % (
                convert_data_to_unicode_escape(json_obj), expected[0].strip(), expect_value, actual_value)