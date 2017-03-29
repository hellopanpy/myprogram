#--*--coding:utf-8--*--
#__author__ = 'Panpy'

import urllib2
import re

url = 'http://www.qiushibaike.com/hot/page/2'
headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
request = urllib2.Request(url,headers=headers)
response = urllib2.urlopen(request)
content = response.read().decode('utf-8')
content_com = re.compile('<div class="author clearfix">.*?<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>',re.S)

items = re.findall(content_com,content)
num = 1
for item in items:
	author = item[0]
	content = item[1].replace('<br/>',' ')
	print "### %d ###" % num
	print "author: %s" % author
	print "content: %s" % content
	print ""
	num+=1
