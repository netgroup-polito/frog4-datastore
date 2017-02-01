# Datastore service for NF images and templates, NF-FG, and more

This project defines some minimal code needed to start a server storing information exploited by the FROG v.4:
* NF template: file that describes the characteristics of the network function, such as the its capapbility (e.g., firewall, NAT), required resources (e.g., amount of CPU, amount of memory), required execution environment (e.g., KVM hypervisor, Docker, etc), number and type of virtual interfaces, and more. Examples of templates, which have to follow a proper [schema](https://github.com/netgroup-polito/vnf-template-library/blob/master/schema.json), are available in [sample-templates](./sample-templates);
* NF image: raw image of the NF (e.g, VM disk, archive file). In some cases the NF image is stored directly in this server; in other cases it is stored in a different backend (e.g., OpenStack Glance);
* NF-FG: file that describes a network functions forwaring graph, written according to a proper [schema](https://github.com/netgroup-polito/nffg-library/blob/master/schema.json).
* YANG model: schema used to validate the configuration forwarded to the VNF by means of the configuration service
* YIN model: it is the JSON representation of a YANG model, it is used by the GUI in order to provide the users a simple interface for the management of their services

Moreover it provides a configuration service exploited by FROG v4 in order to retrieve/push configuration from/into VNFs

## How to configure the datastore

	sudo apt-get install mysql-server libmysqlclient-dev libffi-dev python-virtualenv

This server requires a backend database to store the information.

To create and initialize the SQL database:

	mysql -u root -p
        mysql> CREATE DATABASE frog4_datastore;
        mysql> GRANT ALL PRIVILEGES ON frog4_datastore.* TO 'datastore'@'localhost' \
            IDENTIFIED BY 'datastorePWD';
        mysql> GRANT ALL PRIVILEGES ON frog4_datastore.* TO 'datastore'@'%' \
            IDENTIFIED BY 'datastorePWD';
        mysql> exit

## How to execute the datastore

Creating a private environment in which we run Django 1.8; unfortunately API changed in 1.9, hence it is better to use this specific version only in our project and start the server:

### First time

	$ cd [frog4-datastore]
	$ virtualenv .env
	$ source .env/bin/activate
	$ pip install django==1.8.2 djangorestframework MySQL-python django-rest-swagger==0.3.5 django-chunked-upload django-cors-headers wrapt bcrypt pyang xmltodict
	$ python manage.py makemigrations datastore
	$ python manage.py migrate
	$ python manage.py runserver --d datastore_config.ini [uses config/default-config.ini if '--d' is missing]

### Next times 

	$ cd [frog4-datastore]
	$ source .env/bin/activate
	$ python manage.py runserver --d datastore_config.ini [uses config/default-config.ini if '--d' is missing]

## How to interact with the datastore

A description of the API exposed by the datastore is available at the URL: *ip_address:port/docs*

## How to clear uncompleted uploads

It is also included a management command in order to clear uncompleted NF image uploads which has expired, both from the datastore's DB and from disk. You can set how long (in hours) an upload is valid after its creation in the configuration file of the datastore (i.e. ``deafault-config.ini``) by means of the variable ``upload_expiration_hrs``.
 
You can launch the command manually from your virtual environment like this:

    python manage.py delete_expired_uploads

You can also set a cron-job:

    crontab -e

Add this line and save:

    */60 * * * * cd [frog4-datastore] && .env/bin/python manage.py delete_expired_uploads > /dev/null 2>&1

Change ``[frog4-datastore]`` with the full path where the datastore is located (i.e. /home/user/frog4-datastore).

You can verify if your cron-job is installed with the command

    crontab -l
