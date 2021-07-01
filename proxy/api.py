# _*_ coding: utf-8 _*_
import sys
import time
from adb import Device, AdbTools


def runner() -> None:
    adb = AdbTools()
    devices = [Device(device, adb=adb) for device in adb.get_remote_devices()]
    for device in devices:
        network_on = device.check_4g_network()
        # 开启代理模式，多进程
    # message >> 输出出来

    import time
    import sys
    count = 1
    while count < 99:
        sys.stdout.write("current {0}%\r".format(count))
    sys.stdout.flush()
    count += 1
    time.sleep(0.5)


if __name__ == '__main__':
    runner()
