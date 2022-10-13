#!/usr/bin/python

# based on: https://stackoverflow.com/questions/5755507/creating-a-raw-http-request-with-sockets

import socket
from urllib.parse import urlparse
import re
import os

socket.setdefaulttimeout = 0.50
os.environ['no_proxy'] = '127.0.0.1,localhost'
linkRegex = re.compile('<a\s*href=[\'|"](.*?)[\'"].*?>')
CRLF = "\r\n\r\n"


def GET(url):
    url = urlparse(url)
    path = url.path
    print(path)
    print(url.netloc)
    if path == "":
        path = "/"
    HOST = url.netloc  # The remote host
    PORT = 80          # The same port as used by the server
    # create an INET, STREAMing socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    """
    ***********************************************************************************
    * Note that the connect() operation is subject to the timeout setting,
    * and in general it is recommended to call settimeout() before calling connect()
    * or pass a timeout parameter to create_connection().
    * The system network stack may return a connection timeout error of its own
    * regardless of any Python socket timeout setting.
    ***********************************************************************************
    """
    s.settimeout(0.30)
    """
    **************************************************************************************
    * Avoid socket.error: [Errno 98] Address already in use exception
    * The SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
    * without waiting for its natural timeout to expire.
    **************************************************************************************
    """
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    # set up TCP connection
    s.connect((HOST, PORT))
    
    msg = "GET %s HTTP/1.0%s" % (path, CRLF)
    print("msg request: \n", msg)
    
    # send HTTP get request
    s.send(msg.encode())
    
    dataAppend = ''

    # wait for response from server
    while 1:
        data = (s.recv(10000000))
        if not data: break
        else:
            dataAppend = dataAppend, repr(data)
    
    # shutdown and close tcp connection and socket
    s.shutdown(1)
    s.close()
    print('Received', dataAppend)


GET('http://www.TaylorTJohnson.com/test_cs5283_bad.html')

