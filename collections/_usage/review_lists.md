---
title: Review lists
--- 

Apart from directly traversing the project photo archive according to folder structure, **review lists** allow to traverse a subset of images in sequential order. One review list contains a list of photo entries to traverse.

This can for example be used to supply a set of images intended to be used as model training data, i.e. images that have to be manually annotated. Similarly, one might want to browse through images containing a certain object; By extracting detection info from the metadata one could construct a list of all the images containig this object. Supplying this list as review list then allows the user to easily visually inspect the given images.

Review lists should all be saved into a single directory. This directory is given as `review_list_path` in the project configuration file `config.yaml`, e.g.:

```yaml
review_list_path: photo_review_lists
```

You may store any number of review list files in this directory.

The review list files are in **CSV format** with comma separated columns. Currently they should contain only one column, called `path`. This column stores filepaths pointing to individual images. Filepaths must be relative to the image root directiry `root_data_path`.

The review list folder may contain a CSV file `manual_label_list.csv` e.g:

```CSV
path
photo2_20220101_020101.jpg
photo4_20220101_040101.jpg
```

To **disable a line** in the CSV file set the `#` character at the beginning of a line to comment out that line.

The CSV file name is the name of that review list, without the `.csv` extension.