import sys
import time as tm
import random
from dataclasses import dataclass
from multiprocessing import Process, Lock

cursor_up = lambda lines: '\x1b[{0}A'.format(lines)
cursor_down = lambda lines: '\x1b[{0}B'.format(lines)

COLLECTOR = {"0": 0, "1": 0, "2": 0}


def writer():
    cursor_up = lambda lines: '\x1b[{0}A'.format(lines)
    cursor_down = lambda lines: '\x1b[{0}B'.format(lines)
    global COLLECTOR
    for i in range(3):
        print(f'proccess: {i} pid: {None} | => {COLLECTOR[str(i)]} <=')
    print(cursor_up(3), end='')


def worker(p_number, lock):
    global COLLECTOR
    for i in range(30):
        # print(f'proccess: {p_number} pid: {None} | => {i} <=', end='\r')
        with lock:
            # COLLECTOR[p_number] = i
            print(f'proccess: {p_number} pid: {None} | => {i} <=', end='\r')
        tm.sleep(random.randrange(1, 4))



if __name__ == "__main__":
    p_lst = []
    lock = Lock()
    # Process(target=writer).start()
    for i in range(3):
        p = Process(target=worker, args=(i, lock))
        p_lst.append(p)
        p.start()
    