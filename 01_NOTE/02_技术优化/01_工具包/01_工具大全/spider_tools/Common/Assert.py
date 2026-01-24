# -*- coding: utf-8 -*-

"""
封装Assert方法

"""
from Common import Log
from Common import Consts
import json
from jsoncomparison import Compare, NO_DIFF


class Assertions:
    def __init__(self):
        self.log = Log.MyLog()

    def assert_code(self, code, expected_code):
        """
        验证response状态码
        :param code:
        :param expected_code:
        :return:
        """
        try:
            assert code == expected_code
            self.log.info(
                "code = expected_code, code is %s,expected_code is %s " %
                (code, expected_code))
            return True
        except BaseException:
            self.log.error(
                "statusCode error, expected_code is %s, statusCode is %s " %
                (expected_code, code))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_body(self, body, body_msg, expected_msg):
        """
        验证response body中任意属性的值
        :param body:
        :param body_msg:
        :param expected_msg:
        :return:
        """
        try:
            msg = body[body_msg]
            assert msg == expected_msg
            self.log.info(
                "msg == expected_msg,expected_msg is %s, body_msg is %s" %
                (expected_msg, msg))
            return True

        except BaseException:
            self.log.error(
                "Response body msg != expected_msg, expected_msg is %s, body_msg is %s" %
                (expected_msg, msg))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_in_text(self, body, expected_msg):
        """
        验证response body中是否包含预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            text = json.dumps(body, ensure_ascii=False)
            # print(text)
            assert expected_msg in text
            return True

        except BaseException:
            self.log.error(
                "Response body Does not contain expected_msg, expected_msg is %s" %
                expected_msg)
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_in_list(self, body, msg, expected_msg):
        """
        验证response body中是否包含预期数据
        :param body:[{},{}]
        :param msg:
        :param expected_msg:
        :return:
        """
        try:
            for precinct in body:
                if precinct[msg] == expected_msg:
                    return True
        except BaseException:
            self.log.error(
                "Response body Does not contain expected_msg, expected_msg is %s" %
                expected_msg)
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_text(self, body, expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert body == expected_msg

            return True

        except BaseException:
            self.log.error(
                "Response body != expected_msg, expected_msg is %s, body is %s" %
                (expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_text_str(self, body, expected_msg):
        """
        验证response body中是否等于预期字符串
        :param body:
        :param expected_msg:
        :return:
        """
        try:
            assert str(body) == str(expected_msg)

            return True

        except BaseException:
            self.log.error(
                "Response body != expected_msg, expected_msg is %s, body is %s" %
                (expected_msg, body))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_time(self, time, expected_time):
        """
        验证response body响应时间小于预期最大响应时间,单位：毫秒
        :param body:
        :param expected_time:
        :return:
        """
        try:
            assert time < expected_time
            return True

        except BaseException:
            self.log.error(
                "Response time > expected_time, expected_time is %s, time is %s" %
                (expected_time, time))
            Consts.RESULT_LIST.append('fail')

            raise

    def assert_json_same(self, body, expected_json):
        """
        验证返回json与预期是否一致
        :param body:
        :param expected_json:
        :return:
        """
        print("body", body)
        print("expected_json", expected_json)
        try:
            diff = Compare().check(expected_json, body)
            if isinstance(body, type(u'')):
                self.log.info("actual_res = %s" %
                              body.encode('utf-8').decode('unicode_escape'))
                self.log.info(
                    "expect_res = %s" %
                    expected_json.encode('utf-8').decode('unicode_escape'))
            else:
                self.log.info("actual_res = %s" % body)
                self.log.info("expect_res = %s" % expected_json)
            self.log.debug('json diff: {}'.format(diff))
            assert diff == NO_DIFF
            self.log.info("Response body=expected_json")
            return True

        except BaseException:
            self.log.error(
                "Response body != expected_json, expected_json is %s, body is %s" %
                (expected_json, body))
            Consts.RESULT_LIST.append('fail')
            raise

    def assert_dict_same(self, act_dict, expect_dict):
        '''
        比较字典是否一致
        :param act_dict:
        :param expect_dict:
        :return:
        '''
        try:
            expect_res = json.dumps(
                sorted(
                    expect_dict.items(),
                    key=lambda d: d[0]),
                ensure_ascii=False).encode('utf-8').decode('unicode_escape')
            self.log.info("expect_dict = %s" % expect_res)
            actual_res = json.dumps(
                sorted(
                    json.loads(
                        json.dumps(act_dict)).items(),
                    key=lambda d: d[0]),
                ensure_ascii=False).encode('utf-8').decode('unicode_escape')
            self.log.info("act_dict = %s" % actual_res)
            assert expect_res == actual_res
            self.log.info("act_dict=expect_dict")
            return True

        except BaseException:
            self.log.error(
                "Response body != expected_json, expected_json is %s, body is %s" %
                (expect_dict, act_dict))
            raise
