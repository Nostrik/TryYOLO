import re


def frame_count_extract(line):
    current_frame = None
    all_frames = None
    pattern = r"\((\d+)\/(\d+)\)"
    match = re.search(pattern=pattern, string=line)
    if match:
        current_frame = match.group(1)
        all_frames = match.group(2)
    return current_frame, all_frames


def transform_frames_to_time(frame):
    if frame:
        frame_fl = float(frame)
        seconds = frame_fl // 24
        minutes = seconds // 60
        hours = minutes // 60
        minutes %= 60
        seconds %= 60
        return [seconds, minutes, hours]
    

def remainig_progress(cur_frm, all_frms):
    if cur_frm and all_frms:
        progress = (float(cur_frm) / float(all_frms)) * 100
        return round(progress, 2)