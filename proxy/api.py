# _*_ coding: utf-8 _*_
"""
变换一种方式，在手机上独立运行
启用一个端口，数据被客户端发送到这个端口，然后我拿着这个数据发送到目标端口
这样就完成了一个 Socket 代理的形式。
"""
import logging
from adb import Device
from deploy.cli import create
from functools import partial
from command import CmdExecute
from __init__ import __author__, __version__, __site__

log = logging.getLogger(__name__)


def configure_logging(level):
    logging.basicConfig(
        level=level,
        format='%(asctime)s [%(levelname)s]     %(message)s',
    )


_set_debug_logging = partial(configure_logging, logging.DEBUG)
_set_info_logging = partial(configure_logging, logging.INFO)


def _init_msg(debug: bool) -> None:
    if debug:  # set debug level
        _set_debug_logging()
    else:
        _set_info_logging()

    print(f'\nauthor: [{__author__}] site: [{__site__}]')
    print(f"""
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    '  ███████╗ ██████╗ ██████╗ ██████╗  ██████╗ ██╗  ██╗██╗   ██╗ '
    '  ██╔════╝██╔════╝ ██╔══██╗██╔══██╗██╔═══██╗╚██╗██╔╝╚██╗ ██╔╝ '
    '  █████╗  ██║  ███╗██████╔╝██████╔╝██║   ██║ ╚███╔╝  ╚████╔╝  '
    '  ██╔══╝  ██║   ██║██╔═══╝ ██╔══██╗██║   ██║ ██╔██╗   ╚██╔╝   '
    '  ██║     ╚██████╔╝██║     ██║  ██║╚██████╔╝██╔╝ ██╗   ██║    '
    '  ╚═╝      ╚═════╝ ╚═╝     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝    '
                    {__site__}                             
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    """)
    return None


def init_all_devices():
    """
    List of devices attached
    1daa96050207	device
    1daa96050207	device
    :return: [1daa96050207, 1daa96050207]
    """
    devices_string = CmdExecute.execute_command('adb devices')
    devices_with_str = devices_string.split('\n')[1:-2]
    online_devices = list()
    for device_str in devices_with_str:
        if 'device' in device_str:
            online_devices.append(device_str)
    devices = list(map(lambda x: x.split('\t')[0].strip(), online_devices))
    log.info(f'[{len(devices)}] Devices Found')
    return devices


def runner(
        debug: bool = True,
        ip: str = '0.0.0.0',
        port: int = 30000,
        open_ssl: bool = True,
) -> None:
    """program entry
     1. deploy the application to the phone.
     2. get all device and init all device.
     3. running application and output log.
     """
    # init
    _init_msg(debug=debug)

    # init all devices
    devices_str = init_all_devices()

    # not have devices exit
    if not devices_str:
        log.warning('No connected phones were found')
        exit(1)

    # create all device object
    devices = list()
    for device_id in devices_str:
        devices.append(
            Device(device_id=device_id, port=port, ip=ip)
        )

    # deploy file
    for index, device in enumerate(devices):
        log.info(f'Deploy device: {device.device_id}  {len(devices)}/{index + 1}')
        create(device=device)

    if open_ssl:
        log.info(f'FGProxy {__version__} remote running at {ip}:{port} openSSL: True')
    else:
        log.info(f'FGProxy {__version__} remote running at {ip}:{port} openSSL: False')


if __name__ == '__main__':
    runner(True, '0.0.0.0', 12345)

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