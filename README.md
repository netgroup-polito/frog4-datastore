# FROGv4 Datastore service

This project defines some minimal code needed to start a server that stores most of the information required by the FROG v.4 architecture:
  * **NF template**: file that describes the characteristics of the network function, such as the its capapbility (e.g., firewall, NAT), required resources (e.g., amount of CPU, amount of memory), required execution environment (e.g., KVM hypervisor, Docker, etc), number and type of virtual interfaces, and more. Examples of templates, which have to follow a proper [schema](https://github.com/netgroup-polito/vnf-template-library/blob/master/schema.json), are available in [sample-templates](./sample-templates);
  * **NF Capability**: list of all the functional capabilities supported by the FROG v.4 architecture. Such a list is updated each time a template with a new capability is uploaded into the datastore. 
  * **NF image**: raw image of the NF (e.g, VM disk, archive file). The NF image can be installed either directly in the Datastore, or in a different backend (e.g., OpenStack Glance);
  * **NF-FG**: file that describes a network functions forwaring graph, written according to a proper [schema](https://github.com/netgroup-polito/nffg-library/blob/master/schema.json).
  * **YANG model**: schema used to validate the configuration forwarded to the VNF by means of the configuration service
  * **YIN model**: JSON representation of a YANG model, it is used by the GUI in order to provide the users a simple interface for the management of their services
  * **User**: stores all the user information (username, password and broker keys). Moreover, the datastore provides a rudimental authentication service that can be exploited by all the FROG v.4 architecture components.
  * **VNF Configuration**: configuration that will be loaded into a VNF at booting time
  * **Active VNF**: stores information of the VNF that are currently active (instance ID, bootstrap configuration and REST endpoint that can be used in order to configure the VNF)
  
[here](https://github.com/netgroup-polito/frog4-datastore/blob/conf-orch-db/images/ER_model_datastore.pdf) can be found the ER model of the datastore.


## How to install the Datastore dependencies and setup the SQL database

	sudo apt-get install mysql-server libmysqlclient-dev libffi-dev python-virtualenv python-pip libpython2.7-dev
	
During the installation process, you have to chose the *root* password for the SQL database on the machine where you are going to install/create the Datastore.

The [script](https://github.com/netgroup-polito/frog4-datastore/blob/conf-orch-db/script/mysql_script.sql) creates and initializes the SQL database:

	cd [frog4-datastore]
	mysql -u root -p
        mysql> source script/mysql_script.sql
	
inside the script, `datastore` and `datastorePWD` can be replaced respectively by the username and the password that the Datastore will use to access to the SQL database. In case you change them, you have also to edit these [two lines](https://github.com/netgroup-polito/frog4-datastore/blob/master/datastore_main/settings.py#L71-L72) in the python code.

## Retrieve the code

Now you have to clone this repository and all the submodules using the following command:

   	$ git clone https://github.com/netgroup-polito/frog4-datastore
	$ cd frog4-datastore
	$ git submodule init && git submodule update
    

## How to execute the Datastore

### Datastore configuration file

In order to properly configure the Datastore, edit its [configuration file](https://github.com/netgroup-polito/frog4-datastore/blob/master/config/default-config.ini). Particularly, in this file you have to set the TCP port to be used to interact with the Datastore through its REST API.

### Run it!

Creating a private environment in which we run Django 1.8; unfortunately API changed in 1.9, hence it is better to use this specific version only in our project and start the server:

#### First time

	$ cd [frog4-datastore]
	$ virtualenv .env
	$ source .env/bin/activate
	$ pip install django==1.8.2 djangorestframework MySQL-python django-rest-swagger==0.3.5 django-chunked-upload django-cors-headers wrapt bcrypt pyang xmltodict jsonschema
	$ python manage.py makemigrations datastore
	$ python manage.py migrate
	$ python manage.py runserver [--d datastore_config.ini] 

#### Next times 

	$ cd [frog4-datastore]
	$ source .env/bin/activate
	$ python manage.py runserver [--d datastore_config.ini]

## How to interact with the datastore

A description of the API exposed by the datastore is available at the URL: `ip_address:port/docs` (e.g., `127.0.0.1:8081/docs`).

## How to clear uncompleted uploads

It is also included a management command in order to clear uncompleted NF image uploads which has expired, both from the datastore's DB and from disk. You can set how long (in hours) an upload is valid after its creation in the configuration file of the datastore (i.e. ``deafault-config.ini``) by means of the variable ``upload_expiration_hrs``.
 
You can launch the command manually from your virtual environment like this:

    $ python manage.py delete_expired_uploads

You can also set a cron-job:

    crontab -e

Add this line and save:

    */60 * * * * cd [frog4-datastore] && .env/bin/python manage.py delete_expired_uploads > /dev/null 2>&1

Change ``[frog4-datastore]`` with the full path where the datastore is located (i.e. /home/user/frog4-datastore).

You can verify if your cron-job is installed with the command

    crontab -l
