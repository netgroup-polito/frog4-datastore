# VNF-repository
Code to manage the repository of the VNF template and images

Files taken from PSAR project of SECURED repository some files are not the final ones and need to be modified
Dependecies missing

To configure SQL:
	mysql -u root -p
        mysql> CREATE DATABASE VNF_repository;
        mysql> GRANT ALL PRIVILEGES ON VNF_repository.* TO 'vnfRepo'@'localhost' \
            IDENTIFIED BY 'vnfPass';
        mysql> GRANT ALL PRIVILEGES ON VNF_repository.* TO 'vnfRepo'@'%' \
            IDENTIFIED BY 'vnfPass';
        mysql> exit

To launch:
	python manage.py makemigrations
	python manage.py migrate
	python manage.py runserver IP_ADDR:PORT_NUM
