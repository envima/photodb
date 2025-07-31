---
title: Integrate Automatic Object Detection into PhotoDB
sidebar:
  nav: objectdetection
---

Due to using easily accessible YAML metadata sidecar files PhotoDB enables interaction with image metadata through any programming language at any point of a proccessing workflow. When annotating large image sets you might want to use object detection models, especially if you aim for automation. Here, we show you 2 simple ways in which you can integrate object detection into PhotoDB and an option for automation:

1. use the `photodb_yolo_object_detection` python package

2. run MegaDetector and execute the PhotoDB megadetector task 

3. periodically execute a processing script and save results to PhotoDB metadata

**You can also write your own scripts to integrate other models or perform new processing steps!**