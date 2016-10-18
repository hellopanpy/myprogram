#!--*--coding:utf-8--*--

import urllib_test
import urllib2
import re

url = 'http://tieba.baidu.com/p/3138733512?see_lz=1&pn=1'

class Tieba:
    '''
    baidu tieba class
    '''
    def __init__(self,base_url,seelz=False):
        if seelz:
            self.base_url = str(base_url) + '?see_lz=1&'
        else:
            self.base_url = str(base_url) + '?see_lz=0&'

    def get_page(self,pagenum):
        '''
        get baidu tieba page code
        :param page: page num
        :return: page str
        '''
        self.full_url = self.base_url + 'pn=%d' % pagenum
        headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
        request = urllib2.Request(self.full_url, headers=headers)
        try:
            response = urllib2.urlopen(request)
            content = response.read().decode('utf-8')
            return content
        except Exception,e:
            print u'%s' % e
            return None

    def gettitle(self):
        '''
        get title
        :return: title str
        '''
        page_str = self.get_page(1)
        title_compile = re.compile('<h3 class="core_title_txt.*?title=.*?>(.*?)</h3>',re.S)
        if re.search(title_compile,page_str):
            return re.search(title_compile,page_str).group(1)
        else:
            print "get title error! no found, please check source code!"

    def getnum(self):
        '''
        get reply num
        :return: num
        '''
        page_str = self.get_page(1)
        reply_compile = re.compile('<li class="l_reply_num">.*?<span.*?>(.*?)</span>',re.S)
        if re.search(reply_compile,page_str):
            return re.search(reply_compile,page_str).group(1)
        else:
            print "get num error! no found, please check source code!"

    def getcontent(self,pagenum,print_out=False):
        '''
        get content
        :return: str
        '''
        page_str = self.get_page(pagenum)
        title_str = self.gettitle()
        #content_compile = re.compile(r'<div class="l_post l_post_bright j_l_post clearfix.*?"user_name":"(.*?)".*?"content":"(.*?)".*?"post_no":(.*?),.*?>.*?</div>',re.S)
        #content_compile = re.compile('<div class="content clearfix">.*?"post_no":(.*?),type.*?<a.*?class="p_author_name j_user_card">(.*?)</a>.*?<div id="post_content_.*?>(.*?)</div>')
        content_compile = re.compile('<a.*?class="p_author_name j_user_card".*?>(.*?)</a>.*?<div id="post_content_.*?>(.*?)(<.*?>)?</div>',re.S)
        try:
            items = re.findall(content_compile,page_str)
            if  print_out:
                print "##### %s #####" % title_str
                for item in items:
                    print "user_name : %s" % item[0]
                    print "content : %s" % item[1]
                    print ""
            return  items
        except Exception,e:
            print "check this error:"
            print str(e)



if __name__ == '__main__':
    tieba = Tieba('http://tieba.baidu.com/p/3138733512',seelz=False)
    tieba_str = tieba.getcontent(1,print_out=True)

