# VNF images and templates repository

This project defines some minimal code needed to start a server handling Virtual Network Functions templates and images:
* VNF template: file that describes the characteristics of the VNF, such as the implemented function (e.g., firewall, NAT, etc), required resources (e.g.,  CPU, memory), required environment (e.g., KVM hypervisor, Docker, etc), and more (e.g., number and type of virtual interfaces, etc).
* VNF image: raw image of the VNF (e.g, VM disk). In some case the VNF image is stored directly from this server; in other cases it is stored in a different backend (e.g., OpenStack Glance).

## How to configure the server

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

To start the server:

	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver --d vnfRepo.conf
