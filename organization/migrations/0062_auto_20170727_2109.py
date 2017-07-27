# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-07-27 21:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0076_auto_20170727_2109'),
        ('organization', '0061_auto_20170426_1541'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='authentication_docs',
            field=models.ManyToManyField(blank=True, help_text='Attach any authentication document for your biosample here. e.g. Fragment Analyzer document, Gel images.', related_name='expAddProto', to='wetLab.Protocol', verbose_name='authentication_docs'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='imageObjects',
            field=models.ManyToManyField(blank=True, help_text='additional images.', related_name='expImg', to='dryLab.ImageObjects'),
        ),
    ]