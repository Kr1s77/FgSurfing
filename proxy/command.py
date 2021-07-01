import os
from typing import Optional
from abc import ABCMeta, abstractmethod
from collections import namedtuple
from adb import Device


Cmd = namedtuple('Cmd', 'name           command')

ADB_PREFIX = 'adb -s {} '

ADB = {
    'TURN_ON_AIRPLANE_MODE':   'settings put global airplane_mode_on 1',
    'SET_AIRPLANE_MODE_ON':    'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true',
    'CLOSE_AIRPLANE_MODE':     'settings put global airplane_mode_on 1',
    'SET_AIRPLANE_MODE_OFF':   'am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false',
    'CHECK_AIRPLANE_MODE':     'settings get global airplane_mode_on',
    'PING_BAIDU':              'ping -c 1 baidu.com',
    'FORWARD_DEVICE_PORT':     'forward tcp:{port} tcp:8118',
    'ADB_DEVICES':             'devices',
    'ADB_PUSH':                'push ',
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
    without_shell_list = ['push', ]

    @abstractmethod
    def gen_cmd(self, name: Optional[str], device_id: Optional[str]) -> Optional[str]:
        """generate command...
        """
        pass


class AdbCommand(Command):

    def gen_cmd(self, name: Optional[str], device_id: Optional[str], *args) -> Optional[str]:
        """ Types:
        # adb -s '...' push ././. ././.
        # adb -s '...' shell ...
        """
        command = Commands[name].command  # gen command

        if command in self.without_shell_list:
            cmd = ''.join([ADB_PREFIX.format(device_id), ' '.join([command, *args])])
        else:
            cmd = ''.join([ADB_PREFIX.format(device_id), 'shell ', command, *args])

        return cmd
    
    
class OsCommand(Command):
    def gen_cmd(self, name: Optional[str], device_id: Optional[str]) -> Optional[str]:
        pass


class CmdExecute():
    def __init__(self, command: Command, device: Device):
        self.command = command
        self.device = device

    def get_state(self):
        pass

    def execute(self, name: Optional[str]) -> Optional[str]:
        cmd = self.command.gen_cmd(name=name, device_id=self.device.device_id)
        return self.execute_command(command=cmd)

    @staticmethod
    def execute_command(command: Optional[str]):
        value = os.popen(command).read()
        return value


if __name__ == '__main__':
    print(AdbCommand().gen_cmd('ADB_PUSH', 'FA74W0301990', '/xx.zip', ' /data/local/tmp'))
