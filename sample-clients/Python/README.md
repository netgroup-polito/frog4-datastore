This folder contains `client.py`, a library that can be exploited by a client to 
interact with the datastore to:
* upload/get/delete network functions templates
* delete network functions images

The file `example.py` is instead a minimal client that can be used to test the 
datastore functionalities. Particularly, it uploads the template provided through
command line.

`python client.py switch.json`

where `switch.json` is a template of a L2-switch available in this folder.
