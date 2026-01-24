import os

import pymysql
from sqlalchemy import *

from Common import Log
from Conf.Config import Config


class CheckDBdate():

    def __init__(self, sqlfile=None, env='release'):
        self.log = Log.MyLog()
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        self.url = conf.get_conf(env, 'esurl')
        engines = "mysql+pymysql://" + self.dbuser + ":" + self.dbpw + \
                  "@" + self.dbip + "/" + self.dbname + "?charset=utf8"
        engine = create_engine(engines, max_overflow=5)
        self.conn = engine.connect()
        self.sqlfile = sqlfile

    def get_sqllist(self):
        """
        读取到预设的sql
        :return:
        """
        # f= self.sqlfile
        f = open(str(os.path.abspath(os.path.join(os.path.dirname(
            __file__), os.pardir)) + '/Params/SqlScript/' + self.sqlfile), encoding='utf-8')
        # print("sql文件位置--------------,",f)
        line = f.readline()
        sqlall = ''
        while line:
            sqlall = sqlall + line.strip("\n").strip("\t")
            line = f.readline()
        sqlalllist = sqlall.split(';')
        return sqlalllist

    def exsqlgetdata(self, sqltext, env, doc=""):
        '''
        执行sql,返回数据
        :param sqltext:
        :param env:
        :param doc:
        :return:
        '''
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        engines = "mysql+pymysql://" + self.dbuser + ":" + self.dbpw + \
                  "@" + self.dbip + "/" + self.dbname + "?charset=utf8"
        engine = create_engine(engines, max_overflow=5)
        self.conn = engine.connect()

        self.log.info('{0},执行sql:{1}'.format(doc, sqltext))
        try:
            result = self.conn.execute(text(sqltext))
            row = result.fetchall()
            self.log.info('{0},执行sql成功！！！返回数据：{1}'.format(doc, row))
            return row
            # self.conn.commit()
        except BaseException:
            self.log.info('{0},执行sql失败！！！'.format(doc))
            raise

    def exsqlex(self, sqltext, env, doc=""):
        '''
        执行sql，无返回数据
        :param sqltext:
        :param env:
        :param doc:
        :return:
        '''
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        engines = "mysql+pymysql://" + self.dbuser + ":" + self.dbpw + \
                  "@" + self.dbip + "/" + self.dbname + "?charset=utf8"
        engine = create_engine(engines, max_overflow=5)
        self.conn = engine.connect()

        self.log.info('{0},执行sql:{1}'.format(doc, sqltext))
        try:
            self.log.info('sqltext:%s' % sqltext)
            self.log.info('type(sqltext): %s ' % type(sqltext))
            # if sqltext.startswith('length'):
            #     result= self.conn.execute(sqltext)
            # else:
            # print("sqltext",sqltext)
            for one in sqltext.split(";"):
                print(one)
                if str(one).__len__() > 0:
                    result = self.conn.execute(text(one))
                    # self.conn.commit()
            self.log.info('{0},执行sql成功！！！'.format(doc))
            # self.conn.commit()
        except BaseException:
            # self.conn.commit()
            self.log.info('{0},执行sql失败！！！'.format(doc))
            raise

    def exsqlex02(self, sqltext, env, doc="", param=None):
        '''
                执行sql，无返回数据
                :param sqltext:
                :param env:
                :param doc:
                :return:
                '''
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        engines = "mysql+pymysql://" + self.dbuser + ":" + self.dbpw + \
                  "@" + self.dbip + "/" + self.dbname + "?charset=utf8"
        engine = create_engine(engines, max_overflow=5)
        self.conn = engine.connect()

        self.log.info('{0},执行sql:{1}'.format(doc, sqltext))
        try:

            if param:
                self.log.info('{0},{1}带参数执行'.format(sqltext, param))
                result = self.conn.execute(TEXT(sqltext), param)
                self.log.info(
                    '{0},{1}带参数执行结果{2}'.format(
                        sqltext, param, result))
            else:
                result = self.conn.execute(sqltext)
            self.log.info('{0},执行sql成功！！！'.format(doc))
            # self.conn.commit()
        except BaseException:
            self.log.info('{0},执行sql失败！！！'.format(doc))
            raise

    def exsql_like(self, sqltext, env, likedata, doc=""):
        '''
        执行模糊sql,无返回
        :param sqltext:
        :param env:
        :param likedata:
        :param doc:
        :return:
        '''
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        engines = "mysql+pymysql://" + self.dbuser + ":" + self.dbpw + \
                  "@" + self.dbip + "/" + self.dbname + "?charset=utf8"
        engine = create_engine(engines, max_overflow=5)
        self.conn = engine.connect()
        self.likedata = likedata

        s = text(sqltext)

        self.log.info('{0},执行sql:{1}'.format(doc, sqltext))
        try:
            self.conn.execute(text(s), likedata=self.likedata + "%")
            self.log.info('{0},执行sql成功！！！'.format(doc))
        except BaseException:
            self.log.info('{0},执行sql失败！！！'.format(doc))
            raise

    def import_sql_file(self, file, env):
        """
        执行sql文件
        :param file:
        :param env:
        :return:
        """
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = int(conf.get_conf(env, 'dbport'))
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        connection = pymysql.connect(
            host=self.dbip,
            user=self.dbuser,
            password=self.dbpw,
            database=self.dbname,
            port=self.dbport,
            charset='utf8')
        cur = connection.cursor()
        f = open(file, encoding='utf-8')
        line = f.readline()
        sqltext = ''
        while line:
            sqltext = sqltext + line.strip("\n").strip("\t")
            line = f.readline()
        sqllist = sqltext.split(';')
        for li in sqllist:
            if len(li) > 0:
                cur.execute(li)
        cur.close()
        connection.commit()

    def getdata_sql(self, sqltext, env, doc):
        """
        执行sql文件
        :param file:
        :param env:
        :return:
        """
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = int(conf.get_conf(env, 'dbport'))
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        connection = pymysql.connect(
            host=self.dbip,
            user=self.dbuser,
            password=self.dbpw,
            database=self.dbname,
            port=self.dbport,
            charset='utf8')
        cur = connection.cursor()
        self.log.info('{0},执行sql:{1}'.format(doc, sqltext))
        try:
            result_row = cur.execute(sqltext)
            row = cur.fetchall()
            return row
            self.log.info('{0},执行sql成功！！！'.format(doc))
        except BaseException:
            self.log.info('{0},执行sql失败！！！'.format(doc))
            raise
        cur.close()
        connection.commit()


if __name__ == '__main__':
    sqltext = "select count(1) from (SELECT COUNT(aa.alert_id) num,bb.precinct_id precinctId,bb.precinct_name precinctName FROM alert_alerts aa  RIGHT JOIN ( SELECT p.precinct_id,p.precinct_name  FROM t_cfg_precinct p WHERE p.up_precinct_id = '01' and p.isdel=0 ) bb ON aa.room_id LIKE CONCAT(bb.precinct_id,'%') left join t_cfg_site s on aa.room_id like  CONCAT(s.site_id , '%' )  and s.isdel=0  WHERE aa.alert_level =1 AND aa.show_type = 0 	AND s.site_type in (2)  GROUP BY precinctId ) t ;"
    env = 'release'
    print(CheckDBdate().getdata_sql(sqltext, env, "test")[0][0])
