# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-19 21:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0035_fileset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fileset',
            name='fileSet_name',
        ),
    ]