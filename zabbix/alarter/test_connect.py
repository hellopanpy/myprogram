#!/usr/bin/env python

#!/usr/bin/env python
import sys
import socket
def IsOpen(ip,port):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ip = sys.argv[1]
    port = sys.argv[2]
    try:
        s.connect((ip,int(port)))
        s.shutdown(2)
        print '%d is open' % port
        return True
    except:
        return False
