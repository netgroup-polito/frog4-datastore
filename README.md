# Service repository for VNF images and templates

This project defines some minimal code needed to start a server handling Virtual Network Functions templates and images:
* VNF template: file that describes the characteristics of the VNF, such as the implemented function (e.g., firewall, NAT, etc), required resources (e.g.,  CPU, memory), required environment (e.g., KVM hypervisor, Docker, etc), and more (e.g., number and type of virtual interfaces, etc).
* VNF image: raw image of the VNF (e.g, VM disk). In some case the VNF image is stored directly from this server; in other cases it is stored in a different backend (e.g., OpenStack Glance).

## How to configure the server

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

## How to execute the server

Creating a private environment in which we run Django 1.8; unfortunately API changed in 1.9, hence it is better to use this specific version only in our project and start the server:

	virtualenv .env
	source .env/bin/activate
	pip install django==1.8.2 djangorestframework MySQL-python django-rest-swagger wrapt bcrypt
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver --d VNF_ServiceConfig.ini [uses config/default-config.ini if '--d' is missing]
