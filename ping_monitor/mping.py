# -*- encoding=utf-8 -*-
###
# ping监控
# 1) support mutil group
# 2) install support extra option string
###

import sys,os,re,datetime
from lib.base import mydate, cmd, common,output
from lib.base.log import Log
from lib.helpers import email,html
from lib.helpers.confex import conf
from optparse import OptionParser
import threading
import string
import socket
import traceback

reload(sys) 
sys.setdefaultencoding('utf8')

def get_realpath():
    return os.path.split(os.path.realpath(__file__))[0]

def get_binname():
    return os.path.split(os.path.realpath(__file__))[1]

def get_logstr(list_dict, max_key_len=16, joinstr="\n"):
    log_str = ""
    for conf in list_dict:
        for (key,val) in dict(conf).iteritems():
            log_str = log_str + str(key).ljust(max_key_len) + ": " + str(val) + joinstr
    log_str = log_str.strip() # 去掉尾部 \n
    return log_str

def ds2table(dataset, table_id="result_table", keys=None):
        if not dataset: return ""
        frow = dataset[0]
        if not keys:
            keys = dict(frow).keys()
        html = u"<table id='%s' class='result_table' border='1px'>"  % (table_id)
        
        header_html = u"<tr>"
        for key in keys:
            header_html = u"%s<td style='padding: 4px'>%s</td>"  % (header_html, key)
        header_html = u"%s</tr>"  % (header_html)
        
        html = "%s%s" % (html, header_html)
        for item in dataset:
            item = dict(item)
            row = u"<tr>"
            for key in keys:
                val = item[key]
                val = str(val).replace(" ", "&nbsp;")

                row = u"%s<td class='tb_td' style='padding:4px'>%s</td>" % (row, val)
            row = u"%s</tr>" % (row)
            html = u"%s%s"    % (html, row)

        html = u"%s</table>"    % (html)
        return html
    
class MPing(threading.Thread):
    '''
    Monitor ping
    '''

    def __init__(self, iphosts, mails, logger,name=None, count=2, timeout=30, mail_subfix="fangdd.com"):
        '''
            monitor_conf 监控配置项
        '''
        threading.Thread.__init__(self, name=name)
        self._iphosts = iphosts
        self._mails = mails if mails else "qiujingqin"
        self._mail_subfix = mail_subfix if mail_subfix else "fangdd.com"
        self._count = count if count else 10
        self._timeout = timeout if timeout else 30
        self._logger = logger
    
    def __is_ip_valid(self,ip_str):
       pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
       if re.match(pattern, ip_str):
          return True
       else:
          return False
  
    def get_result(self, iphost, count):
        try:
            cmdstr = 'ping -c %s -W 1 %s ' % (count, iphost)
            (stdo, stde, retcode) = cmd.docmd_ex(cmdstr, timeout=self._timeout)
    
            logconf = [{"cmd": cmdstr}, {"retcode": retcode}, {u"stdo": stdo},{"stde": stde}]
            logstr = get_logstr(logconf, max_key_len=8)
            self._logger.error(logstr)
            
            (min, avg, max, loss, flag) = (0.0, 0.0, 0.0, 0, False)
            if retcode != 0:
                return (min, avg, max, loss, flag)
            
            flag = True
            stdo_ary = re.split("\n", str(stdo).strip())
            stdo_ary = stdo_ary[::-1]
            line1 = stdo_ary[0]
            line2 = stdo_ary[1]
            
            time_ary = re.split("[\s|\t| ]+", str(line1).strip())
            pkt_ary = re.split("[\s|\t| ]+", str(line2).strip())
            
            real_time_ary = re.split("/", str(time_ary[3]).strip())
            min =(float)(real_time_ary[0])
            avg =(float)(real_time_ary[1])
            max =(float)(real_time_ary[2])
            loss = (int)(str(pkt_ary[5]).replace("%", ""))
            return (min, avg, max, loss, flag)
        except Exception as expt:
            tb = traceback.format_exc()
            self._logger.warn(tb)
        
    def get_result_with_retry(self, iphost, count, max_retry=3):
        (min, avg, max, loss, flag) = (0.0, 0.0, 0.0, 0, False)
        for idx in range(max_retry):
            (min, avg, max, loss, flag) = self.get_result(iphost, count)
            if flag == True:
                return (min, avg, max, loss, flag)
        return (min, avg, max, loss, flag)
        
    def check(self):
        iphosts = self._iphosts
        count = self._count
        
        mails = None
        if self._mails:
            mails = str(self._mails).strip().replace(" ", "").strip(",，;；")
            #splitter = "[ |\t|,|;|\n]+"
            splitter = "[ |\t|,|，|;|；|\n]+"
            mails = re.split(splitter, mails)
            
        mail_list = list()
        for mail in mails:
            tmp_mail = str(mail).strip() + "@" + self._mail_subfix
            mail_list.append(tmp_mail)
        mail_list = mail_list if mail_list else ["qiujingqin@fangdd.com"]
            
        (min, avg, max, loss, flag) = self.get_result_with_retry(iphosts, count)
        if(flag == False):
            logconf = [{u"IP/HOST": iphosts},{"msg": u"ping不可达"}]
            logstr = get_logstr(logconf, max_key_len=8)
            self._logger.error(logstr)
            
            subjet = u"【IDC网络监测】IP: %s" % (iphosts)
            ds = [{"IP/HOST": iphosts, "msg": u"ping不可达", "min": min, "avg": avg, "max": max, "loss": loss }]
            email.send_html_mail(subjet, html.get_box_html(u"详细信息", ds2table(ds, keys=["IP/HOST", "msg", "min", "avg", "max", "loss"])), receiver_list=mail_list)
            return
        
        base = 2
        if avg > base:
            msg = u"监测%s次，平均延时大于%s" % (self._count, base)
            logconf = [{u"IP/HOST": iphosts},{u"msg": msg}, {"min": min}, {"avg": avg}, {"max": max}, {"loss": loss}]
            logstr = get_logstr(logconf, max_key_len=8)
            subjet = u"【IDC网络监测】IP: %s" % (iphosts)
            self._logger.error(logstr)
#             content = str(logstr).replace(" ", "&nbsp;")
#             email.send_html_mail(subjet, html.get_box_html(u"详细信息", content), receiver_list=mail_list)
            ds = [{"IP/HOST": iphosts, "msg": msg, "min": min, "avg": avg, "max": max, "loss": loss }]
            email.send_html_mail(subjet, html.get_box_html(u"详细信息", ds2table(ds, keys=["IP/HOST", "msg", "min", "avg", "max", "loss"])), receiver_list=mail_list)
            return
            

        logconf = [{u"IP/HOST": iphosts},{u"msg": "ok"}, {"min": min}, {"avg": avg}, {"max": max}, {"loss": loss}]
        logstr = get_logstr(logconf, max_key_len=8)
        self._logger.info(logstr)
        
        
    
    def run(self):
        self.check()



def main():
    ip = common.get_ip()
    hostname = common.get_hostname()
    binpath = get_realpath()
    binname = get_binname()
    logger = Log("/tmp/ping_check.log")
    try:
        parser = OptionParser()  

        parser.add_option("-f", "--file",  
                          action="store", dest="conffile", default=None,  
                          help="path of config file,must", metavar="FILE")
        parser.add_option("-g", "--groups",  
                          action="store", dest="groups", default=None,  
                          help="which groups to use,when no set,use the field 'groups' in config file as default", metavar="GROUPS")

        (options, args) = parser.parse_args()
        
        #check firstly
        if not options.conffile or os.path.exists(os.path.abspath(options.conffile)) == False:
            parser.print_help()
            sys.exit()

        confpath = None
        groups = None

        if options.groups:
            groups = options.groups

        confpath = os.path.abspath(options.conffile)

        insc = conf(confpath)
        configs = insc.get_config()

        for (path, confs) in dict(configs).iteritems():
            system_conf = confs["system"]
            groups_default = system_conf["groups"]

            if not groups: ## use default group
                groups = groups_default
                
            group_list = re.split("[,|;| |\t]+", groups)
            for group in group_list:
                if dict(confs).has_key(group) == False: ## check if group exist
                    msg = "no this group:%s" %(group)
                    logconf = [{"msg": msg}]
                    logstr = get_logstr(logconf, max_key_len=15)
                    logger.error(logstr)
                    continue

                monitor_conf_list = confs[group]
                thread_list = list()
                total = len(monitor_conf_list)
                
                for (idx,monitor_conf) in enumerate(monitor_conf_list):
                    idx += 1
                    tname = "%s of %s in group:%s" % (idx, total, group)
                    iphosts = monitor_conf["iphosts"]
                    mails = monitor_conf["mails"] if dict(monitor_conf).has_key("mails") else None
                    ftd = MPing(iphosts, mails, logger, name=tname, count=8, timeout=10)
                    ftd.start()
                    #ftd.join()

    except Exception as ept:
        tb = traceback.format_exc()
        logconf = [{"traceback": tb}]
        logstr = get_logstr(logconf, max_key_len=15)
        logger.error(logstr)
        email.send_html_mail(u'【公司监控IDC网络】Exception Happen!', tb, ["qiujingqin@fangdd.com"])
    
if __name__ == "__main__":
    main()

