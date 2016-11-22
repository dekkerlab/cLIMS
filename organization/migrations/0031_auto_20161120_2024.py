# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-20 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0030_auto_20161120_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='experiment_imageObjects',
            field=models.ManyToManyField(blank=True, help_text='Lab gel and fragment analyzer images', related_name='expImg', to='dryLab.ImageObjects'),
        ),
    ]