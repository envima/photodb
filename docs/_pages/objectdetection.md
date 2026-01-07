---
title: Exemplary Object Detection Workflow
sidebar:
  nav: objectdetection
---



Due to using easily accessible YAML metadata sidecar files PhotoDB enables interaction with image metadata through any programming language at any point of a proccessing workflow. When annotating large image sets you might want to use object detection models, especially if you aim for automation. Here, we show you 2 exemplary object detection workflows that access the PhotoDB YAML metadata files for external model application and an option for automation:

1. use the `photodb_yolo_object_detection` python package

2. run MegaDetector and execute the PhotoDB megadetector task 

3. periodically execute a processing script and save results to PhotoDB metadata

**You can also write your own scripts using other models and perform new processing steps!**