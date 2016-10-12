#--*--coding:utf8--*--
# 
from multiprocessing import Pool
import os,time,random

def do_work(name):
	print "run NO %d process PID : %d !" %(name,os.getpid())
	#start_time = time.time()
	sleep_time = random.random() * 5
	time.sleep(sleep_time)
	print "process %d run %.2f" %(name,sleep_time)

def open_file(name):
	pass
if __name__ == "__main__":
	print "start ....."
	p = Pool()
	for i in range(5):
		p.apply_async(do_work,(i,))
	p.close()
	p.join()




