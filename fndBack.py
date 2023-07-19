import subprocess
import re
import torch
from tqdm import tqdm
from frame2timecode import f2t
from frame2timecode import video_duration
from datetime import datetime
from multiprocessing import Lock


def test_cuda():
    result = subprocess.run(['ffmpeg', '-decoders'], capture_output=True)
    output = result.stdout.decode()

    if 'h264_cuvid' in output:
        return True
    else:
        return True

def black_frame_detect(video_path):
    # .\ffmpeg.exe -c:v h264_cuvid -i "k:\nik\Projects\Yolo\from tv 21\Shitfest.mp4" -filter_complex "blackdetect=d=0.1:pix_th=0.05" -f null -
    # command = r'.\ffmpeg.exe -c:v h264_cuvid -i "'+ video_path + r'" -filter_complex "blackdetect=d=0.1:pix_th=0.05" -f null -'


    # if test_cuda():
    #     command = ['ffmpeg', '-i',  video_path, '-c:v', 'h264_cuvid', '-filter_complex', 'blackdetect=d=0.1:pix_th=0.05', '-f', 'null', '-']
    # else:
    #     command = ['ffmpeg', '-i',  video_path, '-filter_complex', 'blackdetect=d=0.1:pix_th=0.05', '-f', 'null', '-']

    command = ['ffmpeg', '-i',  video_path, '-filter_complex', 'blackdetect=d=0.1:pix_th=0.05', '-f', 'null', '-']

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    bf=[]
    frame_pattern = re.compile(r'^frame=(\d+)\b.*fps=')
    fps_pattern = re.compile(r'^.*fps=(\d+(?:\.\d+)?)\b.*$')
    time_pattern = re.compile(r'^.*time=(\d\d:\d\d:\d\d\.\d\d).*')

    print("Поиск чёрных кадров...")
    bar=tqdm(total=round(video_duration(video_path), 1))

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
                time = (time_dt - datetime(1900, 1, 1)).total_seconds()

            bar.n = round(time, 1)
            bar.refresh()

        else:
            match = re.search(r'black_start:([\d\.]+) black_end:([\d\.]+) black_duration:([\d\.]+)', line)
            if match:
                start = float(match.group(1))
                end = float(match.group(2))
                duration = float(match.group(3))
                bf+=[[start,end,duration]]
    return bf


def black_frame_detect_with_multiprocess(video_path, weight_file=None, queue=None, quantity_processes=None, final_results=None, info_container=None, process_number=0):
    command = ['ffmpeg', '-i',  video_path, '-filter_complex', 'blackdetect=d=0.1:pix_th=0.05', '-f', 'null', '-']

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

    bf=[]
    frame_pattern = re.compile(r'^frame=(\d+)\b.*fps=')
    fps_pattern = re.compile(r'^.*fps=(\d+(?:\.\d+)?)\b.*$')
    time_pattern = re.compile(r'^.*time=(\d\d:\d\d:\d\d\.\d\d).*')

    # print("Поиск чёрных кадров...")
    # bar=tqdm(total=round(video_duration(video_path),1))

    # model=torch.load(weight_file, map_location=torch.device('cpu'))
    # classes = {y: x for x, y in model['model'].names.items()}

    # process_lock = Lock()
    # info_dict = {
    #     "process": process_number,
    #     "object": classes.keys(),
    #     "progress": "",
    #     "remaining_time": "",
    #     "recognized_for": "",
    #     "process_completed": False,
    # }
    # info_container

    while True:
        video_dur = video_duration(video_path)
        bar = tqdm(total=video_dur)
        print(video_dur)


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
                time = (time_dt - datetime(1900, 1, 1)).total_seconds()

            # bar.n = round(time, 1)
            # bar.refresh()

        else:
            match = re.search(r'black_start:([\d\.]+) black_end:([\d\.]+) black_duration:([\d\.]+)', line)
            if match:
                start = float(match.group(1))
                end = float(match.group(2))
                duration = float(match.group(3))
                bf+=[[start,end,duration]]
    return bf


q1 = black_frame_detect_with_multiprocess("C:\\Users\\Maxim\\tv-21-app\\tv21-app-rep2\\input\\Shitfest.mp4")
for i in q1:
    print(f'Чёрный кадр с {i[0]:.3f} сек. по {i[1]:.3f} сек. (длительность {i[2]:.3f} сек.)')
