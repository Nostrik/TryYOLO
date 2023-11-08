import argparse
import sys
import subprocess
import os
from loguru import logger
from multiprocessing import Process, Manager
from termcolor import colored

from loader import dictionary
from core import start_predict, terminal_printer
from black_finder import black_frame_detect_with_multiprocess

min_log_level = ["INFO", "DEBUG"]

logger.remove()
logger.add(sink=sys.stderr, level=min_log_level[0], format="<blue>{level}</blue> | <green>{function}</green> : <green>{line}</green> | <yellow>{message}</yellow>")

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


def show_main_phrases(key):
    print(
        dictionary['main_phrases'][0] + "\n" 
        + "=" + dictionary['main_phrases'][key] + "=" + "\n" + dictionary['main_phrases'][0]
        )


def show_minor_phrases(key):
    return dictionary['minor_phrases'][key]


def main():

    run_parameters = {
        "videos": [],
        "weigths": [],
    }
    show_main_phrases(1)

    try:
        weight_files = {}
        video_files = {}
        msg_for_input = show_minor_phrases(0)
        target_folder = input(msg_for_input).replace('\r','')
        file_list = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith(".pt")]
        file_list.append("\\black-frame")
        video_file_list = [os.path.join(target_folder, f) for f in os.listdir(target_folder) if f.endswith(".mp4")]
        for i, w in enumerate(file_list):
            weight_files[i] = w
        for i, v in enumerate(video_file_list):
            video_files[i] = v
    except FileNotFoundError as er:
        print(er)
        exit(0)

    if video_files:
        print(show_minor_phrases(1))
        for i in video_files:
            # print(f"{i+1}:\t{video_files[i].replace(target_folder,'')}")
            msg = f"{i+1}:\t{video_files[i].replace(target_folder,'')}"
            print(colored(msg, "green"))
    else:
        print(show_minor_phrases(10))
        exit(0)

    try:
        msg_for_input = show_minor_phrases(2)
        video_files_input = input(msg_for_input)
        video_files_choice = video_files_input.split(',')
        target_video = video_files[int(video_files_choice[0]) - 1]
    except KeyError as er:
        print(show_minor_phrases(11))
        exit(0)

    if weight_files:
        print(show_minor_phrases(3))
        for i in weight_files:
            # print(f"{i+1}:\t{weight_files[i].replace(target_folder,'').replace('.pt','')}")
            msg = f"{i+1}:\t{weight_files[i].replace(target_folder,'').replace('.pt','')}"
            print(colored(msg, "green"))
    else:
        print(show_minor_phrases(12))
        exit(0)

    msg_for_input = show_minor_phrases(4)
    weight_files_input = input(msg_for_input)
    weight_files_choice = weight_files_input.split(',')
    print()
    show_main_phrases(2)
    print(show_minor_phrases(5) + target_folder)
    print(show_minor_phrases(6), end='') #  Order of video files
    logger.debug(run_parameters)
    try:
        for i in video_files_choice:
            # print(video_files[int(i) - 1].replace(target_folder,''), end='; ')
            msg = video_files[int(i) - 1].replace(target_folder,'')
            print(colored(msg, "green"), end='; ')
            run_parameters['videos'].append(video_files[int(i) - 1])
        print()
        print(show_minor_phrases(7), end='') #  Selected weight files
        for i in weight_files_choice:
            # print(weight_files[int(i) - 1].replace(target_folder,''), end=';\n')
            msg = weight_files[int(i) - 1].replace(target_folder,'')
            print(colored(msg, "green"), end=';\n')
            run_parameters['weigths'].append(weight_files[int(i) - 1])
        print()
        logger.debug(run_parameters)
    except KeyError:
        print(show_minor_phrases(13))
        exit(0)
    
    msg_for_input = show_minor_phrases(8)
    start_detection = input(msg_for_input)

    logger.debug(run_parameters)

    show_main_phrases(3)

    for video in run_parameters['videos']:
        print(f"\nProcessing for video: {video}")
        try:
            with Manager() as process_manager:
                quantity_processes = len(run_parameters['weigths'])
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
                quene = process_manager.Queue()
                p_printer = Process(target=terminal_printer, args=(quantity_processes, info_container))
                for i_process, i_weigth_file in enumerate(run_parameters['weigths']):
                    logger.debug(video)
                    if i_weigth_file != "\\black-frame":
                        p = Process(
                                target=start_predict, args=(
                                i_weigth_file,
                                video,
                                str(i_weigth_file).replace(target_folder,''),
                                quene,
                                quantity_processes,
                                final_results,
                                info_container,
                                i_process,
                                target_folder,
                            )
                        )
                        proc_list.append(p)
                        p.start()
                    else:
                        p = Process(
                            target=black_frame_detect_with_multiprocess, args=(
                                i_weigth_file, 
                                video, 
                                str(i_weigth_file).replace(target_folder,''), 
                                quene,
                                quantity_processes,
                                final_results,
                                info_container,
                                i_process,
                                target_folder,
                            )
                        )
                        proc_list.append(p)
                        p.start()
                
                if proc_list:
                    if proc_list[0].is_alive():
                        p_printer.start()
                    quene.put(None)
                    p_printer.join()
            print()
        except FileNotFoundError as er:
            print(show_minor_phrases(14))
            print(er)
            exit(0)


    print()
    show_main_phrases(4)

if __name__ == "__main__":
    main()
