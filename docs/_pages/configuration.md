---
title: PhotoDB / AudioDB configuration
sidebar:
  nav: configuration
---

PhotoDB / AudioDB can and must be individually configured to your own specific needs. For this, a YAML file called `config.yaml` is used. Open the `config.yaml` file located in the application root directory to see what a PhotoDB / AudioDB configuration file might look like.

In the next chapters, you will learn how to adapt this file to setup your very own local or global PhotoDB / AudioDB instance.

**If you only want to use one of the two platforms you can skip the configuration of the other platform.**

**NOTE**: PhotoDB / AudioDB is meant to be used as a collaborative tool that can be acessed via the internet. For this purpose you need to configure some [server](/photodb/configuration/server.html) and [HTTP(S)](/photodb/configuration/https.html) settings, that cannot be explained in detail in this manual.  
Alternatively, PhotoDB / AudioDB can be set up locally, e.g., to get a first impression of the software.  
You may skip [server](/photodb/configuration/server.html) and [HTTP(S)](/photodb/configuration/https.html) configuration if you just want so set up a local instance, but you always need to configure the basic settings of [PhotoDB](/photodb/configuration/PhotoDB.html) / [AudioDB](/photodb/configuration/AudioDB.html).
