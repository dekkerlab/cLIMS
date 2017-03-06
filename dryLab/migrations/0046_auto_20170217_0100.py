# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-17 01:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0045_auto_20170214_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seqencingfile',
            name='file_barcode',
            field=models.ForeignKey(blank=True, help_text='Barcode attached to the file.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Barcode'),
        ),
    ]
