'''
Created on Oct 7, 2016

@author: nanda
'''

###Python=3.5.2
###Django=1.9.7
###apache-tomcat-8.5.5
##PostgreSQL = 9.5.4

#########DEPENDENCIES######
#postgresql_psycopg2
# django-crispy-forms
# openpyxl
# xlutils
# xlwt
#To create database run the command ( pg_dump clims_db > clims.sql; ) from the cLims base folder where manage.py resides
#CNTTRY$9
###########################

DATABASE_NAME='clims_db'
DATABASE_USER='dekker_lab'
DATABASE_PASSWORD='CHYYTS14#'
LABNAME = "dekker-lab:"

HOST=''
PORT=''
#WORKSPACEPATH = "/Users/nanda/Documents/EclipseWorkspace/clims/cLIMS/"
WORKSPACEPATH = "/djangoProject/cLIMS/"
#FILEUPLOADPATH = "/Users/nanda/Documents/EclipseWorkspace/clims/cLIMS/media/"
FILEUPLOADPATH = "/djangoProject/cLIMS/media/"