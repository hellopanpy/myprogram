#!--*--coding:utf-8--*--

import urllib
import urllib2
import re
import sys

#reload(sys)
#sys.setdefaultencoding('utf-8')


class Taobao:
    '''
    get tao bao mm photo
    '''
    def __init__(self,baseurl,pagenum):
        self.url = str(baseurl) + "?page=%d" % pagenum

    def get_page(self,url):
        '''
        get page str
        :return: str
        '''
        _headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        _request = urllib2.Request(url, headers=_headers)
        try:
            _response = urllib2.urlopen(_request)
            _content = _response.read().decode('gbk')
            #print content
            return _content
        except Exception,e:
            print e

    def get_base_info(self,print_std=False):
        '''
        get lady base info
        :return: list [(name,infourl,imgurl),]
        '''
        page_str = self.get_page(self.url)
        info_compile = re.compile('<div class="list-item">.*?<img src="(.*?)".*?>.*?<a class="lady-name" href="(.*?)".*?>(.*?)</a>',re.S)
        items = re.findall(info_compile,page_str)
        if print_std:
            print "#### mm info ####"
            for item in items:
                print "name: %s" % item[2]
                print "photo: %s" % item[0]
                print "info: %s" % item[1]
                print ""
        return items


if __name__ == "__main__":
    taobao = Taobao('https://mm.taobao.com/json/request_top_list.htm',1)
    taobao.get_base_info(print_std=True)


