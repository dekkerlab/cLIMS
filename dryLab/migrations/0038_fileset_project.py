# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-19 22:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0024_experimentset_experimentset_name'),
        ('dryLab', '0037_fileset_fileset_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileset',
            name='project',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='filesetProject', to='organization.Project'),
            preserve_default=False,
        ),
    ]
