#!/usr/bin/python
# -*- coding: utf-8 -*-

#--------------------------------------------------------
 # Module Name : examples
 # Version : 1.0.0
 #
 # Software Name : SerialCom
 # Version : 1.0
 #
 # Copyright (c) 2015 Zorglub42
 # This software is distributed under the Apache 2 license
 # <http://www.apache.org/licenses/LICENSE-2.0.html>
 #
 #--------------------------------------------------------
 # File Name   : simpleTest.py
 #
 # Created     : 2016-02
 # Authors     : Dechorgnat <dechorgnata(at)gmail.com>
 #
 # Description :
 #     Python example to connect socket server
 #--------------------------------------------------------
 # History     :
 # 1.0.0 - 2016-02-24 : Release of the file
 #
import socket
sock = socket.socket()
sock.connect(("localhost", 9999))

cmd = "V\n";

sock.send(cmd)
while 1: 
    data = sock.recv(128) 
    if not data: break
    print "value=", data
sock.close
