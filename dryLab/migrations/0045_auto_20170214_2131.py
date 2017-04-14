# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-14 21:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0042_auto_20170214_2123'),
        ('dryLab', '0044_auto_20170214_2128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='seqencingfile',
            name='barcode',
        ),
        migrations.AddField(
            model_name='seqencingfile',
            name='file_barcode',
            field=models.ForeignKey(blank=True, help_text='Barcode attached to the file.', null=True, on_delete=django.db.models.deletion.CASCADE, to='wetLab.Barcode'),
        ),
    ]