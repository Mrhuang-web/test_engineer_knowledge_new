from typing import List, Any
from sqlalchemy import create_engine, text
from urllib.parse import quote_plus as urlquote
from spider_tools.Conf.Config import Config  # 你的原始配置入口
import os


# ============ MySQL 连接 ============ #
class MysqlConnect:
    def __init__(self, precinct_id: str, env: str = 'release', **kwargs):
        self.precinct_id = precinct_id
        self.match_mode = kwargs.get('match_mode', 0)
        self.mete_code = kwargs.get('mete_code', '000000')
        self.EsTime = kwargs.get('EsTime', 'T23:50:50')
        self.MinVal = kwargs.get('MinVal', 1)
        self.MaxVal = kwargs.get('MaxVal', 1)
        self.device_id = kwargs.get('device_id', '1')
        self.del_col = kwargs.get('del_col', 'meteID')
        self.del_col_v = kwargs.get('del_clo_v', '1')

        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        self.url = conf.get_conf(env, 'esurl')

        engines = f"mysql+pymysql://{urlquote(self.dbuser)}:{urlquote(self.dbpw)}@{self.dbip}:{self.dbport}/{urlquote(self.dbname)}?charset=utf8"
        self.engine = create_engine(engines, max_overflow=5)
        self.conn = self.engine.connect()

        sql_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'Common', 'SQL', 'selectForESList.sql'
        )
        self.sql_file = open(sql_path, encoding='utf-8')

    def get_sql_list(self) -> List[str]:
        content = self.sql_file.read()
        return [sql.strip() for sql in content.split(';') if sql.strip()]

    def get_provincedata(self, sql_index: int) -> List[Any]:
        sql_list = self.get_sql_list()
        if sql_index >= len(sql_list):
            return []
        sql = sql_list[sql_index]
        params = {'precinct_id': self.precinct_id + '%'}
        if sql_index == 1:
            params.update({'mete_code': self.mete_code, 'device_id': self.device_id})
        elif sql_index == 2:
            params.update({'mete_code': self.mete_code})
        result = self.conn.execute(text(sql), params)
        return result.fetchall()

    def insert_esdata_device(self) -> List[Any]:
        if self.match_mode == 0:
            sql_index = 5
        elif self.match_mode == 1:
            sql_index = 6
        elif self.match_mode == 2:
            if self.device_id == '1' and self.mete_code == '000000':
                sql_index = 4
            else:
                sql_index = 0
        data = self.get_provincedata(sql_index)
        print(f"预计写入数据条数========== {len(data)}")
        return data
