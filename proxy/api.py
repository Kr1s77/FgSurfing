# _*_ coding: utf-8 _*_
"""
Master Process


Why cluster running at ip6-localhost:8899?
/bin/bash$ adb shell cat /etc/hosts
127.0.0.1       localhost
::1             ip6-localhost

It can also run in ::1:8899.
"""
import logging
from adb import Device
from functools import partial
from command import CmdExecute
from deploy.cli import deploy_to_remote
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
    log.info(f'Count: [{len(devices)}] Devices Found')
    return devices


def _running_proxy(device: Device):
    pass


def _daemon_proxy(device: Device):
    pass


def runner(debug: bool = True, ip: str = '0.0.0.0', port: int = 30000, open_ssl: bool = True) -> None:
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

    # deploy file and running proxy and create proxy daemon
    for index, device in enumerate(devices):
        log.info(f'Deploy device: {device.device_id}  {len(devices)}/{index + 1}')
        deploy_to_remote(device=device)
        _running_proxy(device=device)
        _daemon_proxy(device=device)

    if open_ssl:
        log.info(f'FGProxy {__version__} remote running at {ip}:{port} openSSL: True')
    else:
        log.info(f'FGProxy {__version__} remote running at {ip}:{port} openSSL: False')




if __name__ == '__main__':
    runner(True, 'ip6-localhost', 8899)
