import os
import subprocess
import time
import torch
import asyncio
import re
from colorama import init, Fore, Style
import threading
import queue

some_sortof_res=dict()

res_buffer=dict()
output_listing=[]
frames_dict = {}
frames_queue = queue.Queue()


init()
colors = [
    Fore.BLUE,
    Fore.CYAN,
    Fore.GREEN,
    Fore.LIGHTBLACK_EX,
    Fore.LIGHTBLUE_EX,
    Fore.LIGHTCYAN_EX,
    Fore.LIGHTGREEN_EX,
    Fore.LIGHTMAGENTA_EX,
    Fore.LIGHTRED_EX,
    Fore.LIGHTWHITE_EX,
    Fore.LIGHTYELLOW_EX,
    Fore.MAGENTA,
    Fore.RED
    ]

def rainbow_print(*args, **kwargs):
    global colors
    color_index = 0
    for arg in args:
        arg = re.sub(' +', ' ', arg)
        for letter in arg:
            color_index += 1
            if color_index == len(colors):
                color_index = 0

            color = colors[color_index]

            print(color + letter, end="")

    colors = colors[1:] + colors[:1]

    print(Style.RESET_ALL, **kwargs)

def async_f2t(video_path):
    global frames_queue

    command = ['ffprobe', video_path, '-hide_banner', '-show_entries', 'frame=coded_picture_number,best_effort_timestamp_time', '-of', 'json']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, bufsize=1, universal_newlines=True)
    output = ""
    frame = 0
    timecode = 0
    for line in iter(process.stdout.readline, ''):
        linst = line.strip()
        match = re.search(r'"best_effort_timestamp_time": "([\d\.]+)"', linst)
        if match:
            timecode = float(match.group(1))
        match = ''
        match = re.search(r'"coded_picture_number": (\d+)', linst)
        if match:
            frame = float(match.group(1))
        output += linst
        if frame > 0:
            frames_queue.put({frame: timecode})
            frame = -1

    process.wait()
    frames_queue.task_done()

    if process.returncode != 0:
        stderr = process.stderr.read()
        raise Exception(f'Error while executing ffprobe: {stderr.decode()}')

def parse_yoloput(line):
    if not line.startswith('video ') or not line.endswith('s') or ':' not in line:
        return None

    components = line.strip().split(' ')
    video_num, video_total = components[1].split('/')
    current_pos, total_amount = components[2][1:-1].split('/')
    path_to_file, rest_of_line = line.rsplit(': ', 1)
    path_to_file = path_to_file.split(' ', maxsplit=3)[-1].strip()
    video_size, rest_of_line = rest_of_line.split(' ', maxsplit=1)
    detected_objs = rest_of_line.rsplit(',', maxsplit=1)[0]
    processing_time = rest_of_line.rsplit(',', maxsplit=1)[1].strip()

    return {
        # 'video_num': video_num,
        # 'video_total': video_total,
        'current_pos': current_pos,
        'total_amount': total_amount,
        # 'path_to_file': path_to_file,
        # 'video_size': video_size,
        'detected_objs': detected_objs,
        'processing_time': processing_time
    }

async def frame2time(frame):
    global frames_dict
    global frames_queue

    while frame not in frames_dict:
        frame_info = frames_queue.get()
        frames_dict.update(frame_info)
        
    return frames_dict[frame]

async def giveMeLine(cur_frame, detected_objs, classes, res):
    global res_buffer
    global output_listing
    global frames_dict
    if "(no detections)" in res['detected_objs']:
        for el in res_buffer:
            f2t_1, f2t_2, f2t_3 = await asyncio.gather(frame2time(res_buffer[el][0]), frame2time(min(res_buffer[el])), frame2time(max(res_buffer[el])))

            output_listing += [[ [k for k, v in classes.items() if v == el][0],(( f2t_1 ),) if len(res_buffer[el])==1  \
                    else (( f2t_2 ),( f2t_3 )) ]]
        res_buffer = dict()         
        return
    
    some_sortof_res[cur_frame] = []
    for obj in classes.keys():
        pattern = re.compile(r'\b{}\b'.format(obj), re.IGNORECASE)
        matches = re.findall(pattern, detected_objs)
        if matches:
            some_sortof_res[cur_frame] += [classes[obj]]

    temp_list=some_sortof_res[cur_frame]
    if res_buffer:
        for el in list(res_buffer.keys()):
            if el in temp_list:
                temp_list.remove(el)
                res_buffer[el].append(cur_frame)
            else:
                f2t_1, f2t_2, f2t_3 = await asyncio.gather(frame2time(res_buffer[el][0]), frame2time(min(res_buffer[el])), frame2time(max(res_buffer[el])))

                output_listing += [[ [k for k, v in classes.items() if v == el][0],(( f2t_1 ),) if len(res_buffer[el])==1  \
                        else (( f2t_2 ),( f2t_3 )) ]]   
                         
                del res_buffer[el]

    for i in temp_list:
        res_buffer[i]=[cur_frame]

def worker_parser(target_video, weight_file, save_csv, save_video, verbose):
    global frames_dict
    global output_listing

    PopenPars=["yolo", "predict", f"model={weight_file}", f"source={target_video}", ] + \
                ['conf=0.5'] + \
                (['save_txt=True'] if save_csv else []) + \
                (['save_conf=True'] if save_csv else []) + \
                (['save_crop=True'] if save_video else []) + \
                (['save=True'] if save_video else [])

    model=torch.load(weight_file, map_location=torch.device('cpu'))
    classes = {y: x for x, y in model['model'].names.items()}

    # print(f"Мы ищем следующие объекты: {', '.join(list(classes.keys()))}")

    process = subprocess.Popen(PopenPars, stderr=subprocess.PIPE)
    
    start_time = time.time()
    while True:
            output = process.stderr.readline().decode('utf-8')

            if output == '' and process.poll() is not None:
                print()
                end_time = time.time()
                break
            if output:
                res=parse_yoloput(output.strip())
                if res:
                    curpos = int(res['current_pos'])
                    elapsed_time = time.time() - start_time
                    avg_time_per_iteration = elapsed_time / (curpos)
                    remaining_time = avg_time_per_iteration * (int(res['total_amount']) - curpos)

                    if remaining_time < 60:
                        remaining_time_str = f'{remaining_time:.0f} сек'
                    elif remaining_time < 3600:
                        remaining_time_str = f'{remaining_time/60:.0f} мин'
                    else:
                        remaining_time_str = f'{remaining_time/3600:.0f} часов'

                    # output = f"Текущий прогресс: {'{:.2f}'.format(100 * curpos / int(res['total_amount']))}% " + \
                    #             f"{res['current_pos']}/{res['total_amount']} | " + \
                    #             f"Осталось: ~{remaining_time_str} | " + \
                    #             f"Кадр распознан за {res['processing_time']} {res['detected_objs']}                          "
                    output = f"{', '.join(list(classes.keys()))} | Текущий прогресс: {'{:.2f}'.format(100 * curpos / int(res['total_amount']))}% " + \
                                f"{res['current_pos']}/{res['total_amount']} | " + \
                                f"Осталось: ~{remaining_time_str} | " + \
                                f"Кадр распознан за {res['processing_time']} {res['detected_objs']}                          "
                    print(output, end='\r', flush=True)
                    asyncio.run(giveMeLine(curpos, res['detected_objs'], classes, res))

    print(Style.RESET_ALL)

    # print(f'Обработка {(os.path.basename(weight_file)).replace(".pt","")} окончена за: {end_time - start_time:.0f} сек')
    return output_listing

def run_detection(target_video, weight_file, save_csv, save_video, verbose):
    global frames_dict
    thread = threading.Thread(target=async_f2t, args=(target_video,))
    thread.start()

    result = worker_parser(target_video, weight_file, save_csv, save_video, verbose)

    thread.join()

    return result
