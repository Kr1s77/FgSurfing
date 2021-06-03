# _*_ coding: utf-8 _*_
"""
FgSurfing.api
~~~~~~~~~~~~
Use this module to replace the request headers
:copyright: (c) 2021 by Kris
"""


class Header(object):
    """Replace Request Headers"""
    def __init__(self, data: bytes):
        if not data or b'\r\n\r\n' not in data:
            self._header = None
