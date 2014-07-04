# -*- coding: utf-8 -*-
'''
Created on 2014/06/27

@author: deadblue
'''

from util.url import HTTPErrorProcessor2
import base64
import cookielib
import inspect
import json
import logging # @UnusedImport
import os
import random
import re
import rsa
import urllib
import urllib2
import util
import pickle

_BAIDU_APP_ID = 250528

def baidu_api(url, method):
    def invoker_creator(func):
        def invoker(obj, *args, **kwargs):
            data = [
                    ('app_id', _BAIDU_APP_ID),
                    ('channel', 'chunlei'),
                    ('bdstoken', obj.api_token),
                    ('clienttype', 0),
                    ('web', 1),
                    ('_', util.timstamp()),
                    ]
            call_args = inspect.getcallargs(func, obj, *args, **kwargs)
            for arg in call_args.items():
                if arg[0] == 'self' or arg[1] is None: continue
                data.append(arg)
            resp = obj._execute_request(url, data, method)
            result = json.load(resp)
            return result
        return invoker
    return invoker_creator

class LoginException(Exception):
    def __init__(self, errno):
        self.erron = errno
    def __str__(self, *args, **kwargs):
        return 'login error: %d' % self.erron

class BaiduClient():

    def __init__(self):
        # 从文件加载cookie
        cookie_file = os.path.join(os.getenv('HOME'), '.baidu_lixian.cookie')
        self._cookie_jar = cookielib.LWPCookieJar(cookie_file)
        if os.path.exists(cookie_file): self._cookie_jar.load()
        # 初始化urlopner
        cookie_handler = urllib2.HTTPCookieProcessor(self._cookie_jar)
        self._url_opener = urllib2.build_opener(cookie_handler, HTTPErrorProcessor2())
        # 加载配置文件
        self._load_config()
    
    def _load_config(self):
        self.api_token = ''
        self.xss_key = ''
        config_file = os.path.join(os.getenv('HOME'), '.baidu_lixian.config')
        if os.path.exists(config_file):
            config = pickle.load(open(config_file, 'r'))
            self.api_token = config['api_token']
            self.xss_key = config['xss_key']

    def _save_config(self, config):
        config_file = os.path.join(os.getenv('HOME'), '.baidu_lixian.config')
        pickle.dump(config, open(config_file, 'w'))

    def _execute_request(self, url, data=None, method='GET'):
        '''
        执行http请求
        '''
        if method == 'GET':
            if data:
                sep = '?' if url.find('?') < 0 else '&'
                url = '%s%s%s' % (url, sep, urllib.urlencode(data))
            req = urllib2.Request(url)
        else:
            req = urllib2.Request(url)
            if data:
                req.add_data(urllib.urlencode(data))
        req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36')
        req.add_header('Referer', 'http://pan.baidu.com/disk/home')
        resp = self._url_opener.open(req)
        return resp

    def is_login(self):
        resp = self._execute_request('http://pan.baidu.com/disk/home')
        print resp.code
        return resp.code != 302

    def _get_login_token(self):
        '''
        获取登陆用token
        '''
        # 需要先访问网盘首页，获得一个cookie
        self._execute_request('http://pan.baidu.com/')
        # 请求token
        cbs = 'bd__cbs__%s' % _random_str()
        url = 'https://passport.baidu.com/v2/api/?getapi'
        data = [
                ('tpl', 'netdisk'),
                ('apiver', 'v3'),
                ('tt', util.timstamp()),
                ('class', 'login'),
                ('logintype', 'basicLogin'),
                ('callback', cbs)
                ]
        resp = self._execute_request(url, data, 'GET')
        result = (resp.read()[len(cbs)+1:-1]).replace('\'', '"')
        result = json.loads(result)
        return result['data']['token']
    def _login_check(self, token, account):
        '''
        登陆检查，访问该页面主要是为了获取cookie
        '''
        cbs = 'bd__cbs__%s' % _random_str()
        url = 'https://passport.baidu.com/v2/api/?logincheck'
        data = [
                ('token', token),
                ('tpl', 'netdisk'),
                ('apiver', 'v3'),
                ('tt', util.timstamp()),
                ('username', account),
                ('isphone', 'false'),
                ('callback', cbs)
                ]
        self._execute_request(url, data)
    def _get_public_key(self, token):
        '''
        获取加密密码用的rsa公钥
        '''
        cbs = 'bd__cbs__%s' % _random_str()
        url = 'https://passport.baidu.com/v2/getpublickey'
        data = [
                ('token', token),
                ('tpl', 'netdisk'),
                ('apiver', 'v3'),
                ('tt', util.timstamp()),
                ('callback', cbs),
                ]
        resp = self._execute_request(url, data)
        result = (resp.read()[len(cbs)+1:-1]).replace('\'', '"')
        return json.loads(result)
    def _do_login(self, account, password, token, key_info):
        data = {
                'staticpage' : 'http://pan.baidu.com/res/static/thirdparty/pass_v3_jump.html',
                'charset' : 'utf-8',
                'tpl' : 'netdisk',
                'subpro' : '',
                'apiver' : 'v3',
                'tt' : util.timstamp(),
                'codestring' : '',
                'safeflg' : '0',
                'u' : 'http://pan.baidu.com/',
                'isPhone' : 'false',
                'quick_user' : '0',
                'logintype' : 'basicLogin',
                'logLoginType' : 'pc_loginBasic',
                'loginmerge' : 'true',
                'verifycode' : '',
                'mem_pass' : 'on',
                'crypttype' : '12',
                'ppui_logintime' : random.randint(5000, 10000),
                'callback' : 'parent.bd__cbs__%s' % _random_str(),
                'username' : account,
                'token' : token,
                'rsakey' : key_info['key']
                }
        # 使用rsa加密密码
        pubkey = key_info['pubkey'].replace('-----BEGIN PUBLIC KEY-----\r\n', '').replace('\r\n-----END PUBLIC KEY-----', '')
        pubkey = rsa.key.PublicKey.load_pkcs1_openssl_der(base64.decodestring(pubkey))
        data['password'] = base64.b64encode(rsa.encrypt(password, pubkey))
        # 发送登陆请求
        url = 'https://passport.baidu.com/v2/api/?login'
        resp = self._execute_request(url, data, 'POST')
        # 解析登陆结果
        m = re.search('err_no=(\d+)&', resp.read())
        if m is not None:
            err_no = int(m.group(1))
            if err_no > 0: raise LoginException(err_no)
        else:
            raise LoginException(-1)
        logging.debug('login successed!')
        self._cookie_jar.save()
    def _get_api_parameter(self):
        '''
        获取后续API调用需要的参数
        '''
        url = 'http://pan.baidu.com/disk/home'
        resp = self._execute_request(url)
        html = resp.read()
        # 获取api token
        m = re.search(r'yunData.MYBDSTOKEN = "(\w+)"', html)
        if m is not None:
            self.api_token = m.group(1)
        # 获取xss key，通过flash上传时需要传入
        m = re.search(r'yunData.MYBDUSS = "([^"]+)"', html)
        if m is not None:
            self.xss_key = m.group(1)
        self._save_config({
                           'api_token' : self.api_token,
                           'xss_key' : self.xss_key
                           })
    def login(self, account, password):
        token = self._get_login_token()
        logging.debug('login token: %s' % token)
        self._login_check(token, account)
        key_info = self._get_public_key(token)
        self._do_login(account, password, token, key_info)
        # 读取API必要的参数
        self._get_api_parameter()

    
    @baidu_api('http://pan.baidu.com/api/quota', 'GET')
    def quota(self, checkexpire=1, checkfree=1):
        pass

def _random_str():
    return '%x' % random.randint(0x100000, 0xffffff)