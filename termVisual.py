import sys
import time as tm
import random
from dataclasses import dataclass
from multiprocessing import Process, Lock
from loguru import logger

cursor_up = lambda lines: '\x1b[{0}A'.format(lines)
cursor_down = lambda lines: '\x1b[{0}B'.format(lines)

COLLECTOR = {"0": 0, "1": 0, "2": 0}


class Container(object):

    def __init__(self) -> None:
        self.proccess0 = 0
        self.proccess1 = 0
        self.proccess2 = 0

    def set_value(self, number_proccess, value):
        if number_proccess == 0:
            self.proccess1 = value
        elif number_proccess == 1:
            self.proccess2 = value
        elif number_proccess == 2:
            self.proccess3 = value

    def get_value(self, number_proccess):
        if number_proccess == 0:
            return self.proccess1
        elif number_proccess == 1:
            return self.proccess2
        elif number_proccess == 2:
            return self.proccess3
        
    
    def log(self):
        logger.info(f"self.proccess0 = {self.proccess0} | self.proccess1 = {self.proccess1} | self.proccess2 = {self.proccess2}")


def writer(container):
    cursor_up = lambda lines: '\x1b[{0}A'.format(lines)
    cursor_down = lambda lines: '\x1b[{0}B'.format(lines)
    
    cnt = 20
    while cnt != 0:
        tm.sleep(0.5)
        # container.log()
        print(f'proccess: {1} pid: {None} | => {container.get_value(1)} <=')
        print(f'proccess: {2} pid: {None} | => {container.get_value(2)} <=')
        print(f'proccess: {3} pid: {None} | => {container.get_value(3)} <=')
        print(cursor_up(4) + '\r')
        cnt -= 1


def worker_writer(p_number, lock, c_object, value):
    with lock:
        c_object.set_value(p_number, value)
        c_object.log()
    return c_object


def worker(p_number, lock, c_object):
    for i in range(30):
        # print(f'proccess: {p_number} pid: {None} | => {i} <=', end='\r')
        worker_writer(p_number, lock, c_object, i)
        tm.sleep(0.2)
    return c_object


if __name__ == "__main__":
    lock = Lock()
    proc_list = []
    # w = Process(target=writer, args=(container_obj, ))
    # w.start()
    container = Container()
    for i in range(2): 
        p = Process(target=worker, args=(i, lock, container))
        proc_list.append(p)
        p.start()

    for p in proc_list:
        p.join()
    print("-" * 80)
    container.log()

    