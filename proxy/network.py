# _*_ coding: utf-8 _*_
"""
Slaver Process
~~~~~~~~~~~~
Use this module to replace the request headers
:copyright: (c) 2021 by Kris
"""
import sys
import socket


class Network(object):
    def check_local_port(self, port: int, host='localhost'):
        port_msg = dict()
        port_msg['host'] = host
        port_msg['port'] = port
        return self._check_tcp_port(port_msg)

    @staticmethod
    def _check_tcp_port(port_msg: dict, timeout=2):
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (str(port_msg["host"]), int(port_msg["port"]))
        cs.settimeout(timeout)
        status = cs.connect_ex(address)
        return 1 if status == 0 else 0

    def check_remote_port(self, host: str, port: int):
        return self.check_local_port(port, host)


def check():
    host = 'localhost'
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 30000
    network = Network()
    print(network.check_remote_port(host, port))


if __name__ == '__main__':
    check()
