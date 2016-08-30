# --*--coding:utf-8--*--

# test url
import os, sys
import json
from optparse import OptionParser

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
import pycurl


class Test_url():
    def __init__(self, url):
        self.url = url
        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        self.last_url = c.getinfo(pycurl.EFFECTIVE_URL)  ## 请求url
        self.http_code = c.getinfo(pycurl.HTTP_CODE)  ## http状态码
        self.dns_resolve = c.getinfo(pycurl.NAMELOOKUP_TIME)  ## dns解析时间
        self.http_conn_time = c.getinfo(pycurl.CONNECT_TIME)  ## http建立连接时间
        self.http_start_trans = c.getinfo(pycurl.STARTTRANSFER_TIME)  ## 传输开始时间
        self.http_total_time = c.getinfo(pycurl.TOTAL_TIME)  ## 传输总时间
        self.http_download_speed = c.getinfo(pycurl.SPEED_DOWNLOAD)  ## 下载速度
        self.http_download_size = c.getinfo(pycurl.SIZE_DOWNLOAD)  ## 下载文件大小
        self.http_content_type = c.getinfo(pycurl.CONTENT_TYPE)  ## 下载文件类型
        self.http_romote_ip = c.getinfo(pycurl.PRIMARY_IP)  ## 服务器IP
        self.http_romote_port = c.getinfo(pycurl.PRIMARY_PORT)  ## 服务器端口
        self.http_local_ip = c.getinfo(pycurl.LOCAL_IP)  ## 本地IP

    def dump_to_json(self):
        http_info = {
            'last_url': self.last_url,
            'http_code': self.http_code,
            'dns_resolve': self.dns_resolve,
            'http_conn_time': self.http_conn_time,
            'http_start_trans': self.http_start_trans,
            'http_total_time': self.http_total_time,
            'http_download_speed': self.http_download_speed,
            'http_download_size': self.http_download_size,
            'http_content_type': self.http_content_type,
            'http_romote_ip': self.http_romote_ip,
            'http_romote_port': self.http_romote_port,
            'http_local_ip': self.http_local_ip
        }
        return json.dumps(http_info)

    def print_sto(self):
        print "请求URL: %s" % self.last_url
        print "http状态码: %d" % self.http_code
        print "dns解析时间: %.2f" % self.dns_resolve
        print "http建立连接时间: %.2f" % self.http_conn_time
        print "传输开始时间: %.2f" % self.http_start_trans
        print "传输总时间: %.2f" % self.http_total_time
        print "下载速度: %.2f KB/s" % (self.http_download_speed / 1024)
        print "下载文件大小: %.2f KB" % (self.http_download_size / 1024)
        print "下载文件类型: %s" % self.http_content_type
        print "服务器IP: %s" % self.http_romote_ip
        print "服务器端口: %d" % self.http_romote_port
        print "本地IP %s" % self.http_local_ip


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-u", "--url", type="string", help="test url", dest="url", action="store")
    parser.add_option("-p", "--print-sto", help="print output", dest="sto", action="store_true", )
    parser.add_option("-j", "--dump-json", help="dump json", dest="dump", action="store_true")
    (options, args) = parser.parse_args()
    if len(sys.argv) != 4:
        parser.print_help()
    else:
        if options.url and options.dump:
            try:
                test_url = Test_url(options.url)
                test_url.dump_to_json()
            except Exception, e:
                print "some problem for this URL :"
                print e
        elif options.url and options.sto:
            try:
                test_url = Test_url(options.url)
                test_url.print_sto()
            except Exception, e:
                print "Some problem for this URL :"
                print e
        else:
            parser.print_help()
