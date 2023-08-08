import argparse
import os
import csv
from worker import run_detection, terminal_printer
from datetime import datetime
from typing import Any
from multiprocessing import Process, Manager, Lock, Queue
import sys
from fndBack import black_frame_detect_with_multiprocess
from loguru import logger
from pprint import pprint


disclaimer = "| Данное программное обеспечение предназначено для поиска и обнаружения объектов на различных видеоматериалах.|\n|" + \
" Использование данного ПО для других целей запрещено. Передача другим лицам запрещена.                       |"


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


class ArgsParam:
    input=True, 
    save_csv=True, 
    save_video=False, 
    target_video=None, 
    verbose=False, 
    weights=None


def print_disclaimer() -> None:
    print("-" * 111)
    print(disclaimer)


def verbose_function(lines: list) -> None:
    for line in lines:
        print(f"Объект {line[0]} \t| timecode: {' - '.join(map('{:.3f}'.format, line[1]))}")


def black_f_detector_function(video: Any) -> None:
    find_black_frames = black_frame_detect_with_multiprocess(video)
    for i_one_black_frame in find_black_frames:
        print(f'Чёрный кадр с {i_one_black_frame[0]:.3f} сек. по {i_one_black_frame[1]:.3f} сек. (длительность {i_one_black_frame[2]:.3f} сек.)')


def non_interactive_ui(args: Any) -> dict:

    weight_files = {}
    weight_files_choice = []
    video_files = {}

    if args.weights:
        weight_file = args.weights
    if args.target_video:
        target_video = args.target_video
    save_csv = args.save_csv
    save_video = args.save_video
    verbose = args.verbose

    weight_files[0] = weight_file
    video_files[0] = target_video

    print("-" * 111)
    print(f"video: {target_video}\nweight_file: {weight_file}")
    print("-" * 111)

    return {
        "interactive": args.input,
        "target_video": target_video,
        "weight_file": weight_file,
        "save_csv": save_csv,
        "save_video": save_video,
        "verbose": verbose,
        "black_frame_path": "",
        "weight_files": weight_files,
        "weight_files_choice": weight_files_choice,
        "video_files": video_files,
        'video_files_choice': 0,
    }


def interactive_ui(args: Any) -> dict:

    weight_files = {}
    weight_files_choice = []
    video_files = {}
    video_files_choice = []

    black_frame_name = "black-frame.pt"
    save_csv = args.save_csv
    save_video = args.save_video
    verbose = args.verbose
    print_disclaimer()

    try:
        print("-" * 111)
        target_folder = input("Укажите каталог с данными: ").replace('\r','')
        print("-" * 111)
        file_list = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith(".pt")]
        Black_frame_name_path = os.path.join(target_folder, black_frame_name)
        file_list.append(Black_frame_name_path)
        video_file_list = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith(".mp4") or f.endswith(".mkv")]
        for i, w in enumerate(file_list):
            weight_files[i] = w
        for i, v in enumerate(video_file_list):
            video_files[i] = v
    except FileNotFoundError as er:
        print(er)
        exit(0)

    if video_files:
        for i in video_files:
            print(f"{i+1}:\t{video_files[i].replace(target_folder,'')}")
    else:
        print("Видео файлы не обнаружены")
        exit(0)

    try:
        print("Укажите необходимое видео: ")
        video_files_input = input('> ')
        print("-" * 111)
        video_files_choice = video_files_input.split(',')
        target_video = video_files[int(video_files_choice[0]) - 1]
    except KeyError as er:
        print("Неверно узакан видеофайл!..")
        exit(0)

    if weight_files:
        for i in weight_files:
            print(f"{i+1}:\t{weight_files[i].replace(target_folder,'').replace('.pt','')}")
    else:
        print("Файлы весов не обнаружены!")
        exit(0)

    print("Укажите цифрами через запятую необходимые задачи:")
    weight_files_input = input('> ')
    weight_files_choice = weight_files_input.split(',')
    print("-" * 111)

    return {
        "interactive": args.input,
        "target_video": target_video,
        "weight_file": weight_files_choice,
        "save_csv": save_csv,
        "save_video": save_video,
        "verbose": verbose,
        "black_frame_path": Black_frame_name_path,
        "weight_files": weight_files,
        "weight_files_choice": weight_files_choice,
        "video_files": video_files,
        'video_files_choice': 0,
    }


def pre_detection(params: dict) -> None:
    # pprint(params)
    if params['interactive']:
        try:
            with Manager() as process_manager:
                quantity_processes = len(params['weight_files_choice'])
                proc_list = []
                info_container = process_manager.list()
                final_results = process_manager.list([0] * quantity_processes)

                for _ in range(quantity_processes):
                    info_dict = process_manager.dict()
                    info_dict = {
                        "process": 0,
                        "object": None,
                        "progress": "",
                        "remaining_time": "",
                        "recognized_for": "",
                        "process_completed": False,
                    }
                    info_container.append(info_dict)
                queue = process_manager.Queue()
                p_printer = Process(target=terminal_printer, args=(quantity_processes, info_container))
            
                for i_process, i_weight_choice in enumerate(params['weight_files_choice']):
                    if params['weight_files'][int(i_weight_choice) - 1] != params['black_frame_path']:                        
                        p = Process(target=run_detection, args=(
                            params['target_video'], params['weight_files'][int(i_weight_choice) - 1], params['save_csv'], params['save_video'], params['verbose'],
                            queue, quantity_processes, final_results, info_container, i_process,
                            ))
                        proc_list.append(p)
                        p.start()
                    else:
                        p = Process(target=black_frame_detect_with_multiprocess, args=(
                            params['target_video'], params['weight_files'][int(i_weight_choice) - 1], params['save_csv'], params['save_video'], params['verbose'],
                            queue, quantity_processes, final_results, info_container, i_process,
                            ))
                        proc_list.append(p)
                        p.start()

                if proc_list:
                    if proc_list[0].is_alive():
                        p_printer.start()
                    queue.put(None)
                    p_printer.join()
        except FileNotFoundError as er:
            print("Неверно указаны файлы весов!")
            print(er)
            exit(0)
    else:
        queue = None
        quantity_processes = None
        final_results = None
        info_container = None
        process = 0
        one_weight_result = run_detection(
            params['target_video'], params['weight_file'], params['save_csv'], params['save_video'], params['verbose'],
            queue, quantity_processes, final_results, info_container, process,
        )

if __name__ == "__main__":

    # parser = MyParser(
    #     prog='Video-Content-Inspector',
    #     description='Консольный интерфейс детектирования проблем на выбранном видеофрагменте',
    # )

    # parser.add_argument('-i', '--input', dest='input', required=False, help='Интерактивный режим ввода', default=True, action=argparse.BooleanOptionalAction)
    # parser.add_argument('-c', '--save_csv', dest='save_csv', action='store_true', required=False, default=True, help='Сохранение результатов в csv файл')
    # parser.add_argument('-s', '--save_video', dest='save_video', action='store_true', required=False, help='Сохранение видео с результатами работы')
    # parser.add_argument('-t', '--target_video', metavar='target_video', required=False, help='Путь к видео для обработки')
    # parser.add_argument('-v', '--verbose', dest='verbose', action='store_true', required=False, help='debug option')
    # parser.add_argument('-w', '--weights',metavar='weights', required=False, help='Путь к каталогу с файлами весов')

    # args = parser.parse_args()

    # if not args.input:
    #     run_params = non_interactive_ui(args)
    # else:
    #     run_params = interactive_ui(args)
    
    args = ArgsParam()
    run_params = interactive_ui(args)

    pre_detection(run_params)
