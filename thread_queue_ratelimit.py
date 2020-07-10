#coding: utf-8
import threading
import time
import Queue

#
# 脚本通过多线程和队列实现流控处理
#

# 线程数量，一次最多登录多少容器执行命令，也是队列中的个数
concurrency = 3

def get_response(var):
    """模拟任务处理
    """
    print("thread start")
    print("execute %s ..." %var)
    time.sleep(2)
    print("thread end")

def exec_thread(arg, daemon=False):
    """线程调用的简单封装
    """
    t = threading.Thread(target=get_response, args=(arg,))
    t.setDaemon(daemon)
    t.start()

def main():
    """
    使用多线程批量跑任务，提升执行效率:
       通过设定的并发数，计算出需要多少批次来执行任务，实现限流，减轻接口压力.
       通过队列来保证对象的生产与消费
    """
    paramslist = ["task1", "task2", "task3", "task4"]
    # 线程数量，一次执行多少任务，也是队列中的个数
    totalparams = len(paramslist)
    # num_queues: 需要切成几个队列
    # remainder: 相除后的余数
    num_queues, remainder = divmod(totalparams, concurrency)
    # 任务数小于指定的线程数或者任务数等于线程数
    if num_queues == 0 or totalparams == concurrency:
        for i in paramslist:
            exec_thread(i)

        return None

    # 使用队列存储请求参数
    que = Queue.Queue()
    # 余数大于0，需要增加一次循环把余数部分执行完成
    if remainder > 0:
        num_queues = num_queues + 1
    for j in range(num_queues):
        for k in paramslist[j*concurrency:(j+1)*concurrency]:
            que.put(k)
    
        while not que.empty():
            exec_thread(que.get())

        # 最后一次循环，不再sleep
        if j == num_queues - 1:
            break

        # 队列中的任务执行完成后，暂停时间
        time.sleep(2)

    return None

if __name__ == "__main__":
    main()

