#--*--coding=utf-8--*--
import sys,os
import datetime
import ping
from multiprocessing import Process
from multiprocessing import Pool

LOGDIR="."
hosts=['128.199.181.178']


def run(ip):
    now = datetime.datetime.now().strftime('%Y-%m-%d %T')
    loss,max_rtt,avg_rtt = ping.quiet_ping(ip,timeout=1, count=100, psize=8)
    print loss,max_rtt,avg_rtt,ip
    fullname = os.path.join(LOGDIR, "%s.log" % ip)
    with open(fullname, "a") as f:
        if max_rtt:
            f.write("%-16s %4d %8.4f %8.4f\n" %(now,loss,max_rtt,avg_rtt))
        else:
            f.write("%-16s %4d" % (now,loss))
p = Pool()
for ip in hosts:
    p.apply_async(run, args=(ip,))
p.close()
p.join()