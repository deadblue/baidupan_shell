# -*- coding: utf-8 -*-
'''
Created on 2014/07/04

@author: deadblue
'''

import urllib2

class HTTPErrorProcessor2(urllib2.HTTPErrorProcessor):
    '''
    覆盖原有的HTTPErrorProcessor
    将状态码为3XX的响应不视为错误
    '''
    def http_response(self, request, response):
        code, msg, hdrs = response.code, response.msg, response.info()
        if not (200 <= code < 400):
            response = self.parent.error(
                'http', request, response, code, msg, hdrs)
        return response

    https_response = http_response

class HTTPMultipartProcessor(urllib2.BaseHandler):
    def http_request(self, request):
        pass