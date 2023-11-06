# from ultralytics.models.yolo import YOLO
from ultralytics import YOLO
import argparse
import subprocess

parser = argparse.ArgumentParser(description='Детектор')

parser.add_argument('-v', '--target_video', type=str, help='Путь к видео файлу', required=True)
parser.add_argument('-c', '--save_csv', dest='save_csv', action='store_true', required=False, help='Сохранение результатов в csv файл')
parser.add_argument('-s', '--save_video', dest='save_video', action=argparse.BooleanOptionalAction, required=False, help='Сохранение видео с результатами работы')
parser.add_argument('-w', '--weight_file', type=str, help='Путь к файлу с весами', required=True)

args = parser.parse_args()
model = YOLO(args.weight_file)

results = model.predict(source=args.target_video
        , save = bool(args.save_video)
        , save_txt = bool(args.save_csv)
        , exist_ok = True
)
print(
    f"weight_file={args.weight_file}\n" +
    f"target_video={args.target_video}\n" + 
    f"save_video={args.save_video}\n"
)
# results = subprocess.Popen(
#     ["yolo", "predict", f"model={args.weight_file}", f"source={args.target_video}"], shell=True, stderr=subprocess.STDOUT
#     )
