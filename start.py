"""
New's Search Engine

Created on Wes Jun 11, 2020

@author: Liwei Wang
"""

import os
import multiprocessing
import threading

def p0():
    os.system("python Backend/get_data.py&")

def p1():
    os.system("python Backend/api.py&")

def p2():
    os.system("serve -s build&")

if __name__ == "__main__":


#pro1 = threading.Thread(target=p1)
#pro2 = threading.Thread(target=p2)

# multiprocessing -- python start.py/ & !!!!!!!!!!!!!!

    pro0 = multiprocessing.Process(target=p0)
    pro1 = multiprocessing.Process(target=p1)
    pro2 = multiprocessing.Process(target=p2)
    pro0.start()
    pro1.start()
    pro2.start()





