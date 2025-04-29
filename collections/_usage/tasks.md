---
title: PhotoDB / AudioDB Tasks
---

Tasks are possibly long running actions within the PhotoDB / AudioDB application. For example, when using PhotoApp you may generate YAML metadata files by running the `photo_create_yaml` task or refresh the web interface using the `photo_refresh` task.

Currently tasks are executed in the audio web-interface. Even for PhotoDB only tasks, you need to open the audio web-interface to manage tasks.

#### Example:

Application sever is accessible by web address:
```text
http://localhost:8080
```
Then PhotoApp is at:
```text
http://localhost:8080/web/photo
```

To switch to AudioApp, you need to replace the `photo` part with `audio`:
```text
http://localhost:8080/web/audio
```
There, click on the top left button to open the left navigation side panel and select the entry `Task submission` to execute PhotoDB tasks:

<img src="/photodb_documentation/assets/PhotoApp_tasksubmission.png" alt="PhotoDB AudioDB task submission" width="auto" height="300" align="center">

Select a task from the drop down menu at the top left and click `submit task`. A pop-up window will open showing you the progress of the task. Once the pop-up window indicates that the task is done you can switch back you PhotoApp by replacing `audio` with `photo` in the web address.

See below for a list of available tasks and explanations of each task's function.

# Tasks

## PhotoDB

### photo_create_file_hashs

For all photo files create checksums (i.e. a value that represents the number of bits in a transmission message). Skip files with already created checksums.  
*See [image metadata property XXH64](/photodb_documentation/usage/metadata.html)*.

### photo_create_yaml

Traverse `root_data_path` and for all image files without a corresponding YAML file in `root_path` create a new YAML file. Existing YAML files are not overwritten.
*See [image metadata](/photodb_documentation/usage/metadata.html)*.

**This task must be executed when new images are added to PhotoDB!**

### photo_insert_megadetector_detections

Insert **MegaDetector** detections.

MegaDetector is an extenal application to detect **animal**, **person** or **vehicle**. For how to install and run MegaDetector, see [MegaDetector repository on GitHub](https://github.com/microsoft/CameraTraps/blob/main/megadetector.md).

MegaDetector retuns a JSON results file. Detections content of that file can be inserted in PhotDB meta data YAML files with this task.  
*See for inserted MegaDetector detections [image metadata property detections](/photodb_documentation/usage/metadata.html)*.

### photo_refresh

Traverse `root_path` and check for changed, added or removed YAML files to update photo database.  
*See [PhotoDB configuration properties root_path and root_data_path](/photodb_documentation/configuration/PhotoDB.html)*.

This task needs to be run if some data was changed externally, e.g. photo files have been added or YAML meta data has been modified manually.

### photo_update_thumbs

For a quick overview of your images, the PhotoApp web-interface browser page shows small thumbnails of the photo files. For quick user interaction thumbnails are cached and generated on demand.

This tasks scans for not already cached thumbnails and creates all missing thumbnails. This prevents the user to wait for viewing thumbnails at the browser page.

## AudioDB

### audio_compact_sample_storage_db

Compact sample database. Database is closed. AudioDB needs to be restared manually afterwards to access the database again.

### audio_create_file_hashs

Create hashs of all audio files, if missing.

### audio_create_yaml

Traverse root_data_path and for all WAV files without YAML file in root_path create a new YAML file.

### audio_location_timeseries

Create audio recording timeseries per location.

### audio_normalise_meta

Normalise metadata.

### audio_qoa_check

Check QOA audio files.

### audio_qoa_convert

Convert audio files to QOA audio format.

### audio_rebuild

Clear sample database and traverse root_path with reading all YAML files and filling sample database.

### audio_rebuild_label

Clear label database and traverse all entries in sample database to fill label database and write a set of CSV files to output folder containing labeling entries and statistics.

### audio_recreate_locations_from_inventory

Remove locations and insert locations from inventory.

### audio_refresh

Traverse root_path and check for changed or added or removed YAML files to update sample database.

### audio_refresh_worklists

Regenerate worklists.

### audio_sample_statistics

Create statistics about sample time and location.

### audio_sample_storage_refresh_ordered_sample

Refresh ordered sample.

### audio_scan_yaml_orphans

Scan for yaml files with missing data files.

### infinite

Infinite running task. For testing purposes.