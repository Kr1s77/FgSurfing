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


class AdbTools(object):
    """Can use adb cmd...
    """
    def __init__(self):
        pass

    @staticmethod
    def turn_on_airplane_mode(device_id: str):
        os.popen(f'adb -s {device_id} shell settings put global airplane_mode_on 1')
        os.popen(f'adb -s {device_id} shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state true')

    @staticmethod
    def close_airplane_mode(device_id: str):
        os.popen(f'adb -s {device_id} shell settings put global airplane_mode_on 0')
        os.popen(f'adb -s {device_id} shell am broadcast -a android.intent.action.AIRPLANE_MODE --ez state false')
        
     
class Device(object):
    pass
