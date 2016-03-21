# -*- encoding=utf-8 -*-
###
# 配置文件生成助手
#
###

import sys,os,re,datetime
from lib.base import mydate, cmd, common,output
from lib.helpers import email,html
from lib.helpers.confex import conf
from optparse import OptionParser 
import string

reload(sys) 
sys.setdefaultencoding('utf8')

def get_realpath():
    return os.path.split(os.path.realpath(__file__))[0]

def get_binname():
    return os.path.split(os.path.realpath(__file__))[1]


def main():
    parser = OptionParser()  
    parser.add_option("-f", "--file",  
                      action="store", dest="filename", default=None,  
                      help="filename to be handled!", metavar="FILE")
    (options, args) = parser.parse_args()
    
    if not options.filename or os.path.exists(os.path.abspath(options.filename)) == False:
        print "No Filename asign!"
        return
    
    with open(os.path.abspath(options.filename), "r") as f:
        lines = f.readlines()
        for line in lines:
            line = str(line).strip()
            if not line or line.startswith("#"):
                continue
            line = line.replace("\n", "")
            splitter = "[ |\t]+"
            ln_ary = re.split(splitter, line)
            
            module = ln_ary[0]
            port = ln_ary[1]
            hostip = "10.60.20.103,10.60.20.104"   ## ESF
            mails = "zhouzhangjin,qiujingqin"      ##ESF
            
            #hostip = "10.60.10.111,10.60.10.112"      ## XF
            #mails = "lixingru,qiujingqin"           ## XF
            
            content_tpl = u"hosts=$hosts; port=$port; module=$module; mails=$mails";
            contstr = string.Template(content_tpl)
            content = contstr.substitute({"hosts":hostip, "module": module, "port":port,"mails":mails})

            print content

    
if __name__ == "__main__":
    main()
