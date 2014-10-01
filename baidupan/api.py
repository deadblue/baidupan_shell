# -*- coding: utf-8 -*-
'''
Created on 2014/06/27

@author: deadblue
'''

import base64
import cookielib
import inspect
import json
import logging
import os
import random
import re
import urllib
import urllib2
import tempfile

from baidupan import http, util
import rsa

__all__ = ['client', 'LoginException']

_APP_ID = 250528
_BAIDUPAN_HOST = 'http://pan.baidu.com/'
_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:30.0) Gecko/20100101 Firefox/30.0'

_logger = logging.getLogger('api')

def baidu_api(path, preset={}, post_field=[]):
    url = '%s%s' % (_BAIDUPAN_HOST, path)
    def invoker_creator(func):
        def invoker(obj, *args, **kwargs):
            # 必要参数
            get_data = {
                    'app_id' : _APP_ID,
                    'channel' : 'chunlei',
                    'bdstoken' : obj.bdstoken,
                    'clienttype' : 0,
                    'web' : 1,
                    '_': util.timstamp(),
                    't': util.timstamp()
                    }
            # 处理API预设参数
            if preset: get_data.update(preset)
            # 处理传入的参数
            call_args = inspect.getcallargs(func, obj, *args, **kwargs)
            for k,v in call_args.items():
                if k == 'self' or v is None: continue
                if type(v) is unicode: v = v.encode('utf-8')
                get_data[k] = v
            # 处理需要post的参数
            post_data = {}
            if post_field:
                for field in post_field:
                    if not get_data.has_key(field): continue
                    post_data[field] = get_data[field]
                    del get_data[field]
            # 发送请求，出现网络问题时重试
            retry = True
            while retry:
                try:
                    resp = obj.execute_request(url, get_data, post_data)
                    result = json.load(resp)
                    retry = False
                except urllib2.HTTPError as he:
                    result = json.load(he)
                    if result.get('error_code', 0) == -19:
                        # 下载验证码图片
                        vcode_image = obj.download_vcode_image(result['img'])
                        post_data['vcode'] = result['vcode']
                        post_data['input'] = obj.vcode_handler(vcode_image)
                        retry = True
                    else:
                        retry = False
                except:
                    retry = True
            return result
        return invoker
    return invoker_creator

def _calc_download_sign(sign1, sign2):
    '''
    计算下载签名
    '''
    result = []
    # 准备256字节缓冲区
    sbox = []
    for i in xrange(256):
        sbox.append(i)
    # 变换缓冲区数据顺序
    idx = 0
    for i in xrange(256):
        tmp = ord( sign1[ i % len(sign1) ] )
        idx = (idx + sbox[i] + tmp) % 256
        (sbox[i], sbox[idx]) = (sbox[idx], sbox[i])
    # 计算最终签名
    n1 = n2 = 0
    for i in xrange(len(sign2)):
        n1 = (n1 + 1) % 256
        n2 = (n2 + sbox[n1]) % 256
        (sbox[n1], sbox[n2]) = (sbox[n2], sbox[n1])
        tmp = sbox[ (sbox[n1] + sbox[n2]) % 256 ]
        result.append( chr( ord(sign2[i]) ^ tmp ) )
    return base64.b64encode(''.join(result))

class LoginException(Exception):
    def __init__(self, errno):
        self.erron = errno
    def __str__(self, *args, **kwargs):
        return 'login error: %d' % self.erron

class BaiduPanClient():

    def __init__(self, cookie_jar=None, vocde_handler=util.default_vcode_handler):
        # 初始化urlopener
        self._cookie_jar = cookielib.CookieJar() if cookie_jar is None else cookie_jar
        self._url_opener = urllib2.build_opener(
            urllib2.HTTPCookieProcessor(self._cookie_jar)
        )
        # 验证码处理函数
        self.vcode_handler = vocde_handler
        # 获取登陆信息
        self.is_login = False
        self.user_name = self.bdstoken = self.bduss = None
        self.timpstamp = self.download_sign = None
        self._get_login_info()
    def _get_login_info(self):
        '''
        判断是否成功登陆，并获取登陆后的相关信息
        '''
        url = 'http://pan.baidu.com/disk/home'
        resp = self.execute_request(url)
        html = resp.read()
        # 用户名
        try:
            # 搜索赋值到yunData上的数据
            ms = re.findall(r'yunData\.([\w_]+)\s*=\s*[\'"](.*?)[\'"];', html)
            if ms is None or len(ms) == 0:
                raise LoginException(-1)
            yun_data = dict(ms)
            # 提取必要的信息
            self.user_name = yun_data['MYNAME']
            self.bdstoken = yun_data['MYBDSTOKEN']
            self.bduss = yun_data['MYBDUSS']
            self.timpstamp = yun_data['timestamp']
            sign1 = yun_data['sign1']
            sign3 = yun_data['sign3']
            self.download_sign = _calc_download_sign(sign3, sign1)
            # 若成功提取则标记为登陆成功
            self.is_login = True
        except:
            self.is_login = False

    def execute_request(self, url, get_data=None, post_data=None):
        if get_data:
            get_data = urllib.urlencode(get_data)
            sep = '?' if url.find('?') < 0 else '&'
            url = '%s%s%s' % (url, sep, get_data)
        req = urllib2.Request(url)
        if post_data and len(post_data) > 0:
            req.add_data(urllib.urlencode(post_data))
        req.add_header('User-Agent', _USER_AGENT)
        req.add_header('Referer', 'http://pan.baidu.com/disk/home')
        resp = self._url_opener.open(req)
        return resp
    def download_vcode_image(self, url):
        resp = self.execute_request(url)
        return resp.read()

    def login(self, account, password):
        '''
        登录网盘
        @param account: 账户
        @param password: 密码
        '''
        token = self._get_login_token()
        _logger.debug('login token: %s' % token)
        self._login_check(token, account)
        key_info = self._get_public_key(token)
        self._do_login(account, password, token, key_info)
        # 获取登陆信息
        self._get_login_info()
    def _get_login_token(self):
        '''
        获取登陆用token
        '''
        # 需要先访问网盘首页，获得一个cookie
        self.execute_request('http://pan.baidu.com/')
        # 请求token
        cbs = 'bd__cbs__%s' % util.random_hex_str(6)
        url = 'https://passport.baidu.com/v2/api/?getapi'
        query = [
                 ('tpl', 'netdisk'),
                 ('apiver', 'v3'),
                 ('tt', util.timstamp()),
                 ('class', 'login'),
                 ('logintype', 'basicLogin'),
                 ('callback', cbs)
                 ]
        resp = self.execute_request(url, query)
        result = (resp.read()[len(cbs)+1:-1]).replace('\'', '"')
        result = json.loads(result)
        return result['data']['token']
    def _login_check(self, token, account):
        '''
        登陆检查，访问该页面主要是为了获取cookie
        '''
        cbs = 'bd__cbs__%s' % util.random_hex_str(6)
        url = 'https://passport.baidu.com/v2/api/?logincheck'
        query = [
                 ('token', token),
                 ('tpl', 'netdisk'),
                 ('apiver', 'v3'),
                 ('tt', util.timstamp()),
                 ('username', account),
                 ('isphone', 'false'),
                 ('callback', cbs)
                 ]
        self.execute_request(url, query)
    def _get_public_key(self, token):
        '''
        获取加密密码用的rsa公钥
        '''
        cbs = 'bd__cbs__%s' % util.random_hex_str(6)
        url = 'https://passport.baidu.com/v2/getpublickey'
        query = [
                 ('token', token),
                 ('tpl', 'netdisk'),
                 ('apiver', 'v3'),
                 ('tt', util.timstamp()),
                 ('callback', cbs),
                 ]
        resp = self.execute_request(url, query)
        result = (resp.read()[len(cbs)+1:-1]).replace('\'', '"')
        return json.loads(result)
    def _do_login(self, account, password, token, key_info):
        url = 'https://passport.baidu.com/v2/api/?login'
        form = {
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
                'callback' : 'parent.bd__cbs__%s' % util.random_hex_str(6),
                'username' : account,
                'token' : token,
                'rsakey' : key_info['key']
                }
        # 使用rsa加密密码
        pubkey = key_info['pubkey'].replace('-----BEGIN PUBLIC KEY-----\n', '').replace('\n-----END PUBLIC KEY-----', '')
        pubkey = rsa.key.PublicKey.load_pkcs1_openssl_der(base64.decodestring(pubkey))
        form['password'] = base64.b64encode(rsa.encrypt(password, pubkey))
        # 发送登陆请求
        resp = self.execute_request(url, None, form)
        # 解析登陆结果
        body = resp.read()
        m = re.search('err_no=(\d+)&', body)
        if m is not None:
            err_no = int(m.group(1))
            if err_no != 0:
                raise LoginException(err_no)
        else:
            raise LoginException(-1)
        _logger.debug('login successed!')

    def upload(self, savedir, localfile):
        '''
        上传文件
        @param savedir: 远端保存路径
        @param localfile: 本地文件完整路径
        '''
        url = 'https://c.pcs.baidu.com/rest/2.0/pcs/file'
        query = [
            ('method', 'upload'),
            ('app_id', _APP_ID),
            ('ondup', 'newcopy'),
            ('dir', savedir),
            ('filename', os.path.basename(localfile)),
            ('BDUSS', urllib.unquote(self.bduss))
             ]
        url = '%s?%s' % (url, urllib.urlencode(query))
        _logger.debug('upload url: %s' % url)
        req = http.MultipartRequest(url)
        req.set_parts([
                       http.FilePart('file', localfile)
                       ])
        req.add_header('User-Agent', _USER_AGENT)
        try:
            resp = urllib2.urlopen(req)
            return json.load(resp)
        except urllib2.HTTPError as he:
            return json.load(he)
    def upload_data(self, savedir, filename, filedata):
        '''
        上传文件数据
        :param savedir: 远程保存路径
        :param filename: 保存文件名
        :param filedata: 文件数据
        :return:
        '''
        url = 'https://c.pcs.baidu.com/rest/2.0/pcs/file'
        query = [
            ('method', 'upload'),
            ('app_id', _APP_ID),
            ('ondup', 'newcopy'),
            ('dir', savedir),
            ('filename', filename),
            ('BDUSS', urllib.unquote(self.bduss))
             ]
        url = '%s?%s' % (url, urllib.urlencode(query))
        _logger.debug('upload url: %s' % url)
        req = http.MultipartRequest(url)
        req.set_parts([
                       http.FileDataPart('file', filename, filedata)
                       ])
        req.add_header('User-Agent', _USER_AGENT)
        try:
            resp = urllib2.urlopen(req)
            return json.load(resp)
        except urllib2.HTTPError as he:
            return json.load(he)
    def upload_curl(self, savedir, localfile):
        '''
        使用curl上传文件
        上传大文件时使用此接口，可显示上传进度
        @param savedir: 远端保存路径
        @param localfile: 本地文件完整路径
        '''
        url = 'https://c.pcs.baidu.com/rest/2.0/pcs/file'
        query = [
            ('method', 'upload'),
            ('app_id', _APP_ID),
            ('ondup', 'newcopy'),
            ('dir', savedir),
            ('filename', os.path.basename(localfile)),
            ('BDUSS', urllib.unquote(self.bduss))
             ]
        url = '%s?%s' % (url, urllib.urlencode(query))
        # 创建临时文件用来保存输出结果
        _, tmp_file = tempfile.mkstemp(suffix='.json')
        # 调用curl上传文件
        cmd = ['curl',
               '-A "%s"' % _USER_AGENT,
               '-H "Expect:"',
               '-F "file=@%s;type=application/octet-stream"' % localfile,
               '-o "%s"' % tmp_file,
               '"%s"' % url
        ]
        cmd = ' '.join(cmd)
        os.system(cmd)
        # 读取输出结果
        fp = open(tmp_file, 'r')
        result = json.load(fp)
        fp.close()
        return result

    def get_download_request(self, file_id):
        '''
        获取下载文件的请求
        请求中封装了完整地址、必要的请求头和cookie信息
        '''
        fids = file_id if type(file_id) is list else [file_id]
        result = self.download_link(self.download_sign, self.timpstamp, json.dumps(fids))
        if result.get('errno') == 112:
            # 签名超时，刷新签名重新获取
            self._get_login_info()
            result = self.download_link(self.download_sign, self.timpstamp, json.dumps(fids))
        # 获取下载地址
        reqs = []
        for dl in result['dlink']:
            req = urllib2.Request(dl['dlink'])
            req.add_header('User-Agent', _USER_AGENT)
            req.add_header('Referer', 'http://pan.baidu.com/disk/home')
            req.add_header('Pragma', 'no-cache')
            req.add_header('Cache-Control', 'no-cache')
            req.add_header('Accept-Encoding', 'gzip,deflate,sdch')
            req.add_header('Accept', '*/*;q=0.8')
            req.add_header('Connection', 'keep-alive')
            self._cookie_jar.add_cookie_header(req)
            reqs.append(req)
        return reqs[0] if len(reqs) == 1 else reqs
    def download_data(self, file_id):
        '''
        下载数据
        用于直接读取网盘上文件的内容，不建议对大文件使用
        :param file_id:
        :return:
        '''
        req = self.get_download_request(file_id)
        resp = self._url_opener.open(req)
        return resp.read()

    @baidu_api('api/quota')
    def quota(self, checkexpire=1, checkfree=1):
        '''
        获取空间使用状况
        @param checkexpire: 意义不明，使用默认值
        @param checkfree: 意义不明，使用默认值
        '''
        pass
    @baidu_api('api/list')
    def list(self, dir, num=100, page=1, order='time', desc=0, showempty=0):  # @ReservedAssignment
        '''
        文件列表
        @param dir: 父目录
        @param num: 每页显示条数
        @param page: 页码
        @param order: 排序方式(time/size/name)
        @param desc: 传None则升序，其它情况皆为降序
        @param showempty: 不明，使用默认值
        '''
        pass
    @baidu_api('api/create', preset={'a':'commit', 'isdir':1, 'size':'', 'method':'post'}, post_field=['path', 'isdir', 'size', 'block_list', 'method'])
    def create_dir(self, path):
        '''
        创建目录
        @param path: 完整路径（不能一下创建多级目录）
        '''
        pass
    @baidu_api('api/filemanager', preset={'opera':'rename','async':1}, post_field=['filelist'])
    def rename(self, filelist):
        '''
        重命名文件
        @param filelist: 重命名操作，格式：[{"path":"源文件路径","newname":"新文件名"},...]
        '''
        pass
    @baidu_api('api/filemanager', preset={'opera':'copy'}, post_field=['filelist'])
    def copy(self, filelist):
        '''
        复制文件
        @param filelist: 复制操作，格式为：[{"path":"源文件路径","dest":"目标目录","newname":"新名称"},...]
        '''
        pass
    @baidu_api('api/filemanager', preset={'opera':'move'}, post_field=['filelist'])
    def move(self, filelist):
        '''
        移动文件
        @param filelist: 移动操作，格式为：[{"path":"源文件路径","dest":"目标目录","newname":"新名称"},...]
        '''
        pass
    @baidu_api('api/filemanager', preset={'opera':'delete'}, post_field=['filelist'])
    def delete(self, filelist):
        '''
        删除文件
        @param filelist: 删除文件列表，格式为：["文件路径","文件路径",...]
        '''
        pass
    @baidu_api('api/download', preset={'type':'dlink'}, post_field=['sign', 'timestamp', 'fidlist', 'type'])
    def download_link(self, sign, timestamp, fidlist):
        '''
        获取文件下载地址
        @param sign: 下载签名（从网盘首页页面中获取并计算）
        @param timestamp: 时间戳（从网盘首页页面中获取）
        @param fidlist: 要下载的文件列表，格式：[文件ID,文件ID,...]
        '''
        pass

    @baidu_api('rest/2.0/membership/quota', preset={'method':'query'})
    def membership_quota(self, function_name):
        '''
        查询用户功能限额
        目前尚未完全理解返回值意义，此接口暂时不会使用
        已知功能：dl_task_num - 离线下载任务数
        @param function_name: 要查询的功能，格式：["name1","name2",...]
        '''
        pass
    @baidu_api('rest/2.0/services/cloud_dl', preset={'method':'list_task', 'need_task_info':1})
    def cloud_dl_list_task(self, start=0, limit=20, status=255):
        '''
        离线任务列表
        @param start: 列表起始位置
        @param limit: 列表最大数量
        @param status: 推测为任务状态掩码，用来过滤列表，暂时传255即可
        '''
        pass
    @baidu_api('rest/2.0/services/cloud_dl', preset={'method':'query_task', 'op_type':1})
    def cloud_dl_query_task(self, task_ids):
        '''
        查询任务信息
        @param task_ids: 要查询的任务ID集合，格式：id1,id2,id3...
        '''
        pass
    @baidu_api('rest/2.0/services/cloud_dl', preset={'method':'clear_task'})
    def cloud_dl_clear_task(self):
        '''
        清除已完成任务
        '''
        pass
    @baidu_api('rest/2.0/services/cloud_dl', preset={'method':'query_sinfo', 'type':2})
    def cloud_dl_query_bt_info(self, source_path):
        '''
        查询种子文件信息
        @preset type: 2表示种子；推测1表示url，相应的source_path也传url
        @param source_path: 种子文件路径（必须存在于网盘上）
        '''
        pass
    @baidu_api('rest/2.0/services/cloud_dl', preset={'method':'add_task'},
               post_field=['method', 'app_id', 'source_url', 'save_path'])
    def cloud_dl_add_http_task(self, source_url, save_path):
        '''
        创建http离线任务
        @param source_url: 下载地址
        @param save_path: 保存路径
        '''
        pass
    @baidu_api('rest/2.0/services/cloud_dl', preset={'method':'add_task', 'type':2, 'task_from':2}, 
                 post_field=['method', 'app_id', 'source_path', 'selected_idx', 'file_sha1', 'save_path', 'task_from', 'type', 't'])
    def cloud_dl_add_bt_task(self, source_path, selected_idx, file_sha1, save_path):
        '''
        添加bt离线任务
        @preset task_from: 意义不明
        @param source_path: 种子文件路径（必须存在于网盘上）
        @param selected_idx: 要下载的文件索引
        @param file_sha1: 种子文件的哈希值
        @param save_path: 网盘上的保存路径
        '''
        pass
    @baidu_api('rest/2.0/services/cloud_dl', preset={'method':'add_task', 'type':3},
               post_field=['method', 'app_id', 'source_url', 'save_path', 'type'])
    def cloud_dl_add_ed2k_task(self, source_url, save_path):
        '''
        添加ed2k离线任务
        @param source_url: ed2k链接
        @param save_path: 网盘上的保存路径
        '''
        pass
    @baidu_api('rest/2.0/services/cloud_dl', preset={'method':'cancel_task'})
    def cloud_dl_task_cancel(self, task_id):
        '''
        取消一个未完成的离线任务
        @param task_id: 任务id
        '''
        pass

    @baidu_api('share/record', preset={'order':'ctime', 'desc':1})
    def share_list(self, page=1):
        '''
        分享列表
        目前百度盘页面使用本地js排序，因此各参数的取值暂不明确
        @preset order: 排序方式，目前该参数传其他值没有效果
        @preset desc: 是否降序，目前该参数传其他值没有效果
        @param page: 分页页码，没有控制每页数据条数的参数，推测是服务器端定死的
        '''
        pass
    @baidu_api('share/cancel', post_field=['shareid_list'])
    def share_cancel(self, shareid_list):
        '''
        取消分享
        @param shareid_list: 分享内容ID列表，格式：[share1_id,share2_id,...]
        '''
        pass
    @baidu_api('share/set', preset={'channel_list':'[]'}, post_field=['fid_list', 'schannel', 'channel_list', 'pwd'])
    def share_set(self, fid_list, schannel, pwd=None):
        '''
        创建分享
        @preset channel_list: 该参数意义不明，因此暂时传固定值
        @param fid_list: 要分享的文件ID
        @param schannel: 分享渠道，0-公开分享，4-私密分享，其它数值意义不明
        @param pwd: 私密分享时的密码，公开分享时不应传入
        '''
        pass