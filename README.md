# Google Drive Folder Upload and Link Generator

![](https://github.com/krum04/Google-Drive-Folder-Uploader/blob/master/images/Gui.PNG?raw=true)

## Overview

This script will take load take local folder and upload it to a specified folder in Google Drive. When finished, a CSV with the file name and share link is generated and saved in the local source folder. 

## Requirements

* [PyDrive](https://pypi.org/project/PyDrive/)
* client_secrets.json generated from Google Developer API

## Setup and Run

Place your client_secrets.json in the work folder and run the GdriveUpload.py script.

## To Do

* Add error handling
* Add support for recursive folder
* Add command line script