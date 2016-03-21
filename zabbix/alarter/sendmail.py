#!/usr/bin/python
#-*- encoding:utf-8 -*-
'''
Created on 2013-12-22 21:23:37
@author: 邱景钦
## change at 2015-04-20
## for zabbix alert
'''
import types
import time
import smtplib
from email.mime.text import MIMEText
import sys,re


def get_datetime():
        import datetime
        (date,tm2,haomiao) = (None,None,0)
        try:
                dt = datetime.datetime.now()
                string = str(dt)
                (date,tm) = string.split(" ")
                tm_hm_list = tm.split(".")
                haomiao = 0
                tm2 = 0
                if len(tm_hm_list) == 2:
                        tm2 = tm_hm_list[0]
                        haomiao = int(float("0.%s" % tm_hm_list[1]) * 1000)
        except :
                pass
        return (date,tm2,haomiao)

def get_nowdate():
        (date,tm,hm) = get_datetime()
        return date

def get_nowtime():
        (date,tm,hm) = get_datetime()
        return "%s %s" % (date,tm)

def send_mail(m_from, m_to_list, m_title, m_content, username="xxxx@qq.com", password="xxxx", smtp_server="smtp.qq.com", m_port=25, m_type="plain"):
        assert type(m_to_list) == types.ListType
        try:
                m_content = "\
                %s \
                \n\n\
                -------------------------------------------------------------------------\n\
                From OPS! Auto send @%s, please don't reply! \n\
                "  % (m_content, get_nowtime())
                
                if m_type == "html":
                        m_content = m_content.replace("\n", "<br />")
                
                m_charset = "utf-8"
                
                msg=MIMEText(m_content, _subtype=m_type, _charset=m_charset)
                
                msg['Subject']= m_title   #email title
                msg['From']=m_from   #sender
                msg['To']=','.join(m_to_list)  #recipient
                msg['date']=time.strftime('%a, %d %b %Y %H:%M:%S %z')  #define send datetime
                 
                smtp=smtplib.SMTP()
                smtp.connect(smtp_server, port=m_port)  #smtp server,
                #username password to login stmp server
                smtp.ehlo()
                smtp.starttls()
                smtp.login(username , password)
                smtp.sendmail(m_from , m_to_list , msg.as_string())
                smtp.quit()
                return True
        except Exception,data:
                import traceback
                tb = traceback.format_exc()
                print str(tb)
                return False
                
def send_html_mail(m_from, m_to_list, m_title, m_content, username, password, smtp_server, m_port=25):
        send_mail(m_from, m_to_list, m_title, m_content,   username, password, smtp_server, m_port=m_port, m_type ="html")
                
if __name__ == "__main__":
    

    
    if len(sys.argv[1:]) < 3:
        print "Usage:\n    %s to subject body" % (sys.argv[0])
        sys.exit()
        
    tolist = [sys.argv[1]]
    subject = sys.argv[2]
    body = sys.argv[3]
    send_html_mail(EMAIL_SENDER, tolist, subject, body, EMAIL_LOGIN_NAME, EMAIL_LOGIN_PASSWD, EMAIL_SERVER, EMAIL_SERVER_PORT)
