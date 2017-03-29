#--coding:utf8--
import xlrd,xlwt
import sys
import os

def file_handle(filename):
	file_base = os.path.splitext(filename)[0]
	data = xlrd.open_workbook(filename)
	table = data.sheets()[1]
	x = table.col_values(0)[1:]
	y = table.col_values(1)[1:]
	z = zip(x,y)
	s = sorted(set(y))
	result = {}
	for i in s:
		l = []
		for j in z:
			if i in j:
				l.append(j[0])
		result[i] = l
	file = xlwt.Workbook()
	table = file.add_sheet('result',cell_overwrite_ok=True)
	table.write(0,0,u'物料')
	table.write(0,1,u'机型')
	m = 1
	for (k,v) in result.items():
		table.write(m,0,k)
		table.write(m,1,','.join(str(v))
		m = m + 1
	result_file = '%s_result.xls' % file_base
	file.save(result_file)
if __name__ == '__main__' and len(sys.argv) == 2:
	f = sys.argv[1]
	file_handle(f)

