# 一个简化的oauth2库
## 无需特殊配置 
无需特殊配置，使用sample下面的例子就可以运行   
默认配置有以下局限：   
问题1、重启会导致重启之前的登录信息无效。   
因为每次启动fastoauth会默认生成一个随机的secret_key，之前旧的secret_key生成的token将作废。   
问题2、多个oauth进程之间不能共用token    
因为不同的进程生成的随机secret_key是不一样的，导致不同进程之间不能互相解析token   
问题3、不能注销已经发放的token   
因为默认不存储token，每次都是通过解密来识别token可用性，因此已发放的token，在有效期内不能注销
## 配置secret_key
通常建议设置secret_key或者设置Redis以便获得更好的可用性。   
可以解决默认配置的问题1和问题2. 
> 注意：设置Redis之后，secret_key的设置无效，详情参考关于Redis的部分
---
生成secret_key的方式
```commandline
openssl rand -hex 32
```
如果没有openssl指令，你需要单独安装openssl。
```commandline
# windows下安装，choco的安装可以参考https://zhuanlan.zhihu.com/p/108833705
choco install openssl -y
```
## 配置Redis
通常建议配置Redis以获取最高的安全性。      
配置Redis之后，能解决默认配置的所有问题。   
同时配置Redis之后，在HTTP传输过程中只需要使用更简短的token，就能在Redis中存储更丰富内容。    
# 简化的服务端的例子
在工程目录./sample/oauth_server.py
```
