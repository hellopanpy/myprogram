#--*--coding:utf-8--*--

'''
monit port
'''

__version__ = '1.0'
__author__ = 'panpy'

import os
import socket
import json
import ConfigParser
from optparse import OptionParser


class Monit_port:
    '''

    '''
    def __init__(self,config_file):

        self.config_file = config_file

    def get_hostname(self):

        return socket.gethostname()

    def get_sock_list(self):

        cp = ConfigParser.ConfigParser()
        try:
            cp.read(self.config_file)
        except IOError,e:
            print e
        sock_list = [ item[1] for item in cp.items(self.get_hostname()) ]
        socks_list = [ port.split(':') for port in sock_list ]
        return  socks_list

    def test_port(self,host,port,print_std=False):
        '''

        :return:
        '''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(3)
        try:
            s.connect((str(host),int(port)))
            return 0
        except socket.error,e:
            return 111
        except:
            return 256
        # command_str = 'nc -zv %s -w 3 %s' % (host,port)
        # (exitstatus, outtext) = commands.getstatusoutput(command_str)
        # if print_std:
        #     print outtext
        # return exitstatus

if __name__ == "__main__":

    parser = OptionParser()
    parser.add_option("-p", "--port", type="string", help="monit port", dest="port", action="store")
    parser.add_option("-d", "--discovery", help="discovery json dump", dest="discovery", action="store_true")

    (options, args) = parser.parse_args()
    config_file = "/usr/local/zabbix/conf/monitor_port.conf"
    mp = Monit_port(config_file)
    if options.discovery and options.port:
        print "Print only input one options!"
        exit(1)
    elif options.discovery:
        sock_list = mp.get_sock_list()
        port_list = [ sock[1] for sock in sock_list ]
        port_data = []
        for port in port_list:
            port_data += [{'{#PORT}':port}]
        print json.dumps({'data':port_data},sort_keys=True,indent=7,separators=(',',':'))
    elif options.port:
        sock_list = mp.get_sock_list()
        for sock in sock_list:
            if options.port in sock:
                host = sock[0]
                port = sock[1]
                print mp.test_port(host,port)
    else:
        print "Invalid input!"
        exit(1)

