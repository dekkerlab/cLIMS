# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-13 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0036_auto_20170209_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='dbxrefs',
            field=models.CharField(blank=True, help_text='Unique identifiers from external resources, enter as a database name:identifier eg. HGNC:PARK2', max_length=100, null=True),
        ),
    ]
