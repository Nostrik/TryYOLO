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
    def __init__(self, yolo_line) -> None:
        self.line = yolo_line
        self.values = self.extract_values()

    def extract_values(self):
        self.line
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
            return self.values['current_pos']
            
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
    yolo.load_model('C:\\Users\Maxim\\tv-21-app\my-tv21-app\input\cigarette_18092023_911ep.pt')
    yolo.preprocess_input('C:\\Users\Maxim\\tv-21-app\\my-tv21-app\\input\\ad1.mp4')
    yolo.postprocess_output('C:\\Users\\Maxim\\tv-21-app\\my-tv21-app\\input')
    yolo.get_summary()
    process = yolo.run_predict()
    while True:

        output = process.stderr.readline().decode('utf-8')
        # print(output, end='')
        print(parse_string(output.strip()))
