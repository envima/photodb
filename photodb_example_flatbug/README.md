# PhotoDB Example with Flatbug Dataset

[Svenning, A., Mougeot, G., Alison, J., Chevalier, D., Molina, N.L.C., Ong, S.-Q., Bjerge, K., Carrillo, J., Hoeye, T.T., Geissmann, Q., 2025. A General Method for Detection and Segmentation of Terrestrial Arthropods in Images.](Svenning_2025_flatbug.pdf)

flatbug dataset [download link](https://www.doi.org/10.5281/zenodo.14761447)

This is an example PhotoDB setup using the flatbug dataset.

## Setup the Flatbug PhotoDB Instance

1. Download and unpack the [``database/``](database) folder. This is your PhotoDB instance.  

This folder includes the PhotoDB source code and utility files / folders as well as:

### ``photo_data/``

This is where image data should be stored in this example. To do so:

2.  Download the [flatbug dataset](https://www.doi.org/10.5281/zenodo.14761447) and save the unzipped dataset in the ``photo_data/`` folder within your PhotoDB instance.  
Your folder structure should look like this:  
```shell
database
    |-- photo_data
            |-- flatbug_dataset
                    |-- abram2023
                    |-- ALUS
                    |-- amarathunga2022
                    ...
    ...
```
You have now saved the flatbug image data in parallel to the already instantiated metadata (stored in ``photo_meta/``).

### ``photo_meta/``

This is where YAML metadata files are stored in this example. Here, we have already instantiated the metadata files (see [documentation | tasks](https://envima.github.io/photodb/usage/tasks.html)) and populated them with the flatbug detections, using the [``flatbug_json_to_yaml.ipynb``](flatbug_json_to_yaml.ipynb) notebook.

### ``config.yaml``

This file contains the configuration of this PhotoDB instance, e.g., data / metadata storage location, project name, etc. (see [documentation | configuration](https://envima.github.io/photodb/_pages/configuration.html)).

### ``photo_classification_definitions.csv``

This file contains annotation classes used in the web interface PhotoApp (see [documentation | classification definition](https://envima.github.io/photodb/usage/classification_definition.html)).

### ``win_audio.cmd``

3. Execute this file to start the application.

**You can now open the web interface in a browser at http://127.0.0.1:8080/ (see [documentation | operating](https://envima.github.io/photodb/operating/operating_windows.html)), e.g., to inspect, correct, or add additional annotations.**






