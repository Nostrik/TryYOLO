from abc import ABC, abstractclassmethod


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
        pass

    
class Line(ABC):
    @abstractclassmethod
    def show_line(self):
        pass


if __name__ == "__main__":
    ...
