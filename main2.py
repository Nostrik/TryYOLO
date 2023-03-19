from ultralytics import YOLO
from loguru import logger
import time

model = YOLO("yolov8n.yaml")
# model = YOLO("yolov8n.pt")


def main():
    #  196: Cigar/Cigarette
    results = model.train(data="Objects365.yaml", epochs=1)


if __name__ == '__main__':
    logger.info(f"started main at {time.strftime('%X')}")
    main()
    logger.info(f"finished main at {time.strftime('%X')}")