#!/bin/bash

git clone https://github.com/dekkerlab/cLIMS.git
mkdir /djangoProject
mv cLIMS /djangoProject/
chmod 777 /djangoProject -R

sudo /djangoProject/cLIMS/setup_scripts/setup_main.sh

echo "Making Migrations.."
python3 /djangoProject/cLIMS/manage.py makemigrations
echo "Migrate.."
python3 /djangoProject/cLIMS/manage.py migrate

echo "Enter date for database backup recovery dd-mm-yyyy"
read input_variable
echo "Fetching database backup from AWS backup: " $input_variable".sql.txt"

aws s3 cp s3://dekkerlab-web/db-backups/$input_variable.sql.txt .
echo "drop database clims_db;" | sudo -u postgres psql
echo "create database clims_db;" | sudo -u postgres psql
echo "GRANT ALL PRIVILEGES ON DATABASE clims_db TO dekker_lab;" | sudo -u postgres psql
cat $input_variable.sql.txt | sudo -u postgres psql clims_db

sudo rm -r /djangoProject/cLIMS/media/*
sudo aws s3 cp s3://dekkerlab-web/media-backups /djangoProject/cLIMS/media --recursive
sudo chmod -R 777 media/

sudo python3 /djangoProject/cLIMS/manage.py collectstatic

sudo rm $input_variable.sql.txt

sudo /etc/init.d/apache2 start
