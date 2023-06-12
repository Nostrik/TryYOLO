import sys
import time as tm
from dataclasses import dataclass
from multiprocessing import Process, Lock

cursor_up = lambda lines: '\x1b[{0}A'.format(lines)
cursor_down = lambda lines: '\x1b[{0}B'.format(lines)


def multiPrint():
    sys.stdout.close()


def worker(p_number):
    for i in range(30):
        print(f'proccess: {p_number} pid: {None} | => {i} <=', end='\r')
        tm.sleep(0.5)


if __name__ == "__main__":
    p_lst = []
    lock = Lock()
    
    for i in range(3):
        p = Process(target=worker, args=(lock, i))
        p_lst.append(p)
        p.start()
    