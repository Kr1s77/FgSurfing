# _*_ coding: utf-8 _*_
"""
Master Process


Why cluster running at ip6-localhost:8899?
/bin/bash$ adb shell cat /etc/hosts
127.0.0.1       localhost
::1             ip6-localhost

It can also running at ::1:8899.

Next step: Check if 4G is available.
"""
import time
import logging
from adb import Device
from functools import partial
from command import CmdExecute
from multiprocessing import Queue
from multiprocessing import Process
from deploy.cli import deploy_to_remote
from __init__ import __author__, __version__, __site__

log = logging.getLogger(__name__)


def configure_logging(level):
    logging.basicConfig(
        level=level,
        format='[Agent %(asctime)s %(levelname)s]  ->  %(message)s',
    )


_set_debug_logging = partial(configure_logging, logging.DEBUG)
_set_info_logging = partial(configure_logging, logging.INFO)

IP_SWITCHING_TIME = 1 * 60   # second
MASTER_PORT_START = 30000
HEALTH_CHECK_TIME = 1        # second
WAIT_AIRPLANE_MODE_TIME = 8  # second


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


def _forward_tcp_port(device: Device, local_port, remote_port):
    # nginx complex balanced local port
    return device.adb.forward_tcp_port(local_port, remote_port)


def kill_master_port(device: Device, port: int):
    return device.adb.kill_master_process(port)


def run_server(device, master_port):
    """
    if int(device.adb.check_remote_port(ip, port).strip()) != 0:
    The port is already in use
    """
    kill_master_port(device, master_port)
    device.adb.kill_port_process(device.port)

    # :If airplane mode is opened, first need close airplane mode
    if device.airplane_mode_is_open:
        device.adb.close_airplane_mode()
        time.sleep(WAIT_AIRPLANE_MODE_TIME)

    # :Running Proxy server command
    device.adb.running_server(host=device.ip, port=device.port)
    _forward_tcp_port(device, master_port, device.port)


def _change_ip(master_port: int, cluster_device: Device, change_ip_queue):
    """
    # :Close master port for nginx
    # :Get device info
    # :Check proxy running port
    # :Time to change ip
    # :Open master port for nginx
    """
    change_ip_queue.put_nowait(cluster_device.device_id)

    cluster_device.adb.remove_forward(master_port)
    cluster_device.adb.kill_port_process(cluster_device.port)
    cluster_device.initialize_device()

    if not cluster_device.airplane_mode_is_open:
        cluster_device.adb.turn_on_airplane_mode()
    cluster_device.adb.close_airplane_mode()

    time.sleep(WAIT_AIRPLANE_MODE_TIME)
    # if cluster_device.transfer_port_is_open is False:
    cluster_device.adb.running_server(
        host=cluster_device.ip,
        port=cluster_device.port
    )

    _forward_tcp_port(
        device=cluster_device,
        local_port=master_port,
        remote_port=cluster_device.port
    )

    change_ip_queue.get_nowait()

    time.sleep(IP_SWITCHING_TIME)


def _health_check(master_port: int, device: Device, change_ip_queue):
    # The device will not pass health check if the IP
    # is being switched, otherwise problems will occur
    if not change_ip_queue.empty():
        if device.device_id == change_ip_queue.get_nowait():
            change_ip_queue.put_nowait(device.device_id)
            time.sleep(HEALTH_CHECK_TIME)
            return None

        change_ip_queue.put_nowait(device.device_id)
        time.sleep(HEALTH_CHECK_TIME)

    device.initialize_device()
    if not device.transfer_port_is_open:
        device.adb.remove_forward(port=master_port)

    if device.airplane_mode_is_open:
        device.adb.remove_forward(port=master_port)

    time.sleep(HEALTH_CHECK_TIME)
    return None


class Daemon(object):
    def __init__(self, devices: list):
        self.devices = devices
        self.change_ip_queue = Queue()

    def worker(self, work_func, change_ip_queue):
        while True:
            for index, device in enumerate(self.devices):
                master_port = MASTER_PORT_START + index
                work_func(master_port, device, change_ip_queue)

    def run_forever(self):
        """Running change ip and health check"""
        process = [Process(target=self.worker, args=(_change_ip, self.change_ip_queue)),
                   Process(target=self.worker, args=(_health_check, self.change_ip_queue))]

        [p.start() for p in process]
        [p.join() for p in process]


def _deploy_all_device(devices: list) -> None:
    for index, device in enumerate(devices):
        log.info(f'Deploy device: {device.device_id}  {len(devices)}/{index + 1}')
        log.info(f'Device: {device.device_id} transfer port running is {device.transfer_port_is_open}')
        log.info(f'Device: {device.device_id} transfer airplane mode open is {device.airplane_mode_is_open}')
        # :Deploy and run server...
        deploy_to_remote(device=device)
        master_port = MASTER_PORT_START + index
        run_server(device=device, master_port=master_port)
        time.sleep(5)

    daemon = Daemon(devices=devices)
    daemon.run_forever()


def runner(debug: bool = True, ip: str = '0.0.0.0', port: int = 30000) -> None:
    """master entry
     1. deploy the application to the phone.
     2. get all device and init all device.
     3. kill all proxy running port
     4. running application and output log.
     """
    _init_msg(debug=debug)
    devices_str = init_all_devices()

    if not devices_str:
        log.warning('No connected mobile phone was found')
        exit(1)

    devices = [Device(device_id=device_id, port=port, ip=ip) for device_id in devices_str]
    _deploy_all_device(devices)

    log.info(f'FGProxy {__version__} remote running at {ip}:{port}')


if __name__ == '__main__':
    runner(True, 'ip6-localhost', 10000)
