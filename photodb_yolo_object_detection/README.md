# PhotoDB Automatic Object Detection

custom YOLO model training and dubsequent automated object detection in PhotoDB

## Prerequisits

* **Python > 3.2**

* **photodb_yolo_object_detection installation**
  
  * [download the latest distribution](/photodb_yolo_object_detection/dist)
    
    ```shell
    pip install photodb_yolo_object_detection-1.0.0-py3-none-any.whl
    ```

* **configure PhotoDB**
  
  - make sure to name the image data root directory ```images/``` to comply with YOLO formating expectations
  
  - make sure your config.yaml (located in PhotoDB root directory) is up to date

* **annotated training, validation, and optionally testing data**
  
  * use photo_review_lists to mark subsets of your image data for model training / validation / testing
  
  * draw training / validation / testing bounding boxes in PhotoApp

## Workflow

--- Use ``-h`` or ``--help`` to show command line tool usage. ---

First, convert your training / validation / testing data into YOLO format, i.e. generate individual YOLO format label files stored in ```labels/``` parallel to ```images/```, and some YOLO configuration files stored in ```[project name]/``` within specified output directory.

```shell
photodb_yolo_reformat
```

Second, use your custom data to train a YOLO model for object detection. This tool provides minimal training, i.e. uses default training parameters and does not do hyperparameter tuning. Adjust the [script](/photodb_yolo_object_detection/photodb_yolo_object_detection/photodb_yolo_train.py) to include hyperparameter tuning for optimal model results, if needed.

```shell
photodb_yolo_train
```

Third, apply your custom trained model to all images.

```shell
photodb_yolo_detect
```