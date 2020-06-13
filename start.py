"""
New's Search Engine

Created on Wes Jun 11, 2020

@author: Liwei Wang
"""

import os
import multiprocessing
import threading

def p1():
    os.system("python Backend/api.py")

def p2():
    os.system("serve -s build")

if __name__ == "__main__":

# 多线程启动 成功 （一个进程多个线程）

    #pro1 = threading.Thread(target=p1)
    #pro2 = threading.Thread(target=p2)

# multiprocessing -- 多进程 相当于多核。要在terminal里跑而不能在IDE的terminal里跑 -- python start.py/ & !!!!!!!!!!!!!!

    pro1 = multiprocessing.Process(target=p1)
    pro2 = multiprocessing.Process(target=p2)
    pro1.start()
    pro2.start()





