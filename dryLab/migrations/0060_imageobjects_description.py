# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-03 21:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0059_auto_20170403_2124'),
    ]

    operations = [
        migrations.AddField(
            model_name='imageobjects',
            name='description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
