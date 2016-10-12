#--*--coding:utf-8--*--

import urllib
import urllib2

url = 'http://zabbix.leoers.com/index.php'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
data = { 'name':'admin',
		 'password':'leomaster2015'
		 }
headers = { 'User-Agent' : user_agent,
			'Referer':'http:///zabbix.leoers.com'} 
data = urllib.urlencode(data)
request = urllib2.Request(url,data,headers)
response = urllib2.urlopen(request)
print response.read()

