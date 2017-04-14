# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-14 21:27
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0055_auto_20170403_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experimentset',
            name='experimentSet_name',
            field=models.CharField(db_index=True, default='', max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='publication',
            name='name',
            field=models.CharField(db_index=True, default='', max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(db_index=True, default='', max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')]),
        ),
    ]
