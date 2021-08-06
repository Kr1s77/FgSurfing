# _*_ coding: utf-8 _*_
"""
FGSurfing.api
~~~~~~~~~~~~
Use this module connect your mobile by android debug bridge
:copyright: (c) 2021 by Kris
"""
import os
import re
import time
from network import Network
# from func_timeout import exceptions
# from func_timeout import func_set_timeout
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

    def forward_tcp_port(self, local_port, device_port):
        return self.cmd.execute('FORWARD_DEVICE_PORT', f'tcp:{local_port} tcp:{device_port}')

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
        return self.cmd.execute('RUN_SERVER', host, str(port), '> /dev/null 2>&1 &')

    def get_server_pid(self, port: int):
        return self.cmd.execute('PROCESS_ID', str(port), '| grep python')

    def check_remote_port(self, port: int) -> bool:
        return True if self.get_server_pid(port) else False

    def start_as_root(self):
        flag = self.cmd.execute('ROOT')
        time.sleep(2)
        return flag

    def bridge_process(self):
        return self.cmd.execute('GREP')

    def kill_port_process(self, port):
        # info = self.get_server_pid(port=port)
        # # 'ps -ef | grep {port} | grep -v grep | awk "{print $2}"| sed -e "s/^/kill -9 /g" | sh'
        #
        # pid = info.split(' ')[-1].strip().split('/')[0]
        pid = self.bridge_process()
        if not pid:
            return
        return self.cmd.execute('KILL_PROCESS', pid)

    def remove_forward(self, port):
        return self.cmd.execute('FORWARD_DEVICE_PORT', f'--remove tcp:{port}')

    @staticmethod
    def kill_master_process(port):
        pid = os.popen(f'lsof -t -i:{port}').read()
        if not pid:
            return
        command = f'kill -9 {pid}'
        print(f'[Command]: {command}')
        return os.popen(command).read()

    def ping_test(self):
        ping = self.cmd.execute('PING_TEST')
        if 'ping: unknown host baidu.com' in ping:
            # 不通杀死端口
            return False

        match = re.search(r'time=(.*?) ms', ping)
        if not match:
            return False

        return True

    @staticmethod
    def check_local_port(port: int):
        """检测本地端口"""
        result = os.popen(f'echo "" | telnet 127.0.0.1 {port}').read()
        if "Escape character is '^]'" not in result:
            return False
        return True


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

        self.airplane_mode_is_open = False  # airplane mode status
        self.transfer_port_is_open = False  # device port status

        self.adb.start_as_root()  # start device as root
        self.initialize_device()  # init device message

        self.is_change_ip = False

    def initialize_device(self) -> tuple:
        self.airplane_mode_is_open = self.adb.check_airplane_status()
        self.transfer_port_is_open = self.adb.check_remote_port(
            port=self.port
        )
        return self.airplane_mode_is_open, self.transfer_port_is_open
