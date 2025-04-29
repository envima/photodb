---
title: PhotoDB Project Configuration
---

In PhotoDB you will set up so-called `projects`. A `project` my coincide with a study. Within a `project` you need to specify the directory your image data is stored in and the directory the corresponding metadata shall be stored in. You can also use PhotoDB as an annotation tool, i.e., you may draw and label bounding boxes with the PhotoDB web application, PhotoApp. To this end, you may specify class names and image subsets that shall be annotated. Lastly, PhotoDB allows you to set your own folder structure to store your image data. You simply need to pass whatever folder structure you choose to PhotoDB.

All of this is specified in the `config.yaml` file using the following keys: *project*, *root_path*, *root_data_path*, *classification_definition_csv*, *review_list_path*, and *original_project_keys*.

See below for examples and a detailed explanation of each key.

A `config.yaml` file for a local PhotoDB instance (without [server](server.html) and [HTTPS](https.html) configuration) may look like this:

#### `config.yaml` example:

```yaml
login: true
http_port: 8080
    
photo:
  projects:

  - project: my_photo_project
    root_path: 'photo_meta'
    root_data_path: 'photo_data'
    classification_definition_csv: photo_classification_definitions.csv
    review_list_path: 'photo_review_lists'
    original_project_keys: ['location', 'category']
```

## PhotoDB project configuration YAML properties

### project

Name of the project, e.g. shown at the top panel at PhotoApp web-interface:
```yaml
project: my_photo_project
```
---

### root_path

Root directory containing project metadata files.

Relative to application root folder:
```yaml
root_path: 'photo_meta'
```
---

### root_data_path

Root directory containing project image files. If not set, image files are expected to be in same folder as metadata files of `root_path`.

Folder relative to application root folder:
```yaml
root_data_path: 'photo_data'
```
---

### classification_definition_csv

List of classification names as CSV file, i.e. classes to be annotated.

File relative to application folder:
```yaml
classification_definition_csv: photo_classification_definitions.csv
```
*See [classification definitions](/photodb_documentation/usage/classification_definition.html)*.

---

### review_list_path

Root directory containing project review list files. Directory may be empty if you don't have any review lists.

Folder relative to application folder:
```yaml
review_list_path: 'photo_review_lists'
```
*See [review lists](/photodb_documentation/usage/review_lists.html)*.

---

### original_path_keys

Description of directory sturcture within photo_data root directory.

When creating metadata files with [photo_create_yaml task](/photodb_documentation/usage/tasks.html) path elements are saved as list "original_path". The keys supplied here are mapped to the elements of original_path and written to the metadata file as key/value pairs.

The following keys will be ignored:  
' ', '*', '_', 'PhotoSens', 'original_path', 'file', 'file_size', 'log' 

original_path_keys and original_path are not neccessaryly of the same length (see example 2).  
Use '_' to skip a key (see example 3).

#### example 1: full path is specified

directory:
```bash
photo_meta
├─── loc1
│    |─── forest
|    |    └─── image.jpg 
|    └─── meadow
└─── loc2
     |─── forest
     └─── meadow
```
`config.yaml`:
```yaml
...
  original_path_keys: ['location', 'category']
```
`image.jpg.yaml`:
```yaml
...
original_path: [loc1, forest]
...
location: loc1
category: forest
...
```

#### example 2: path is partly omitted

directory:
```bash
photo_meta
├─── control
│    |─── Haematopota_pluvialis
|    |    |─── mitochondria
|    |    |    └─── image.jpg  
|    |    └─── ribosome
|    └─── Stomoxys_calcitrans
|         ...
└─── treatment
     ...
```
`config.yaml`:
```yaml
...
  original_path_keys: ['experimental_group', 'species']
```
`image.jpg.yaml`:
```yaml
...
original_path: [control, Haematopota_pluvialis, mitochondria]
...
experimental_group: control
species: Haematopota_pluvialis
...
```
#### example 3: skip specific part of path

directory:
```bash
photo_meta
├─── France
│    |─── Paris
|    |    |─── buildings
|    |    |    └─── image.jpg  
|    |    └─── parks
|    └─── Bordeaux
|         ..
└─── Germany
     ..
```
`config.yaml`:
```yaml
...
  original_path_keys: ['_', 'city', 'category']
```
`image.jpg.yaml`:
```yaml
...
original_path: [France, Paris, buildings]
...
city: Paris
category: buildings
...
```