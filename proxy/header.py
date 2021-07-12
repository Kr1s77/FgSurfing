# _*_ coding: utf-8 _*_
"""
FgSurfing.api
~~~~~~~~~~~~
Use this module to replace the request headers
:copyright: (c) 2021 by Kris
"""


import re


FILTER_HEADER_SEGMENTS = (
    'connection',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailers',
    'transfer-encoding',
    'upgrade'
)
FILTER_HEADER_SEGMENTS_UPPER = tuple([i.upper() for i in FILTER_HEADER_SEGMENTS])


def filter_header(headers):
    for key, upper_key in zip(FILTER_HEADER_SEGMENTS, FILTER_HEADER_SEGMENTS_UPPER):
        del headers[key]
        del headers[upper_key]

    if 'Accept-Encoding' in headers:
        ae = headers['Accept-Encoding']
        filtered_encodings = [x for x in re.split(r',\s*', ae) if x in ('identity', 'gzip', 'x-gzip', 'deflate')]
        headers['Accept-Encoding'] = ', '.join(filtered_encodings)

    return headers
