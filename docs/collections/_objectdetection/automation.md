---
title: Automatically Process Incoming Images
---

If you have a continous data influx you may want to analyse incoming images regularly, e.g., running a script in the background that periodically invokes your processing scripts. Here, we show you how to use external scripts that access the image data and metadata maintained by PhotoBD, invoke an external model using this data, and finally write the results back into the PhotoDB metadata.

### Example Processing Scripts

#### Initial Metadata Generation
```R
if(!require('yaml')) install.packages('yaml')

photosens_write_yaml <- function(meta, path) {
  yaml::write_yaml(meta, file = path, precision = 11)
}

image_root_path <- 'archive_photo/'
meta_root_path  <- 'archive_meta/'

image_files <- list.files(image_root_path, pattern = '*.(JPG|jpg)$', recursive = TRUE, full.names = FALSE)

for(image_file in image_files) {
  # images and metadata files are stored in parallel
  # metadata file names: image_file_name.ext.yaml
  image_file_path <- file.path(image_root_path, image_file)
  meta_file_path <- file.path(meta_root_path, paste0(image_file, '.yaml'))
  
  if(file.exists(meta_file_path)) {
    cat(paste0('Skip existing  ', meta_file_path, '\n'))
  } else {
    filename <- basename(image_file)
    timetext <- substring(filename, 2, 13) # example: filename contains timestamp
    timestamp <- format(as.POSIXlt(timetext, format='%y%m%d%H%M%S'), format='%Y-%m-%dT%H:%M:%S')
    meta <- list(PhotoSens='v1.0')
    meta$file <- filename
    meta$date = timestamp        
    meta$log = list()
    meta$log = c(meta$log, list(list(action='create yaml', date=format(as.POSIXlt(Sys.time()), format='%Y-%m-%dT%H:%M:%S'))))
    dir.create(dirname(meta_file_path), showWarnings = FALSE, recursive = TRUE)
    photosens_write_yaml(meta, meta_file_path)
    cat(paste0('Created  ', meta_file_path, '\n'))
  }
}
```

#### Invoke Megadetector and Mark Images Containing People

```R
if(!require('tools')) install.packages('tools')
if(!require('reticulate')) install.packages('reticulate')
if(!require('rjson')) install.packages('rjson')

photosens_write_yaml <- function(meta, path) {
  yaml::write_yaml(meta, file = path, precision = 11)
}

source_image_root_path <- 'archive_photo/'
source_meta_root_path  <- 'archive_meta/'

megadetector_script_path  <- 'run_detector_batch.py'  # download from MegaDetector repository
megadetector_model_path   <- 'md_v5a.0.0.pt'          # download from MegaDetector repository
megadetector_result_path  <- 'mdresult.json'

meta_files <- list.files(source_meta_root_path, pattern = '*.yaml$', recursive = TRUE, full.names = FALSE)

for(meta_file in meta_files) {
  # images and metadata files are stored in parallel
  # metadata file names: image_file_name.ext.yaml
  image_file_path <- file.path(source_meta_root_path, tools::file_path_sans_ext(meta_file))
  meta_file_path <- file.path(source_image_root_path, meta_file)

  arguments <- c(megadetector_model_path, image_file_path, megadetector_result_path, '--quiet')
  command <- paste0("import sys; ", "sys.argv = ['", megadetector_script_path, "', '", paste(arguments, collapse = "', '"), "']; ", "exec(open('", megadetector_script_path, "').read())")
  reticulate::py_run_string(command)
        
  megadetector_result_file <- rjson::fromJSON(file = megadetector_result_path)
  contains_person <- any(sapply(megadetector_result_file$images[[1]]$detections, function(det) det[['category']] == '2' && det[['conf']] >= 0.7))
  
  meta_data <- yaml::yaml.load_file(meta_file_path)
  meta_data$log[[2]] <- list(
    action='run MegaDetector',
    date=format(as.POSIXlt(Sys.time()), format='%Y-%m-%dT%H:%M:%S'),
    contains_person=contains_person
    )
  photosens_write_yaml(meta_data, source_meta_file_path)

  file.remove(megadetector_result_path)
}
```

### Example Background Script

```bash
#!/bin/bash

for i in {1..1000000} # long-running but not infinite loop
do
  # safe loop exit: delete this file to stop loop after current iteration
  if [ ! -f textfile.txt ]; then
  echo "File not found: textfile.txt!"
  exit 1
  fi

  echo "step $i: start processing scripts..."

  Rscript initial_yaml_generation.R
  Rscript invoke_megadetector_and_mark_people.R

  echo "step $i: Sleep 15 min. "
  sleep 450  # 450 seconds = 15 minutes
done

```

## How it works

The backrgpound scripts runs continously and iterates over 3 streps:

1. **execute initial_yaml_generation.R**: lists image files in root data path and generates a YAML metadata file for each image

2. **execute invoke_megadetector_and_mark_people.R**: invokes MegaDetector on each image file (creating a json results file), reads the resulting json file, defines booean denoting presence/absence of human detections, and writes this result into PhotoDB YAML metadata file

3. **wait 15 minutes** before starting with next iteration

## Example modificatios of this workflow

* write detection bounding boxes into YAML files

* use a different model

* add processing more processing steps after detecting humans, e.g. blurring humans for privacy reasons