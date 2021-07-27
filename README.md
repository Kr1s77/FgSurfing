<h2 align="center"> FGProxy </h2>

<p align="center"><img src="https://raw.githubusercontent.com/Kr1s77/FgSurfing/main/log.png" 
        alt="Master"></p>



FGProxy  is an enterprise-level 4g agent program with automatic deployment. It is a more stable agent program than the 4g agent implemented by the Raspberry Pi. It discards the drawbacks of the Internet of Things card and uses a real 4g mobile phone card to build.

---

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
