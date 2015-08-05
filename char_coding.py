# -*- coding: utf-8 -*-
s="苦海无边"
print repr(s)
s2=s.decode("utf-8").encode("gbk")
print(s2)
uni=s2.decode("gbk")
print(uni)

#首先s作为utf-8的方式存储，此时的s相当于一个utf-8的编码序列，
#如果想做后续处理，首先要把它重新用utf-8解码。
#第4行的s2相当于一个gbk的编码序列，想要显示或后续处理，需要gbk解码。

#Why this error?
##UnicodeDecodeError: 'ascii' codec can't decode byte 0xe8 in position 0: ordinal not in range(128)
#在第4行，程序要做的事情是先解码，s.decode()函数默认使用ascii参数，因为是中文，必然报错。
#所以需要显式调用，并使用utf-8参数。
