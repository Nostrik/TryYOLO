import argparse
import os
import csv
from worker import worker_parser, run_detection
from datetime import datetime
import sys
from fndBack import black_frame_detect

WEIGHT_FILES = {}
WEIGHT_FILES_CHOICE = []
VIDEO_FILES = {}
VIDEO_FILES_CHOICE = []

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)



def create_txt(file_name, header, data):
    with open('runs/detect/predict/' + file_name, "w+") as txt_file:
        txt_file.write(header + "\n")
        for v in data:
            txt_file.write(f"Объект {v[0]}\t| timecode: {str([q for q in v[1]])}\n")


def create_csv(file_name, header, data):
    with open('runs/detect/predict/' + file_name, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|')
        csv_file.write("Объект|Таймкод|Таймкод окончания\n")
        for v in data:
            writer.writerow([v[0]]+[q for q in v[1]])


def create_result_file(data, weight_file_name, video_file_name):
    txt_file_name = str(datetime.now())[:19].replace(' ', ' ').replace(':', ',') + " .txt"
    csv_file_name = str(datetime.now())[:19].replace(' ', ' ').replace(':', '') + " .csv"
    header_name = f"{str(datetime.now())[:19]} | {str(weight_file_name).replace('.pt', '')} | {str(video_file_name).replace('.', '')}"

    try:
        create_txt('runs/detect/predict/' + txt_file_name, header_name, data)
        create_csv('runs/detect/predict/' + csv_file_name, header_name, data)
    except FileNotFoundError:
        create_txt(txt_file_name, header_name, data)
        create_csv(csv_file_name, header_name, data)



parser = MyParser(
	prog='Video-Content-Inspector',
	description='Консольный интерфейс детектирования проблем на выбранном видеофрагменте',
)

parser.add_argument('-i', '--input', dest='input', required=False, help='Интерактивный режим ввода', default=False, action=argparse.BooleanOptionalAction)
parser.add_argument('-c', '--save_csv', dest='save_csv', action='store_true', required=False, help='Сохранение результатов в csv файл')
parser.add_argument('-s', '--save_video', dest='save_video', action='store_true', required=False, help='Сохранение видео с результатами работы')
parser.add_argument('-t', '--target_video', metavar='target_video', required=False, help='Путь к видео для обработки')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', required=False, help='debug option')
parser.add_argument('-w', '--weights',metavar='weights', required=False, help='Путь к каталогу с файлами весов')

args = parser.parse_args()

if not args.input:
    if not (args.weights and args.target_video):
        parser.error('Необходимо указать видео для обработки и файлы весов')
    if args.weights:
        target_folder = args.weights
    if args.target_video:
        target_video = args.target_video
else:
    print()
    # target_video = input("Видео: ").replace('\r','')
    # print()
    # weight_folder = input("Каталог с файлами весов: ").replace('\r','')
    target_folder = input("Укажите каталог с данными: ")
print()

save_csv = args.save_csv
save_video = args.save_video
verbose = args.verbose

if args.input:
    file_list = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith(".pt")]
    video_file_list = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith(".mp4") or f.endswith(".mkv")]
else:
    video_file_list = []
    video_file_list.append(target_video)
    file_list = []
    file_list.append(target_folder)

try:
    for i, w in enumerate(file_list):
        WEIGHT_FILES[i] = w
    for i, v in enumerate(video_file_list):
        VIDEO_FILES[i] = v
except FileNotFoundError:
    print("Системе не удается найти указанный путь")
    exit(0)


if VIDEO_FILES:
    for i in VIDEO_FILES:
        print(f"{i+1}:\t{VIDEO_FILES[i].replace(target_folder,'')}")
else:
    print("Видео файлы не обнаружены")
    exit(0)

print("Укажите необходимое видео: ")
video_files_input = input('> ')
VIDEO_FILES_CHOICE = video_files_input.split(',')
target_video = VIDEO_FILES[int(VIDEO_FILES_CHOICE[0]) - 1]


print()

print("Задачи для выполнения: ") # ?????

WEIGHT_FILES[len(WEIGHT_FILES)] = "Поиск чёрных кадров"
if WEIGHT_FILES:
    for i in WEIGHT_FILES:
        print(f"{i+1}:\t{WEIGHT_FILES[i].replace(target_folder,'').replace('.pt','')}")
else:
    print("Файлы весов не обнаружены!")
    exit(0)

print()

print("Укажите цифрами через запятую необходимые задачи:")
weight_files_input = input('> ')
WEIGHT_FILES_CHOICE = weight_files_input.split(',')

print("=" * 80)
try:
    for weight_choice in WEIGHT_FILES_CHOICE:
        # if weight_choice==str(len(WEIGHT_FILES)):
        if int(weight_choice)==len(WEIGHT_FILES):
        # "Поиск чёрных кадров"
            q=black_frame_detect(target_video)
            for i in q:
                print(f'Чёрный кадр с {i[0]:.3f} сек. по {i[1]:.3f} сек. (длительность {i[2]:.3f} сек.)')
            WEIGHT_FILES_CHOICE.remove(str(len(WEIGHT_FILES)))
        else:
            # print(WEIGHT_FILES[int(weight_choice)-1].replace(weight_folder,'').replace('.pt',''))
            results = run_detection(target_video, WEIGHT_FILES[int(weight_choice)-1], save_csv, save_video, verbose)
            if verbose:
                for q in results:
                    print(f"Объект {q[0]} \t| timecode: {' - '.join(map('{:.3f}'.format,q[1]))}")
            if save_csv:
                create_result_file(results, WEIGHT_FILES[int(weight_choice)-1], target_video)

except KeyError as er:
    print("Неверно указаны файлы весов!")
    exit(0)
    