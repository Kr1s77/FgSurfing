<h2 align="center"> FGProxy </h2>

<p align="center"><img src="https://raw.githubusercontent.com/Kr1s77/FgSurfing/main/log.png" 
        alt="Master"></p>



FGProxy  is an enterprise-level 4g agent program with automatic deployment. It is a more stable agent program than the 4g agent implemented by the Raspberry Pi. It discards the drawbacks of the Internet of Things card and uses a real 4g mobile phone card to build.

---

#### Before You Begin
1. 手机必须使用可以执行 `adb root` 的手机，我用的是 google pixel，我的系统是 `lineageos` 第三方系统
2. 在使用此程序之前需要确认你的手机里面已经按照下面链接配置了：https://kr1s77.github.io/2021/7/12/How-do-I-run-python-on-Android-devices/
3. 然后就可以执行 Fgproxy 的程序，执行完成后，端口会被映射到 30000， 30001， 30002... 端口数量就是设备数量
4. 之后就是配置 haproxy 做负载均衡:https://github.com/haproxy/haproxy
5. 由于机器在我们本地，接下来需要做内网穿透将本地的 haproxy 负载均衡端口转发出去，这里我们就需要 frp：https://github.com/fatedier/frp

=======以上就是整体的配置流程，配置完成之后 frp 出口就是我们的代理端口，就可以在爬虫中使用了。

#### Create

>   ```shell
>   $ git clone https://github.com/Kr1s77/FgSurfing.git
>   $ cd FgSurfing/proxy
>   $ python3 api.py
>   >> [2021-07-15 14:22:32,522 INFO]  ->  Count: [1] Devices Found
>   >> [2021-07-15 14:22:32,522 INFO]  ->  Deploy device: FAXXXXXXX  1/1
>   ```

#### Overall structure
```python3
 import requests
 
 url = 'https://httpbin.org/ip'
 proxies = {
     'http': 'http://{host}:{port}',
     'https': 'https://{host}:{port}'
 }
 
 requests.get(url=url, proxies=proxies)

# The following logic is then triggered：
# Clients -> Frp -> Haproxy -> Master PC -> Mobile Slaver
"""
 +----------------------------+
 | CLIENT || CLIENT || CLIENT |  
 +-------------+--------------+
               |
               |
               v
 +-------------+--------------+
 |          FRP SERVER        |
 +-------------+--------------+
               |
               |
               v
 +-------------+--------------+
 |           HAPROXY          |
 +-------------+--------------+
               |
               |
               v
+--------------+--------------+
|                             |
|           FGPROXY           |
|                             |
+-----------------------------+
"""
```

##### HAPROXY STATUS 
<p align="center"><img src="https://raw.githubusercontent.com/Kr1s77/FgSurfing/main/haproxy.png" 
        alt="Master"></p>

##### Currently most of it has been completed
> Anyone is welcome to participate and improve
> one person can go fast, but a group of people can go further
