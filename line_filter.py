import os
import re
from termcolor import colored

EX_PATH = 'C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input'


class NumberChecker:
    def __init__(self) -> None:
        self.previous_number = None

    def check_number(self, number):
        if number is not None:
            number = int(number)
            if self.previous_number is None or number == self.previous_number + 1:
                self.previous_number = number
                return True
            else:
                self.previous_number = None
                return False


def read_lines(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


def extract_value_from_line(line):
    patern = r"\((\d+)\)"
    matches = re.findall(pattern=patern, string=line)
    if matches:
        exctracted_number = matches[0]
        return exctracted_number
    return None


def find_files(path):
    txt_files = {}
    list_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".txt")]
    for i, f in enumerate(list_files):
        txt_files[i] = f
    for key, val in txt_files.items():
        print(key + 1, val.replace(path, '').replace('\\', ''))
    input_file_number = int(input('Select file: '))
    print("File selected is: ")
    choice_file = txt_files[input_file_number - 1]
    print(choice_file)

    checker = NumberChecker()
    for l in read_lines(choice_file):
        val = extract_value_from_line(l)
        print(l, end=':')
        print(colored(checker.check_number(val), "yellow"))


def main():
    find_files(EX_PATH)


if __name__ == "__main__":
    main()
