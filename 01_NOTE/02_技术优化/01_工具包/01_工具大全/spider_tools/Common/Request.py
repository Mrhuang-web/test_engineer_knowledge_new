# -*- coding: utf-8 -*-

"""
封装request

"""

import os
import random

import requests
from requests_toolbelt import MultipartEncoder

import Common.Consts
from Common.Log import MyLog


class Request:

    def __init__(self, env):
        """
        :param env:
        """

    def get_request(self, url, data, header):
        """
        Get请求
        :param url:
        :param data:
        :param header:
        :return:

        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)

        try:
            if data is None:
                response = requests.get(url=url, headers=header)
            else:
                response = requests.get(url=url, params=data, headers=header)

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''
        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers
        MyLog.debug("=> 【Request】: GET %s" % (url,))
        MyLog.debug("...params: %s" % (data,))
        MyLog.debug("...header: %s" % (header,))
        MyLog.debug("<= 【Repsonse】 code: %s" % (response.status_code))
        MyLog.debug("...headers: %s" % (response.headers))
        if 'Content-Type' in response.headers.keys(
        ) and "application" not in response.headers['Content-Type']:
            MyLog.debug("...body: %s" % (response.text))
        return response_dicts

    def post_request(self, url, data, header):
        """
        Post请求
        :param url:
        :param data:
        :param header:
        :return:

        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)
        try:
            if data is None:
                response = requests.post(url=url, headers=header)
            else:
                response = requests.post(url=url, params=data, headers=header)

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        # time_consuming为响应时间，单位为毫秒
        time_consuming = response.elapsed.microseconds / 1000
        # time_total为响应时间，单位为秒
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''

        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers
        MyLog.debug("=> 【Request】: POST %s" % (url,))
        MyLog.debug("...params: %s" % (data,))
        MyLog.debug("...header: %s" % (header,))
        MyLog.debug("<= 【Repsonse】 code: %s" % (response.status_code))
        MyLog.debug("...headers: %s" % (response.headers))
        if 'Content-Type' in response.headers.keys(
        ) and "application" not in response.headers['Content-Type']:
            MyLog.debug("...body: %s" % (response.text))

        return response_dicts

    def post_request_multipart(
            self,
            url,
            data,
            header,
            file_parm,
            file,
            f_type):
        """
        提交Multipart/form-data 格式的Post请求
        :param url:
        :param data:
        :param header:
        :param file_parm:
        :param file:
        :param type:
        :return:
        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)
        try:
            if data is None:
                response = requests.post(url=url, headers=header)
            else:
                data[file_parm] = os.path.basename(
                    file), open(file, 'rb'), f_type

                enc = MultipartEncoder(
                    fields=data,
                    boundary='--------------' + str(random.randint(1e28, 1e29 - 1))
                )

                header['Content-Type'] = enc.content_type
                response = requests.post(url=url, params=data, headers=header)

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        # time_consuming为响应时间，单位为毫秒
        time_consuming = response.elapsed.microseconds / 1000
        # time_total为响应时间，单位为秒
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''

        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers

        return response_dicts

    def post_request_uploadfile_01(
            self,
            url,
            filename,
            headers=None,
            file_label='file',**kwargs):
        """
        上传文件
        :param url:
        :param file: 直接给文件名，缺省读取Param/upload目录，例如:'somefile.xlsx'
        :param headers: 缺省为None， 此时传值为excel
        :param file_label: 有些fields中的file是file，有些是files， 目前来看大部分是file
        :return:
        """

        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)
        path_dir = str(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    os.pardir)))
        m = MultipartEncoder(
            fields={
                file_label: (filename,open(os.path.join(path_dir,'Params/upload',filename),'rb'), 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                "fileName": filename,
                "type":str(kwargs["typestr"])})

        headers['Content-Type'] = m.content_type

        try:
            response = requests.post(url=url, data=m, headers=headers)
        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()
        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        # time_consuming为响应时间，单位为毫秒
        time_consuming = response.elapsed.microseconds / 1000
        # time_total为响应时间，单位为秒
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''

        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers

        return response_dicts


    def post_request_uploadfileV3(
            self,
            url,
            m,
            headers=None,):
        """
        上传文件
        :param url:
        :param file: 直接给文件名，缺省读取Param/upload目录，例如:'somefile.xlsx'
        :param headers: 缺省为None， 此时传值为excel
        :param m
        :param file_label: 有些fields中的file是file，有些是files， 目前来看大部分是file
        :return:
        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
        try:
            response = requests.post(url=url, data=m, headers=headers)
        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()
        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        # time_consuming为响应时间，单位为毫秒
        time_consuming = response.elapsed.microseconds / 1000
        # time_total为响应时间，单位为秒
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''

        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers

        return response_dicts
    def post_request_uploadfile(
            self,
            url,
            filename,
            headers=None,
            file_label='file'):
        """
        上传文件
        :param url:
        :param file: 直接给文件名，缺省读取Param/upload目录，例如:'somefile.xlsx'
        :param headers: 缺省为None， 此时传值为excel
        :param file_label: 有些fields中的file是file，有些是files， 目前来看大部分是file
        :return:
        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)
        path_dir = str(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    os.pardir)))
        m = MultipartEncoder(
            fields={
                file_label: (
                    filename,
                    open(
                        os.path.join(
                            path_dir,
                            'Params/upload',
                            filename),
                        'rb'),
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                "fileName": filename})

        headers['Content-Type'] = m.content_type

        try:
            response = requests.post(url=url, data=m, headers=headers)
        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()
        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        # time_consuming为响应时间，单位为毫秒
        time_consuming = response.elapsed.microseconds / 1000
        # time_total为响应时间，单位为秒
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''

        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers

        return response_dicts

    def post_request_uploadfile_byprecinct(
            self, url, requestpart, headers=None):
        """
        上传文件
        :param url:
        :param file: 直接给文件名，缺省读取Param/upload目录，例如:'somefile.xlsx'
        :param headers: 缺省为None， 此时传值为excel
        :param file_label: 有些fields中的file是file，有些是files， 目前来看大部分是file
        :return:
        """
        path_dir = str(
            os.path.abspath(
                os.path.join(
                    os.path.dirname(__file__),
                    os.pardir)))
        fields_ = {}
        alldata = (requestpart).split("|")
        for kv in alldata:
            keyvvalue = kv.split("=")
            if keyvvalue[0] == "filename":
                fields_["file"] = (
                    keyvvalue[1],
                    open(
                        os.path.join(
                            path_dir,
                            'Params/upload',
                            keyvvalue[1]),
                        'rb'),
                    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,image/png')
                fields_["fileName"] = keyvvalue[1]
            else:
                fields_[keyvvalue[0]] = keyvvalue[1]
        print("fields_", fields_)
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)

        m = MultipartEncoder(
            fields=fields_
        )

        headers['Content-Type'] = m.content_type

        try:
            response = requests.post(url=url, data=m, headers=headers)
        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()
        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        # time_consuming为响应时间，单位为毫秒
        time_consuming = response.elapsed.microseconds / 1000
        # time_total为响应时间，单位为秒
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''

        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers

        return response_dicts

    def put_request(self, url, data, header):
        """
        Put请求
        :param url:
        :param data:
        :param header:
        :return:

        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)

        try:
            if data is None:
                response = requests.put(url=url, headers=header)
            else:
                response = requests.put(url=url, params=data, headers=header)

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''
        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers
        MyLog.debug("=> 【Request】: PUT %s" % (url,))
        MyLog.debug("...params: %s" % (data,))
        MyLog.debug("...header: %s" % (header,))
        MyLog.debug("<= 【Repsonse】 code: %s" % (response.status_code))
        MyLog.debug("...headers: %s" % (response.headers))
        if 'Content-Type' in response.headers.keys(
        ) and "application" not in response.headers['Content-Type']:
            MyLog.debug("...body: %s" % (response.text))

        return response_dicts

    def delete_request(self, url, data, header):
        """
        Delete请求
        :param url:
        :param data:
        :param header:
        :return:

        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)

        try:
            if data is None:
                response = requests.delete(url=url, headers=header)
            else:
                response = requests.delete(url=url, data=data, headers=header)

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        time_consuming = response.elapsed.microseconds / 1000
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''
        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers
        MyLog.debug("=> 【Request】: PUT %s" % (url,))
        MyLog.debug("...params: %s" % (data,))
        MyLog.debug("...header: %s" % (header,))
        MyLog.debug("<= 【Repsonse】 code: %s" % (response.status_code))
        MyLog.debug("...headers: %s" % (response.headers))
        MyLog.debug("...body: %s" % (response.text))

        return response_dicts

    def post_request_data(self, url, data, header):
        """
        Post请求
        :param url:
        :param data:
        :param header:
        :return:

        """
        if not url.startswith('http://'):
            url = '%s%s' % ('http://', url)
            print(url)
        try:
            if data is None:
                response = requests.post(url=url, headers=header)
            else:
                response = requests.post(url=url, data=data, headers=header)

        except requests.RequestException as e:
            print('%s%s' % ('RequestException url: ', url))
            print(e)
            return ()

        except Exception as e:
            print('%s%s' % ('Exception url: ', url))
            print(e)
            return ()

        # time_consuming为响应时间，单位为毫秒
        time_consuming = response.elapsed.microseconds / 1000
        # time_total为响应时间，单位为秒
        time_total = response.elapsed.total_seconds()

        Common.Consts.STRESS_LIST.append(time_consuming)

        response_dicts = dict()
        response_dicts['code'] = response.status_code
        try:
            response_dicts['body'] = response.json()
        except Exception as e:
            print(e)
            response_dicts['body'] = ''

        response_dicts['text'] = response.text
        response_dicts['time_consuming'] = time_consuming
        response_dicts['time_total'] = time_total
        response_dicts['headers'] = response.headers
        MyLog.debug("=> 【Request】: POST %s" % (url,))
        MyLog.debug("...body: %s" % (data,))
        MyLog.debug("...header: %s" % (header,))
        MyLog.debug("<= 【Repsonse】 code: %s" % (response.status_code))
        MyLog.debug("...headers: %s" % (response.headers))
        if 'Content-Type' in response.headers.keys(
        ) and "application" not in response.headers['Content-Type']:
            MyLog.debug("...body: %s" % (response.text))

        return response_dicts
