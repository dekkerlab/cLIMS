# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-25 21:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_auto_20161025_2039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jsonobjfield',
            name='jsonField_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
