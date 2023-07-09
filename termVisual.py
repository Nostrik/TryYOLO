import time as tm
import sys
from multiprocessing import Process, Manager, Lock, Queue
from pprint import pprint
from loguru import logger

logger.remove(0)
i = "INFO"
d = "DEBUG"
logger.add(sys.stdout, level=d)


def worker(process_number, info_container, queue):
    process_lock = Lock()
    for i in range(20):
        info_dict = {"process": process_number, "value": i}
        with process_lock:
            info_container[process_number] = info_dict
        queue.put((process_number, info_container))
        tm.sleep(0.3)


def printer(queue, quantity_processes, info_container):
    cursor_up = lambda lines: '\x1b[{0}A'.format(lines)
    value = 0
    while True:
        output = ""
        sorted_info_container = sorted(info_container, key=lambda x: x["process"])

        for info_dict in sorted_info_container:
            output += f"Process {info_dict['process']}, value {info_dict['value']}    "
            output += '\n'
        # for i in range(quantity_processes):
        #     try:
        #         process_number, value = queue.get(block=False)
        #         output += f"Process {process_number}, value {value[process_number]['value']}    "
        #         output += '\n'
        #     except:
        #         output += " " * (len(f"Process {i}: 0    ") - 1)
        print(output, end='\r')
        if info_container[0]['value'] > 18:
            break
        tm.sleep(0.3)
        print(cursor_up(quantity_processes + 1))


if __name__ == "__main__":
    quantity_processes = 3  # Задаем количество процессов
    with Manager() as m:
        process_list = []
        info_container = m.list()
        for i in range(quantity_processes):
            info_dict = m.dict()
            info_dict["process"] = i
            info_dict["value"] = 0
            info_container.append(info_dict)
        results_container = m.list([0] * quantity_processes)
        lock = Lock()
        queue = Queue()
        print('\n' * (quantity_processes - 1))
        p_printer = Process(target=printer, args=(queue, quantity_processes, info_container))
        p_printer.start()
        logger.debug(f"priner {p_printer.pid}")
        for i in range(quantity_processes):
            p = Process(target=worker, args=(i, info_container, queue))
            process_list.append(p)
            p.start()
            logger.debug(f"worker {p.pid}")
        for p in process_list:
            p.join()
        queue.put(None)
        p_printer.join()
        
        # for info_dict in info_container:
        #     pprint(info_dict)
