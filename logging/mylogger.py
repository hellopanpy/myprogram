#!/usr/bin/env python
# --*--coding=utf-8--*--

# auther panpy

'''
create a logger to format output 

'''
import os,sys
import logging
from logging.handlers import RotatingFileHandler

class Mylogger:
    '''
    log message to file or stdout with level
    
    '''
    def __init__(self,filename,level="debug",logid="mylog",stdout=False):
        '''
        init Mylogger class  

        '''
        self._filename=filename
        self._level = level
        self._logid = logid
        self._stdout = stdout
        # create logger
        self._level = level
        self._logid = logid
        self._stdout = stdout
        self._logger = logging.getLogger(self._logid)
        loglevel = self.get_level(self._level)
        self._logger.setLevel(loglevel)
        # set format
        formatter = logging.Formatter('%(asctime)s  %(name)s-%(levelname)s : %(message)s')
        # create fileHandler conHandler
        file_handler = RotatingFileHandler(self._filename, mode='a',maxBytes=10*1024*1024,backupCount=5)
        file_handler.setFormatter(formatter)
        self._logger.addHandler(file_handler)

        con_handler = logging.StreamHandler(sys.stdout)
        con_handler.setFormatter(formatter)
        if self._stdout == True:
            self._logger.addHandler(con_handler)
    
    def writelog(self,mess,level="debug"):
        '''
        write different level log to files

        ''' 
        level = level  if level else self._level
        level = str(level).lower()
        if level == "debug":
            self._logger.debug(mess)
        if level == "info":
            self._logger.info(mess)
        if level == "warn":
            self._logger.warn(mess)
        if level == "error":
            self._logger.error(mess)
        if level == "critical":
            self._logger.critical(mess)

    def get_level(self,level):
        '''
        change argv level to logging.level
        
        ''' 
        loglevel = str(level).lower()
        if loglevel == "debug":
            return logging.DEBUG
        if loglevel == "info":
            return logging.INFO
        if level == "warn":
            return logging.WARN
        if level == "error":
            return logging.ERROR
        if level == "critical":
            return logging.CRITICAL

if __name__ == '__main__':

    logfile="test.log"
    test_str="this is a error"
    logins=Mylogger(logfile,stdout=True)
    logins.writelog(test_str,level='error')
