# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-18 23:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0031_seqencingfile_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='analysis_hiGlass',
            field=models.FileField(blank=True, help_text='Import HiGlass file', null=True, upload_to='uploads/'),
        ),
    ]