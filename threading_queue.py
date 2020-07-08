#coding: utf-8

#
# Get url with multiple threading and Queue.
#

import threading
import time
import Queue
import urllib2

# url列表
link_list = ['http://www.baidu.com',
             'http://www.qq.com',
             'http://www.sogou.com']

start = time.time()

class myThread(threading.Thread):
    def __init__(self, name, q):
        threading.Thread.__init__(self)
        self.name = name
        self.q = q

    def run(self):
        print("Starting " + self.name)
        while True:
            try:
                crawler(self.name, self.q)
            except:
                break
        print("Exiting " + self.name)

def crawler(threadname, q):
    # 从队列里获取url
    url = q.get(timeout=2)
    try:
        r = urllib2.urlopen(url)
        print(q.qsize(), threadname, r.getcode(),r.geturl()) 
    except Exception as e:
        print(q.qsize(), threadname, "Error:", e)

# 创建5个线程
threadList = ["Thread-1","Thread-2","Thread-3","Thread-4","Thread-5"]

# 设置队列长度
workQueue = Queue.Queue(2)

# 线程池
threads = []

# 创建新线程
for tName in threadList:
    t1 = myThread(tName, workQueue)
    t1.start()
    threads.append(t1)

# 将url填充到队列
for url in link_list:
    workQueue.put(url)

# 等待所有线程完成
for t2 in threads:
    t2.join()

end = time.time()
#print("Queue多线程爬虫总时间为：", end-start)
print("Queue multiple threading total time: %d" %(end-start))
print("Exiting Main Thread")

