# _*_ coding: utf-8 _*_
"""
FGSurfing.api
~~~~~~~~~~~~
Use this module connect your mobile by android debug bridge
:copyright: (c) 2021 by Kris
"""
import os
import time
from network import Network
from func_timeout import exceptions
from func_timeout import func_set_timeout
from command import CmdExecute, AdbCommand


class AdbTools(object):
    """Can use adb cmd...
    """
    def __init__(self, device_id):
        self.command = AdbCommand(device_id=device_id)
        self.cmd = CmdExecute(self.command)

    # @staticmethod
    # def turn_on_airplane_mode(device_id: str):
    #     os.popen(f'adb -s {device_id} shell settings put global airplane_mode_on 1')
    #     os.popen(f'adb -s {device_id} shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true')
    #
    # @staticmethod
    # def close_airplane_mode(device_id: str):
    #     os.popen(f'adb -s {device_id} shell settings put global airplane_mode_on 0')
    #     os.popen(f'adb -s {device_id} shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false')

    def push(self, filepath: str, remote_path: str) -> str:
        return self.cmd.execute('ADB_PUSH', filepath, remote_path)

    def decompress(self, remote_path: str, remote_file: str) -> str:
        return self.cmd.execute('GZ_DECOMPRESS', remote_path, '-C', remote_file)

    def delete_and_create_dir(self, remote_path: str) -> str:
        self.cmd.execute('RM_DIR', remote_path)
        return self.cmd.execute('MK_DIR', remote_path)

     
class Device(object):
    """Android Device...
    """
    def __init__(
            self,
            device_id: str,
            port: int = 8118,
            ip: str = '0.0.0.0',
            # network: Network = Network()
    ):
        self.ip = ip
        self.port = port
        # self.network = network
        self.device_id = device_id
        self.airplane_mode_is_open = False  # 飞行模式
        self.transfer_port_is_open = False  # 手机端口
        self.device_is_died = False
        self.adb = AdbTools(device_id=device_id)  # adb
        # self.fg_network_is_open = False

        # self.init_mobile_settings()  # 初始化手机的信息

    # def init_mobile_settings(self):
    #     self.airplane_mode_is_open = self.adb.check_airplane_status(
    #         device_id=self.device_id
    #     )
    #
    #     self.transfer_port_is_open = self.network.check_local_port(
    #         port=self.port
    #     )
    #
    #     if not self.transfer_port_is_open:
    #         self.device_is_died = True
