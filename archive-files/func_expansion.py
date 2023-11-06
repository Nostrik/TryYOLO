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


def parse_string(line):
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
        'current_pos': current_pos,
        'total_amount': total_amount,
        'detected_objs': detected_objs,
        'processing_time': processing_time
    }


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