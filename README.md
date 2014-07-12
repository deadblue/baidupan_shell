baidu_lixian
============

## 项目简介
本来打算只做百度盘离线功能，结果变成了管理终端  
然后发现离线任务加多了还要输入验证码，目前没有什么解决验证码的方案  
~~所以离线的功能就先这么坑着了~~  

## 环境要求
 * Required:
  * python 2.7.x: https://www.python.org/download/
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
命令格式：login your-account your-password  
登录后会保存cookie，下次使用时不用重新登录  
如需换号直接再执行login命令即可  
*TODO：增加注销命令*  

#### conf - 配置
命令格式：conf <config-name> <config-value>  
 * 不带参数时，列出全部配置项
 * 只传入config-name时，列出对应配置项的值
 * 同时传入config-name和config-value时，表示更新配置

目前有效的配置包括：
 * downloader: 要使用的下载器，可选aria2c/curl/wget，默认curl
 * localhome: 初始的本地工作目录

#### ls - 列印文件
命令格式：ls  
目前列印格式还在调整中  
*TODO：加上过滤参数*  

#### cd - 改变远程工作目录
命令格式：cd remote-dir  
remote-dir可输入相对路径或绝对路径  
目前自动提示存在问题，推测与unicode有关，找时间好好修一下  
*TODO：完善自动完成提示，校验远程目录是否存在*  

#### lcd - 改变本地工作目录
命令格式：lcd local-dir  
remote-dir可是输入相对路径或绝对路径  
*TODO：本地工作目录作为可配置项存储起来*  

#### pwd - 输出工作目录
命令格式：pwd  
会显示远程工作目录和本地工作目录  

#### upload - 上传
命令格式：upload file-to-upload  
file-to-upload可以是绝对路径或相对路径。使用相对路径时，是相对于本地工作目录  
文件将上传到远程工作目录下  
依赖curl工具  
**一次只能上传一个文件**  
*TODO：实现自动完成提示，支持批量上传*  

#### download - 下载
命令格式：download fileid-to-download  
默认使用curl下载，支持wget（有问题）和aria2c  
**一次只能下载一个文件**  
*TODO：支持批量下载*  

#### play - 播放
命令格式：play fileid-to-play  
调用mplayer进行播放  
暂时其它需要支持的播放器  

#### exit - 退出
命令格式：exit  
退出终端  

#### debug - 调试
命令格式：debug  
输出调试信息，随着开发的推进，输出的信息也会不一样  

## 待添加的指令
logout（注销）、cp（复制文件）、mv（移动文件）、rename（重命名）、  
rm（删除）、mkdir（创建目录）、tasklist（离线任务列表）、taskadd（添加离线任务）