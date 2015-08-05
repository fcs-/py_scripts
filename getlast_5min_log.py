#!/usr/bin/env python
'''
Scripts is used to get last 5 minutes access log.
For log files like message or maillog.
'''

#import re
import time
import os, sys
from datetime import date, datetime, timedelta

#month_dict = {
#    'Jan': 1,
#    'Feb': 2,
#    'Mar': 3,
#    'Apr': 4,
#    'May': 5,
#    'Jun': 6,
#    'Jul': 7,
#    'Aug': 8,
#    'Sep': 9,
#    'Oct': 10,
#    'Nov': 11,
#    'Dec': 12,
#}

def read_line(filename, bs=1024):
    """
    Read one file in a block size.
    From end to beginning.
    """
    with open(filename) as fd:
        fd.seek(0, os.SEEK_END)
        ##Total size
        here = fd.tell()
        buf = ''
        while here > 0:
            delta = min(here, bs)
            here -= delta
            fd.seek(here, os.SEEK_SET)
            ##Read file in one block size
            chunck = fd.read(delta)
            buf = chunck + buf
            linesplit = buf.split('\n')
            buf = linesplit[0]
            for line in linesplit[1:]:
                yield line

def get_url(filename):
    '''
      Main function.
    '''
    #line_list = []
    for line in read_line(filename):
        if line == '' or line == '\n':
            continue
        log_date = convert_time(line)
        before_time = datetime.now() - timedelta(minutes=3)
        if log_date > before_time:
            yield line
        else:
            break

def convert_time(eachline):
    '''
       Function is used to find the time string and convert it
       into a datetime object.
    '''
    strdate = eachline[:15]
    Day = int(strdate[4:6])
    Month = time.strptime(strdate[:3], "%b").tm_mon
    Year = date.today().year
    Hour = int(strdate[7:9])
    Minute = int(strdate[10:12])
    Second = int(strdate[13:15])
    return datetime(Year, Month, Day, Hour, Minute, Second)

if __name__ =='__main__':
    logfile = sys.argv[1]
    #It should be sure!
    #final_list = get_url(logfile)
    for Lin in get_url(logfile):
        print Lin

