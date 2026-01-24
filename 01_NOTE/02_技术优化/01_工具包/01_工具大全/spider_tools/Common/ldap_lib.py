# -*- coding: utf-8 -*-
import time

from ldap3 import MODIFY_REPLACE
from ldap3 import Server, Connection, ALL
from ldap3.utils.hashed import *

conn = None
from asptest.common.logservice import LogBuilder

logger = LogBuilder.get_instance()


def get_global_ldap_variable():
    '''从RF框架取G_Ldap全局变量，取到则返回
    如果没有取到，即为独立执行测试，此时使用本机ldap数据库，日志输出到stdout'''
    # try:
    #    G_Ldap = BuiltIn().get_library_instance('BuiltIn').get_variable_value('&{G_Ldap}')
    # except Exception as e:
    # G_Ldap = {'host':'192.168.56.3','port':'389','base':'dc=migu,dc=cn','username':'admin','password':'password'}
    G_Ldap = {'host': '10.1.203.38', 'port': '389', 'base': 'dc=migu,dc=cn', 'username': 'admin',
              'password': 'UmS$dp#23-04'}
    return G_Ldap


def get_ldap_conn():
    global conn
    G_Ldap = get_global_ldap_variable()
    if conn == None:
        server = Server(G_Ldap['host'], port=int(G_Ldap['port']),
                        get_info=ALL)
        conn = Connection(server,
                          'cn={},{}'.format(G_Ldap['username'], G_Ldap['base']),
                          G_Ldap['password'],
                          auto_bind=True)
    return conn


def add_user(user, password='123456', name=u'姓名', company=u'咪咕文化',
             dept=u'市场三部', project=u'p1', ou=u'migu.Inc',
             employee_type=u'user', namespace=u'miguAdmin2', o=u'migu.cn'):
    '''project=p1,p2,p3 (受组织mkgu初始化时的影响);   
    employee_type＝admin即根账号'''
    G_Ldap = get_global_ldap_variable()
    if not user_exist(user):
        conn = get_ldap_conn()
        if project.find(',') != -1:
            project = project.split(',')
        ou_list = []
        if ou.find(',') != -1:
            ou_list = ou.split(',')
        else:
            ou_list.append(ou)
        for ou in ou_list:
            conn.add('uid={},uid={},ou={},{}'.format(user, namespace, ou, G_Ldap['base']),
                     'inetOrgPerson',
                     {'sn': name, 'cn': user, 'ou': ou, 'uid': user,
                      'departmentNumber': dept,
                      'userPassword': password,
                      'project': project,
                      'mobile': '13500000000',
                      'mail': '{}@migutest.cn'.format(user),
                      'employeeType': '{}.{}'.format(employee_type, namespace),
                      'jpegPhoto': 'base64',
                      'o': o,
                      'createTime': time.strftime('%Y-%m-%dT%H:%M:%S:000Z',
                                                  time.localtime()),
                      'updateTime': time.strftime('%Y-%m-%dT%H:%M:%S:000Z',
                                                  time.localtime()),
                      }
                     )
            logger.info(
                u'ldap数据库用户添加成功: uid={}, namespace={}, ou={}'.format(user, namespace, ou))
    else:
        logger.info(u'ldap数据库用户已存在,不用再次添加: uid=%s' % user)


def user_exist(user):
    '''通过接口创建的用户没有ou属性，所以查找时不能带ou'''
    G_Ldap = get_global_ldap_variable()
    conn = get_ldap_conn()
    conn.search(G_Ldap['base'],
                '(&(objectclass=inetOrgPerson)(uid={}))'.format(
                    user, ),
                attributes=['*', ])
    entries = conn.entries
    if len(entries) != 0:
        logger.info(u'ldap数据库用户存在： uid=%s' % user)
        logger.debug(entries[0].entry_to_json())
        return True
    else:
        logger.info(u'ldap数据库用户不存在： uid=%s' % user)
        return False


def get_password(user):
    ''' 有些用户没有ou属性，所以直接查uid就成了'''
    G_Ldap = get_global_ldap_variable()
    conn = get_ldap_conn()
    conn.search(G_Ldap['base'],
                '(&(objectclass=inetOrgPerson)(uid={}))'.format(
                    user, ),
                attributes=['*', ])
    entries = conn.entries
    if len(entries) != 0:
        password = entries[0].userPassword
        logger.debug(entries[0].entry_to_json())
        logger.info(u'ldap数据库用户密码获取成功: uid={} => {}'.format(user, password))
        return password
    else:
        return None


def modify_replace_user_attr(user, ou=u'migu.Inc', namespace=u'miguAdmin2', *args):
    '''修改用户属性，只做MODIFY_REPLACE操作，不做MODIFY_ADD/MODIFY_DELETE操作
    可用的属性：userPassword, mobile,mail, jpegPhoto, sn(即name), o(即company), ou(即department)
    传参格式例如：'userPassword=123456', sn=chenzw, o=migu, ou=testDept, mobile=1351000000,13510000001
                mail=abc@abc.cn,abc2@abc.cn
    '''
    G_Ldap = get_global_ldap_variable()
    conn = get_ldap_conn()
    for li in args:
        key, value = li.split('=')
        value_list = value.split(',')
        if user == namespace:  # 根账号的修改
            conn.modify('uid={},ou=migu.Inc,{}'.format(
                namespace, G_Ldap['base']),
                {key: [(MODIFY_REPLACE, value_list)]})
        else:
            conn.modify('uid={},uid={},ou=migu.Inc,{}'.format(
                user, namespace, G_Ldap['base']),
                {key: [(MODIFY_REPLACE, value_list)]})


def modify_user_password(user, password='123456', ou=u'migu.Inc', namespace=u'miguAdmin2'):
    modify_replace_user_attr(user, ou, namespace, 'userPassword={}'.format(password))


def get_user_entries_obj(user):
    G_Ldap = BuiltIn().get_library_instance(
        'BuiltIn').get_variable_value('&{G_Ldap}')
    conn = get_ldap_conn()
    conn.search(G_Ldap['base'],
                '(&(objectclass=inetOrgPerson)(uid={}))'.format(user, ),
                attributes=['*', ])
    entries = conn.entries
    logger.info(entries)
    if len(entries) != 0:
        # logger.warn(entries[0].cn)
        # logger.warn(type(entries[0].cn))
        # logger.warn(dir(entries[0].cn))
        # logger.warn(entries[0].cn.value)
        return entries[0]
    else:
        return None


def delete_user(user, ou=u'migu.Inc', namespace=u'alauda'):
    G_Ldap = get_global_ldap_variable()
    if user_exist(user):
        conn = get_ldap_conn()
        conn.delete('uid={},uid={},ou={},{}'.format(
            user, namespace, ou, G_Ldap['base']))
        logger.info(u'ldap数据库用户已删除: uid={}'.format(user))


def ldap_encrypt_password(password, algorithm='SHA1', salt=None):
    '''加密算法有: MD5,SHA1,SHA256,SHA384,SHA512'''
    if salt != None:
        salt = str(salt)
    result = hashed(algorithm=str(algorithm), value=str(password), salt=salt)
    return result


def update_all_user_password(new_password = '6475e42605f5ded2b306f03063334aae'):
    '''有时需要批量更新集团数据库'''
    G_Ldap = get_global_ldap_variable()
    conn = get_ldap_conn()
    conn.search('ou=migu.Inc,dc=migu,dc=cn', '(objectClass=person)', attributes=['*', ])
    result = conn.entries
    for entry in result:
        #print(entry.uid,entry.userPassword)
        #if entry.uid == 'chenzw223':
        #    modify_user_password(entry.uid, password=new_password, ou=u'migu.Inc', namespace=u'alauda')
        #    print('11111111111111111111111111')
        modify_user_password(entry.uid, password=new_password, ou=u'migu.Inc', namespace=u'alauda')
        print(f'用户{entry.uid}的密码修改为：{new_password}')

def count_ldap_user():
    G_Ldap = get_global_ldap_variable()
    conn = get_ldap_conn()
    conn.search('ou=migu.Inc,dc=migu,dc=cn', '(objectClass=person)', attributes=['*', ])
    result = conn.entries
    print(len(result))
if __name__ == "__main__":
    # password = ldap_encrypt_password('123456')
    # print password
    # user_exist(u'user_tobe_delete')
    user_exist('alauda')
    some_pass = '!sl!6^ig*UhUGLtM'
    md5_pass = ldap_encrypt_password(some_pass, 'md5')
    print(md5_pass)
    sha1_pass = ldap_encrypt_password(some_pass)
    #print(sha1_pass)
    #print(get_password('alauda'))
    # delete_user('user_tobe_delete')
    # update_all_user_password(new_password = '6475e42605f5ded2b306f03063334aae')
    count_ldap_user()