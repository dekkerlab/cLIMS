# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-18 18:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0002_auto_20161018_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='analysis_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysisType', to='organization.JsonkeyField'),
        ),
    ]
