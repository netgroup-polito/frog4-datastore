import os

#General
YOUR_IP = os.getenv('YOUR_IP', 'your_ip') 

#Glance & Keystone
ADMIN_USER = os.getenv('OS_USERNAME','admin')
ADMIN_PASS = os.getenv('OS_PASSWORD', 'admin')
TENANT_NAME= os.getenv('OS_TENANT_NAME','admin')
GLANCE_PORT= os.getenv('GLANCE_PORT','9292')
KEYSTONE_ADMIN_PORT=os.getenv('KEYSTONE_ADMIN_PORT','35357')

#Swift
SWIFT_USER=os.getenv('SWIFT_USER','test:tester')
SWIFT_KEY= os.getenv('SWIFT_KEY','testing')
CONTAINER_NAME=os.getenv('CONTAINER_NAME','container2')
SWIFT_AUTH_URL=os.getenv('SWIFT_AUTH_URL','http://127.0.0.1:8080/auth/v1.0')

