#!/usr/bin/env python
import zmq.green as zmq
import threading
import threadpool
import sendmail
import MySQLdb
ctx = zmq.Context() # create a new context to kick the wheels
sock = ctx.socket(zmq.PULL)
sock.bind('tcp://127.0.0.1:5000')

#class Alarmthread(threading.Thread):
#    def __init__(self,t_id):
#        threading.Thread.__init__(self)
#        self.t_id = t_id
#    def run():

def data_handler(alist):
    title = alist[1]
    host = title.split('--')[1].strip()
    status = title.split('--')[0].split(',')[-1]
    item = title.split('--')[0].split(',')[-2]
    new = [host,status,item]
    return new

def sendemail(user,title,body):
    
    EMAIL_SENDER="opsnotice@fangdd.com"
    EMAIL_LOGIN_NAME="opsnotice@fangdd.com"
    EMAIL_LOGIN_PASSWD="fd125@!34QW!aq"
    EMAIL_SERVER="smtp.exmail.qq.com"
    EMAIL_SERVER_PORT = 25
    user = [user]
    sendmail.send_html_mail(EMAIL_SENDER,user,title,body, EMAIL_LOGIN_NAME, EMAIL_LOGIN_PASSWD, EMAIL_SERVER, EMAIL_SERVER_PORT)
    
def write_to_db(alist):

    conn = MySQLdb.connect(host="localhost",user="root",passwd="",db="zabbix_alarm",unix_socket="/tmp/mysql.sock",charset="utf8")
    cursor = conn.cursor()
    host,status,item = alist
    sql = "insert into alarm_info(host,status,item) values ('%s','%s','%s')" % (host,status,item)
    #param = (host,status,item)
    result = cursor.execute(sql)

pool = threadpool.ThreadPool(100)
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
