#-*- encoding:utf-8 -*-
'''
Created on 2013-12-22 21:23:37
@author: 邱景钦
'''
from lib.base import msg


EMAIL_SENDER="opsnotice@fangdd.com"
EMAIL_LOGIN_NAME="opsnotice@fangdd.com"
EMAIL_LOGIN_PASSWD="fd125@!34QW!aq"
EMAIL_SERVER="smtp.exmail.qq.com"
EMAIL_SERVER_PORT = 25

def send_mail(m_title, m_content, receiver_list=list()):
        msg.send_mail(EMAIL_SENDER, receiver_list , m_title, m_content,   EMAIL_LOGIN_NAME, EMAIL_LOGIN_PASSWD, EMAIL_SERVER, EMAIL_SERVER_PORT, m_type ="plain")
        
def send_html_mail(m_title, m_content, receiver_list=list()):
        msg.send_mail(EMAIL_SENDER, receiver_list , m_title, m_content,   EMAIL_LOGIN_NAME, EMAIL_LOGIN_PASSWD, EMAIL_SERVER, EMAIL_SERVER_PORT, m_type ="html")

if __name__ == "__main__":
    send_mail("test", "body-content", ["qiujingqin@fangdd.com"])