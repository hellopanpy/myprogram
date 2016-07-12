#--*--coding:utf8--*--

'''
stat host information : cpu mem network disk process
@author: panpy
'''

import sys,os
import re
import socket,struct,fcntl,fileinput
import psutil
import os.path
import time
import subprocess,datetime,signal,platform

############
# cpu info #
############

def cpuinfo():
    '''
    return a dict contain  cpu count , cpu use percent

    '''
    obj = {}
    count=psutil.cpu_count()
    cpu_use='%0.2f' % psutil.cpu_percent()
    cpu_use_per=psutil.cpu_percent(percpu=True)
    cpu_use_per=[ float('%d'%x) for x in cpu_use_per ]
    obj['count']=count
    obj['cpu_use']=cpu_use
    obj['cpu_use_per']=cpu_use_per
    return obj

############
# mem info #
############

def meminfo(all=False,unit='KB'):
    '''
    return a dict contain mem total , mem free , cached , swap ; only for linux

    '''
    obj = {}
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
            obj[key] = value
    if all == False:
        obj = {'MemTotal': obj['MemTotal'],
           'MemFree': obj['MemFree'],
           'Buffers': obj['Buffers'],
           'Cached': obj['Cached'],
           'SwapTotal': obj['SwapTotal'],
           'SwapFree': obj['SwapFree']
           }
    return obj

#############
# disk info #
#############

def diskinfo():
    obj = {}
    alist = []
    l = psutil.disk_partitions()
    for i in l:
        t = [ x for x in i ]
        alist.append(t)
        obj['partition'] = alist
        obj['io_counters'] = psutil.disk_io_counters(perdisk=False)
    return obj

def diskusage():
    obj = {}
    for p in psutil.disk_partitions():
        duse = psutil.disk_usage(p.mountpoint)
        total = "total:%s GB" %(duse.total/1024/1024/1024)
        free = "free:%s GB" % (duse.free/1024/1024/1024)
        used = "used:%s GB" % (duse.used/1024/1024/1024)
        percent = "pused: %s" % duse.percent
        obj[p.mountpoint] = [total,free,used,percent]
    return obj

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
            if re.match(com,line):
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
    cmdstr='/sbin/ifconfig | grep %s -A 1' % name
    f=os.popen(cmdstr)
    f=f.read()
    addr_pattern=re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
    if re.findall(addr_pattern,f):
        ip_str = re.findall(addr_pattern,f)[0]
    else:
        ip_str=''
    if netmask == True and re.findall(addr_pattern,f):
        mask_str = re.findall(addr_pattern,f)[1]
    else:
        mask_str=''
    addr_str='%s/%s' % (ip_str,mask_str)
    return addr_str

def get_mac(name='eth0'):
    '''
    get interface HWADDR for linux

    '''
    cmdstr='/sbin/ifconfig | grep %s -A 5' % name
    f=os.popen(cmdstr)
    f=f.read()
    mac_reg='([0-9a-zA-Z]{1,2}:){5}[0-9a-zA-Z]{1,2}'
    mac_pattern=re.compile(mac_reg)
    if re.search(mac_pattern,f):
        mac_str=re.search(mac_pattern,f).group()
    else:
        mac_str=''
    return mac_str

def get_interface(name='eth0'):
    '''
    get interface info
    '''
    obj = {}
    ipaddr=get_ip(name,netmask=True).split('/')[0]
    netmask=get_ip(name,netmask=True).split('/')[1]
    hwaddr=get_mac(name)
    obj['mac']=hwaddr
    obj['ip']=ipaddr
    obj['netmask']=netmask
    return obj
def get_dev_speed(dev):
    '''
    get dev speed
    '''
    obj = {}
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
    rx_speed = "%d KB/s" %((rx_end - rx_start)/1024)
    tx_speed = "%d KB/s" %((tx_end - tx_start)/1024)
    obj = {
        'RX':rx_speed,
        'TX':tx_speed
    }
    return obj

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

    obj = {}
    kernel_key = ('ip_local_port_range', 'tcp_keepalive_time', 'tcp_syncookies', 'tcp_max_tw_buckets')
    for k in kernel_key:
        obj[k] = get_tcp_value(k)
    return obj

def docmd(command, timeout=300, debug=False, raw=False):
    '''
    run a linux shell command
    :return stdout stderr retcode
    '''
    start = datetime.datetime.now()
    ps = None
    retcode = 0
    if platform.system() == "Linux":
        ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    else:
        ps = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    while ps.poll() is None:
        time.sleep(0.2)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(ps.pid, signal.SIGINT)
            retcode = -1
            return (None, None, retcode)
    stdo = ps.stdout.readlines()
    stde = ps.stderr.readlines()

    if not ps.returncode:
        retcode = ps.returncode

    if raw == True:
        stdo = [line.strip("\n") for line in stdo]
        stde = [line.strip("\n") for line in stde]

    if raw == False:
        stdo = [str.strip(line) for line in stdo]
        stde = [str.strip(line) for line in stde]

    if debug:
        tmp_list = ["*"] * 20
        tmp_str = "".join(tmp_list)

        dbg_info = "".join(["="] * 30)
        print "%s DEBUG BEGIN %s" % (dbg_info, dbg_info)
        print "\n"

        now = time.strftime("%Y/%m/%d %H:%M:%S ", time.localtime())

        print "%s[ time ]%s\n%s\n" % (tmp_str, tmp_str, now)
        print "%s[ cmd ]%s\n%s\n" % (tmp_str, tmp_str, command)

        print "%s[ std out ]%s" % (tmp_str, tmp_str)
        for line in stdo:
            print line

        print "%s[ std error ]%s\n" % (tmp_str, tmp_str)
        for line in stde:
            print line
        print "\n"

        print "%s[ retcode ]%s\n%s\n" % (tmp_str, tmp_str, ps.returncode)

        print "%s DEBUG END %s" % (dbg_info, dbg_info)
        print "\n\n"

    return (stdo, stde, retcode)

def get_listen_port():
    '''
    get listen port
    :return: a list for listen port
    '''
    cmdstr = "netstat  -nlpt |grep -v ':::'| grep ':' | awk '{print $4}' | awk -F: '{print $2}'"
    (stdo, stde, retcode) = docmd(cmdstr)
    return stdo

def get_pid_by_port(port):
    '''
    give a port for progress and get the pid
    :param port: int
    :return: pid type int
    '''
    cmdstr = "netstat -nlpt | grep ':%s' | grep -v ':::'  |  awk '{split($7,a,\"/\");print a[1]}'" % port
    (stdo, stde, retcode) = docmd(cmdstr)
    return int(stdo[0])

def get_process_name(pid):
    '''
    get process name
    :param pid: int
    :return: process name
    '''
    p = psutil.Process(pid)
    p_name = p.name()
    return p_name
def get_process_info(pid):
    '''
    get process info
    :param pid: int
    :return: a dict for process info
    '''
    p = psutil.Process(pid)
    p_name = p.name()
    p_pwd = p.cwd()
    p_exe = p.exe()
    p_command = p.cmdline()
    p_create_time = p.create_time()
    p_cpu_time = p.cpu_times()
    p_cpu_percent = p.cpu_percent()
    p_memory_percent = p.memory_percent()
    p_memory_info = p.memory_info()
    p_connections = p.connections()
    obj = {
        'name': p_name,
        'pwd': p_pwd,
        'exe': p_exe,
        'cmdline': p_command,
        'create_time': p_create_time,
        'cpu_time': p_cpu_time,
        'cpu_percent': p_cpu_percent,
        'memory_percent': p_memory_percent,
        'memory_info': p_memory_info,
        'connections': p_connections
    }
    return obj

def print_host_status():
    '''
    print info stdout
    :return:
    '''
    astr = '#'*10
    print "%s hostname %s" %(astr,astr)
    print get_hostname()
    print "%s cpuinfo %s" %(astr,astr)
    print cpuinfo()
    print "%s meminfo %s" % (astr, astr)
    print meminfo(unit='MB')
    print "%s diskinfo %s" % (astr, astr)
    print diskinfo()
    print "%s diskusage %s" % (astr, astr)
    print diskusage()
    print "%s dev info %s" % (astr, astr)
    for dev in get_dev():
        print "%s: "%dev,get_interface(dev)
        print "%s: " %dev,get_dev_speed(dev)
    print "%s tcp info %s" % (astr, astr)
    print "tcp_connection: ",tcp_connection()
    print "tcp_value: ",get_default_tcp_value()
    print "%s process info %s" % (astr, astr)
    listen_port = get_listen_port()
    for port in listen_port:
        pid = get_pid_by_port(port)
        ps_name = get_process_name(pid)
        ps_info = get_process_info(pid)
        print "%s   %d  " % (ps_name,pid),ps_info
        print "\n"
def dump_to_json():
    '''
    dump info json
    :return: json
    '''

if __name__ == "__main__":
    print_host_status()









