import matplotlib.pyplot as plt
from ultralytics import YOLO
import urllib
import matplotlib.patches as patches
import cv2
import os
import shutil
import subprocess




# Load the YOLO model
model = YOLO("model/11/best.pt")		
#predict
 
results = model.predict(source="../../data/glasses_yolo/train/images/",stream=True)  
print("3")
print("Results",results)
for result in results:
    print("result",result)
    plt.imshow(result.orig_img)
    print("4")
    result.boxes.xyxy   # box with xyxy format, (N, 4)
    result.boxes.xywh   # box with xywh format, (N, 4)
    result.boxes.xyxyn  # box with xyxy format but normalized, (N, 4)
    result.boxes.xywhn  # box with xywh format but normalized, (N, 4)
    result.boxes.conf   # confidence score, (N, 1)
    result.boxes.cls    # cls, (N, 1)
# REMOVE THIS 
    # if result.boxes.xyxy.numel() == 0:
    #     continue
#---------------- 
    print("5")
    for box in result.boxes.xyxy:
        x, y, xmax, ymax = box.tolist()
        width = xmax - x
        height = ymax - y
        # Create a rectangle patch
        rect = patches.Rectangle(
            (x, y), width, height, linewidth=2, edgecolor='r', facecolor='none')
    # Add the rectangle to the current axis
        plt.gca().add_patch(rect)
    print("6")
    plt.savefig("result.jpg")
    # answer = input("number ? [Y/n]]")
    # if answer == "n":
    #     shutil.copy(result.path, "wrongdetection/")
    # # Segmentation
    # result.masks.data      # masks, (N, H, W)
    # result.masks.xy        # x,y segments (pixels), List[segment] * N
    # result.masks.xyn       # x,y segments (normalized), List[segment] * N
    # # Classification
    # result.probs     # cls prob, (num_class, )
# Each result is composed of torch.Tensor by default,
# in which you can easily use following functionality:
result = result.cuda()
result = result.cpu()
result = result.to("cpu")
result = result.numpy()