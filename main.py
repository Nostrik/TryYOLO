# docker run -it --user root -p 8080:8080 -v `pwd`/mydata:/label-studio/data heartexlabs/label-studio:latest
from ultralytics import YOLO
from loguru import logger
import time

model = YOLO("runs/detect/train11/weights/best.pt")
# model = YOLO("yolov8n.pt")
img1 = 'images/bb0684.jpg'
img3 = 'images/000001.jpg'
img4 = 'images/000002.jpg'
img5 = 'images/000003.gif'
img6 = 'images/000003.jpg'
img7 = 'images/000004.jpeg'
img8 = 'images/000004.jpg'
img9 = 'images/000005.jpg'
img0 = 'images/000006.jpg'
img_list = [img0, img1, img3, img4, img5, img6, img7, img8, img9]


def main():
    #  196: Cigar/Cigarette
#    results = model.train(data="coco128.yaml", epochs=3000)
    for img in img_list:
        find = model(img)
#     res = model('videos/videoplayback.mp4')


if __name__ == '__main__':
    start_time = time.time()
    logger.info(f"started main at {time.strftime('%X')}")
    main()
    end_time = time.time()
    logger.info(f"finished main at {time.strftime('%X')}")
    logger.info(f"time spent is {end_time - start_time}")

