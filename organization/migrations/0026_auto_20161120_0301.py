# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-20 03:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0025_auto_20161119_2214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='experiment_protocol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expPro', to='wetLab.Protocol'),
        ),
    ]
