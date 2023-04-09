from ultralytics import YOLO

# model = YOLO("yolov8x.pt")
model = YOLO("c:\\Downloads\\testing\\smoking\\cigar\\train\\weights\\best.pt")

results = model.predict(source="ad1.mkv", save=True        
        ,exist_ok = True      # whether to overwrite existing experiment
)
# results = model.predict(source="gf.mp4", save=True)

