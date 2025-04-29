########
#
# convert_bbox_to_yolo.py
#
# Convert PhotoDB bounding boxes to YOLO format training data.
# Images must be saved in directory named 'images', as this is what YOLO will expect.
# PhotoDB config.yaml is used to get path / project info. Must include upt to date path information, be located in PhotoDB root project, and named "config.yaml".
# YOLO labels are written to directory 'labels', created by replacing the last instance of 'images' in the root_data_path specified in the PhotoDB configuraion file.
# YOLO configuration files are written to diretcory specified in command line argument.
#
########

#%% imports, environment

import argparse
import yaml
import pandas as pd
import os
import sys
from pathlib import Path

#%% support function for individual format conversion

def photodb_bbox_to_yolo(metadata, class_definition):
    """Convert PhotoDB bbox to YOLOv8 bbox xywh format

    Args:
        metadata: photodb yaml metadata file containing image info and detection bboxes in photoDB format:
            normalized x, normalized y, normalized directional width, normalized directional height
            e.g.: 0.4, 0.9, 0.2, -0.3
        class_definition (dict[<photodb_classification_definition>: <yolo_class_name>])

    Returns:
        label in yolov8 format:
            [class] [normalized x center] [normalized y center] [normalized width] [normalized height]
            e.g.: 0 0.4 0.3 0.6 0.1
    """
    yolov8_labels = []
    
    class_list = class_definition['name']
    
    for detection in metadata["detections"]:

        class_name = detection['classifications'][0]['classification']
        
        if class_list.isin([class_name]).any():
            
            # get bbox x center, y center, width, and height
            x = detection['bbox'][0] + (detection['bbox'][2] / 2)
            y = detection['bbox'][1] + (detection['bbox'][3] / 2)
            w = abs(detection['bbox'][2])
            h = abs(detection['bbox'][3])

            # class_id
            class_id = class_definition.loc[class_definition['name'] == class_name, 'yolo_name'].values[0]

            # label in yolov8 format
            yolov8_bbox = [class_id, x, y, w, h]
            yolov8_labels.append(yolov8_bbox)
        
    return yolov8_labels

#%% support function to get label path

def replace_last_instance(path, old, new):
    '''
    replace last instance of specified directory name in filepath with specified new directory name
    arguments:
        path {str} : filepath
        old {str} : directory name to be replaced
        new {str} : directory name replacement
    returns:
        updated filepath {str}
    '''
    parts = path.rsplit(old, 1)  # Split from the right at the last occurrence
    return new.join(parts)  # Join with the new substring

#%% main functions

def append_image_path_to_txt_file(txt_file, image_path, verbose = False):
    '''
    opens / creates YOLO format txt file containig list of image file paths and appends new image filepath if it is not contained in txt file already

    arguments:
        txt_file {str} : path to YOLO format txt file with image filepath collection
        image_path {str} : path to image file that should be appended to txt file
        verbose {boolean}

    returns:
        True if image_path has been added to txt_file
        False if image_path was already in txt_file (txt_file is not altered)
    '''
    # Normalize the new path to use a consistent separator (e.g., forward slashes)
    new_path = os.path.normpath(image_path)  # Normalize path (converts backslashes to forward slashes)
    
    # create file if doesn't exist or open and read all lines
    with open(txt_file, 'a+') as file:
        file.seek(0) # move file pointer to beginning of file
        paths = file.readlines()

        # Normalize each path in the file
        paths = [os.path.normpath(path.strip()) for path in paths]

        # Check if the normalized new path is already in the list
        if new_path in [path for path in paths]:
            # return false to indicate that file is not altered
            return(False)
        else:
            # If not, append the new path to the file
            file.write(new_path + '\n')
            if verbose:
                print(f"Path '{new_path}' has been added to {os.path.basename(txt_file)}.")
            # and return True to indicate file altercation
            return(True)

def write_yolo_label(yaml_path, cls_def, label_path, verbose = False):
    '''
    converts PhotoDB detection box format to YOLO format and writes YOLO label file to disc
    
    arguments:
        yaml_path {str} : path to PhotoDB metadata yaml file
        cls_def {pd.df} : dataframe containig columns 'name' indicating PhotoDB classification definition and 'yolo_name' indicating YOLO integer classification definition
        label_path {str} : desired output file path
        verbose {boolean}

    returns:
        True if label_path file has been created
        False if label_path file already exists (file will not be altered)
    '''
    # yaml metadata
    with open(yaml_path, 'r') as file:
        meta = yaml.safe_load(file)
    
    # convert detections to YOLOv8 format
    yolov8_labels = photodb_bbox_to_yolo(meta, cls_def)
    
    # check if label already exists
    if os.path.exists(label_path):
        # return False to indicate that function did not do anything
        return(False)
    else:
        # else create label file
        os.makedirs(os.path.split(label_path)[0], exist_ok = True)
        with open(label_path, 'w') as f:
            for label in yolov8_labels:
                # Convert each tuple into a space-separated string
                f.write(" ".join(map(str, label)) + "\n")
        if verbose:
            print(f"Label '{os.path.basename(label_path)}' has been written to {os.path.dirname(label_path)}.")
        # and return True to indicate that label file has been created
        return(True)

def write_yolo_config(yolo_config_directory, photo_train_list, photo_val_list, cls_def, photo_test_list = None):
    '''
    construct and write out YOLO format configuration file "dataset.yml"
    arguments:
        yolo_config_directory {str} : absolute path to output directory
        photo_train_list {str} : filename of PhotoDB review list of training images
        photo_val_list {str} : filename of PhotoDB review list of validation images
        cls_def {pd.df} : dataframe containig columns 'name' indicating PhotoDB classification definition and 'yolo_name' indicating YOLO integer
        photo_test_list {str} : optional, filename of PhotoDB review list of testing images
    returns:
        True if "dataset.yml" has been created
        False if "dataset.yml" already exists (file is not altered)
    '''
    # dataset configuration needed for yolo training
    yolo_config = {
        'path': yolo_config_directory,
        'train': os.path.splitext(photo_train_list)[0] + ".txt",
        'val': os.path.splitext(photo_val_list)[0] + ".txt",
        'names': dict(zip(cls_def['yolo_name'], cls_def['name']))
    }
    if photo_test_list is not None:
        yolo_config['test'] = os.path.splitext(photo_test_list)[0] + ".txt"
        key_order = ['path', 'train', 'val', 'test', 'names']
        yolo_config = {key: yolo_config[key] for key in key_order}
    
    dataset_config_path = os.path.join(yolo_config_directory, "dataset.yml")
    # check if file already exists
    if os.path.exists(dataset_config_path):
        # read existing file
        with open(dataset_config_path, 'r') as f:
            dataset = yaml.safe_load(f)
        # check if there is any new info to add
        if dataset == yolo_config:
            # if not return false to indicate that file has not been changed
            return(False)
        else:
            # or update file
            dataset.update(yolo_config)
            dataset = {key: dataset[key] for key in key_order}
            with open(dataset_config_path, 'w') as f:
                yaml.dump(dataset, f, default_flow_style = False, sort_keys = False)
            return(True) # indicate that file has been changed
    # else create dataset.yml
    else:
        with open(dataset_config_path, 'w') as f:
            yaml.dump(yolo_config, f, default_flow_style = False, sort_keys = False)
        return(True) # indicate that file has been changed

#%% command line driver

def main():

    # command line arguments
    parser = argparse.ArgumentParser(
        description = "Module to convert object detection labels created in PhotoDB to YOLO format. Images must be directly or indirectly in directory named 'images'. PhotoDB config.yaml is used to get path / project info. Must include up to to date path information, be located in PhotoDB root project, and named 'config.yaml'. YOLO labels are written to directory 'labels', created by replacing the last instance of 'images' in root_data_path specified in the PhotoDB configuraion file. YOLO configuration files are written to directory called [project name] within specified output directory.")
    parser.add_argument("photo_config",
                        type = str,
                        help = "absulote path to PhotoDB config.yaml located inside PhotoDB root directory")
    parser.add_argument("yolo_config_dir",
                        type = str,
                        help = "absolute path to directory in which YOLO configuration output shall be created")
    parser.add_argument("photo_project",
                        type = str,
                        help = "project name as specified in PhotoDB configuration file")
    parser.add_argument("photo_train_list",
                        type = str,
                        help = "filename of PhotoDB review list training images, relative to 'review_list_path' specified in PhotoDB configuration file")
    parser.add_argument("photo_val_list",
                        type = str,
                        help = "filename of PhotoDB review list of validation images, relative to 'review_list_path' specified in PhotoDB configuration file labels")
    parser.add_argument("--photo_test_list",
                        type = str,
                        help = "optional, filename of PhotoDB review list of testing images, relative to 'review_list_path' specified in PhotoDB configuration file")
    parser.add_argument("--outdir_exist_ok",
                        action = "store_true",
                        help = "By default the module will throw an error if the YOLO output directory already exists. This can be bypassed by passing the --outdir_exist_ok flag.")
    parser.add_argument("--verbose",
                        action = "store_true",
                        help = "enable more detailed command line output")
    args = parser.parse_args()

    # standardize path variable
    args.photo_config = os.path.normpath(args.photo_config)
    args.yolo_config_dir = os.path.normpath(args.yolo_config_dir)
    
    # PhotoDB project definition
    with open(args.photo_config, 'r') as f:
        cnfg = yaml.safe_load(f)
    project_config = next((item for item in cnfg['photo']['projects'] if item['project'] == args.photo_project), None)

    # check if root_data_path specified in photodb config contains "images"
    if "images" not in project_config['root_data_path']:
        print("ERROR: image path specified in PhotoDB configuration as root_data_path does not contain directory 'images'.")
        sys.exit(1)

    # PhotoDB root directory
    photo_root_path = os.path.dirname(args.photo_config)
    
    # output directories, absolute paths
    yolo_config_directory = os.path.join(args.yolo_config_dir, args.photo_project)
    yolo_labels_dir = replace_last_instance(project_config['root_data_path'], "images", "labels")
    yolo_labels_directory = os.path.join(photo_root_path, yolo_labels_dir)

    # check if YOLO output directory already exists
    exists = []
    if os.path.exists(yolo_config_directory) and args.outdir_exist_ok == False:
        print("ERROR: The following output directory already exists:")
        print(yolo_config_directory)
        print("Use --outdir_exist_ok to write output into existing directory.")
        sys.exit(1)
    
    # else create output directories
    os.makedirs(yolo_config_directory, exist_ok = True)
    os.makedirs(yolo_labels_directory, exist_ok = True)
    
    # classification definition
    cls_def_csv_path = os.path.join(photo_root_path, project_config['classification_definition_csv'])
    cls_def = pd.read_csv(cls_def_csv_path, comment = '#')
    cls_def['yolo_name'] = range(0, len(cls_def))

    # which files to read and where to store them
    photo_review_list_root_path = os.path.join(photo_root_path, project_config['review_list_path'])
    review_lists = {"train" : os.path.join(photo_review_list_root_path, args.photo_train_list),
                    "val" : os.path.join(photo_review_list_root_path, args.photo_val_list)}
    if args.photo_test_list:
        review_lists['test'] = os.path.join(photo_review_list_root_path, args.photo_test_list)

    # tracker for file altering
    files_altered = {'Image_paths_txt_file': [],
                     'Label_files': []}

    # write image paths txt files and label files
    for dp, rl in review_lists.items():
        
        # read in list of files to manipulate for current review_list (= data partition)
        review_list = pd.read_csv(rl)
    
        # path to txt file containing all image paths
        txt_file = os.path.join(yolo_config_directory, os.path.splitext(os.path.basename(rl))[0] + ".txt")

        # loop over individual image paths
        for image_path in review_list['path']:
            absolute_image_path = os.path.join(photo_root_path, project_config['root_data_path'], image_path)

            # append to txt file with image path collection
            files_altered['Image_paths_txt_file'].append(append_image_path_to_txt_file(txt_file, absolute_image_path, verbose = args.verbose))

            # write yolo label file
            label_path = os.path.join(yolo_labels_directory, os.path.splitext(image_path)[0] + ".txt")
            yaml_path = os.path.join(photo_root_path, project_config['root_path'], image_path +'.yaml')
            files_altered['Label_files'].append(write_yolo_label(yaml_path, cls_def, label_path, verbose = args.verbose))

    # dataset configuration needed for yolo training
    if args.photo_test_list:
        files_altered['Yolo_configuration_file'] = [write_yolo_config(yolo_config_directory, args.photo_train_list, args.photo_val_list, cls_def, photo_test_list = args.photo_test_list)]
    else:
        files_altered['Yolo_configuration_file'] = [write_yolo_config(yolo_config_directory, args.photo_train_list, args.photo_val_list, cls_def)]

    # command line output
    for key, value in files_altered.items():
        key_string = " ".join(key.split('_'))
        if all(val is False for val in value):
            print(f"{key_string} already up to date.")
        else:
            print(f"Updated {key_string}.")

if __name__ == '__main__':
    main()























