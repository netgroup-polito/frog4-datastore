DROP DATABASE IF EXISTS frog4_datastore;
CREATE DATABASE frog4_datastore;
GRANT ALL PRIVILEGES ON frog4_datastore.* TO 'datastore'@'localhost' \
        IDENTIFIED BY 'datastorePWD';
GRANT ALL PRIVILEGES ON frog4_datastore.* TO 'datastore'@'%' \
        IDENTIFIED BY 'datastorePWD';
ALTER DATABASE `frog4_datastore` CHARACTER SET utf8;
