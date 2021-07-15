# _*_ coding: utf-8 _*_
"""
Socket bridge // Send & Receive
http.server: https://docs.python.org/3/library/http.server.html
"""
import ssl
import socket
import select
import sys
import threading
from socketserver import ThreadingMixIn
from urllib.parse import urlsplit

from header import filter_header
import http.client as http_lib

from http.server import BaseHTTPRequestHandler, HTTPServer

DEFAULT_CHARSET = 'UTF-8'
REQUEST_TIMEOUT = 20
RECEIVE_BUFFER_SIZE = 2 ** 14


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    address_family = socket.AF_INET6
    daemon_threads = True

    def handle_error(self, request, client_address):
        cls, e = sys.exc_info()[:2]
        if cls is socket.error or cls is ssl.SSLError:
            pass
        else:
            return HTTPServer.handle_error(self, request, client_address)


class ProxyBridge(BaseHTTPRequestHandler):
    lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.tls = threading.local()
        self.tls.conns = dict()

        self._headers_buffer = list()
        super(ProxyBridge, self).__init__(*args, **kwargs)

    def parse_request(self) -> bool:
        symbol = super(ProxyBridge, self).parse_request()
        self.command = self.command.lower()
        return symbol
