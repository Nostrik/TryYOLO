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


class OutPutter(ABC):
    @abstractclassmethod
    def send_to_terminal(self):
        pass
    

def for_multiproicessing(queue=None, quantity_processes=None, final_results=None, info_container=None, process_number=0):
    def decorator(func):
        def wrapper(*args, **kwargs):
            pass
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator
