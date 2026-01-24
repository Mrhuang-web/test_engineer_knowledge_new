class MysqlConnect:
    """MySQL连接"""
    """match_mode - 为0站点匹配，为1机房匹配 - 为2走原逻辑（需要接入设备的机房才可以匹配）"""

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

        # 数据库连接
        conf = Config()
        self.dbip = conf.get_conf(env, 'dbip')
        self.dbport = conf.get_conf(env, 'dbport')
        self.dbname = conf.get_conf(env, 'dbname')
        self.dbuser = conf.get_conf(env, 'dbuser')
        self.dbpw = conf.get_conf(env, 'dbpw')
        self.url = conf.get_conf(env, 'esurl')

        # 创建引擎
        engines = f"mysql+pymysql://{urlquote(self.dbuser)}:{urlquote(self.dbpw)}@{self.dbip}:{self.dbport}/{urlquote(self.dbname)}?charset=utf8"
        self.engine = create_engine(engines, max_overflow=5)
        self.conn = self.engine.connect()

        # SQL文件路径
        sql_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))),
            'project_tools', 'Common', 'SQL', 'selectForESList.sql'
        )
        self.sql_file = open(sql_path, encoding='utf-8')

    def get_sql_list(self) -> List[str]:
        """读取SQL文件 - 保留原始逻辑"""
        content = self.sql_file.read()
        return [sql.strip() for sql in content.split(';') if sql.strip()]

    def get_provincedata(self, sql_index: int) -> List[Tuple]:
        """执行查询 - 保留原始逻辑"""
        sql_list = self.get_sql_list()
        if sql_index >= len(sql_list):
            print(f"SQL索引 {sql_index} 超出范围")
            return []

        sql = sql_list[sql_index]
        params = {'precinct_id': self.precinct_id + '%'}

        if sql_index == 1:
            params.update({'mete_code': self.mete_code, 'device_id': self.device_id})
        elif sql_index == 2:
            params.update({'mete_code': self.mete_code})

        result = self.conn.execute(text(sql), params)
        return result.fetchall()

    def insert_esdata_device(self) -> List[Tuple]:
        """插入设备数据 - 保留原始逻辑"""
        # todo 待完善[目前展示只有0和else两种模式]
        if self.match_mode == 0:
            print("全量站点匹配==========")
            sql_index = 5
        elif self.match_mode == 1:
            print("全量机房匹配==========")
            sql_index = 6
        elif self.match_mode == 2:
            if self.device_id == '1' and self.mete_code == '000000':
                print("机房全量查询未传设备==========")
                sql_index = 4
            else:
                print("机房全量查询==========")
                sql_index = 0

        data = self.get_provincedata(sql_index)
        print(f"预计写入数据条数========== {len(data)}")
        return data