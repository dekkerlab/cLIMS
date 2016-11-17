# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-16 16:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0021_auto_20161115_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='analysis_import',
            field=models.FileField(blank=True, help_text='Import .gz file', null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='analysis',
            name='analysis_paste',
            field=models.TextField(blank=True, help_text='Paste cMapping pipeline analysis result', null=True),
        ),
        migrations.AlterField(
            model_name='analysis',
            name='analysis_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='analysisType', to='organization.JsonObjField'),
        ),
    ]
