# _*_ coding: utf-8 _*_
"""
FgSurfing.api
~~~~~~~~~~~~
Use this module to replace the request headers
:copyright: (c) 2021 by Kris
"""
import socket


class Network(object):
    def check_local_port(self, port: int):
        port_msg = dict()
        port_msg['host'] = 'localhost'
        port_msg['port'] = port
        return self._check_tcp_port(port_msg)

    @staticmethod
    def _check_tcp_port(port_msg: dict, timeout=2):
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (str(port_msg["host"]), int(port_msg["port"]))
        cs.settimeout(timeout)
        status = cs.connect_ex(address)
        return True if status == 0 else False
    
    
class ProxyServer(object):
    pass
