# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-20 03:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0026_auto_20161120_0301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='experiment_protocol',
            field=models.ForeignKey(default=7, on_delete=django.db.models.deletion.CASCADE, related_name='expPro', to='wetLab.Protocol'),
            preserve_default=False,
        ),
    ]