#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText

def send_mail(sub, content):
    '''
        to_list: to who
        sub: subject
        content: content
        send_mail(to_list, 'sub', 'content')
    ''' 
    mailto_list=['2256280155@qq.com']
    #mail_host='mail.monitor.com'
    mail_user='test1@monitor.com'
    #mail_pass='xxxx'

    #mail_user='test1'
    #mail_domain='monitor.com'
    #me = mail_user+'<'+mail_user+'@'+mail_domain+'>'

    me = mail_user+'<'+mail_user+'>'
    msg = MIMEText(content, _charset='gbk')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ';'.join(mailto_list) 

    try:
        server = smtplib.SMTP('localhost')

        ##call really mail server 
        #server = smtplib.SMTP(mail_host)
        #server.login(mail_user, mail_pass)

        server.sendmail(me, mailto_list, msg.as_string())
        server.quit()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    if send_mail(u'This is python test mail', u'python sends mail'):
        print u'Successfully sent!'
    else:
        print u'Failure sent!'
