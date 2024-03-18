#!/bin/bash

sudo arp-scan --interface=eth0 --localnet > /home/tprli/Python-3.8.12/tps_iaBOX_2022_glass_detector/src/multistream_yolo/nmap_output.txt

source yolov8env/bin/activate

python  /home/tprli/Python-3.8.12/tps_iaBOX_2022_glass_detector/src/multistream_yolo/analyze_nmap.py
