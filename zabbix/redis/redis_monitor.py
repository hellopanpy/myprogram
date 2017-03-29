#!/usr/bin/env python
#-*- coding:utf8 -*-
import sys
import time
import socket 
import re
import ConfigParser
import json
import argparse
from threading import Thread
try:
	import redis
except ImportError:
	os.system('easy_install redis')

class TimeoutException(Exception):
    pass
 

class RedisServer(object):
	"""Fetches the Redis info and info commandstats metrics.
	Attributes:
		addr: Redis server hostname,as well as the Endpoint.
		port: Redis tcp port number.
		password: Redis require password, if not empty string.
	"""	
	def __init__(self,addr='127.0.0.1',port='6379',password=''):
#	def __init__(self,addr,port,password):
        	self.timelimit = 2
		self.addr = addr
		self.port = port
		self.password = password
#		logging.config.fileConfig("logging.ini")
#               self.logger = logging.getLogger(__name__)
	def redis_info(self):
		"""Fetches the Redis info and info commandstats
		
		Returns:
			redisInfo: The Redis info dict. For example: {'aof_rewrite_in_progress': 0, 'total_connections_received': 610}
			redisInfoCmdStat: The Redis info commandstats dict. For example: {'cmdstat_config': {'usec_per_call': 13.94, 'usec': 5269, 'calls': 378}}i
			redis_maxclients: The Redis maxclients configuration item, default 10000.
			redis_maxmemory:  The Redis maxmemory configuration item, default 0.
		
		"""
		
		redis_cli = redis.StrictRedis(host=self.addr,port=self.port,password=self.password)
		redisInfo = redis_cli.info()
		redisInfoCmdStat = None
                if (redisInfo["redis_version"] > "2.6"):		# version 2.6+  "info commandstats"
                        redisInfoCmdStat = redis_cli.info("commandstats") 	#All cmdstat_xx nfo
                redis_maxclients = 0
                redis_maxmemory = 0
                try:
                        maxclients_list = redis_cli.execute_command("config get maxclients")
                        if(len(maxclients_list)==2):
                                redis_maxclients = int(maxclients_list[1])
                        maxmemory_list = redis_cli.execute_command("config get maxmemory")
                        if(len(maxmemory_list) == 2 ):
                                redis_maxmemory = int(maxmemory_list[1])
                except:
	                #If you rename the "config" command in your configration file, please change the below "config_command" string.
                        maxclients_list = redis_cli.execute_command("config_command get maxclients")
                        if(len(maxclients_list) == 2):
                                redis_maxclients = int( maxclients_list[1] )
                        maxmemory_list = redis_cli.execute_command("config_command get maxmemory")
                        if(len(maxmemory_list) == 2 ):
                                redis_maxmemory = int(maxmemory_list[1])
		return (redisInfo,redisInfoCmdStat,redis_maxclients,redis_maxmemory)
	def collect_info_data(self):
		""" Restructure the redis info dict
		
		Returns:
			redis_info_dict: The final info dict.			
		"""
		redisInfo,redisInfoCmdStat,redis_maxclients,redis_maxmemory = self.redis_info()
                info_dict_all_keys = redisInfo.keys()  # the info command keys
                redis_info_dict = {}
                alldb_size = 0  	#all database keys size	
		if(redis_maxclients > 0):
                        redis_info_dict["connected_clients_pct"] =  redisInfo["connected_clients"]/float(redis_maxclients)*100
                if ( redis_maxmemory > 0 ):
                        redis_info_dict["used_memory_pct"] = redisInfo["used_memory"]/float(redis_maxmemory)*100
               # info commandstats
                if (redisInfoCmdStat is not None):
                        for cmdkey in redisInfoCmdStat:
                                redis_info_dict[cmdkey] = redisInfoCmdStat[cmdkey]["calls"]
		# discarded keys in the same list.
		redis_info_except_list = ["redis_git_sha1",
					"redis_git_sha1",
					"redis_git_dirty",
					"redis_build_id",
					"redis_mode",
					"os",
					"multiplexing_api",
					"gcc_version",
					"run_id",
					"config_file",
					"used_memory_human",
					"used_memory_peak_human",
					"mem_allocator",
					"master_host",
					"master_port"
					]
		for info_key in info_dict_all_keys:
			if info_key in redis_info_except_list:   # discard the keys 
				continue
			elif re.match("slave[0-9]+",info_key) : # slave0:ip=   discarded . 
				continue
			elif info_key == "rdb_last_bgsave_status": 
				redis_info_dict["rdb_last_bgsave_status"]=1 if redisInfo["rdb_last_bgsave_status"]=="ok" else 0
				continue
			elif info_key == "aof_last_bgrewrite_status":
				redis_info_dict["aof_last_bgrewrite_status"]=1 if redisInfo["aof_last_bgrewrite_status"]=="ok" else 0
				continue
			elif info_key == "aof_last_write_status":
				redis_info_dict["aof_last_write_status"]=1 if redisInfo["aof_last_write_status"]=="ok" else 0
				continue
			elif info_key == "role":
				redis_info_dict["role"]=1 if redisInfo["role"]=="master" else 0
				continue
			elif info_key == "master_link_status":
				redis_info_dict["master_link_status"]=1 if redisInfo["master_link_status"]=="up" else 0
				continue
			elif re.match("db[0-9]+",info_key): # sum all databases keys
				current_db = info_key	
				alldb_size = alldb_size + int(redisInfo[current_db]["keys"])
				continue
			redis_info_dict[info_key] = redisInfo[info_key]  # Normal keys
		redis_info_dict["keys"] = alldb_size		#dbsize
		## keyspace_hit_ratio
		## calculate the keyspace hit ratio every 60 seconds(one cycle).
		## the tmp files in the . path. 
                keyspace_hit_filename = "/tmp/keyspace_hits_" + str(self.port) + ".tmp"
                keyspace_miss_filename = "/tmp/keyspace_misses_" + str(self.port) + ".tmp"
                f_keyspace_hit = None
                f_keyspace_miss = None
                try:
                        f_keyspace_hit = open(keyspace_hit_filename,"r")
                        f_keyspace_miss = open(keyspace_miss_filename,"r")
                        last_hit_number = float(f_keyspace_hit.read().strip())
                        last_miss_number = float(f_keyspace_miss.read().strip())
                except IOError:
                        last_hit_number = 0
                        last_miss_number = 0
                finally:
                        if f_keyspace_hit is not None:
                                f_keyspace_hit.close()
                        if f_keyspace_miss is not None:
                                f_keyspace_miss.close()
                hit_number = float(redisInfo["keyspace_hits"])
                miss_number = float(redisInfo["keyspace_misses"])
                keyspace_hit_ratio = 0
                try:
                        keyspace_hit_ratio = (hit_number-last_hit_number)/((hit_number-last_hit_number) + (miss_number - last_miss_number))*100
                except ZeroDivisionError: 
                        keyspace_hit_ratio = 100
                f_keyspace_hit = open(keyspace_hit_filename,"w")
                f_keyspace_miss = open(keyspace_miss_filename,"w")
                f_keyspace_hit.write(str(hit_number))
                f_keyspace_miss.write(str(miss_number))
                f_keyspace_hit.close()
                f_keyspace_miss.close()
                redis_info_dict["keyspace_hit_ratio"] = keyspace_hit_ratio
		return (redis_info_dict)
    		def timelimited(timeout):
        		def decorator(function):
            			def decorator2(*args,**kwargs):
                			ThreadStop = Thread._Thread__stop
                			class TimeLimited(Thread):
                    				def __init__(self,_error= None,):
                        				Thread.__init__(self)
                        				self._error =  _error
                         
                    				def run(self):
                        				try:
                            					self.result = function(*args,**kwargs)
                        				except Exception,e:
                            					self._error =e
						 
                    				def _stop(self):
                        				if self.isAlive():
                            					ThreadStop(self)
						
                				t = TimeLimited()
                				t.start()
                				t.join(timeout)
       						
                				if isinstance(t._error,TimeoutException):
                    					t._stop()
                    					raise TimeoutException('timeout for %s' % (repr(function)))
                    					return False
                				if t.isAlive():
                    					t._stop()
                    					raise TimeoutException('timeout for %s' % (repr(function)))
                    					return False
                				if t._error is None:
                    					#return t.result
                    					#return True
            			return decorator2
        		return decorator
	@timelimited(self.timelimit)
	def get_key(self):
		key = self.get('zabbix_monitor')
        	if key == 'ok':
            		return True
    	@timelimited(self.timelimit)
    	def set_key(self):
        	return self.set('zabbix_monitor','ok')
    	@timelimited(self.timelimit)
    	def delete_key(self):
        	return self.delete('zabbix_monitor')



if __name__ == "__main__" :
	
	parser = argparse.ArgumentParser()
	parser.add_argument('-l','--list',help='get redis config section list',action='store_true') 	
	parser.add_argument('-s','--section',help='redis section',type=str)
	parser.add_argument('-k','--key',help='redis monitor key',type=str)
	parser.add_argument('-v','--value',help='redis monitor key',type=str)
	args = parser.parse_args()
	
	cf = ConfigParser.ConfigParser()
	cf.read('redis.conf')
	sections = cf.sections()
	if args.list:
		lists = []
		for i in sections:
			lists += [{'{#SECT_PORT}': i}]
			print json.dumps({'data':lists},sort_keys=True,indent=7,separators=(',',':'))
	if args.section and args.key:
		host = cf.get(args.section, "host")
		port = cf.get(args.section,"port")
		password = cf.get(args.section,"password")
		ins = RedisServer(host,port,password)

		dict = ins.collect_info_data()
		value = dict[args.key]
		print value
    	if args.section and args.value:
        	host = cf.get(args.section, "host")
        	port = cf.get(args.section,"port")
        	password = cf.get(args.section,"password")
        	ins = RedisServer(host,port,password)
        	s_result = ins.set_key()
        	g_result = ins.get_key()
        	d_result = ins.delete()
        	if s_result and g_result and d_result:
            		print 0
        	else:
            		if not s_result:
                		print 1
            		elif not g_result:
                		print 2
            		elif not d_result:
                		print 3
