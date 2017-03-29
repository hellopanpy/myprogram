#--*--coding:utf-8--*--

import urllib2
from lxml import etree

url = 'http://www.qiushibaike.com/hot/page/2'
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
request = urllib2.Request(url,headers=headers)
response = urllib2.urlopen(request)
html = response.read().decode('utf-8')

selector=etree.HTML(html)
authors = selector.xpath('//div[@class="author clearfix"]/a/h2/text()')
contents = selector.xpath('//div[@class="content"]/span/text()')
num = 1
for author,content in zip(authors,contents):
    print "### %d ###" % num
    print "author: %s" % author
    print "content: %s" % content
    print ""
    num += 1
