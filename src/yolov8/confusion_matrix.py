import matplotlib.pyplot as plt
from ultralytics import YOLO
import urllib
import matplotlib.patches as patches
import cv2
import os
import shutil
import subprocess




# Load the YOLO model
model = YOLO("src/yolov8/model/11/best.pt")		
#predict
 
results = model.predict(source="data/test_dataset/",stream=True)  
matrix_confusion={"1":0,"2":0,"3":0,"4":0}
for result in results:
    plt.imshow(result.orig_img)
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
    for box in result.boxes.xyxy:
        x, y, xmax, ymax = box.tolist()
        width = xmax - x
        height = ymax - y
        # Create a rectangle patch
        rect = patches.Rectangle(
            (x, y), width, height, linewidth=2, edgecolor='r', facecolor='none')
    # Add the rectangle to the current axis
        plt.gca().add_patch(rect)
    plt.show()
    answer = input("number? [1/2/3/4]]")
    matrix_confusion[answer]+=1
    
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


print("matrix_confusion",matrix_confusion)

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

# Sample confusion matrix values (replace this with your actual values)
# 238 -> 
matrix_confusion = {"1": 166, "2": 6, "3": 12, "4": 54}

# Extract values from the dictionary
TP = matrix_confusion.get("1", 0)
FP = matrix_confusion.get("2", 0)
FN = matrix_confusion.get("3", 0)
TN = matrix_confusion.get("4", 0)

# Calculate percentages
total_present = TP  + FN 
total_absent = FP + TN
TP_percentage = (TP / total_present) * 100
FP_percentage = (FP / total_absent) * 100
FN_percentage = (FN / total_present) * 100
TN_percentage = (TN / total_absent) * 100

# Create the confusion matrix
conf_matrix = np.array([[TP_percentage, FP_percentage], [FN_percentage, TN_percentage]])

# Define a custom color map from green to red with more green for high TP and TN values
cmap = plt.cm.get_cmap('BuGn', 100)  # Use 100 levels for more granularity

# Create a figure and axis
fig, ax = plt.subplots()

# Plot the confusion matrix with colored cells
im = ax.imshow(conf_matrix, cmap=cmap, vmin=0, vmax=100)  # Set vmin and vmax for percentage scale

# Add a colorbar
cbar = ax.figure.colorbar(im, ax=ax)

# Set the tick labels
classes = ["Présent", "Absent"]
ax.set_xticks(np.arange(len(classes)))
ax.set_yticks(np.arange(len(classes)))
ax.set_xticklabels(classes)
ax.set_yticklabels(classes)

# Label each cell with the corresponding value
for i in range(len(classes)):
    for j in range(len(classes)):
        text = ax.text(j, i, f'{conf_matrix[i, j]:.2f}%', ha='center', va='center', color='black')

# Set labels and title
ax.set_xlabel('Predit')
ax.set_ylabel('Réalité')
ax.set_title('Matrice De Confusion (Pourcentages Verticals)')

# Save the figure
plt.savefig('confusion_matrix_percentage_custom.png')

# Show the plot
plt.show()

