#--*--coding=utf-8--*--
import os
from pyh import *

"""
data :

2016-05-23-21,172.28.12.130,95.4,0.4,0.4,1.6,89.8,12.7,16,1540,1785,66
2016-05-23-21,172.28.12.131,92.9,0.1,0.1,0.1,78.5,8.0,16,4151,3103,98
2016-05-23-21,172.28.12.132,97.4,0.1,0.1,0.5,86.9,10.1,16,14,6,0
"""

page = PyH('zabbix report')
page << h2('zabbix report ')
#page << meta(http-equiv="Content-Type",content="text/html",charset="utf-8")
page << '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
mytab = page << table()
#with open('/var/log/zabbix/zabbix_report.csv') as f:
with open('test.txt') as f:
	lines = []
	for row in f.readlines():
		line = row.split(',')
		lines.append(line)

for r in range(len(lines)):
	mytr = mytab << tr()
	for c in range(len(lines[0])):
		mytr << td(lines[r][c])
page.printOut('out.html')