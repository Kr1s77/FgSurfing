# _*_ coding: utf-8 _*_
"""
FGSurfing.api
~~~~~~~~~~~~
Use this module connect your mobile by android debug bridge
:copyright: (c) 2021 by Kris
"""
import time
from network import Network
from command import CmdExecute, AdbCommand


class AdbTools(object):
    """Can use adb cmd...
    """

    def __init__(self, device_id):
        self.command = AdbCommand(device_id=device_id)
        self.cmd = CmdExecute(self.command)

    def check_airplane_status(self):
        # :Check airplane mode is open
        return True if int(self.cmd.execute('CHECK_AIRPLANE_MODE')) else False

    def turn_on_airplane_mode(self):
        self.cmd.execute('TURN_ON_AIRPLANE_MODE')
        self.cmd.execute('SET_AIRPLANE_MODE_ON')
        time.sleep(3)
        return None

    def close_airplane_mode(self):
        self.cmd.execute('CLOSE_AIRPLANE_MODE')
        self.cmd.execute('SET_AIRPLANE_MODE_OFF')
        return None

    def push(self, filepath: str, remote_path: str) -> str:
        return self.cmd.execute('ADB_PUSH', filepath, remote_path)

    def decompress(self, remote_path: str, remote_file: str) -> str:
        return self.cmd.execute('GZ_DECOMPRESS', remote_path, '-C', remote_file)

    def delete_and_create_dir(self, remote_path: str) -> str:
        self.cmd.execute('RM_DIR', remote_path)
        return self.cmd.execute('MK_DIR', remote_path)

    def running_server(self, host, port):
        return self.cmd.execute('RUN_SERVER', host, str(port), '> /dev/null', '&')

    def check_remote_port(self, port: int) -> bool:
        return True if int(self.cmd.execute('CHECK_PORT', str(port))) else False

    def start_as_root(self):
        flag = self.cmd.execute('ROOT')
        time.sleep(2)
        return flag

    def kill_port(self, port):
        return self.cmd.execute(
            'PROCESS_ID',
            str(port),
            '| grep -v grep | awk "{print $2}"| sed -e "s/^/kill -9 /g" | sh'
        )


class Device(object):
    """Android Device...
    """

    def __init__(
            self,
            device_id: str,
            port: int = 8118,
            ip: str = '0.0.0.0',
            network: Network = Network()
    ):
        self.ip = ip
        self.port = port
        self.network = network
        self.device_id = device_id
        self.adb = AdbTools(device_id=device_id)  # adb

        self.airplane_mode_is_open = False  # 飞行模式
        self.transfer_port_is_open = False  # 手机端口

        self.initialize_device()  # 初始化手机的信息

    def initialize_device(self) -> None:
        self.adb.start_as_root()  # start device as root

        self.airplane_mode_is_open = self.adb.check_airplane_status()
        self.transfer_port_is_open = self.adb.check_remote_port(
            port=self.port
        )
        return None
