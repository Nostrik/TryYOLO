import sys
from dataclasses import dataclass


class TerminalVisualiser:
    
    proccess_counter: int = 0
    proccess_list: list = []

    def __init__(self, proc_cnt: int, proc_lst: list) -> None:
        self.proccess_counter = proc_cnt
        self.proccess_list = proc_lst

    def cursor_up():
        sys.stdout.write('\x1b[1A')
        sys.stdout.flush()

    def cursor_down():
        sys.stdout.write('\n')
        sys.stdout.flush()

    def print_to_terminal(line: str):
        sys.stdout.write(line)


    def print_all(self):
        for proc in self.proccess_list:
            self.print_to_terminal(proc)
            self.cursor_down()    
