# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-29 21:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0052_auto_20170329_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seqencingfile',
            name='dcic_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
    ]
