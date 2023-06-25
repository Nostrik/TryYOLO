import time as tm
from multiprocessing import Process, Manager, Lock, Barrier, Queue


def worker(process_number, info_container, queue):
    process_lock = Lock()
    for i in range(20):
        info_dict = {"process": process_number, "value": i}
        with process_lock:
            info_container[process_number] = info_dict
        queue.put((process_number, i))
        tm.sleep(0.2)


def printer(queue, num_processes, final_results, info_container):
    while True:
        output = ""
        for i in range(num_processes):
            try:
                process_number, value = queue.get(block=False)
                output += f"Process {process_number}: {value}    "
                output += '\n'
                final_results[process_number] = value
            except:
                output += " " * (len(f"Process {i}: 0    ")-1)
        results = [info_dict["value"] for info_dict in info_container]
        print(output, end='\r')
        # if all(final_results):
        #     break
        tm.sleep(1)


if __name__ == "__main__":
    num_processes = 5  # Задаем количество процессов
    with Manager() as m:
        process_list = []
        info_container = m.list()
        final_results = m.list([0] * num_processes)
        for i in range(num_processes):
            info_dict = m.dict()
            info_dict["process"] = i
            info_dict["value"] = 0
            info_container.append(info_dict)
        results_container = m.list([0] * num_processes)
        lock = Lock()
        queue = Queue()
        p_printer = Process(target=printer, args=(queue, num_processes, final_results, info_container))
        p_printer.start()
        for i in range(num_processes):
            p = Process(target=worker, args=(i, info_container, queue))
            process_list.append(p)
            p.start()
        for p in process_list:
            p.join()
        queue.put(None)
        p_printer.join()
        
        for info_dict in info_container:
            print(info_dict)
