from ultralytics import YOLO
from loguru import logger
import time


def main():
    # model = YOLO("trained_models/from-nik/weights/last.pt")
    model = YOLO("yolov8n.yaml")

    model.train(
        data = "cigarette_data.yaml"
        # data = None           # path to data file, i.e. coco128.yaml
        # ,model = "./cigar/train3/weights/best.pt" # path to model file, i.e. yolov8n.pt, yolov8n.yaml
        # ,model = "yolov8n.pt" # path to model file, i.e. yolov8n.pt, yolov8n.yaml
        ,epochs = 2000        # number of epochs to train for
        ,patience = 0         # epochs to wait for no observable improvement for early stopping of training
        ,batch = -1            # number of images per batch (-1 for AutoBatch)
        # ,imgsz = 640           # size of input images as integer or w,h
        ,save = True           # save train checkpoints and predict results
        # ,save_period = 10      # Save checkpoint every x epochs (disabled if < 1)
        ,cache = False         # True/ram, disk or False. Use cache for data loading
        # ,device = None         # device to run on, i.e. cuda device=0 or device=0,1,2,3 or device=cpu
        # ,workers = 8           # number of worker threads for data loading (per RANK if DDP)
        ,project = "cigarette"        # project name
        # ,name = None           # experiment name
        ,exist_ok = True      # whether to overwrite existing experiment
        ,pretrained = True    # whether to use a pretrained model
        # ,optimizer = 'SGD'     # optimizer to use, choices=['SGD', 'Adam', 'AdamW', 'RMSProp']
        ,verbose = True       # whether to print verbose output
        # ,seed = 0              # random seed for reproducibility
        # ,deterministic = True  # whether to enable deterministic mode
        # ,single_cls = True    # train multi-class data as single-class
        # ,image_weights = True # use weighted image selection for training
        # ,rect = False          # support rectangular training
        # ,cos_lr = False        # use cosine learning rate scheduler
        # ,close_mosaic = 10     # disable mosaic augmentation for final 10 epochs
         ,resume = True        # resume training from last checkpoint
        # ,amp = True            # Automatic Mixed Precision (AMP) training, choices=[True, False]
        # ,lr0 = 0.01            # initial learning rate (i.e. SGD=1E-2, Adam=1E-3)
        # ,lrf = 0.01            # final learning rate (lr0 * lrf)
        # ,momentum = 0.937      # SGD momentum/Adam beta1
        # ,weight_decay = 0.0005 # optimizer weight decay 5e-4
        # ,warmup_epochs = 3.0   # warmup epochs (fractions ok)
        # ,warmup_momentum = 0.8 # warmup initial momentum
        # ,warmup_bias_lr = 0.1  # warmup initial bias lr
        # ,box = 7.5             # box loss gain
        # ,cls = 0.5             # cls loss gain (scale with pixels)
        # ,dfl = 1.5             # dfl loss gain
        # ,fl_gamma = 0.0        # focal loss gamma (efficientDet default gamma=1.5)
        # ,label_smoothing = 0.0 # label smoothing (fraction)
        # ,nbs = 64              # nominal batch size
        # ,overlap_mask = True   # masks should overlap during training (segment train only)
        # ,mask_ratio = 4        # mask downsample ratio (segment train only)
        # ,dropout = 0.0         # use dropout regularization (classify train only)
        # ,val = True            # validate/test during training
    )
    

if __name__ == '__main__':
    start_time = time.time()
    logger.info(f"started main at {time.strftime('%X')}")
    main()
    end_time = time.time()
    logger.info(f"finished main at {time.strftime('%X')}")
    logger.info(f"time spent is {end_time - start_time}")
    
