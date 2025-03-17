# PhotoDB Configuration

All application settings are in the YAML file `config.yaml`.

Here, you configure your own PhotoDB instance. To configure a PhotoDB project you need to specifiy *project*, *root_path*, *root_data_path*, *classification_definition_csv*, and *review_list_path*.

A `config.yaml`file for a local PhotoDB instance (without [server configuration](config.md)) may look like this:

`config.yaml` example:
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

# PhotoDB project configuration YAML properties

**project**

Name of the project, e.g. shown at the top panel at PhotoApp web-interface:
```yaml
project: my_photo_project
```
---

**root_path**

Root directory containing project metadata files.

Relative to application root folder:
```yaml
root_path: 'photo_meta'
```
---

**root_data_path**

Root directory containing project image files. If not set, image files are expected to be in same folder as metadata files of `root_path`.

Folder relative to application root folder:
```yaml
root_data_path: 'photo_data'
```
---

**classification_definition_csv**

List of classification names as CSV file, i.e. classes to be annotated.

File relative to application folder:
```yaml
classification_definition_csv: photo_classification_definitions.csv
```
*See [classification definitions](classification_definition.md)*.

---

**review_list_path**

Root directory containing project review list files.

Folder relative to application folder:
```yaml
review_list_path: 'photo_review_lists'
```
*See [review lists](review_lists.md)*.

---

**original_path_keys**

Description of directory sturcture within photo_data root directory.

When creating metadata files with [photo_create_yaml task](photodb_tasks.md) path elements are saved as list "original_path". The keys supplied here are mapped to the elements of original_path and written to the metadata file as key/value pairs.

The following keys will be ignored:  
' ', '*', '_', 'PhotoSens', 'original_path', 'file', 'file_size', 'log' 

original_path_keys and original_path are not neccessaryly of the same length (see example 2).  
Use '_' to skip a key (see example 3).

example 1:

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

example 2:

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
example 3:

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