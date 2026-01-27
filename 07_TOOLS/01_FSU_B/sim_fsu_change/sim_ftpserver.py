#-*- coding:utf-8 *-*
from pyftpdlib.authorizers import DummyAuthorizer,AuthenticationFailed
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from utils.logger import logger
from module import queryFtpPassword,queryAllFSUAccount,queryFsuId
import os

'''权限
"e" =更改目录（CWD，CDUP命令）
"l" =列表文件（LIST，NLST，STAT，MLSD，MLST，SIZE命令）
"r" =从服务器检索文件（RETR命令）
"a" =将数据追加到现有文件（APPE命令）
"d" =删除文件或目录（DELE，RMD命令）
"f" =重命名文件或目录（RNFR，RNTO命令）
"m" =创建目录（MKD命令）
"w" =将文件存储到服务器（STOR，STOU命令）
"M"=更改文件模式/权限（SITE CHMOD命令）
"T"=更改文件修改时间（SITE MFMT命令）
'''

class DummyAuthorizer2(DummyAuthorizer):
    def validate_authentication(self, username, password, handler):
        msg = "Authentication failed."
        if not self.has_user(username):
            if username == 'anonymous':
                msg = "Anonymous access not allowed."
                raise AuthenticationFailed(msg)
            #没有用户，就加这个用户，但密码需要后续到数据库校验
            fsuid = queryFsuId(username)
            authorizer.add_user(username, 'aspire+888', './ftpfolder/{}'.format(fsuid), perm='elradfmwM')
        if username != 'anonymous':
            #if self.user_table[username]['pwd'] != password:
            db_password =queryFtpPassword(username)
            logger.debug("FTP user:%s, db_password:%s, input_password=%s" % (username,db_password,password))
            if  db_password != password:
                raise AuthenticationFailed(msg)

#实例化虚拟用户，这是FTP验证首要条件
authorizer = DummyAuthorizer2()

#添加用户权限和路径，括号内的参数是(用户名， 密码， 用户目录， 权限)
#authorizer.add_user('user', 'root', './ftpfolder', perm='elradfmwM')
for li in queryAllFSUAccount():
    (username,password) = li
    fsuid = queryFsuId(username)
    ftp_home = './ftpfolder/{}'.format(fsuid)
    if not os.path.exists(ftp_home):
        os.makedirs('{}/Alarm'.format(ftp_home))
        os.makedirs('{}/Measurement'.format(ftp_home))
        os.makedirs('{}/Config'.format(ftp_home))
    authorizer.add_user(username, 'aspire+888', ftp_home, perm='elradfmwM')
logger.info("Init DB authorizer: %s" % authorizer.user_table)

#添加匿名用户 只需要路径
authorizer.add_anonymous('./ftpfolder')

#初始化ftp句柄
handler = FTPHandler
handler.authorizer = authorizer

#添加被动端口范围
#handler.passive_ports = range(2000, 2333)

#监听ip 和 端口,因为linux里非root用户无法使用21端口，所以我使用了2121端口
server = FTPServer(('0.0.0.0', 21), handler)

#开始服务
server.serve_forever()