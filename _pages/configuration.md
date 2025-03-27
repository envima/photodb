---
title: PhotoDB configuration
sidebar:
  nav: configuration
---

PhotoDB can and must be individually configured to your own specific needs. For this, a YAML file called `config.yaml` is used. Open the `config.yaml` file located in the PhotoDB root directory to see what a PhotoDB configuration file might look like.

In the next chapters, you will learn how to adapt this file to setup your very own local or global PhotoDB instance.

**NOTE**: PhotoDB is meant to be used as a collaborative tool that can be acessed via the internet. For this purpose you need to configure some [server](/photodb_documentation/configuration/server.html) and [HTTP(S)](/photodb_documentation/configuration/https.html) settings, that cannot be explained in detail in this manual.  
Alternatively, PhotoDB can be set up locally, e.g., to get a first impression of the software.  
You may skip [server](/photodb_documentation/configuration/server.html) and [HTTP(S)](/photodb_documentation/configuration/https.html) configuration if you just want so set up a local instance, but you always need to configure [basic PhotoDB settings](/photodb_documentation/configuration/PhotoDB.html).