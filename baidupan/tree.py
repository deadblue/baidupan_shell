# -*- coding: utf-8 -*-

__author__ = 'deadblue'

class RemoteTree():
    '''
    对远程文件树的访问和缓存处理
    '''
    def __init__(self, client):
        self.client = client
        self.tree_cache = {}
        self.file_cache = {}

    def _list_from_cache(self, parent_dir):
        if self.tree_cache.has_key(parent_dir):
            return self.tree_cache[parent_dir]
        else:
            return None
    def _list_from_server(self, parent_dir):
        # 从服务器读取目录下全部文件列表
        file_list, page_num = [], 1
        while True:
            result = self.client.list(dir=parent_dir, page=page_num, num=100, order='name', desc=None)
            file_list.extend(result['list'])
            if len(result['list']) < 100:
                break
            else:
                page_num += 1
        # 更新缓存
        self.tree_cache[parent_dir] = file_list
        self._cache_file(file_list)
        return file_list
    def _cache_file(self, file_list):
        for file_obj in file_list:
            file_id = str(file_obj['fs_id'])
            self.file_cache[file_id] = file_obj

    def list(self, parent_dir='/', show_dir=True, show_file=True, show_exts=None, force_fetch=False):
        # 获取完整文件列表
        full_list = self._list_from_cache(parent_dir)
        if force_fetch or full_list is None:
            full_list = self._list_from_server(parent_dir)
        # 按条件过滤文件列表
        file_list = []
        for file_obj in full_list:
            if file_obj['isdir'] == 1 and show_dir:
                file_list.append(file_obj)
            elif file_obj['isdir'] == 0 and show_file:
                if show_exts is None or len(show_exts) == 0:
                    file_list.append(file_obj)
                else:
                    file_name = file_obj['server_filename']
                    for ext in show_exts:
                        if file_name.endswith(ext):
                            file_list.append(file_obj)
                            break
        return file_list
    def list_dir(self, parent_dir='/'):
        return self.list(parent_dir=parent_dir, show_dir=True, show_file=False, force_fetch=False)
    def list_file(self, parent_dir='/'):
        return self.list(parent_dir=parent_dir, show_dir=False, show_file=True, force_fetch=False)
    def get_file_by_id(self, file_id):
        return self.file_cache.get(file_id)
    def remote_file_from_cache(self, file_id):
        file_obj = self.file_cache.get(file_id)
        if file_obj:
            # TODO: delete from tree cache
            # delete from file cahce
            del self.file_cache[file_id]

class LocalTree():
    def __init__(self):
        import platform
        sys_name = platform.system()
        self.is_win = sys_name == 'Windows'
    def is_full_path(self, path):
        if self.is_win:
            pass
        else:
            return path.startswith('/')