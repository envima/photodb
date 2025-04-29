########
#
# detect_custom_objects.py
#
# Apply custom trained YOLO model to all images for object detection.
#
########

#%% imports, environment

import os
import sys
import torch
import yaml
import argparse
from pathlib import Path
from datetime import datetime
from ultralytics import YOLO

#%% support functions

def tensor_to_list(tensor):
    return tensor.cpu().tolist()  # Convert tensor to list and move to CPU if necessary

def define_detection_entry(box, cls_def, training_run):
    '''
    Define PhotoDB detection entry based in YOLO prediction
    arguments:
        box {tensor} : yolo result object .boxes
        cls_def {dict}: <yolo_class_id>:<photodb_classification_definition>
        training_run {str} : Name of the model training run.
    returns:
        dict
    '''
    # transform tensor to list
    bbox = tensor_to_list(box.xywhn[0])
    bbox[0], bbox[1] = bbox[0] - bbox[2] / 2, bbox[1] - bbox[3] /2 # reformat from xy center to xy corner

    # classification name
    cls  = int(tensor_to_list(box.cls[0]))
    classification = cls_def[cls]

    # confidence
    conf = round(tensor_to_list(box.conf)[0], 3)

    # identification
    classificator = 'YOLO'
    identity = training_run

    # date
    date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # complete detection entry
    new_detection = {
        'bbox': bbox,
        'classifications': [
            {'classification':  classification,
                'conf': conf,
                'classificator': classificator,
                'identity': identity,
                'date': date}
        ]
    }
    return(new_detection)

def define_log_entry(training_run, action):
    '''
    PhotoDB metadata log entry for automatic object detection

    arguments:
        training_run {str} : Name of the model training run.
        action {str} 
    returns:
        dict        
    '''
    # datetime
    date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    # complete entry
    log_entry = {'action': action,
                 'training_run': training_run,
                 'date':date}
    return(log_entry)    
    

#%% main functions

def list_images(photo_meta_root, action, training_run):
    '''
    list all images in which objects have not been automatically detected
    
    arguments:
        photo_meta_root {os.path.normpath} : path to PhotoDB metadata root directory
        action {str} : action entry in metadata log
        training_run {str} : project entry in metadata log
    returns:
        filtered list of image file paths
    '''    
    # list all metadata files
    photo_meta_root = Path(photo_meta_root)
    meta_files = [file.relative_to(photo_meta_root) for file in photo_meta_root.rglob('*') if file.is_file()]
    
    contains_action = []
    # filter out files that have been used for automatic object detection with specified model before
    for meta_file in meta_files:
        # open yaml
        complete_path = os.path.join(photo_meta_root, meta_file)
        with open(complete_path, 'r') as f:
            meta = yaml.safe_load(f)

        # does the file contain the specified action?
        contains_action.append(any(entry['action'] == action and entry['training_run'] == training_run for entry in meta['log']))
    # subset files that do not contain action
    filtered_meta_files = [file for file, action in zip(meta_files, contains_action) if not action]

    # get image filepaths
    filtered_image_files = [os.path.splitext(file)[0] for file in filtered_meta_files]
    filtered_image_files = [os.path.normpath(file) for file in filtered_image_files]
    return(filtered_image_files)

def detect_objects(images, model):
    '''
    apply yolo object detection model

    arguments:
        images {list} : list of image filepaths
        model {str} : path to yolo model
        confidence {int} : minimum confidence threshold for detections
        image_size {int} : image size for inference
    returns:
        list of yolo results objects
    '''
    # load the YOLOv8 model
    model = YOLO(model)

    # run the model on the image
    results = model.predict(images, save = False) # returns a list of results objects
    return(results)

def write_detections_to_meta(detections, photo_meta_root, photo_data_root, training_run, action):
    '''
    convert detection to PhotoDB format and save in yaml
    arguments:
        detection {ultralytics.engine.results.Results object}
        photo_meta_root {os.path.normpath} : PhotoDB metadata root path
        photo_data_root {os.path.normpath} : PhotoDB image data root path
    returns:
        PhotoDB format detection results are written to yaml
    '''    
    # open corresponding yaml
    image_path = Path(detections.path)
    photo_data_root = Path(photo_data_root)
    image_path_relative = image_path.relative_to(photo_data_root)
    image_path_relative = os.path.normpath(image_path_relative)
    yaml_path = os.path.join(photo_meta_root, str(image_path_relative) + ".yaml")
    with open(yaml_path, 'r') as file:
        meta = yaml.safe_load(file)
    
    # Check if 'detections' key exists, if not, initialize it as an empty list
    if 'detections' not in meta:
        meta['detections'] = []
    
    # append new entry/entries
    for box in detections.boxes:
        new_detection = define_detection_entry(box, detections.names, training_run)
        meta['detections'].append(new_detection)
    new_log_entry = define_log_entry(training_run, action)
    meta['log'].append(new_log_entry)

    # save the modified metadata back to the YAML file
    with open(yaml_path, 'w') as file:
        yaml.dump(meta, file, default_flow_style=False, sort_keys=False)


#%% command line driver

def main():

    parser = argparse.ArgumentParser(description = "automatic object detection with custom trained YOLO model")
    parser.add_argument("photo_config",
                        type = str,
                        help = "absulote path to PhotoDB config.yaml located inside PhotoDB root directory")
    parser.add_argument("photo_project",
                        type = str,
                        help = "project name as specified in PhotoDB configuration file")
    parser.add_argument("training_run",
                        type = str,
                        help = "absolute path to training run directory")
    args = parser.parse_args()

    # standardize path variable
    args.photo_config = os.path.normpath(args.photo_config)
    args.training_run = os.path.normpath(args.training_run)

    # PhotoDB project definition
    with open(args.photo_config, 'r') as f:
        cnfg = yaml.safe_load(f)
    project_config = next((item for item in cnfg['photo']['projects'] if item['project'] == args.photo_project), None)

    # PhotoDB root directory
    photo_root_path = os.path.dirname(args.photo_config)
    # PhotoDB meta root directory
    photo_meta_root = os.path.join(photo_root_path, project_config['root_path'])
    photo_meta_root = os.path.normpath(photo_meta_root)
    # PhotoDB image root directory
    photo_data_root = os.path.join(photo_root_path, project_config['root_data_path'])
    photo_data_root = os.path.normpath(photo_data_root)

    action = "automatic object detection"
    training_run = os.path.basename(args.training_run)

    # input images
    images = list_images(photo_meta_root, action, training_run)
    images = [os.path.join(photo_data_root, image) for image in images]
    if len(images) == 0:
        print(f"No images without detection by {training_run}. \n Did you already use this model for object detection?")
        sys.exit(0)

    # object detection
    model = os.path.join(args.training_run, "weights/best.pt")
    detections_list = detect_objects(images, model)

    # save results in yaml files
    for detections in detections_list:
        write_detections_to_meta(detections, photo_meta_root, photo_data_root, training_run, action)
    print("Done! Go to PhotoApp to see your detection results!")

if __name__ == "__main__":
    main()

    