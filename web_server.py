#!/usr/bin/python

# based on: https://pythonbasics.org/webserver/
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer, SimpleHTTPRequestHandler
import time
from urllib.parse import urlparse

hostName = "localhost"
serverPort = 8080
serverDirectory = "./www/"

class MyServer(BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    # this handles the GET functionality for the web server
    def do_GET(self):
        # set server name for header
        MyServer.server_version = 'Brian Goldsmith'
        MyServer.sys_version = ''

        # enclosed main GET code in a try, just in case there are any errors
        try:
                # first check that the request file exists, if so proceed
                if(self._check_file()):
                    self.send_response(200)
                    self._set_headers()
                    with open(os.path.curdir + self.path, 'rb') as file:
                        self.wfile.write(bytes(file.read()))
                    print("should be done")

        except:
            # if the try failed for any reason, throw a 501 error
            self.send_error(501, "Server is unable to the handle request")
            self.end_headers()

    # this handles the HEAD functionality
    def do_HEAD(self):
        # set server name for header
        MyServer.server_version = 'Brian Goldsmith'
        MyServer.sys_version = ''

        # enclosed main HEAD code in a try, just in case there are any errors
        try:
            # first check that the request file exists, if so proceed
            if(self._check_file()):
                self.send_response(200)
                self._set_headers()
        except:
            # if the try failed for any reason, throw a 501 error
            self.send_error(501, "Server is unable to the handle request")
            self.end_headers()


    # _set_headers sets the additional headers and calls end_headers()
    def _set_headers(self):
        self.send_header("Content-Length", os.path.getsize(os.path.curdir + self.path))
        self.send_header("Content-type", "text/html")
        self.send_header("Connection", "close")
        self.end_headers()

    # this is a helper-method to verify the file exists or throw a 404 if it does not
    def _check_file(self):
        if self.path == "/":
            self.path = "/index.html"
        if not os.path.isfile(os.path.curdir + self.path):
            print("no files found for: " + os.path.curdir + self.path)
            self.send_error(404, "File not found")
            self.end_headers()
            return False
        else:
            print("found the file: " + os.path.curdir + self.path)
            return True




# starts the web server
def start_server(port, directory):
    web_dir = os.path.join(os.path.dirname(__file__), directory)
    print(web_dir)
    os.chdir(web_dir)
    webServer = HTTPServer((hostName, int(port)), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


# Handle the commandline arguments and make the call to start the web server
if (len(sys.argv) == 3):
    serverPort= sys.argv[1]
    serverDirectory = sys.argv[2]
    if (serverDirectory[0] == "/"):
        serverDirectory = serverDirectory[1:]

    start_server(serverPort, serverDirectory)
else:
    print("Please use the following format to start the web server:\r\npython3 web_server.py PORT DIRECTORY")