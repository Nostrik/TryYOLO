from ultralytics import YOLO
from loguru import logger
import time

model = YOLO("yolov8n.yaml")


def main():
    res = model('images/bb0684.jpg')


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f"started main at {time.strftime('%X')}")
    main()
    end_time = time.time()
    logger.info(f"finished main at {time.strftime('%X')}")
    logger.info(f"time spent is {end_time - start_time}")
