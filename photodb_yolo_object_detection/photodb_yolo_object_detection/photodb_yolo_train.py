########
#
# minimal_yolo_model_training.py
#
# Minimal YOLO model training with custom data.
#
########

#%% imports, environment

import argparse
import os
from ultralytics import YOLO

#%% main function

def train_yolo(yolo_model, yolo_config, yolo_directory, training_run, training_epochs):
    
    # Load a model
    model = YOLO(yolo_model)  # load an official model

    # use the model
    model.train(data = yolo_config,
                project = yolo_directory,
                name = training_run,
                epochs = training_epochs)


#%% command line driver

def main():

    # command line arguments
    parser = argparse.ArgumentParser(description = "Minimal YOLO11 model training with custom data.")
    parser.add_argument("--yolo_model",
                        type = str,
                        default = "yolo11n.pt",
                        help = "YOLO model version to use as starting point for training; default: 'yolo11n.pt'")
    parser.add_argument("--training_epochs",
                        type = int,
                        default = 100,
                        help = "number of training epochs; default: 100")
    parser.add_argument("yolo_project_dir",
                        type = str,
                        help = "absulote path to YOLO project directory containing dataset.yml")
    args = parser.parse_args()

    # standardize path variable
    args.yolo_project_dir = os.path.normpath(args.yolo_project_dir)

    # output path variables
    yolo_config = os.path.join(args.yolo_project_dir, "dataset.yml") # follows naming convention of convert_bbox_to_yolo_format.py
    training_run = "_".join([args.yolo_model.split(".")[0], str(args.training_epochs) + "epochs"])

    # model training
    train_yolo(args.yolo_model, yolo_config, args.yolo_project_dir, training_run, args.training_epochs)

if __name__ == "__main__":
    main()
    
    







