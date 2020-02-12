# coding:utf-8

import requests


class RequestBuilder:

    def __init__(self, method, url, data = None, headers = None):

        self._method = method
        self._url = url
        self._data = data
        self._headers = headers
        '''
        self._headers.update({
            'OSLC-Core-version': '2.0'
        })
        '''

    def build(self):

        return requests.Request(self._method,
            self._url,
            data = self._data,
            headers = self._headers)

    def post(self):
        pass

    def logout(self):
        pass
