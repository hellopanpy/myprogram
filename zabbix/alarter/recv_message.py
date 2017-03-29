#!/usr/bin/env python
import zmq.green as zmq
import threading
import threadpool
import sendmail
import MySQLdb


def test_connect(ip,port):
    '''
    make a socket to test port

    '''
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((ip,int(port)))
        s.close()
        return True
    except:
        return False

#class Alarmthread(threading.Thread):
#    def __init__(self,t_id):
#        threading.Thread.__init__(self)
#        self.t_id = t_id
#    def run():

def data_handler(alist):
    '''
    format alarm data

    '''
    title = alist[1]
    host = title.split('--')[1].strip()
    status = title.split('--')[0].split(',')[-1]
    item = title.split('--')[0].split(',')[-2]
    new = [host,status,item]
    return new

def sendemail(user,title,body):
    '''
    send email to users

    '''

    user = [user]
    sendmail.send_html_mail(EMAIL_SENDER,user,title,body, EMAIL_LOGIN_NAME, EMAIL_LOGIN_PASSWD, EMAIL_SERVER, EMAIL_SERVER_PORT)

def write_to_db(alist):
    '''
    write some data to database , (IP,status,item)

    '''
    conn = MySQLdb.connect(host="localhost",user="root",passwd="",db="zabbix_alarm",unix_socket="/tmp/mysql.sock",charset="utf8")
    cursor = conn.cursor()
    host,status,item = alist
    sql = "insert into alarm_info(host,status,item) values ('%s','%s','%s')" % (host,status,item)
    #param = (host,status,item)
    result = cursor.execute(sql)

#### main part

bind_ip = '127.0.0.1'
bind_port = 5000
tcp_sock = 'tcp://%s:%s' %(bind_ip,str(bind_port))
thread_num = 100

if not test_connect(bind_ip,bind_port):
    sys.exit(1)

pool = threadpool.ThreadPool(thread_num)
ctx = zmq.Context() # create a new context to kick the wheels
sock = ctx.socket(zmq.PULL)
sock.bind(tcp_sock)

while True:
    mess = sock.recv_pyobj()
    print 'received python object:', mess
    requests = threadpool.makeRequests(sendemail,[(mess,None)])
    [pool.putRequest(req) for req in requests]
    #pool.wait()
    #user,title,body = mess
    #sendemail(user,title,body)
    db_data = data_handler(mess)
    write_to_db(db_data)