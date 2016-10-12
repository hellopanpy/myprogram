#!/usr/bin/python

import os.path
import fileinput
import collections
######################
#/proc/net/tcp 'st':
#/proc/net/tcp 'st':
#00  ERROR_STATUS
#01  TCP_ESTABLISHED
#02  TCP_SYN_SENT
#03  TCP_SYN_RECV
#04  TCP_FIN_WAIT1
#05  TCP_FIN_WAIT2
#06  TCP_TIME_WAIT
#07  TCP_CLOSE
#08  TCP_CLOSE_WAIT
#09  TCP_LAST_ACK
#0A  TCP_LISTEN
#0B  TCP_CLOSING
#######################


tcp_files=['/proc/net/tcp','/proc/net/tcp6']
exists_tcp_files=[]
for f in tcp_files:
    if os.path.isfile(f):
        exists_tcp_files.append(f)
result = []
fh = fileinput.input(exists_tcp_files)
for line in fh:
    if line and ( 'address' not in line ):
        result.append(line.split()[3])
conn_types = {
        #'ERROR':'00',
        'ESTABLISHED':'01',
        #'SYN_SENT':'02',
        'SYN_RECV':'03',
        'FIN_WAIT1':'04',
        'FIN_WAIT2':'05',
        'TIME_WAIT':'06',
        #'CLOSE':'07',
        'CLOSE_WAIT':'08',
        'LAST_ACK':'09',
        #'LISTEN':'0A',
        #'CLOSING':'0B',
        }
TOTAL = {}
TOTAL_CONN = 0 
for k,v in conn_types.iteritems():
    c = result.count(v)
    TOTAL_CONN += c
    TOTAL[k] = c 
TOTAL['TOTAL_CONN'] = TOTAL_CONN
print TOTAL
