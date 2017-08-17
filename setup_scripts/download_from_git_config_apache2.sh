#!/bin/bash

CONFIG_FILE=/etc/apache2/sites-available/000-default.conf

echo "<VirtualHost *:80>" > $CONFIG_FILE
echo "   ServerAdmin webmaster@localhost" >> $CONFIG_FILE
echo "   DocumentRoot /var/www/html" >> $CONFIG_FILE
echo "   Alias /static /djangoProject/cLIMS/static" >> $CONFIG_FILE
echo "   <Directory \"/djangoProject/cLIMS/static\">" >> $CONFIG_FILE
echo "      Require all granted" >> $CONFIG_FILE
echo "   </Directory>" >> $CONFIG_FILE
echo "   " >> $CONFIG_FILE
echo "   WSGIScriptAlias / /djangoProject/cLIMS/cLIMS/apache/wsgi.py" >> $CONFIG_FILE
echo "   <Directory \"/djangoProject/cLIMS/cLIMS/apache\">" >> $CONFIG_FILE
echo "      <Files wsgi.py>" >> $CONFIG_FILE
echo "         Require all granted" >> $CONFIG_FILE
echo "      </Files>" >> $CONFIG_FILE
echo "   </Directory>" >> $CONFIG_FILE
echo "   " >> $CONFIG_FILE
echo "   " >> $CONFIG_FILE
echo "   " >> $CONFIG_FILE
echo "</VirtualHost>" >> $CONFIG_FILE


echo "<VirtualHost *:443>" >> $CONFIG_FILE
echo "   ServerAdmin webmaster@localhost" >> $CONFIG_FILE
echo "   DocumentRoot /var/www/html" >> $CONFIG_FILE
echo "   Alias /static /djangoProject/cLIMS/static" >> $CONFIG_FILE
echo "   <Directory \"/djangoProject/cLIMS/static\">" >> $CONFIG_FILE
echo "      Require all granted" >> $CONFIG_FILE
echo "   </Directory>" >> $CONFIG_FILE
echo "   " >> $CONFIG_FILE
echo "   WSGIScriptAlias / /djangoProject/cLIMS/cLIMS/apache/wsgi.py" >> $CONFIG_FILE
echo "   <Directory \"/djangoProject/cLIMS/cLIMS/apache\">" >> $CONFIG_FILE
echo "      <Files wsgi.py>" >> $CONFIG_FILE
echo "         Require all granted" >> $CONFIG_FILE
echo "      </Files>" >> $CONFIG_FILE
echo "   </Directory>" >> $CONFIG_FILE
echo "   SSLEngine on" >> $CONFIG_FILE
echo "   SSLCertificateFile /etc/apache2/server.crt" >> $CONFIG_FILE
echo "   SSLCertificateKeyFile /etc/apache2/server.key" >> $CONFIG_FILE
echo "   " >> $CONFIG_FILE
echo "   " >> $CONFIG_FILE
echo "   " >> $CONFIG_FILE
echo "</VirtualHost>" >> $CONFIG_FILE
echo "WSGIPythonPath /djangoProject/cLIMS/:/usr/local/lib/python3.5/dist-packages/" >> $CONFIG_FILE

openssl genrsa -des3 -out /etc/apache2/server.key 1024
openssl req -new -key /etc/apache2/server.key -out /etc/apache2/server.csr
cp /etc/apache2/server.key /etc/apache2/server.key.org
openssl rsa -in /etc/apache2/server.key.org -out /etc/apache2/server.key
openssl x509 -req -days 365 -in /etc/apache2/server.csr -signkey /etc/apache2/server.key -out /etc/apache2/server.crt

a2enmod rewrite
a2enmod ssl

ufw allow 'Apache Full'
apache2ctl configtest
systemctl restart apache2

echo "Apache2 has been configured!"

python3 /djangoProject/cLIMS/manage.py collectstatic

echo "static files have been collected."

cat /djangoProject/cLIMS/clims.sql.txt | sudo -u postgres psql clims_db

echo "Database is set"

