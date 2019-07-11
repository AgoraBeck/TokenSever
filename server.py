# !/usr/bin/env python
# ! -*- coding: utf-8 -*-
"""
python2.7

Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse

import sys
import unittest
import os
import time
from random import randint
import  json

sys.path.append(os.path.join(os.path.dirname(__file__), 'Token/src/'))
import SimpleTokenBuilder
import AccessToken

appID = "970CA35de60c44645bbae8a215061b33"
appCertificate = "5CFd2fd1755d40ecb72977518be15d3b"
#channelName = "7d72365eb983485397e3e3f9d460bdda"
#uid = 2882341273
expireTimestamp = 0


class S(BaseHTTPRequestHandler):
    # def __init__(self):
    #     self.queryString = ''

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        #self.wfile.write("<html><body><h1>hi!</h1></body></html>")
        self.wfile.write("{\"key\": \"Hello Beck !\"}")

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        urlPath = urlparse.urlparse(self.path)
        print(dict(urlparse.parse_qsl(urlPath.query)))
        dicVal = dict(urlparse.parse_qsl(urlPath.query))
        cname = dicVal['cname']
        uid = dicVal['uid']
        print (cname)
        print (uid)
        token = self.getToken(cname,uid)
        print ("=========")
        print(token)
        dictToken = {}
        dictToken['Token'] = str(token)
        print (json.dumps(dictToken))
        self._set_headers()
        #self.wfile.write("<html><body><h1>beck POST!</h1></body></html>")
        #self.wfile.write("{\"Token\": \"Hello Beck !\"}")
        self.wfile.write(json.dumps(dictToken))

    def getToken(self, channelName,uid):
        builder = SimpleTokenBuilder.SimpleTokenBuilder(appID, appCertificate, channelName, uid)
        builder.initPrivileges(SimpleTokenBuilder.Role_Attendee)
        builder.setPrivilege(AccessToken.kJoinChannel, expireTimestamp)
        builder.setPrivilege(AccessToken.kPublishAudioStream, expireTimestamp)
        builder.setPrivilege(AccessToken.kPublishVideoStream, expireTimestamp)
        builder.setPrivilege(AccessToken.kPublishDataStream, expireTimestamp)

        result = builder.buildToken()
        return result

def run(server_class=HTTPServer, handler_class=S, port=8081):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()