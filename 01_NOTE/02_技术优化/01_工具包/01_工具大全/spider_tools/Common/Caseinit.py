# -*- coding: utf-8 -*-
from Params.params import readYml
from Conf.Config import Config
from Common import Consts
from Common import Assert
from Common.Getmysqldata import CheckDBdate


class Caseinit:
    def __init__(self, yml_filename):
        self.test = Assert.Assertions()
        self.yml_file = yml_filename
        self.env = Consts.API_ENVIRONMENT_RELEASE
        self.host = Config().get_conf(Consts.API_ENVIRONMENT_RELEASE, 'host')
        self.exsql = CheckDBdate()
        self.req_url = 'http://' + self.host + ':'
        self.url = readYml(self.yml_file).url
        self.params = readYml(self.yml_file).data
        self.headers = readYml(self.yml_file).header
        self.exsqldata = readYml(self.yml_file).exsql
        self.expectjson = readYml(self.yml_file).expectjson
