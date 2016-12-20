'''
Created on Dec 20, 2016

@author: nanda
'''

#############CREATE ACCOUNT ##############
###RUN COMMAND FROM SHELL###
#python3 manage.py shell
#import create_account
#create_account.readAccounts("/home/ubuntu/clims_automated_emails/lab_emails.txt")
###########################################

def createAccounts(userEmail,userName, userPassword):
    from django.contrib.auth.models import User
    from django.contrib.auth.models import Group
    user = User.objects.create_user(userName, userEmail, userPassword)
    user.save()
    name=userEmail.split("@")
    flName=name[0].split(".")
    print(flName)
    user.first_name=flName[0]
    user.last_name=flName[1]
    user.save()
    group = Group.objects.get(name='Member')
    user.groups.add(group) 
    
    
def readAccounts(accountList):
    with open(accountList, 'r') as f:
        read_data = f.readlines()
        for line in read_data:
            userInfoArray = line.split()
            userEmail = userInfoArray[0]
            userName = userInfoArray[1]
            userPassword = userInfoArray[2]
            createAccounts(userEmail,userName, userPassword)
            