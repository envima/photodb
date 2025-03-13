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