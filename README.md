<h3 align="center"> FGProxy </h2>

<p align="center"><img src="https://raw.githubusercontent.com/Kr1s77/FgSurfing/main/log.png" 
        alt="Master"></p>


##### FGProxy 是一个企业级 `4G` 代理程序。它是一个比树莓派实现的4g代理程序更稳定的代理程序。它摒弃了物联网卡的缺点，使用了真正的4g手机卡来实现，部署实现都非常的简单。

#### 文档可能比较简洁，部署失败的可以邮件联系我，或者找我远程协助搭建，有啥问题也可以在 issues 里面提出。
##### 有兴趣的同学可以尝试使用 haproxy + prometheus + grafana 做个代理的监控，还是非常不错的！
#### Email: criselyj@163.com

---

#### Before You Begin
1. The mobile phone must use a mobile phone that can execute `adb root`, I use [Google Pixel](https://en.wikipedia.org/wiki/Pixel_(1st_generation))，My system is [lineageos](https://www.lineageos.org/) 
2. Before using this program, you need to confirm that your phone has been configured according to the link below [How-do-I-run-python-on-Android-devices](https://kr1s77.github.io/2021/7/12/How-do-I-run-python-on-Android-devices/)
3. Then you can execute the Fgproxy program. After the execution is completed, the port will be mapped to 30000, 30001, 30002... The number of ports is the number of devices 
4. After that, configure haproxy for load balancing [Haproxy](https://github.com/haproxy/haproxy)
5. Since the machine is in our local area, we need to do intranet penetration to forward the local haproxy load balancing port, here we need [FRP](https://github.com/fatedier/frp)

The above is the overall configuration process. After the configuration is completed, the frp exit is our proxy port, which can be used in the crawler. 

#### Create

>   ```shell
>   $ git clone https://github.com/Kr1s77/FgSurfing.git
>   $ cd FgSurfing/proxy
>   $ python3 api.py
>   >> [2021-07-15 14:22:32,522 INFO]  ->  Count: [1] Devices Found
>   >> [2021-07-15 14:22:32,522 INFO]  ->  Deploy device: FAXXXXXXX  1/1
>   ```

#### Overall structure

The following logic is then triggered：
Clients -> Frp -> Haproxy -> Master PC -> Mobile Slaver

>         +----------------------------+
>         | CLIENT || CLIENT || CLIENT |  
>         +-------------+--------------+
>                       |
>                       |
>                       v
>         +-------------+--------------+
>         |          FRP SERVER        |
>         +-------------+--------------+
>                       |
>                       |
>                       v
>         +-------------+--------------+
>         |           HAPROXY          |
>         +-------------+--------------+
>                       |
>                       |
>                       v
>        +--------------+--------------+
>        |                             |
>        |           FGPROXY           |
>        |                             |
>        +-----------------------------+

##### HAPROXY STATUS 
<p align="center"><img src="https://raw.githubusercontent.com/Kr1s77/FgSurfing/main/haproxy.png" alt="Master"></p>

##### Currently most of it has been completed
> Anyone is welcome to participate and improve
> one person can go fast, but a group of people can go further

