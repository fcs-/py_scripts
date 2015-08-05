#!/usr/bin/env python
#Script is used to get meta data and set password.
#It just run once.

import string
import random
import crypt
import os
import sys
from shlex import split
from subprocess import check_call, PIPE

def set_passwd():
    cmd_mount = '/bin/mount /dev/sr0 /mnt'
    cmd_umount = '/bin/umount /mnt'

    #Mount cdrom get meta data
    #Actually use PIPE in check_call is not good, use Popen instead.
    check_call(split(cmd_mount), stdout=PIPE, stderr=PIPE)
    with open('/mnt/openstack/latest/meta_data.json') as f:
        mt_dict = eval(f.read())

    #Encrypt password
    alphnum = string.letters + string.digits
    passwd = crypt.crypt(mt_dict['admin_pass'], 
             "$6$"+''.join([random.choice(alphnum) for i in range(8)]))
    
    cmd_setpwd = '/usr/sbin/usermod -p %s root' % passwd
    #Set password
    check_call(split(cmd_setpwd))

    #Umount cdrom
    check_call(split(cmd_umount), stdout=PIPE, stderr=PIPE)

if __name__ == '__main__':
    set_passwd()
    os.remove(sys.argv[0])
