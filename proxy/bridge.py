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

REQUEST_TIMEOUT = 20
DEFAULT_CHARSET = 'UTF-8'
RECEIVE_BUFFER_SIZE = 8192


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
    # lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.tls = threading.local()
        self.tls.conns = dict()
        self._headers_buffer = list()
        super(ProxyBridge, self).__init__(*args, **kwargs)

    def parse_request(self) -> bool:
        symbol = super(ProxyBridge, self).parse_request()
        self.command = self.command.lower()
        return symbol

    def do_connect(self):
        """HANDLE HTTPS CONNECT REQUEST
        """
        return self.exec_connect_options()

    def do_get(self):
        """Handle all request protocol and all request method
        """
        return self.handle_request()

    def handle_request(self) -> None:
        req = self
        content_length = int(req.headers.get('Content-Length', 0))
        req_body = self.rfile.read(content_length) if content_length else None

        if req.path[0] == '/':
            if isinstance(self.connection, ssl.SSLSocket):
                req.path = "https://%s%s" % (req.headers['Host'], req.path)
            else:
                req.path = "http://%s%s" % (req.headers['Host'], req.path)

        u = urlsplit(req.path)
        scheme, netloc, path = u.scheme, u.netloc, (u.path + '?' + u.query if u.query else u.path)
        assert scheme in ('http', 'https')
        if netloc:
            req.headers['Host'] = netloc
        setattr(req, 'headers', filter_header(req.headers))
        origin = (scheme, netloc)

        try:
            if origin not in self.tls.conns:
                if scheme == 'https':
                    self.tls.conns[origin] = http_lib.HTTPSConnection(netloc, timeout=self.timeout)
                else:
                    self.tls.conns[origin] = http_lib.HTTPConnection(netloc, timeout=self.timeout)

            conn = self.tls.conns[origin]
            conn.request(self.command.upper(), path, req_body, dict(req.headers))
            res = conn.getresponse()
            version_table = {10: 'HTTP/1.0', 11: 'HTTP/1.1'}
            setattr(res, 'response_version', version_table[res.version])
            print("Headers: ", res.headers)
            if 'Content-Length' not in res.headers and 'no-store' in res.headers.get('Cache-Control', '')\
                    and 'Content-Encoding' not in res.headers:
                self.relay_streaming(res)
                return

            res_body = res.read()
        except Exception as e:
            if origin in self.tls.conns:
                del self.tls.conns[origin]
            self.send_error(502, str(e))
            return

        if req_body is False:
            self.send_error(403)
            return

        setattr(res, 'headers', filter_header(res.headers))

        self.wfile.write(f'{self.protocol_version} {res.status} {res.reason}\r\n'.encode(DEFAULT_CHARSET))
        for line in res.headers:
            self.wfile.write((line + ': ' + res.headers[line] + '\r\n').encode(DEFAULT_CHARSET))

        # self.end_headers()
        self._headers_buffer = [b"\r\n"]
        self.flush_headers()

        self.wfile.write(res_body)
        self.wfile.flush()

    def write_and_flush_headers(self, headers: list):
        self._headers_buffer += headers
        self.flush_headers()

    def relay_streaming(self, res):
        """查看client 是否断开链接"""
        self.wfile.write(f'{self.protocol_version} {res.status} {res.reason}\r\n' .encode(DEFAULT_CHARSET))
        for line in res.headers.headers:
            self.wfile.write(line)
        self.end_headers()
        try:
            while True:
                chunk = res.read(8192)
                if not chunk:
                    break
                self.wfile.write(chunk)
            self.wfile.flush()
        except socket.error:
            print('connection closed by client')

    def exec_connect_options(self):
        host, port = self.path.split(':', 1)
        port = int(port) or 443
        try:
            server = socket.create_connection((host, port), timeout=REQUEST_TIMEOUT)
        except Exception as e:
            return self.send_error(502, str(e))

        self.send_response(200, 'Connection Established')
        self.end_headers()

        conns = [self.connection, server]
        self.close_connection = False
        while not self.close_connection:
            read_list, write_list, error_list = select.select(conns, [], conns, self.timeout)

            if not read_list or error_list:
                break

            for read in read_list:
                symbol = self.exec_read_fd(read_conn=read, conns=conns)
                if not symbol:
                    break

    def exec_read_fd(self, read_conn, conns) -> bool:
        other = conns[1] if read_conn is conns[0] else conns[0]
        buffer = read_conn.recv(RECEIVE_BUFFER_SIZE)
        if not buffer:
            self.close_connection = True
            return False

        other.sendall(buffer)
        return True


def run(server_class=ThreadingHTTPServer, handler_class=ProxyBridge):
    host = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 10000
    print(f'server running at {host}:{port}')
    server_address = (host, int(port))
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()


if __name__ == '__main__':
    run()
