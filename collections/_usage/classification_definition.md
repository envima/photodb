---
title: Classification definitions
---

The PhotoDB web interface, PhotoApp can be used as an annotation tool. For a detailed explanation of this functionility see [PhotoApp Viewer](/photodb_documentation/usage/photoapp_viewer.html).

During annotation a list of possible classification labels, i.e., classes, can be specified. These predefined classes can then be selected effortlessly by the user during annotation. This  prevents having different notations of the same object in the metadata, which might happen when users type the labels themselves.  
If an object is not in the predefined classification list, it is always possible for the users to type the label themselves during annotation.

The classification definition is supplied as a csv file. This file is given as `classification_definition_csv` in the project configuration file `config.yaml`, e.g.:

```yaml
classification_definition_csv: photo_classification_definitions.csv
```

Inside the `photo_classification_definitions.csv` file, class names and descriptions are supplied, e.g.:

```CSV
#comment
name,description
branch, singular oak branch
leaf, singular oak leafs
herbivory, visible inner leaf damage
newflush, newly developed leaf flush
crp, color reference panel
oak1, top left potted plant
oak2, top middle potted plant
oak3, top right potted plant
oak4, bottom left potted plant
oak5, bottom middle potted plant
oak6, bottom right potted plant
```

During annotation these classes can be selected from a drop-down menu:

<img src="/photodb_documentation/assets/PhotoApp_classificationdefinition.png" alt="PhotoApp classification definition drop down menu" width="auto" height="300" align="center">

The classification definition file is in **CSV format** with comma separated columns `name` and `description`.

`name` will be used as classification label that can be set at the web-interface, and that is stored in the photo meta data. Short names are recommended.

`description` specifies the exact meaning of `name`. It is shown at the web-interface classification label selection control as descriptive annotation.

To **disable a line** in the CSV file set the `#` character at the beginning of a line to comment out that line.