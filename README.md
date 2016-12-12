# Datastore service for NF images and templates, NF-FG, and more

This project defines some minimal code needed to start a server storing information exploited by the FROG v.4:
* NF template: file that describes the characteristics of the network function, such as the implemented function (e.g., firewall, NAT, etc), required resources (e.g.,  CPU, memory), required environment (e.g., KVM hypervisor, Docker, etc), and more (e.g., number and type of virtual interfaces, etc). Examples of templates, which have to follow a proper [schema](https://github.com/netgroup-polito/vnf-template-library/schema.json), are available in [sample-templates](./sample-templates);
* NF image: raw image of the NF (e.g, VM disk, archive file). In some cases the NF image is stored directly from this server; in other cases it is stored in a different backend (e.g., OpenStack Glance);
* NF-FG: file that describes a network functions forwaring graph, written according to a proper [schema](https://github.com/netgroup-polito/nffg-library/schema.json).

## How to configure the datastore

	sudo apt-get install mysql-server libmysqlclient-dev libffi-dev python-virtualenv
	
This server requires a backend database to store the information.

To create and initialize the SQL database:

	mysql -u root -p
        mysql> CREATE DATABASE VNF_repository;
        mysql> GRANT ALL PRIVILEGES ON VNF_repository.* TO 'vnfRepo'@'localhost' \
            IDENTIFIED BY 'vnfPass';
        mysql> GRANT ALL PRIVILEGES ON VNF_repository.* TO 'vnfRepo'@'%' \
            IDENTIFIED BY 'vnfPass';
        mysql> exit

## How to execute the datastore

Creating a private environment in which we run Django 1.8; unfortunately API changed in 1.9, hence it is better to use this specific version only in our project and start the server:

	$ cd [frog4-datastore]
	$ virtualenv .env
	$ source .env/bin/activate
	$ pip install django==1.8.2 djangorestframework MySQL-python django-rest-swagger==0.3.5 django-chunked-upload django-cors-headers wrapt bcrypt
	$ python manage.py makemigrations VNF
	$ python manage.py migrate
	$ python manage.py runserver --d VNF_ServiceConfig.ini [uses config/default-config.ini if '--d' is missing]

## How to interact with the datastore

A description of the API exposed by the datastore is available at the URL: *ip_address:port/docs*

## How to clear expired uploads
In the project is included also a management command in order to clear uncompleted expired uploads, both from the repository database and from disk. You can set how long (in hours) an upload is valid after its creation in the configuration file of the repository (i.e. ``deafault-config.ini``) by means of the variable ``upload_expiration_hrs``.
 
You can launch the command manually from your virtual environment like this:

    python manage.py delete_expired_uploads

You can also set a cron-job:

    crontab -e

Add this line and save:

    */60 * * * * cd FULL_PATH_TO_VNF_REPOSITORY && .env/bin/python manage.py delete_expired_uploads > /dev/null 2>&1

Change ``FULL_PATH_TO_VNF_REPOSITORY`` with the full path where the VNF-repository is located (i.e. /home/user/VNF-repository).

You can verify if your cron-job is installed with the command

    crontab -l
