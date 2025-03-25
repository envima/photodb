---
title: Classification definitions
---

The PhotoDB web interface, PhotoApp can be used as an annotation tool. For a detailed explanation of this functionility see [PhotoApp Viewer](../_usage/photoapp_viewer.md).

During annotation a list of possible classification labels, i.e., classes, can be specified. These predefined classes can then be selected effortlessly by the during annotation. This  prevents having different notations of the same object in the metadata, which might happen when users type the labels themselves.  
If an object is not in the predefined classification list, it is always possible for the users to type the label themselves.

The classification definition is supplied as a csv file. This file is given as `classification_definition_csv` in the project configuration file `config.yaml`, e.g.:

```yaml
classification_definition_csv: photo_classification_definitions.csv
```

Inside the `photo_classification_definitions.csv` file, class names and descriptions are supplied, e.g.:

```CSV
#comment
name,description
incorrect box, Box does not mark (correctly) an object.
person, Photo will be locked. (DSGVO)
animal, unspecified animal
Kleintier, unbestimmt
Großtier, unbestimmt
Katze, generisch
Hauskatze, Felis catus
Wildkatze, Felis silvestris silvestris
#Hirsch, generisch
Wildschwein, Sus scrofa
Waschbaer, Procyon lotor
```

The classification definition file is in **CSV format** with comma separated columns `name` and `description`.

`name` will be used as classification label that can be set at the web-interface, and that is stored in the photo meta data. Short names are recommended.

`description` specifies the exact meaning of `name`. It is shown at the web-interface classification label selection control as descriptive annotation.

To **disable a line** in the CSV file set the `#` character at the beginning of a line to comment out that line.