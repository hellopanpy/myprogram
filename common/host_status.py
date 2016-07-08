#--*--coding:utf8--*--

'''
stat host information : cpu mem network disk
@author: panpy
'''

import os
import sys
import re
import socket
import struct
import fcntl
import psutil
import os.path
import fileinput


############
# cpu info #
############

def cpuinfo():
    '''
    return a dict contain  cpu count , cpu use percent

    '''
    d={}
    count=psutil.cpu_count()
    cpu_use='%0.2f' % psutil.cpu_percent()
    cpu_use_per=psutil.cpu_percent(percpu=True)
    cpu_use_per=[ float('%d'%x) for x in cpu_use_per ]
    d['count']=count
    d['cpu_use']=cpu_use
    d['cpu_use_per']=cpu_use_per
    return d

############
# mem info #
############

def meminfo(all=False,unit='KB'):
    '''
    return a dict contain mem total , mem free , cached , swap ; only for linux

    '''
    d={}
    with open('/proc/meminfo') as f:
        for line in f:
            key=line.split(':')[0].strip()
            num=line.split(':')[1].strip().split()[0]
            num=float(num)
            if unit == 'KB':
                value='%0.2f KB' % num
            elif unit == 'MB':
                value='%0.2f MB' % (num/1024)
            elif unit == 'GB':
                value='%0.2f GB' % (num/1024/1024)
            d[key] = value
    if all == False:
        d = {'MemTotal': d['MemTotal'],
           'MemFree': d['MemFree'],
           'Buffers': d['Buffers'],
           'Cached': d['Cached'],
           'SwapTotal': d['SwapTotal'],
           'SwapFree': d['SwapFree']
           }
    return d

#############
# disk info #
#############

def diskinfo():
    d = {}
    lt = []
    duse = {}
    l = psutil.disk_partitions()
    for i in l:
        t = [ x for x in i ]
        lt.append(t)
    d['partition'] = lt
    d['io_counters'] = psutil.disk_io_counters(perdisk=False)
    return d

def diskusage():
    d = {}
    for p in psutil.disk_partitions():
        duse = psutil.disk_usage(p.mountpoint)
        total = "total:%s GB" %(duse.total/1024/1024/1024)
        free = "free:%s GB" % (duse.free/1024/1024/1024)
        used = "used:%s GB" % (duse.used/1024/1024/1024)
        percent = "pused: %s" % duse.percent
        d[p.mountpoint] = [total,free,used,percent]
    return d
#############
# net  info #
#############

def get_hostname():
    '''
    Get fully qualified domain name from name

    '''
    return socket.getfqdn()

def get_dev():
    dev = []
    with open('/proc/net/dev','r') as f:
        for line in f:
            com = re.compile('(.*):')
            if re.match(com,line).group(1):
                dev.append(re.match(com,line).group(1).strip())
    return dev

def get_ip_old(name):
    '''
    get interface IP address for linux

    >>>import Mycommon
    >>>Mycommon.get_ip('eth0')
    '10.0.1.22'

    '''
    s=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0X8915, struct.pack('256s', ethname[:15]))[20:24])

def get_ip(name='eth0',netmask=False):
    '''
    get interface IP address for linux

    '''
    l=[]
    cmdstr='/sbin/ifconfig | grep %s -A 1' % name
    f=os.popen(cmdstr)
    f=f.read()
    ip_reg=r'([0-9]{1,3}.){3}[0-9]{1,3}'
    addr_reg=r'inet addr:%s' % ip_reg
    mask_reg=r'Mask:%s' % ip_reg
    ip_pattern=re.compile(ip_reg)
    addr_pattern=re.compile(addr_reg)
    mask_pattern=re.compile(mask_reg)
    m=re.search(addr_pattern,f)
    n=re.search(mask_pattern,f)
    if m:
        ip_str=re.search(ip_pattern,m.group()).group()
    else:
        ip_str=''
    if netmask == True:
        if n:
            mask_str=re.search(ip_pattern,n.group()).group()
        else:
            mask_str=''
        ip_str='%s/%s' % (ip_str,mask_str)
    return ip_str

def get_mac(name='eth0'):
    '''
    get interface HWADDR for linux

    '''
    cmdstr='/sbin/ifconfig | grep %s -A 1' % name
    f=os.popen(cmdstr)
    f=f.read()
    mac_reg='([0-9a-zA-Z]{1,2}\:){5}[0-9a-zA-Z]{1,2}'
    addr_reg='HWaddr %s' % mac_reg
    mac_pattern=re.compile(mac_reg)
    addr_pattern=re.compile(addr_reg)
    m=re.search(addr_pattern,f)
    if m:
        mac_str=re.search(mac_pattern,m.group()).group()
    else:
        mac_str=''
    return mac_str
def get_interface(name='eth0'):
    '''
    get interface info

    '''
    d={}
    ipaddr=get_ip(name,netmask=True).split('/')[0]
    netmask=get_ip(name,netmask=True).split('/')[1]
    hwaddr=get_mac(name)
    d['mac']=hwaddr
    d['ip']=ipaddr
    d['netmask']=netmask
    return d
def get_dev_speed(dev):
    '''
    get dev speed
    '''
    with open("/proc/net/dev","r") as f:
        com = re.compile(".*%s" %dev)
        for line in f:
            if re.match(com,line):
                rx_start = int(line.split()[1])
                tx_start = int(line.split()[9])
    time.sleep(1)
    with open("/proc/net/dev", "r") as f:
        com = re.compile(".*%s" % dev)
        for line in f:
            if re.match(com, line):
                rx_end = int(line.split()[1])
                tx_end = int(line.split()[9])
    rx_speed = "RX: %d KB/s" %((rx_end - rx_start)/1024)
    tx_speed = "TX: %d KB/s" %((tx_end - tx_start)/1024)
    return (rx_speed,tx_speed)
def tcp_connection():
    '''
    get tcp connections

    '''
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
    return TOTAL
def get_tcp_value(name):
    '''
    get tcp kernel value

    '''
    tcp_file = '/proc/sys/net/ipv4/%s' % name
    with open(tcp_file) as f:
        v = f.read().strip()
    return v
def get_default_tcp_value():
    d = {}
    kernel_key = ('ip_local_port_range', 'tcp_keepalive_time', 'tcp_syncookies', 'tcp_max_tw_buckets')
    for k in kernel_key:
        d[k] = get_tcp_value(k)
    return d

def print_host_status(self):
    print "hostname: ",get_hostname()
    print "cpuinfo: ",cpuinfo()
    print "meminfo: ",meminfo(unit='MB')
    print "diskinfo: ",diskinfo()
    print "diskusage: ",diskusage()
    for dev in get_dev():
        print "%s: "%dev,get_interface(dev)
        print "%s: " %dev,get_dev_speed(dev)
    print "tcp_connection: ",tcp_connection()
    print "tcp_value: ",get_default_tcp_value()

if __name__ == "__main__":
    hs = Host_status()
    hs.print_host_status()









