# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-20 19:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0039_imageobjects'),
        ('organization', '0028_auto_20161120_0333'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='experiment_imageObjects',
            field=models.ManyToManyField(help_text='Lab gel and fragment analyzer images', related_name='expImg', to='dryLab.ImageObjects'),
        ),
    ]
