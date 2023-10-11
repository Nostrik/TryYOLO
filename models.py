import subprocess
from abc import ABC, abstractclassmethod

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
    def get_summary():
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
    def show_progress(self):
        pass


class NWorkerYoloV8(NWorker):
    def __init__(self):
        self.netwok_model = None
        self.line_model = None

    def load_network_model(self, n_model):
        self.netwok_model = n_model
    
    def load_line_model(self, l_model):
        self.line_model = l_model

    # def show_progress(self, current_pos, total_amount, detected_objects, processing_time):
    #     progress = self.remainig_progress(current_pos, total_amount)
    #     remaining_time = self.transform_frames_to_time(current_pos)
    #     pt = self.line_model.get_processing_time()
    #     print(
    #         f"{self.netwok_model} | {progress} | {remaining_time} | {pt}", end='\r'
    #     )
    #     pass

    def show_progress(self):
        progress = self.remainig_progress(
            self.line_model.get_current_position(),
            self.line_model.get_total_amount()
        )
        remaining_time = self.transform_frames_to_time(self.line_model.get_current_position())
        processing_time = self.line_model.get_processing_time()
        print(
            f"{self.netwok_model} | {progress} | {remaining_time} | {processing_time}", end='\r'
        )

    def transform_frames_to_time(self, frame):
        if frame:
            frame_fl = float(frame)
            seconds = frame_fl // 24
            minutes = seconds // 60
            hours = minutes // 60
            minutes %= 60
            seconds %= 60
            return [seconds, minutes, hours]

    def remainig_progress(self, cur_frm, all_frms):
        if cur_frm and all_frms:
            progress = (float(cur_frm) / float(all_frms)) * 100
            return round(progress, 2)
            


class YoloNeuralNetwork(NeuralNetwork):
    def __init__(self) -> None:
        self.model = None
        self.video = None

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

    def get_summary(self):
        summary = f"[model] - {self.model} | [video] - {self.video}"
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


if __name__ == "__main__":
    yolo = YoloNeuralNetwork()
    yolo_line = YoloV8Line()
    yolo_worker = NWorkerYoloV8()
    yolo_worker.load_network_model(yolo)
    yolo_worker.load_line_model(yolo_line)
    # yolo.load_model('C:\\Users\Maxim\\tv-21-app\my-tv21-app\input\cigarette_18092023_911ep.pt')
    # yolo.preprocess_input('C:\\Users\Maxim\\tv-21-app\\my-tv21-app\\input\\ad1.mp4')
    # yolo.postprocess_output('C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input')
    yolo.load_model('C:\\Users\\Maksim\\tv-21-app\\TryYOLO\\input\\cigarette_911ep.pt')
    yolo.preprocess_input('C:\\Users\\Maksim\\tv-21-app\\TryYOLO\\input\\ad1.mp4')
    yolo.postprocess_output('C:\\Users\\Maksim\\tv-21-app\\TryYOLO\\input\\')
    yolo.get_summary()
    process = yolo.run_predict()
    while True:

        output = process.stderr.readline().decode('utf-8')
        yolo_line.update_values(output.strip())
        # if output:
        #     print(output)
        # print(
        #     f'{yolo_line.get_current_position()} | {yolo_line.get_total_amount()} | {yolo_line.get_getected_objects()} | {yolo_line.get_processing_time()}'
        #     )
        yolo_worker.show_progress()
        