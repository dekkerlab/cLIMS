# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-27 14:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0003_auto_20161025_2133'),
        ('organization', '0012_auto_20161025_2134'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='experiment_enzyme',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='expEnz', to='wetLab.Enzyme'),
            preserve_default=False,
        ),
    ]
