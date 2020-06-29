#!/usr/bin/env python
'''
This script is used to convert epoch time(unix time) to 
human access time in history file.
It used readlines method in file object.
'''

import time

def epoch_to_acctime():

    f=open('~/.bash_history','r')
    flist=f.readlines()
    f.close()
    Len=len(flist)
    for i in range(Len):
        #if flist[i][0]=='#' and len(flist[i][1:].strip())==10:
        if flist[i][0]=='#':
            try:
                float(flist[i][1:].strip())
            except Exception, e:
                pass
            else:
                t1 = time.localtime(float(flist[i][1:].strip()))
                tim = '#'+time.strftime("%Y-%m-%d %H:%M:%S", t1) 
                flist[i] = tim+'\n'

    f=open('~/.bash_history','w')
    f.writelines(flist)
    f.close()

if __name__ == '__main__':
    epoch_to_acctime()
