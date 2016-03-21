#-*- encoding:utf-8 -*-
'''
Created on 2015-03-06
@author: qiujingqin
'''

import logging
from logging.handlers import RotatingFileHandler
import os
import sys

class ColoredFormatter(logging.Formatter):
    '''A colorful formatter.'''

    def __init__(self, fmt = None, datefmt = None):
        logging.Formatter.__init__(self, fmt, datefmt)
        # Color escape string
        COLOR_RED='\033[1;31m'
        COLOR_GREEN='\033[1;32m'
        COLOR_YELLOW='\033[1;33m'
        COLOR_BLUE='\033[1;34m'
        COLOR_PURPLE='\033[1;35m'
        COLOR_CYAN='\033[1;36m'
        COLOR_GRAY='\033[1;37m'
        COLOR_WHITE='\033[1;38m'
        COLOR_RESET='\033[1;0m'
         
        # Define log color
        self.LOG_COLORS = {
            'DEBUG': '%s',
            'INFO': COLOR_GREEN + '%s' + COLOR_RESET,
            'WARNING': COLOR_YELLOW + '%s' + COLOR_RESET,
            'ERROR': COLOR_RED + '%s' + COLOR_RESET,
            'CRITICAL': COLOR_RED + '%s' + COLOR_RESET,
            'EXCEPTION': COLOR_RED + '%s' + COLOR_RESET,
        }
        
 
    def format(self, record):
        level_name = record.levelname
        msg = logging.Formatter.format(self, record)
 
        return self.LOG_COLORS.get(level_name, '%s') % msg
    


class Log(object):
    
    '''
    log
    '''
    def __init__(self, filename, level="debug", logid="qiueer"):
        try:
            self._level = level
            #print "init,level:",level,"\t","get_map_level:",self._level
            self._filename = filename
            self._logid = logid
            if os.path.exists(filename) == False:
                pass
#                 print "[ERROR] %s not EXIST!" % (filename)
#                 return
            self._logger = logging.getLogger(self._logid)

            if not len(self._logger.handlers):
                self._logger.setLevel(self.get_map_level(self._level))  
                
                fmt = '[%(asctime)s] %(levelname)s\n%(message)s'
                datefmt = '%Y-%m-%d %H:%M:%S'
                formatter = logging.Formatter(fmt, datefmt)
                
                #最多备份5个日志文件，每个日志文件最大10M
                file_handler = RotatingFileHandler(self._filename, mode='a',maxBytes=10*1024*1024,backupCount=5)
                self._logger.setLevel(self.get_map_level(self._level))  
                file_handler.setFormatter(formatter)  
                self._logger.addHandler(file_handler)
    
                stream_handler = logging.StreamHandler(sys.stderr)
                console_formatter = ColoredFormatter(fmt, datefmt)
                stream_handler.setFormatter(console_formatter)
                self._logger.addHandler(stream_handler)

        except Exception as expt:
            print expt
            
    def tolog(self, msg, level=None):
        try:
            level = level if level else self._level
            level = str(level).lower()
            level = self.get_map_level(level)
            if level == logging.DEBUG:
                self._logger.debug(msg)
            if level == logging.INFO:
                self._logger.info(msg)
            if level == logging.WARN:
                self._logger.warn(msg)
            if level == logging.ERROR:
                self._logger.error(msg)
            if level == logging.CRITICAL:
                self._logger.critical(msg)
        except Exception as expt:
            print expt
            
    def dictlog(self, level=None, width=12, fill=" ", **kwargs):
        '''
        kwargs: dict类型，如果包含order_keys，则按order_keys的先后顺序
        '''
        kwargs = dict(kwargs)
        order_keys = kwargs["order_keys"] if kwargs.has_key("order_keys") else []
        msgstr = ""
        if order_keys:
            for key in order_keys:
                if not kwargs.has_key(key): continue
                val = kwargs[key]
                msgstr = "%s%s: %s\n" % (msgstr, str(key).rjust(width), str(val))
        for (key, val) in kwargs.iteritems():
            if kwargs.has_key(key) and key not in order_keys:
                val = kwargs[key]
                msgstr = "%s%s:%s\n" % (msgstr, str(key).rjust(width), str(val))
        msgstr = "%s" % (msgstr)
        self.tolog(msgstr, level=level)
            
    def debug(self,msg):
        self.tolog(msg, level="debug")
        
    def info(self,msg):
        self.tolog(msg, level="info")
        
    def warn(self,msg):
        self.tolog(msg, level="warn")
        
    def error(self,msg):
        self.tolog(msg, level="error")
        
    def critical(self,msg):
        self.tolog(msg, level="critical")
            
    def get_map_level(self,level="debug"):
        level = str(level).lower()
        #print "get_map_level:",level
        if level == "debug":
            return logging.DEBUG
        if level == "info":
            return logging.INFO
        if level == "warn":
            return logging.WARN
        if level == "error":
            return logging.ERROR
        if level == "critical":
            return logging.CRITICAL
            
    def get_logger(self):
        return self._logger
    
    
if __name__ == "__main__":
    filename = "log-test.log"
    print "##### filename: ",filename
    Log(filename).critical("ttest")

