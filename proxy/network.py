# _*_ coding: utf-8 _*_
"""
FgSurfing.api
~~~~~~~~~~~~
Use this module to replace the request headers
:copyright: (c) 2021 by Kris
"""
import os
import socket
import tempfile
try:
    import ssl
except ImportError:
    ssl = None

_DEFAULT_SSL_KEY = '''\
-----BEGIN PRIVATE KEY-----
-----END PRIVATE KEY-----
'''
_DEFAULT_SSL_CERT = '''\
-----BEGIN CERTIFICATE-----
-----END CERTIFICATE-----
'''


def _make_ssl_context():
    """Create ssl context
    https://docs.python.org/3/library/ssl.html
    """
    if ssl is None:
        return ssl
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.check_hostname = False
    ctx.load_default_certs(ssl.Purpose.SERVER_AUTH)
    ctx.verify_mode = ssl.CERT_NONE

    _cert_file = tempfile.mktemp()
    with open(_cert_file, 'w') as fw:
        fw.write(_DEFAULT_SSL_CERT)

    _keyfile = tempfile.mktemp()
    with open(_keyfile, 'w') as fw:
        fw.write(_DEFAULT_SSL_KEY)

    # load cert
    ctx.load_cert_chain(_cert_file, _keyfile)
    os.remove(_cert_file)
    os.remove(_keyfile)

    return ctx


class Network(object):
    def __init__(self, open_ssl: bool):
        if open_ssl:
            _make_ssl_context()  # open ssl context

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
    def __init__(self):
        pass
