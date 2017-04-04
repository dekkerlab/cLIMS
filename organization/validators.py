'''
Created on Apr 1, 2017

@author: nanda
'''
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')
