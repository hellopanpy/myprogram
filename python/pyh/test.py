#--*--coding=utf-8--*--
import os
from pyh import *

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

