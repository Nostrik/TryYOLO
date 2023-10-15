import argparse
import sys
import subprocess
import os
from loguru import logger
from locale_text import lang_en, lang_ru

from models import start_predict

dictionary = lang_en
min_log_level = ["INFO", "DEBUG"]

logger.remove()
logger.add(sink=sys.stderr, level=min_log_level[0])

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
            print(f"{i+1}:\t{video_files[i].replace(target_folder,'')}")
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
            print(f"{i+1}:\t{weight_files[i].replace(target_folder,'').replace('.pt','')}")
    else:
        print(show_minor_phrases(12))
        exit(0)

    msg_for_input = show_minor_phrases(4)
    weight_files_input = input(msg_for_input)
    weight_files_choice = weight_files_input.split(',')
    print()
    show_main_phrases(2)
    print(show_minor_phrases(5) + target_folder)
    print(show_minor_phrases(6), end='')
    try:
        for i in video_files_choice:
            print(video_files[int(i) - 1].replace(target_folder,''), end='; ')
            run_parameters['videos'].append(video_files[int(i) - 1])
        print()
        print(show_minor_phrases(7), end='')
        for i in weight_files_choice:
            print(weight_files[int(i) - 1].replace(target_folder,''), end='; ')
            run_parameters['weigths'].append(weight_files[int(i) - 1])
        print()
    except KeyError:
        print(show_minor_phrases(13))
        exit(0)
    
    msg_for_input = show_minor_phrases(8)
    start_detection = input(msg_for_input)

    logger.debug(run_parameters)

    # logger.debug(target_folder)
    # logger.debug(video_files)
    # logger.debug(video_files_choice)
    # logger.debug(weight_files)
    # logger.debug(weight_files_choice)

    show_main_phrases(3)

    print(f"\nProcessing for video: {run_parameters['videos'][0]}")

    for weight in run_parameters['weigths']:
        logger.debug(weight)
        start_predict(
            weigth_file=weight,
            target_video=run_parameters['videos'][0]
        )

if __name__ == "__main__":
    main()
