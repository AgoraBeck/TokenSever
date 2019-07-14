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
import urlparse
import urllib

import sys
import os
import time
from random import randint
import ast
import  json
from zlib import crc32

sys.path.append(os.path.join(os.path.dirname(__file__), 'Token/src/'))
import SimpleTokenBuilder
import AccessToken

appID = "970CA35de60c44645bbae8a215061b33"
appCertificate = "5CFd2fd1755d40ecb72977518be15d3b"
#channelName = "7d72365eb983485397e3e3f9d460bdda"
#uid = 2882341273
expireTimestamp = 0


def getToken(channelName,uid):
    builder = SimpleTokenBuilder.SimpleTokenBuilder(appID, appCertificate, channelName, uid)
    builder.initPrivileges(SimpleTokenBuilder.Role_Attendee)
    builder.setPrivilege(AccessToken.kJoinChannel, expireTimestamp)
    builder.setPrivilege(AccessToken.kPublishAudioStream, expireTimestamp)
    builder.setPrivilege(AccessToken.kPublishVideoStream, expireTimestamp)
    builder.setPrivilege(AccessToken.kPublishDataStream, expireTimestamp)

    result = builder.buildToken()
    return result

def decorderToken(token,cname, uid):

    print ("token : " + token,  "channel : " + cname, "uid :" + str(uid))

    builder = SimpleTokenBuilder.SimpleTokenBuilder("", "", "", "")
    decoded = builder.decode(token)
    print (decoded)

    crc_uid = crc32(str(uid)) & 0xffffffff
    crc_channel = crc32(str(cname)) & 0xffffffff

    crc_uid_decoded = decoded["crc_uid"]
    crc_channel_decoded = decoded["crc_channel"]

    if crc_uid != crc_uid_decoded:
        print "uid is not matching, given " + str(crc_uid) + ", decoded " + str(decoded["crc_uid"])
    if crc_channel != crc_channel_decoded:
        print "channel is not matching, given " + str(crc_channel) + ", decoded " + str(decoded["crc_channel"])

    return decoded

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
        print (urlPath)
        #Convert 'query' to dict
        #print(dict(urlparse.parse_qsl(urlPath.query)))

        if '/getToken' == urlPath.path:
            print "success !! "
            # Get Post Data
            data1 = self.rfile.read(int(self.headers['content-length']))
            datas = urllib.unquote(data1).decode("utf-8", 'ignore')

            print (datas)
            #Convert string to dict
            print(type(ast.literal_eval(datas)))
            d = ast.literal_eval(datas)
            print(d["cname"])
            cname = d['cname']
            uid = d['uid']

            #token = self.getToken(cname,uid)
            token = getToken(cname,uid)
            print(token)
            dictToken = {}
            dictToken['token'] = str(token)
            print (json.dumps(dictToken))
            self._set_headers()
            #self.wfile.write("<html><body><h1>beck POST!</h1></body></html>")
            self.wfile.write(json.dumps(dictToken))

        if '/inverseToken' == urlPath.path:
            print ("inverseToken")
            # Get Post Data
            datas = self.rfile.read(int(self.headers['content-length']))
            data2 = urllib.unquote(datas).decode("utf-8", 'ignore')

            print (data2)
            #Convert string to dict
            print(type(ast.literal_eval(data2)))
            d = ast.literal_eval(data2)
            print(d["cname"])
            cname = d['cname']
            uid = d['uid']
            token = d["token"]

            ret = decorderToken(token,cname,uid)

            self._set_headers()
            self.wfile.write(json.dumps(ret))


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