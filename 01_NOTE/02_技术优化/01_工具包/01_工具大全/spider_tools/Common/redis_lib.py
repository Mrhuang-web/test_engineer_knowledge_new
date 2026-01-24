# -*- coding:utf-8 -*-
import redis3
from Conf.Config import Config


class RedisLib:

    def __init__(self, env='release', db=0):
        conf = Config()
        redis_host = conf.get_conf(env, 'redis_host')
        redis_port = int(conf.get_conf(env, 'redis_port'))
        redis_password = conf.get_conf(env, 'redis_password')
        self.conn = redis3.Redis(
            redis_host,
            redis_port,
            db=db,
            password=redis_password)

    def hget(self, name, key):
        '''我们的程序在写库时， key为"message",即字符前后都加了双引号'''
        if not key.startswith('"'):
            key = '"' + key + '"'
        result = self.conn.hget(name, key)
        if result is not None:
            return result.decode('utf-8')
        else:
            return result

    def hset(self, name, key, value):
        self.conn.hset(name. key, vlaue)

    def hset(self, name, key, value):
        return self.conn.hset(name, key, value)

    def hdel(self, name, *key):
        self.conn.hdel(name, *key)

    def hkeys(self, name):
        return self.conn.hkeys(name)


if __name__ == "__main__":
    r = RedisLib(env='release')
    # r.hdel("temperatureMeteExportResult:_chenzw105_2021-08-23",'"message"')
    print(r.hget("temperatureMeteExportResult:_chenzw105", 'message'))
