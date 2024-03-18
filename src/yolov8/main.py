from ultralytics import YOLO

# load a pretrained model (recommended for training)
model = YOLO("yolov8x.pt")

# Use the model
model.train(data="/home/mcollette/Documents/3A/PI/tps_iaBOX_2022_glass_detector/data/glasses_yolov8/data.yaml",
            epochs = 5)  # train the model
# metrics = model.val()  # evaluate model performance on the validation set
# # predict on an image
# results = model("https://ultralytics.com/images/bus.jpg")
# # path = model.export(format="onnx")  # export the model to ONNX format


#Load model 

model = YOLO("data/runs/detect4/weights/best.pt")
