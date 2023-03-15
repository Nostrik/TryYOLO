# docker run -it --user root -p 8080:8080 -v `pwd`/mydata:/label-studio/data heartexlabs/label-studio:latest
from ultralytics import YOLO
from loguru import logger
import time

model = YOLO("yolov8n.yaml")
# model = YOLO("yolov8n.pt")


def main():
    results = model.train(data="coco128.yaml", epochs=3)


if __name__ == '__main__':
    logger.info(f"started main at {time.strftime('%X')}")
    main()
    logger.info(f"finished main at {time.strftime('%X')}")

