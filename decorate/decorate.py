#!/usr/bin/evn python

def deco(func):
	def deco_func(*args):
		print 'before func execute:'
		func(*args)
		print 'after func execute:'
	return deco_func

@deco
def jia(x,y):
	print 'x+y = %d' % (x+y)

jia(5,3)

