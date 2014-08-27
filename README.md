baidu_lixian
============

## 项目简介
百度盘管理终端  

## 环境要求
 * Required:
  * python 2.7.x: https://www.python.org/download/
  * Pillow: https://pillow.readthedocs.org/en/latest/
  * curl: http://curl.haxx.se/download.html
 * Optional:
  * mplayer: http://www.mplayerhq.hu/design7/dload.html
  * wget: https://www.gnu.org/software/wget/
  * aria2c: http://aria2.sourceforge.net/

## 使用方式
```
python baidupan_cli.py
YunPan:/>login your-account your-password
YunPan:/>ls
...
```

## 命令说明
#### login - 登录
格式：login your-account your-password  
登录后会保存cookie，下次使用时不用重新登录  
如需换号直接再执行login命令即可  
**登录时需要输入验证码的情况尚未处理**  
*TODO：增加注销命令*  

#### conf - 配置
格式：conf config-name config-value  
不带参数时，列出全部配置项；只传入config-name时，列出对应配置项的值；同时传入config-name和config-value时，表示更新配置  
目前有效的配置包括：
 * downloader: 要使用的下载器，可选aria2c/curl/wget，默认curl
 * localhome: 初始的本地工作目录

#### ls - 列印文件  
格式：ls file-type  
列印指定类型的文件  
file-type为可选参数，不传时列出全部文件  
要列出目录时，file-type传dir，其它情况传文件扩展名，如zip、mp4  
可同时传入多个file-type，以空格分开，如```ls dir zip rar```   

#### cd - 改变远程工作目录
格式：cd remote-dir  
remote-dir可输入相对路径或绝对路径  
目前自动提示存在问题，推测与unicode有关，找时间好好修一下  
*TODO：完善自动完成提示，校验远程目录是否存在*  

#### lcd - 改变本地工作目录
格式：lcd local-dir  
remote-dir可是输入相对路径或绝对路径  

#### pwd - 输出工作目录
格式：pwd  
会显示远程工作目录和本地工作目录  

#### mkdir - 创建目录
格式：mkdir dir-name  
在远程当前目录下，创建指定名称的目录  
若已存在同名目录则不创建  

#### rm - 删除文件
格式：rm fileid1-to-delete fileid2-to-delete ...  
可批量删除网盘中的文件  
**只可删除用ls命令列出过的文件，因为列印出的文件会缓存起来**  

#### push - 上传（原upload命令）
格式：push file-to-upload  
file-to-upload可以是绝对路径或相对路径  
使用相对路径时，是相对于本地工作目录  
文件将上传到远程工作目录下  
依赖curl工具  
**一次只能上传一个文件**  
*TODO：实现自动完成提示，支持批量上传*  

#### pull - 下载（原download命令）
格式：pull fileid1-to-download fileid2-to-download ...  
默认使用curl下载，支持wget和aria2c，通过conf指令配置  
**只可下载用ls命令列出过的文件，因为列印出的文件会缓存起来**  

#### play - 播放
格式：play fileid-to-play  
调用mplayer进行播放  
暂无其它需要支持的播放器  

#### tasks - 列出离线任务列表  
格式：tasks  
列出全部离线任务，包括正在进行的和已完成的  

#### dl - 创建离线下载任务  
格式：dl download_link  
创建离线下载任务，支持http/https/ed2k/bt种子  
创建http/https/ed2k离线任务时，download_link为对应的链接  
创建bt离线任务时，download_link为网盘上或本地的种子文件名  
每天创建超过10个任务后会要求输入验证码  

#### exit - 退出  
格式：exit  
退出终端  

#### debug - 调试
格式：debug  
输出调试信息，随着开发的推进，输出的信息也会不一样  

## 待添加的指令
logout（注销）、cp（复制文件）、mv（移动文件）、rename（重命名）