import os
from typing import Optional
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from adb import Device


Cmd = namedtuple('Cmd', 'name           command')

ADB_PREFIX = 'adb -s {device_id} shell '

ADB = {
    'TURN_ON_AIRPLANE_MODE':   'settings put global airplane_mode_on 1',
    'SET_AIRPLANE_MODE_ON':    'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true',
    'CLOSE_AIRPLANE_MODE':     'settings put global airplane_mode_on 1',
    'SET_AIRPLANE_MODE_OFF':   'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false',
    'CHECK_AIRPLANE_MODE':     'settings get global airplane_mode_on',
    'PING_BAIDU':              'ping -c 1 baidu.com',
    'FORWARD_DEVICE_PORT':     'forward tcp:{port} tcp:8118',
    'ADB_DEVICES':             'adb devices',
    'ADB_PUSH':                'adb push',
}


Commands = {
    'TURN_ON_AIRPLANE_MODE':  Cmd('TURN_ON_AIRPLANE_MODE',   ADB['TURN_ON_AIRPLANE_MODE']),
    'SET_AIRPLANE_MODE_ON':   Cmd('SET_AIRPLANE_MODE_ON',    ADB['SET_AIRPLANE_MODE_ON']),
    'CLOSE_AIRPLANE_MODE':    Cmd('CLOSE_AIRPLANE_MODE',     ADB['CLOSE_AIRPLANE_MODE']),
    'SET_AIRPLANE_MODE_OFF':  Cmd('SET_AIRPLANE_MODE_OFF',   ADB['SET_AIRPLANE_MODE_OFF']),
    'CHECK_AIRPLANE_MODE':    Cmd('CHECK_AIRPLANE_MODE',     ADB['CHECK_AIRPLANE_MODE']),
    'PING_BAIDU':             Cmd('PING_BAIDU',              ADB['CHECK_AIRPLANE_MODE']),
    'FORWARD_DEVICE_PORT':    Cmd('FORWARD_DEVICE_PORT',     ADB['FORWARD_DEVICE_PORT']),
    'ADB_DEVICES':            Cmd('ADB_DEVICES',             ADB['ADB_DEVICES']),
    'ADB_PUSH':               Cmd('ADB_PUSH',                ADB['ADB_PUSH']),
}


class Command(metaclass=ABCMeta):
    @abstractmethod
    def gen_cmd(self, name: Optional[str], device_id: Optional[str]) -> Optional[str]:
        """generate command...
        """
        pass


class AdbCommand(Command):
    def gen_cmd(self, name: Optional[str], device_id: Optional[str], *args) -> Optional[str]:
        cmd = ''.join([ADB_PREFIX.format(device_id), Commands[name].command, *args])
        return cmd
    
    
# class OsCommand(Command):
#     def gen_cmd(self, name: Optional[str], device_id: Optional[str]) -> Optional[str]:
#         pass


class CmdConnector():
    def __init__(self, command: Command, device: Device):
        self.command = command
        self.device = device

    def get_state(self):
        pass

    def execute(self, name: Optional[str]) -> Optional[str]:
        cmd = self.command.gen_cmd(name=name, device_id=self.device.device_id)
        value = os.popen(cmd).read()
        return value
