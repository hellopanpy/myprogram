#-*- encoding:utf-8 -*-
'''
Created on 2013-12-22 21:23:37
@author: 邱景钦
'''
import types
import time
import smtplib
from email.mime.text import MIMEText
from optparse import OptionParser
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
    
    EMAIL_SENDER="opsnotice@fangdd.com"
    EMAIL_LOGIN_NAME="opsnotice@fangdd.com"
    EMAIL_LOGIN_PASSWD="A8ikj0cD2"
    EMAIL_SERVER="smtp.exmail.qq.com"
    EMAIL_SERVER_PORT = 25
    
    parser = OptionParser()  
    parser.add_option("-s", "--subject", dest="subject", default=None,
                      action="store", help="the subject of this email", metavar="SUBJECT")  
    parser.add_option("-b", "--body",  
                      action="store", dest="body", default=None,  
                      help="the body of this email", metavar="BODY")
    parser.add_option("-t", "--to",  
                      action="store", dest="to", default=None,  
                      help="who(s) can recevice this email", metavar="TOLIST")
    parser.add_option("-f", "--format",  
                      action="store", dest="format", default=None,  
                      help="plain or html", metavar="FORMAT")
    
    (options, args) = parser.parse_args()

    
    (subject, body, tolist, fmt) = (options.subject, options.body, options.to, options.format)
    
    
    if subject and body and tolist:
        tolist = re.split("[,; ]", tolist)
        if fmt == 'html':
            send_html_mail(EMAIL_SENDER, tolist, subject, body, EMAIL_LOGIN_NAME, EMAIL_LOGIN_PASSWD, EMAIL_SERVER, EMAIL_SERVER_PORT)
        else:
            send_mail(EMAIL_SENDER, tolist, subject, body, EMAIL_LOGIN_NAME, EMAIL_LOGIN_PASSWD, EMAIL_SERVER, m_port=EMAIL_SERVER_PORT)
    else:
        print "Usage:\n\tpython %s -h" % (sys.argv[0])
    