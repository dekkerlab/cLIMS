# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-26 21:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0064_remove_seqencingfile_file_classification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seqencingfile',
            name='file_format',
            field=models.ForeignKey(help_text='Type of file format.', on_delete=django.db.models.deletion.CASCADE, related_name='fileChoice', to='organization.Choice'),
        ),
    ]