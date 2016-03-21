#!/usr/bin/env python
# send message to mq

import zmq.green as zmq
import sys
import socket

def test_connect(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.close()
        return True
    except:
        return False
if test_connect('127.0.0.1',5000):

    ctx = zmq.Context()
    sock = ctx.socket(zmq.PUSH)
    sock.connect('tcp://127.0.0.1:5000')
    list = sys.argv[1:]
    sock.send_pyobj(list)
else: 
    sys.exit(1)

