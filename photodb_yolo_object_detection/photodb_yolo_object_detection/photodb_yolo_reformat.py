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

def photodb_bbox_to_yolo(metadata:dict, cls_def:pd.DataFrame):
    """Convert PhotoDB bbox to YOLOv8 bbox xywh format

    Args:
        metadata: photodb metadata containing image info and detection bboxes in photoDB format:
            normalized x, normalized y, normalized directional width, normalized directional height
            e.g.: 0.4, 0.9, 0.2, -0.3
        cls_def: dataframe containig column 'name' indicating PhotoDB classification definition

    Returns:
        label in yolov8 format:
            [class] [normalized x center] [normalized y center] [normalized width] [normalized height]
            e.g.: 0 0.4 0.3 0.6 0.1
        OR
        empty list if there are no detections in metadata / none classified as a value of cls_def
    """
    yolov8_labels = []

    if 'detections' in metadata:
    
        class_list = cls_def['name']
        
        for detection in metadata['detections']:

            if 'bbox' not in detection:
                continue

            class_name = detection['classifications'][0]['classification']
            
            if class_list.isin([class_name]).any():
                
                # get bbox x center, y center, width, and height
                x = detection['bbox'][0] + (detection['bbox'][2] / 2)
                y = detection['bbox'][1] + (detection['bbox'][3] / 2)
                w = abs(detection['bbox'][2])
                h = abs(detection['bbox'][3])

                # class_id
                class_id = cls_def.loc[cls_def['name'] == class_name].index[0]

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
    if not 'images' in path:
        raise ValueError('Image path does not contan directory "images".')
    else:
        parts = path.rsplit(old, 1)
        return new.join(parts)

#%% main functions

def append_image_path_to_txt_file(txt_file, image_path, verbose = False):
    '''
    opens / creates YOLO format txt file containig list of image file paths and appends new image filepath if it is not contained in txt file already

    arguments:
        txt_file {str} : path to YOLO format txt file with image filepath collection
        image_path {str} : path to image file that should be appended to txt file
        verbose {boolean}

    returns:
        txt_file filename if image_path has been added to txt_file
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
        if len(paths) > 0 and new_path in [path for path in paths]:
            # return false to indicate that file is not altered
            return(False)
        else:
            # If not, append the new path to the file
            file.write(new_path + '\n')
            if verbose:
                print(f"Path '{new_path}' has been added to {os.path.basename(txt_file)}.")
            # and return True to indicate file altercation
            return(os.path.basename(txt_file))

def write_yolo_label(yaml_path, cls_def, label_path, verbose = False):
    '''
    converts PhotoDB detection box format to YOLO format and writes YOLO label file to disc
    
    arguments:
        yaml_path {str} : path to PhotoDB metadata yaml file
        cls_def {pd.DF} : dataframe containig columns 'name' indicating PhotoDB classification definition
        label_path {str} : desired output file path
        verbose {boolean}

    returns:
        0 - new label_path file has been created
        1 - label_path file already exists (file will not be altered)
        2 - PhotoDB metadata does not include bbox of any class specified in cls_def; no label_path file created 
    '''
    # yaml metadata
    with open(yaml_path, 'r') as file:
        meta = yaml.safe_load(file)
    
    # convert detections to YOLOv8 format
    yolov8_labels = photodb_bbox_to_yolo(meta, cls_def)

    # check if label already exists
    if os.path.exists(label_path):
        # return 1 to indicate that function did not do anything
        return 1
    
    # return 2 if no (matching) detections were found
    if len(yolov8_labels) == 0:
        if verbose:
            print(f"No detections matching specified classes found in {yaml_path}.")
            return 2
    else:
        # else create label file
        os.makedirs(os.path.split(label_path)[0], exist_ok = True)
        with open(label_path, 'w') as f:
            for label in yolov8_labels:
                # Convert each tuple into a space-separated string
                f.write(" ".join(map(str, label)) + "\n")
        if verbose:
            print(f"Label '{os.path.basename(label_path)}' has been written to {os.path.dirname(label_path)}.")
        # and return 0 to indicate that label file has been created
        return 0

def write_yolo_config(yolo_config_directory, photo_train_list, photo_val_list, cls_def, photo_test_list = None):
    '''
    construct and write out YOLO format configuration file "dataset.yml"
    arguments:
        yolo_config_directory {str} : absolute path to output directory
        photo_train_list {str} : filename of PhotoDB review list of training images
        photo_val_list {str} : filename of PhotoDB review list of validation images
        cls_def {pd.df} : dataframe containig columns 'name' indicating PhotoDB classification definition
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
        'names': dict(zip(cls_def.index.tolist(), cls_def['name']))
    }
    if photo_test_list is None:
        key_order = ['path', 'train', 'val', 'names']
    else:
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
    parser.add_argument("--classes",
                        nargs = "+",
                        type = str,
                        default = None,
                        help = "label classes to convert to YOLO format. If omitted classes are inferred from the PhotoDB classification_definitions csv file specified in config.yaml")
    parser.add_argument("--outdir_exist_ok",
                        action = "store_true",
                        default = False,
                        help = "By default the module will throw an error if the YOLO output directory already exists. This can be bypassed by passing the --outdir_exist_ok flag.")
    parser.add_argument("--verbose",
                        action = "store_true",
                        default = False,
                        help = "enable more detailed command line output")
    args = parser.parse_args()

    # standardize path variable
    args.photo_config = os.path.normpath(args.photo_config)
    args.yolo_config_dir = os.path.normpath(args.yolo_config_dir)
    
    # PhotoDB project definition
    with open(args.photo_config, 'r') as f:
        cnfg = yaml.safe_load(f)
    project_config = next((item for item in cnfg['photo']['projects'] if item['project'] == args.photo_project), None)
    if project_config is None:
        print(f"project {args.photo_project} not in {args.photo_config}")
        sys.exit(1)    

    # PhotoDB root directory
    photo_root_path = os.path.dirname(args.photo_config)
    
    # output directory, absolute paths
    yolo_config_directory = os.path.join(args.yolo_config_dir, args.photo_project)

    # check if YOLO output directory already exists
    exists = []
    if os.path.exists(yolo_config_directory) and args.outdir_exist_ok == False:
        print("ERROR: The following output directory already exists:")
        print(yolo_config_directory)
        print("Use --outdir_exist_ok to write output into existing directory.")
        sys.exit(1)
    
    # else create output directory
    os.makedirs(yolo_config_directory, exist_ok = True)
    
    # classification definition
    if args.classes is None:
        cls_def_csv_path = os.path.join(photo_root_path, project_config['classification_definition_csv'])
        cls_def = pd.read_csv(cls_def_csv_path, comment = '#')
    else:
        cls_def = pd.DataFrame({'name': args.classes})

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
            # write yolo label file if possible
            image_dir = os.path.join(photo_root_path, project_config['root_data_path'])
            label_path = os.path.join(image_dir, os.path.splitext(image_path)[0] + ".txt")
            label_path = replace_last_instance(label_path, 'images', 'labels')
            
            yaml_path = os.path.join(photo_root_path, project_config['root_path'], image_path +'.yaml')
            write_yolo_label_return_value = write_yolo_label(yaml_path, cls_def, label_path, verbose = args.verbose)

            absolute_image_path = os.path.join(photo_root_path, project_config['root_data_path'], image_path)
            if write_yolo_label_return_value in (0, 1): # 0 = label file was created; 1 = file already exists and wasn't altered
                # append to txt file with image path collection
                files_altered['Image_paths_txt_file'].append(append_image_path_to_txt_file(txt_file, absolute_image_path, verbose = args.verbose))
            
            files_altered['Label_files'].append(write_yolo_label_return_value)

    # dataset configuration needed for yolo training
    if args.photo_test_list:
        files_altered['Yolo_configuration_file'] = [write_yolo_config(yolo_config_directory, args.photo_train_list, args.photo_val_list, cls_def, photo_test_list = args.photo_test_list)]
    else:
        files_altered['Yolo_configuration_file'] = [write_yolo_config(yolo_config_directory, args.photo_train_list, args.photo_val_list, cls_def)]

    # command line output
    def plural(count: int, singular: str, plural_form: str | None = None) -> str:
        return singular if count == 1 else (plural_form or singular + 's')
    for key, value in files_altered.items():
        if key == 'Label_files':
            messages = {
                0: "Created {n} new label file{s}.",
                1: "Found {n} preexisting label file{s}, did not alter {them}.",
                2: "Found {n} image{s} without detections or none matching the specified classes.",
            }
            for val, template in messages.items():
                count = sum(v == val for v in value)
                if count:
                    print(template.format(n=count, s=plural(count, ''), them=plural(count, 'it', 'them')))

        if key == 'Image_paths_txt_file':
            if all(v is False for v in value):
                print("No changes made to YOLO image paths txt files.")
            else:
                for tf in set(value) - {False}:
                    print(f"Added {sum(v == tf for v in value)} paths to {tf}.")

if __name__ == '__main__':
    main()























