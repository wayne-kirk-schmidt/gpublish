Google Publish
==============

These command line tools are wrappers aorund the Google Drive API to help DevOps.

In this toolbox we have tools to download, upload, move files as well as convert formats.

As this repository grows, we will add more DevOps friendly tools handle single tasks.

Installing the Project
======================

All of these scripts are command line based, designed to be used within a batch script or DevOPs tool.
The complete list of the python modules are listed in a Pipfile for install.

You will need to use Python 3.6 or higher and the modules listed in the dependency section.  

The steps are as follows: 

    1. Install python 3.6 or higher from python.org. Append python3 to the LIB and PATH env.

    2. Download and install git for your platform if you don't already have it installed.
       It can be downloaded from https://git-scm.com/downloads
    
    3. Open a new shell/command prompt, so it will reflect the new python path configured in step 1.
       cd to the folder where you want to install the scripts.
    
    4. Execute the following command to install pipenv, which will manage all of the library dependencies:
    
        sudo -H pip3 install pipenv 
 
    5. Clone this repository. This will create a new folder

    6. Change into the folder. Type the following to install all the package dependencies 
       (this may take a while as this will download all of the libraries that it uses):

        pipenv install
        
Getting this set up
===================

    1. The first thing to do is to enable the Google Drive API

[Enable-Google-Drive-API](https://developers.google.com/drive/api/v3/enable-drive-api)

    2. The next thing to do is to configure the quickstart for the Google Drive API

[Google-Drive-Quickstart](https://developers.google.com/drive/api/v3/quickstart/python)

    3. Then you will run the quickstart python script providing two arguments

       * CREDENTIALS file - this is the credentials set up for the account

       * TOKENPICKLE file - the file where the session token is stored and refreshed

CAUTION: Please note that the SCOPE is for the Gdrive which means read and write access.

[Specific Google Setup Steps](https://github.com/wks-sumo-logic/gpublish/blob/master/doc/GSETUP.md)

IMPORTANT: Please follow all of the steps in the above instructions to setup the google credentials.

Quicksttart Script Usage
========================

prompt> quickstart.py /path/where/secret/is/read/from/credentials.json /path/where/token/is/written/token.pickle

GPublish Script Usage
========================

* to show the help screen

prompt> gpublish.py -h

* to publish to your google drive

prompt> gpublish.py -t /tmp/token.pickle -c /tmp/credentials.json -f /tmp/file_to_publish.pptx -d MyTest-Directory

* to publish to your google drive verbosely

prompt> gpublish.py -t /tmp/token.pickle -c /tmp/credentials.json -f /tmp/file_to_publish.pptx -d MyTest-Directory -v

Dependencies
============

See the contents of "pipfile"

Script Names and Purposes
=========================

Scripts and Functions:

    1. gpublish - this is the first script combining upload, download, and file conversion

    2. mymimetypes - this is a helper file containing mapping for mime types used by gpublish

    3. quickstart - this is the boot strapper for confirming credentials and storing tokens

To Do List:
===========

* Extend more scripts to include discrete functions

* Extend the mime type support

* Build the tools into a subject verb object format

License
=======

Copyright 2020, 2022 Wayne Kirk Schmidt
https://www.linkedin.com/in/waynekirkschmidt

Licensed under the Apache 2.0 License (the "License");

You may not use this file except in compliance with the License.
You may obtain a copy of the License at

    license-name   APACHE 2.0
    license-url    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Support
=======

Feel free to e-mail me with issues to: 

wayne.kirk.schmidt@gmail.com

I will provide "best effort" fixes and extend the scripts.
