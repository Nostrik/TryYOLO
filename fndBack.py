import subprocess
import re
import torch
import sys
import time
from tqdm import tqdm
from frame2timecode import f2t
from frame2timecode import video_duration
from worker import create_result_file
from datetime import datetime
from multiprocessing import Lock
from loguru import logger

logger.remove(0)
i = "INFO"
d = "DEBUG"
logger.add(sys.stdout, level=d)


def test_cuda():
    result = subprocess.run(['ffmpeg', '-decoders'], capture_output=True)
    output = result.stdout.decode()

    if 'h264_cuvid' in output:
        return True
    else:
        return True


def black_frame_detect_with_multiprocess(video_path, weight_file, save_csv, save_video, verbose, queue=None, quantity_processes=None, final_results=None, info_container=None, process_number=0):
    command = ['ffmpeg', '-i',  video_path, '-filter_complex', 'blackdetect=d=0.1:pix_th=0.05', '-f', 'null', '-']

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    bf=[]
    frame_pattern = re.compile(r'^frame=(\d+)\b.*fps=')
    fps_pattern = re.compile(r'^.*fps=(\d+(?:\.\d+)?)\b.*$')
    time_pattern = re.compile(r'^.*time=(\d\d:\d\d:\d\d\.\d\d).*')

    process_lock = Lock()
    info_dict = {
        "process": process_number,
        "object": "['black-frame']",
        "progress": "",
        "remaining_time": "",
        "recognized_for": "~",
        "process_completed": False,
    }
    info_container

    total_t= video_duration(video_path)
    for line in process.stdout:
        if line.startswith('frame='):
            match_frame = frame_pattern.match(line)
            if match_frame:
                current_frame = int(match_frame.group(1))
            match_fps = fps_pattern.match(line)
            if match_fps:
                fps = float(match_fps.group(1))
            match_time = time_pattern.match(line)
            if match_time:
                time_str = match_time.group(1)
                time_dt = datetime.strptime(time_str, '%H:%M:%S.%f')
                time_r = (time_dt - datetime(1900, 1, 1)).total_seconds()
            t_progress = round(time_r / total_t * 100, 1)
            info_dict['progress'] = str(t_progress)
            if t_progress == 100:
                info_dict['process_completed'] = True
        else:
            match = re.search(r'black_start:([\d\.]+) black_end:([\d\.]+) black_duration:([\d\.]+)', line)
            if match:
                start = float(match.group(1))
                end = float(match.group(2))
                duration = float(match.group(3))
                bf+=[[start,end,duration]]
        # t_progress = str(round(time_r / total_t * 100, 1))
        # info_dict['progress'] = t_progress
        # info_dict['remaining_time'] = '~'
        with process_lock:
            try:
                info_container[process_number] = info_dict
            except Exception as e:
                # print(e)s
                pass
        try:
            queue.put(process_number, info_container)
        except Exception:
            pass
    if save_csv:
        create_result_file(data=bf, weight_file_name='black-frame.pt', video_file_name=video_path)


# q1 = black_frame_detect_with_multiprocess("C:\\Users\\Maxim\\tv-21-app\\tv21-app-rep2\\input\\Shitfest.mp4", )
# for i in q1:
#     print(f'Чёрный кадр с {i[0]:.3f} сек. по {i[1]:.3f} сек. (длительность {i[2]:.3f} сек.)')
