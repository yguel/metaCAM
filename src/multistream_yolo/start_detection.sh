#!/bin/bash

source /home/tprli/yolov8env/bin/activate

cd /home/tprli/Python-3.8.12/tps_iaBOX_2022_glass_detector

python src/multistream_yolo/api_detection.py
