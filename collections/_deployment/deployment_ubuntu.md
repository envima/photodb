---
title: Deployment on Ubuntu
---

## Prerequesite: Java 11

Install Java 11 or newer, e.g.:

```bash
sudo apt update
sudo apt install openjdk-11-jdk
java -version
```

## Download Latest Release

PhotoDB / AudioDB release packages are found on [GitHub](https://github.com/Nature40/audiodb/releases). Download the latest package using [this download link](https://github.com/Nature40/audiodb/releases/latest/download/package.zip).

After downloading the latest distribution package, change into the directory you downloaded PhotoDB into:

```bash
cd path/to/distribution/package/ # replace with actual path!
```

Then extract it and make it executable:

```bash
unzip *.zip
chmod +x *.sh
```

The distribution package includes some example files, that we will have a look at later on.