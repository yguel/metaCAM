### Multistream_yolo launch the backend for the TPS2023 IaBox project

## install pipenv for python 3.10
pip3.10 install --user pipenv

## install
pipenv --python 3.10
pipenv --python 3.10 install -r requirements.txt
## Run
pipenv --python 3.10 run python3 api_detection.py
## Test
It takes some time and report errors but ignore them
After some time, it will display a url with the port 5000, click on it or copy it in your browser

### IA models

## RetinaNet  
Code from RetinaNet guide work with coco/2017 dataset

## Yolov5 

The code of yolov5 used  until R3 glasses detection 

## Yolov8

