#!/usr/bin/python
# -*- coding: UTF-8 -*-

import Queue
import threading
import time

exitFlag = 0
queueLock = threading.Lock()
workQueue = Queue.Queue(50)    # 数字代表的队列的最大长度，如为空则无上限
valid_infor = []

class myThread(threading.Thread):

    def __init__(self, threadID, name, q):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.q = q

    def run(self):
        # print "Starting " + self.name
        process_data(self.q)
        # print "Exiting " + self.name


def process_data(q):
    global queueLock
    global workQueue
    global valid_infor
    global exitFlag

    while not exitFlag:
        queueLock.acquire()
        if not workQueue.empty():
            data = q.get()
            queueLock.release()

            result = add_something(data)
            if result == "TenA":
                valid_infor.append(result)
            else:
                pass
        else:
            queueLock.release()


def add_something(data):
    result = data + 'A'
    return result


def main():
    global queueLock
    global workQueue
    global valid_infor
    global exitFlag

    threads = []
    threadID = 1
    # 创建新线程
    threadList = range(5)
    for t_Num in threadList:
        thread = myThread(threadID, t_Num, workQueue)
        thread.start()
        threads.append(thread)
        threadID += 1

    # 填充队列
    queueLock.acquire()
    nameList = ["One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Ten", "Ten"]
    for word in nameList:
        workQueue.put(word)
    queueLock.release()

    # 等待队列清空
    while not workQueue.empty():
        pass

    # 通知线程是时候退出
    exitFlag = 1

    # 等待所有线程完成
    for t in threads:
        t.join()
    print "Exiting Main Thread"

    print valid_infor


if __name__ == '__main__':
    main()
