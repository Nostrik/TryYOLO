import os

EX_PATH = 'C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input'


def read_lines(filename):
    with open(filename, 'r') as file:
        for line in file:
            yield line.rstrip('\n')


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

    for l in read_lines(choice_file):
        print(l)



def main():
    find_files(EX_PATH)


if __name__ == "__main__":
    main()
