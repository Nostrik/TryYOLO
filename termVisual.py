import time as tm
from multiprocessing import Process, Manager, Lock, Queue
from pprint import pprint


def worker(process_number, info_container, queue):
    process_lock = Lock()
    for i in range(20):
        info_dict = {"process": process_number, "value": i}
        with process_lock:
            info_container[process_number] = info_dict
        queue.put((process_number, i))
        tm.sleep(0.1)


def printer(queue, quantity_processes, final_results, info_container):
    cursor_up = lambda lines: '\x1b[{0}A'.format(lines)
    value = 0
    while True:
        output = ""
        for i in range(quantity_processes):
            try:
                process_number, value = queue.get(block=False)
                output += f"Process {process_number}: {value}    "
                output += '\n'
                final_results[process_number] = value
            except:
                output += " " * (len(f"Process {i}: 0    ")-1)
        results = [info_dict["value"] for info_dict in info_container]
        print(output, end='\r')
        if value > 18:
            break
        tm.sleep(0.3)
        print(cursor_up(quantity_processes + 1))


if __name__ == "__main__":
    quantity_processes = 10  # Задаем количество процессов
    with Manager() as m:
        process_list = []
        info_container = m.list()
        final_results = m.list([0] * quantity_processes)
        for i in range(quantity_processes):
            info_dict = m.dict()
            info_dict["process"] = i
            info_dict["value"] = 0
            info_container.append(info_dict)
        results_container = m.list([0] * quantity_processes)
        lock = Lock()
        queue = Queue()
        print('\n' * quantity_processes)
        p_printer = Process(target=printer, args=(queue, quantity_processes, final_results, info_container))
        p_printer.start()
        for i in range(quantity_processes):
            p = Process(target=worker, args=(i, info_container, queue))
            process_list.append(p)
            p.start()
        for p in process_list:
            p.join()
        queue.put(None)
        p_printer.join()
        
        for info_dict in info_container:
            pprint(info_dict)
