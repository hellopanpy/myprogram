#-*- encoding:utf-8 -*-
'''
Created on 2013-3-28

@author: albertqiu
'''

import datetime , time

class GMT8(datetime.tzinfo):
    def utcoffset(self, dt):
        return datetime.timedelta(hours=8)
      
    def dst(self, dt):
        return datetime.timedelta(hours=8)
    
    def tzname(self, dt):
        return "GMT+8"

class ADatetime():
    def __init__(self, days = 0, hours=0, minutes=0, seconds=0, debug=False):
        '''
        time offset here 
        include days, hours, minutes, seconds
        '''
        self.reset(days=days, hours=hours, minutes=minutes, seconds=seconds)
        if debug == True:
            self.debug()

    def reset(self, days = 0, hours=0, minutes=0, seconds=0):
        self._days = days
        self._hours = hours
        self._minutes = minutes
        self._seconds = seconds
        
        self._dt = datetime.datetime.now(GMT8()) - datetime.timedelta(days=self._days,hours=self._hours, minutes=self._minutes,seconds=self._seconds)
        
        return self
    
    def get_tzname(self):
        return self._dt.tzname()
    
    def get_year(self):
        return self._dt.year

    def get_month(self):
        return self._dt.month
   
    def get_day(self):
        return self._dt.day
   
    def get_hour(self):
        return self._dt.hour
   
    def get_minute(self):
        return self._dt.minute
   
    def get_weekday(self):
        return self._dt.weekday
    
    def get_second(self):
        return self._dt.second
    
    def get_microsecond(self):
        return self._dt.microsecond
    
    def get_datetime_str(self):
        return "%s%s" % (self._dt.strftime("%Y%m%d%H%M%S"), int(self.get_microsecond()/1000))
    
    def get_datetime(self):
        return self._dt.strftime("%Y-%m-%d %H:%M:%S")
    
    def get_date(self):
        return self._dt.strftime("%Y-%m-%d")
    
    def get_time(self):
        return self._dt.strftime("%H:%M:%S")
    
    def get_unix_timestap(self):
        return int(time.mktime(self._dt.timetuple()))
    
    def get_iso8601(self):
        '''
        NOT include: microsecond and time zone info
        '''
        dtstr = datetime.datetime(self.get_year(), self.get_month(), self.get_day(), self.get_hour(), self.get_minute(),self.get_second()).isoformat()
        return dtstr

    def get_iso8601_ms(self):
        '''
        include microsecond but not time zone info
        '''
        dtstr =  datetime.datetime.isoformat(self._dt)
        return dtstr
    
    def get_iso8601_tz(self):
        '''
        include: time zone info
        '''
        dtstr = datetime.datetime(self.get_year(), self.get_month(), self.get_day(), self.get_hour(), self.get_minute(),self.get_second(), 0, GMT8()).isoformat()
        return dtstr
    
    def get_iso8601_ms_tz(self):
        '''
        include: microsecond and time zone info
        '''
        dtstr = datetime.datetime(self.get_year(), self.get_month(), self.get_day(), self.get_hour(), self.get_minute(),self.get_second(), self.get_microsecond(), GMT8()).isoformat()
        return dtstr

    def debug(self):
        import string
        dtinfo = {
            "tzname": self.get_tzname(),
            "year":self.get_year(),
            "month":self.get_month(),
            "day":self.get_day(),
            "hour":self.get_hour(),
            "minute":self.get_minute(),
            "second":self.get_second(),
            "microsecond": self.get_microsecond(),
            "datetimestr": self.get_datetime_str(),
            "datetime": self.get_datetime(),
            "date": self.get_date(),
            "iso8601": self.get_iso8601(),
            "iso8601_ms": self.get_iso8601_ms(),
            "iso8601_tz": self.get_iso8601_tz(),
            "iso8601_ms_tz": self.get_iso8601_ms_tz(),
        }
        str_tpl = "tzname:$tzname\nyear:$year\nmonth:$month\nday:$day\nhour:$hour\nminute:$minute\
        \nsecond:$second\nmicrosecond:$microsecond\n\ndatetimestr:$datetimestr\ndatetime:$datetime\ndate:$date\
        \n\niso8601:$iso8601\niso8601_ms:$iso8601_ms\niso8601_tz:$iso8601_tz\niso8601_ms_tz:$iso8601_ms_tz"
        tpl = string.Template(str_tpl)
        print tpl.substitute(dtinfo)

def get_datetime():
    adt = ADatetime()
    date = adt.get_date()
    tm2 = adt.get_time()
    ms = int(adt.get_microsecond() / 1000)
    return (date,tm2,ms)


def get_nowdate():
    return ADatetime().get_date()

def get_nowtime():
    return ADatetime().get_time()

def get_datetime_str():
    return ADatetime().get_datetime_str()

def get_unix_timestamp():
    return ADatetime().get_unix_timestap()

def get_iso8601(minutes=0):
    return ADatetime(minutes=minutes).get_iso8601()
    
if __name__== "__main__":
    adt = ADatetime(days=0, hours=0, minutes=0, debug=True)
    
    print "\n############ module method ################"
    print get_datetime_str()
    print get_iso8601(minutes=0)
    print get_datetime()
    print get_nowtime()
    print get_nowdate()
    print get_unix_timestamp()

        