# -*- encoding=utf-8 -*-
###
# ping监控
# 1) support mutil group
# 2) install support extra option string
###

import sys,os,re,datetime
from lib.base import mydate, cmd, common,output
from lib.helpers import email,html
from lib.helpers.confex import conf
from optparse import OptionParser
import threading
import string
import socket

reload(sys) 
sys.setdefaultencoding('utf8')

def get_realpath():
    return os.path.split(os.path.realpath(__file__))[0]

def get_binname():
    return os.path.split(os.path.realpath(__file__))[1]

class MPing(threading.Thread):
    '''
    Monitor ping
    '''

    def __init__(self,monitor_conf, name=None, times=2, mail_subfix="fangdd.com"):
        '''
            monitor_conf 监控配置项
        '''
        threading.Thread.__init__(self,name=name)
        self.monitor_conf = monitor_conf
        self.mail_subfix = mail_subfix
        self.times = times
    
    def __is_ip_valid(self,ip_str):
       pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"
       if re.match(pattern, ip_str):
          return True
       else:
          return False
  
    def check(self, ip):
        """
            return: -2  exception, -1 Wrong IP, 1 ok, 0 failure
        """
        try:
            if self.__is_ip_valid(ip) == False:
                return (-1, "Wrong IP")
            result = os.system('ping -c %s -W 1 %s 1>/dev/null 2>&1' % (self.times,ip))
            if(result == 0):
                return (1,"Check OK")
            return (0, "Failure")
        except Exception as e:
            return (-2,"Exception")
    
    def run(self):
        """
        """
        try:
            monitor_conf = dict(self.monitor_conf)
            
            must_fds = ["hosts","mails","module"]
            check_res = True
            for fds in must_fds:
                check_res = check_res & monitor_conf.has_key(fds) 
            if check_res == False:
                output.error("[%s][ERROR] monitor config item must contain [%s],ignore" % (self.getName(), ",".join(must_fds)))
                print monitor_conf,"\n"
                return
            
            hosts_str = monitor_conf["hosts"]
            mails_str = monitor_conf["mails"]
            module  = monitor_conf["module"]
            
            tmp_mails = list()
            mails = list()
            if mails_str:
                splitter = "[ |\t,]+"
                tmp_mails = re.split(splitter, mails_str)

            for mail in tmp_mails:
                mails.append("%s@%s" % (mail, self.mail_subfix))

            hosts = list()
            if hosts_str:
                splitter = "[ |\t,]+"
                hosts = re.split(splitter, hosts_str)

            for host in hosts:
                (ret, status) = self.check(host)
                infostr = "[%s][%s]\nIPHOST:%s\nMODULE:%s\nRET:%s\nSTATUS:%s\n" % (self.getName(),mydate.ADatetime().get_datetime(),host, module, ret, status)
                if ret in [0,"0"]:
                    output.error(infostr)
                    self.mail(host, module, mails)
                else:
                    print infostr
                    
        except Exception as expt:
            tb = common.print_traceback_detail()
            
    def mail(self, host_ip, module, mails):
        try:
            subject = u"【Ping监控】服务:%s 主机IP:%s Ping不可达 " % (module, host_ip)

            content_tpl = "\
            主机IP：$host_ip<br />\
            服务：$module <br />\
            "
            contstr = string.Template(content_tpl)
            content = contstr.substitute({"host_ip":host_ip, "module": module})
            content = html.get_box_html(u"详细信息",content)
    
            email.send_html_mail(subject, content, mails)
        except Exception as expt:
            tb = common.print_traceback_detail()
            print tb
            
def install_this(option_str=None):
    uninstall_this()
    binname = get_binname()
    binpath = get_realpath()
    now = mydate.get_datetime_str()
    backup_file = "/tmp/bakcront_%s" % (now)
    (stdo, stde, retcode) = cmd.docmd("crontab -l > %s" % (backup_file))
    if retcode == 0:
        output.info("backup crontab OK! stored in : %s" % (backup_file))
    
    tmp_cron_file = "/tmp/tmpcront_%s" % (now)
    (stdo, stde, retcode) = cmd.docmd("crontab -l > %s" % (tmp_cron_file))
    print (stdo, stde, retcode)
    fd = open(tmp_cron_file, "a")

    if not option_str:
        option_str = ""
    this_cron_str = "\n##[%s] %s\n\
*/1 * * * * cd %s && python %s %s >/tmp/%s.log 2>&1\n\n" % (mydate.ADatetime().get_datetime(),binname, binpath, binname, option_str, binname)
    fd.write(this_cron_str)
    fd.close()
    
    (stdo, stde, retcode) = cmd.docmd("crontab %s" % (tmp_cron_file))
    print (stdo, stde, retcode)

def uninstall_this():
    binname = get_binname()
    binpath = get_realpath()
    now = mydate.get_datetime_str()
    backup_file = "/tmp/bakcront_%s" % (now)
    (stdo, stde, retcode) = cmd.docmd("crontab -l > %s" % (backup_file))
    if retcode == 0:
        output.info("backup crontab OK! stored in : %s" % (backup_file))
        
    tmp_cron_file = "/tmp/tmpcront_%s" % (now)
    (stdo, stde, retcode) = cmd.docmd("crontab -l | grep -Ev '%s' | grep -Ev '%s' > %s" % (binname, binpath, tmp_cron_file))
    (stdo, stde, retcode) = cmd.docmd("crontab %s" % (tmp_cron_file))
    print (stdo, stde, retcode)

def main():
    ip = common.get_ip()
    hostname = common.get_hostname()
    binpath = get_realpath()
    binname = get_binname()
    try:
        parser = OptionParser()  
        parser.add_option("-i", "--install", dest="install", default=False,
                          action="store_true", help="install this script to crontab")  
        parser.add_option("-u", "--uninstall",  
                          action="store_true", dest="uninstall", default=False,  
                          help="uninstall this script fron crontab")
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

        if options.install == True:
            option_str = ""
            if options.conffile:
                option_str = "%s -f %s" % (option_str, options.conffile)
            if options.groups:
                 option_str = "%s -g %s" % (option_str, options.groups)
            install_this(option_str)
            return

        if options.uninstall == True:
            uninstall_this()
            return

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
                    errstr = "[%s]No this group: %s\n" % (mydate.ADatetime().get_datetime(),group)
                    output.error(errstr)
                    continue

                monitor_conf_list = confs[group]
                thread_list = list()
                total = len(monitor_conf_list)
                
                for (idx,monitor_conf) in enumerate(monitor_conf_list):
                    idx += 1
                    tname = "%s of %s in group:%s" % (idx, total, group)
                    ftd = MPing(monitor_conf,name=tname)
                    ftd.start()
                    #ftd.join()

    except Exception as ept:
        tb = common.print_traceback_detail()
        tb = "%s<br />@%s|%s %s/%s" % (tb, ip, hostname, binpath, binname)
        email.send_html_mail(u'Exception Happen!', tb, ["qiujingqin@fangdd.com"])
    
if __name__ == "__main__":
    main()

