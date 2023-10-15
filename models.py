import time
import subprocess
from abc import ABC, abstractclassmethod
from loguru import logger

from func_expansion import frame_count_extract, transform_frames_to_time, remainig_progress, parse_string


class NeuralNetwork(ABC):
    @abstractclassmethod
    def load_model(self, model_path):
        pass

    @abstractclassmethod
    def preprocess_input(self, input_data):
        pass

    @abstractclassmethod
    def postprocess_output(self, output_data):
        pass

    @abstractclassmethod
    def get_model():
        pass

    
class Line(ABC):
    @abstractclassmethod
    def show_values(self):
        pass

    @abstractclassmethod
    def get_current_position(self):
        pass

    @abstractclassmethod
    def get_total_amount(self):
        pass

    @abstractclassmethod
    def get_getected_objects(self):
        pass

    @abstractclassmethod
    def get_processing_time(self):
        pass


class NWorker(ABC):
    @abstractclassmethod
    def load_network_model(self):
        pass

    @abstractclassmethod
    def load_line_model(self):
        pass

    @abstractclassmethod
    def show_progress_results(self):
        pass


class NWorkerYoloV8(NWorker):
    def __init__(self, network_model, line_model):
        self.netwok_model = network_model
        self.line_model = line_model
        self.start_time = None

    def load_network_model(self, n_model):
        self.netwok_model = n_model
    
    def load_line_model(self, l_model):
        self.line_model = l_model

    def show_progress_results(self):
        progress = self.remainig_progress(
            self.line_model.get_current_position(),
            self.line_model.get_total_amount()
        )
        if self.line_model.get_current_position():
            current_position = int(self.line_model.get_current_position())
            elapsed_time = time.time() - self.start_time
            avg_time_per_iteration = elapsed_time / current_position
            remaining_time = avg_time_per_iteration * (int(self.line_model.get_total_amount()) -  current_position)
            time_in_seconds_minutes_hours = self.transform_time(remaining_time)
        else:
            time_in_seconds_minutes_hours = None
        if self.line_model.get_processing_time():
            processing_time = self.line_model.get_processing_time()
        else:
            processing_time = None
        # print(
        #     f"{self.netwok_model} | {progress}% | {time_in_seconds_minutes_hours} | {processing_time}", end='\r'
        # )

        print(
            f"Object: {self.netwok_model} | Processing Time: {processing_time} | Progress: {progress} | Remaining Time: {time_in_seconds_minutes_hours}", end='\r'
        )   

    def set_start_time(self, start_time):
        self.start_time = start_time

    def transform_time(self, value):
        # if value:
        #     frame_fl = float(value)
        #     seconds = frame_fl // 24
        #     minutes = seconds // 60
        #     hours = minutes // 60
        #     minutes %= 60
        #     seconds %= 60
        #     return [seconds, minutes, hours]
        if value:
            if value < 60:
                updt_value = f'{value:.0f} sec'
            elif value < 3600:
                updt_value = f'{value/60:.0f} min'
            else:
                updt_value = f'{value/3600:.0f} hours'
            return updt_value

    def remainig_progress(self, cur_frm, all_frms):
        if cur_frm and all_frms:
            progress = (float(cur_frm) / float(all_frms)) * 100
            result = round(progress, 0)
            return str(result).replace('.0', '')
        

    def run_predict(self, start_time):
        self.start_time = start_time
        process = self.netwok_model.run_predict()
        return process


class YoloNeuralNetwork(NeuralNetwork):
    def __init__(self, model_path, video_path) -> None:
        self.model = model_path
        self.video = video_path

    def load_model(self, model_path):
        self.model = model_path

    def preprocess_input(self, video_path):
        self.video = video_path

    def postprocess_output(self, output_data):
        pass

    def run_predict(self):
        PopenPars = [
            "yolo", "predict", f"model={self.model}", f"source={self.video}",
            ]
        return subprocess.Popen(PopenPars, stderr=subprocess.PIPE)

    def get_model(self):
        summary = f"{self.model}"
        print(summary)


class YoloV8Line(Line):
    def __init__(self) -> None:
        self.line = None
        self.values = None

    def update_values(self, new_line):
        self.line = new_line
        self.values = self.extract_values()

    def extract_values(self):
        if not self.line.startswith('video ') or not self.line.endswith('s') or ':' not in self.line:
            return None

        components = self.line.strip().split(' ')
        video_num, video_total = components[1].split('/')
        current_pos, total_amount = components[2][1:-1].split('/')
        path_to_file, rest_of_line = self.line.rsplit(': ', 1)
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
    
    def show_values(self):
        print(self.values)

    def get_current_position(self):
        if self.values:
            cur_pos = self.values['current_pos']
            return cur_pos
            
    def get_total_amount(self):
        if self.values:
            return self.values['total_amount']

    def get_getected_objects(self):
        if self.values:
            return self.values['detected_objs']

    def get_processing_time(self):
        if self.values:
            return self.values['processing_time']
        

def start_predict(weigth_file, target_video):
    logger.debug(weigth_file, target_video)
    yolo = YoloNeuralNetwork(
        model_path=weigth_file,
        video_path=target_video
    )
    yolo_line = YoloV8Line()
    yolo_worker = NWorkerYoloV8(
        network_model=yolo,
        line_model=yolo_line
    )
    process = yolo_worker.run_predict(time.time())
    while True:

        output = process.stderr.readline().decode('utf-8')
        yolo_line.update_values(output.strip())
        yolo_worker.show_progress_results()


# if __name__ == "__main__":
#     # yolo = YoloNeuralNetwork()
#     # yolo.load_model('C:\\Users\Maxim\\tv-21-app\my-tv21-app\input\cigarette_18092023_911ep.pt')
#     # yolo.preprocess_input('C:\\Users\Maxim\\tv-21-app\\my-tv21-app\\input\\ad1.mp4')
#     # yolo.postprocess_output('C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input')

#     # load_model = 'C:\\Users\\Maksim\\tv-21-app\\TryYOLO\\input\\cigarette_911ep.pt'
#     # preprocess_input = 'C:\\Users\\Maksim\\tv-21-app\\TryYOLO\\input\\ad1.mp4'

#     # yolo = YoloNeuralNetwork(
#     #     model_path='C:\\Users\\Maksim\\tv-21-app\\TryYOLO\\input\\cigarette_911ep.pt',
#     #     video_path='C:\\Users\\Maksim\\tv-21-app\\TryYOLO\\input\\ad1.mp4'
#     # )
#     # yolo_line = YoloV8Line()
#     # yolo_worker = NWorkerYoloV8(yolo, yolo_line)
#     # yolo_worker.load_line_model(yolo_line)
#     # process = yolo.run_predict()
#     # yolo_worker.set_start_time(time.time())
#     # while True:

#     #     output = process.stderr.readline().decode('utf-8')
#     #     yolo_line.update_values(output.strip())
#     #     yolo_worker.show_progress_results()
#     start_predict(
#         weigth_file='C:\\Users\\Maksim\\tv-21-app\\TryYOLO\\input\\cigarette_911ep.pt',
#         target_video='C:\\Users\\Maksim\\tv-21-app\\TryYOLO\\input\\ad1.mp4',
#     )
