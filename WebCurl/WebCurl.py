# -*- coding: utf-8 -*-
import wave
import time
import logging
import pycurl
try:
    from io import BytesIO as StringIO
except ImportError:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO

def time_reckon(function):
    def decorated_fun(*args,**kwargs):
        time_start = time.time()
        result = function(*args,**kwargs)
        time_end = time.time()
        logging.info(("Time reckon",time_end - time_start))
        return result
    return decorated_fun

@time_reckon
def get_page_data(url, head = None, curl = None):
    stream_buffer = StringIO()
    if not curl:
        curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)#curl doesn't support unicode
    if head:
        curl.setopt(pycurl.HTTPHEADER,  head)#must be list, not dict
    curl.setopt(pycurl.WRITEFUNCTION, stream_buffer.write)
    curl.setopt(pycurl.CUSTOMREQUEST,"GET")
    curl.setopt(pycurl.CONNECTTIMEOUT, 30)
    curl.setopt(pycurl.TIMEOUT, 30)
    curl.setopt(pycurl.SSL_VERIFYPEER, 0)
    curl.setopt(pycurl.SSL_VERIFYHOST, 0)
    curl.perform()
    page_data =stream_buffer.getvalue()
    stream_buffer.close()
    return page_data

@time_reckon
def post_page_data(url, data = None, head = None, curl = None):
    stream_buffer = StringIO()
    if not curl:
        curl = pycurl.Curl()
    curl.setopt(pycurl.URL, url)#curl doesn't support unicode
    if head:
        curl.setopt(pycurl.HTTPHEADER,  head)#must be list, not dict
    curl.setopt(pycurl.POSTFIELDS,  data)
    curl.setopt(pycurl.WRITEFUNCTION, stream_buffer.write)
    curl.setopt(pycurl.CUSTOMREQUEST,"POST")
    # curl.setopt(pycurl.CONNECTTIMEOUT, 30)
    # curl.setopt(pycurl.TIMEOUT, 30)
    curl.perform()
    page_data = stream_buffer.getvalue()
    stream_buffer.close()
    return page_data
