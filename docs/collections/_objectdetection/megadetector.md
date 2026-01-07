---
title: photo_insert_megadetector_detections
---

MegaDetector is an extenal application to detect **animals**, **persons** or **vehicles**. Install and run MegaDetector following the official instructions by Microsoft, see [MegaDetector repository on GitHub](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md).

MegaDetector outputs a single `json` file containing detection results of all the images it analysed. After installing and running MegaDetector (external to PhotoDB) you can use the PhotoDB `photo_insert_megadetector_detections` task to write these results into the individual PhotoDB YAML metadata files with a few clicks:

1. Switch to audio web interface and open the task submission panel as described under [tasks](/photodb/usage/tasks.html).

2. Provide your MegaDetector output file and click `SUBMIT TASK`.

<img src="/photodb/assets/PhotoApp_tasksubmission_megadetector.png" alt="photo_insert_megadetector_detections" width="auto" height="300" align="center">

The detection results are now written to the metadata files.

3. Execute the `photo_refresh` task to make sure the bounding boxes will be displayed in the PhotoApp Viewer and switch back to PhotoApp to inspect MegaDetector's detections.