# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-19 20:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0018_auto_20161118_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='experimentset',
            name='experiment_name',
            field=models.CharField(default='', max_length=100),
        ),
        
    ]
