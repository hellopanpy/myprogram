#!/usr/bin/env python
import zmq.green as zmq
import threading
import threadpool
import sendmail
import MySQLdb
ctx = zmq.Context() # create a new context to kick the wheels
sock = ctx.socket(zmq.ROUTER)
sock.bind('tcp://127.0.0.1:5000')
