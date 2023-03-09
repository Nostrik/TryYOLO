from ultralytics import YOLO

model = YOLO("yolov8n.pt")  # загрузите предварительно обученную модель YOLOv8n

model.train(data="coco128.yaml")  # обучите модель
model.val()  # оцените производительность модели на наборе проверки
model.predict(source="https://ultralytics.com/images/bus.jpg")  # предсказать по изображению
model.export(format="onnx")  # экспортируйте модель в формат ONNX

# https://habr.com/ru/post/710016/
