#!/bin/bash
#####################################################
### This script installs requirements for 
### Dekker Lab Information Management System
### This script has to be run in sudo mode

# Update repository and install the essentials
apt-get update
apt-get install git -y
apt-get install vim -y

### Python3
apt-get install python3-pip -y
apt-get install python3-dev -y

### Apache2
apt-get install apache2 -y
apt-get install libapache2-mod-wsgi-py3 -y

### PostgreSql
apt-get install postgresql-9.5 libpq-dev postgresql-contrib -y

### pip3
pip3 install Django==1.9.7
pip3 install django-crispy-forms==1.6.0
pip3 install openpyxl==2.4.0
pip3 install xlutils==2.0.0
pip3 install xlwt==1.1.2
pip3 install psycopg2==2.6.2
pip3 install awscli
aws configure

