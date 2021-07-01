# _*_ coding: utf-8 _*_
"""
变换一种方式，在手机上独立运行
启用一个端口，数据被客户端发送到这个端口，然后我拿着这个数据发送到目标端口
这样就完成了一个 Socket 代理的形式。
"""
import logging
from functools import partial
# from adb import Device, AdbTools
from __init__ import __author__, __version__, __site__

log = logging.getLogger(__name__)


def configure_logging(level):
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s]     %(message)s',
    )


_set_debug = partial(configure_logging, logging.DEBUG)
_set_info = partial(configure_logging, logging.INFO)


def runner(debug: bool, ip: str, port: int, open_ssl: bool = True) -> None:
    if debug:
        _set_debug()
    else:
        _set_info()

    log.info(f'author: {__author__} site: {__site__}')
    if open_ssl:
        log.info(f'FGProxy {__version__} running at {ip}:{port} openSSL: True')
    else:
        log.info(f'FGProxy {__version__} running at {ip}:{port} openSSL: False')

    # adb = AdbTools()
    # devices = [Device(device, adb=adb) for device in adb.get_remote_devices()]
    # for device in devices:
    #     network_on = device.check_4g_network()
    #     # 开启代理模式，多进程
    # # message >> 输出出来
    #
    # import time
    # import sys
    # count = 1
    # while count < 99:
    #     sys.stdout.write("current {0}%\r".format(count))
    # sys.stdout.flush()
    # count += 1
    # time.sleep(0.5)
    pass


if __name__ == '__main__':
    runner(True, '0.0.0.0', 12345)
