import os
from typing import Optional
from abc import ABCMeta, abstractmethod
from collections import namedtuple


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
    'ADB_PUSH':                'push',
    'GZ_DECOMPRESS':           'tar -zxf',
    'RM_DIR':                  'rm -rf',
    'MK_DIR':                  'mkdir',
    'RUN_SERVER':              'nohup python /data/local/tmp/proxy/bridge.py',
    'CHECK_PORT':              'python /data/local/tmp/proxy/network.py',
    'ROOT':                    'root',
    'PROCESS_ID':              'ps -ef | grep',
    'KILL_PROCESS':            'kill -9',
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
    'GZ_DECOMPRESS':          Cmd('GZ_DECOMPRESS',           ADB['GZ_DECOMPRESS']),
    'RM_DIR':                 Cmd('RM_DIR',                  ADB['RM_DIR']),
    'MK_DIR':                 Cmd('MK_DIR',                  ADB['MK_DIR']),
    'RUN_SERVER':             Cmd('RUN_SERVER',              ADB['RUN_SERVER']),
    'CHECK_PORT':             Cmd('CHECK_PORT',              ADB['CHECK_PORT']),
    'ROOT':                   Cmd('ROOT',                    ADB['ROOT']),
    'PROCESS_ID':             Cmd('PROCESS_ID',              ADB['PROCESS_ID']),
    'KILL_PROCESS':           Cmd('KILL_PROCESS',            ADB['KILL_PROCESS']),
}


class Command(metaclass=ABCMeta):
    without_shell_list = ['push', ]

    def __init__(self, device_id: str = None):
        self.device_id = device_id

    @abstractmethod
    def gen_cmd(self, name: Optional[str], *args) -> Optional[str]:
        """generate command...
        """
        pass


class AdbCommand(Command):
    def __init__(self, device_id: str = None):
        super(AdbCommand, self).__init__(device_id=device_id)
        self.device_id = device_id

    def gen_cmd(self, name: Optional[str], *args) -> Optional[str]:
        """ Types:
        # adb -s '...' push ././. ././.
        # adb -s '...' shell ...
        """
        command = Commands[name].command  # gen command

        if command in self.without_shell_list:
            cmd = ''.join([ADB_PREFIX.format(self.device_id), ' '.join([command, *args])])
        else:
            cmd = ''.join([ADB_PREFIX.format(self.device_id), 'shell ', ' '.join([command, *args])])

        return cmd


class CmdExecute():
    def __init__(self, command: Command):
        self.command = command

    def get_state(self):
        pass

    def execute(self, name: Optional[str], *args) -> Optional[str]:
        cmd = self.command.gen_cmd(name, *args)
        print('[Command]:', cmd)
        return self.execute_command(command=cmd)

    @staticmethod
    def execute_command(command: Optional[str]):
        value = os.popen(command).read()
        return value


