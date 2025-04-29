---
title: PhotoApp Query
---

When opening the PhotoDB web interface PhotoApp, you first need to specify a set of images to display. This is done in the `Query`tab.

Image sequences can be specified by filtering by camera location and date. Implementation of image filtering according to the image directory's structure given as `original_path_keys` in the project configuration file [`config.yaml`](/photodb_documentation/configuration/PhotoDB.html) is planned. Alternatively, images sequences may be specified by supplying [`review_lists`](/photodb_documentation/usage/review_lists.html).

## Query

*A custom image sequence is specified.*

Images are filtered by `location` and `date`. One day in time is selected. Days that contain images at the specified location are marked with black text, days that contain images at some locations, but not at the currently selected location are marked with grey text.

Planned feature:  
Keys supplied in [`config.yaml`](/photodb_documentation/configuration/photodb.html) as **original_path_keys** may be used to filter images, creating customized image subsets.

### Example:

In the given example images are stored according to the location  of the camera and the date of capturing:

directory:
```bash
photo_meta
├─── Germany
│    |─── 20240430
|    |    └─── image.jpg 
|    └─── 20240429
└─── France
     |─── 20240430
     └─── 20240429
```

In the query tab images can be filtered by location / date using drop down menus:

<img src="/photodb_documentation/assets/PhotoApp_query_query.png" alt="PhotoApp Query Query" width="auto" height="300" align="center">

## Review list

*A review list is a stored image sequence. A review list set is a collection of image sequences.*

### Review lists from files

Review lists can be loaded from files.  
*See [review lists](/photodb_documentation/usage/review_lists.html)*.  
Review lists can be selected from the drop down menu in the query / review panel. The available review lists can be viewed and selected, structured by review list sets reflecting file system folder structure.

<img src="/photodb_documentation/assets/PhotoApp_query_reviewlist.png" alt="PhotoApp Query Review" width="auto" height="300" align="center">

### Review lists from generation

A click on the round **manage image list sets button** on the right opens the manage image list sets dialog box.

The currently created review list sets are listed.

A click on the **regenerated lists of selected sets button** recreates selected sets to update for changes in the image archive, e.g. newly added images.

A click on the **remove selected sets button** deletes selected sets.

A click on the **add new review list set button** opens a dialog box to specify a new review list set. The dialog box contains controls to type the name of the review list set, to filter images by classifier and thresholds, to group sequences by classifier, to exclude already reviewed images and to sort images by classification confidence.

## Image sequence

At the bottom of the page the count of images of the current image sequence is shown.

To view the selected image sequence move on to the [**browser**-page](/photodb_documentation/usage/photoapp_browser.html) by click on the browser-entry on the left side panel.
