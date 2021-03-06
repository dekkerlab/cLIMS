# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-19 17:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0033_auto_20161219_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='document_attachment',
            new_name='attachment',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='document_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='document_references',
            new_name='references',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='document_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='document',
            old_name='document_url',
            new_name='url',
        ),
    ]
