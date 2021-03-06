# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-19 17:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0032_auto_20161219_1638'),
    ]

    operations = [
        migrations.RenameField(
            model_name='protocol',
            old_name='protocol_description',
            new_name='description',
        ),
        migrations.RenameField(
            model_name='protocol',
            old_name='protocol_document',
            new_name='document',
        ),
        migrations.RenameField(
            model_name='protocol',
            old_name='protocol_enzyme',
            new_name='enzyme',
        ),
        migrations.RenameField(
            model_name='protocol',
            old_name='protocol_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='protocol',
            old_name='protocol_type',
            new_name='type',
        ),
        migrations.RenameField(
            model_name='protocol',
            old_name='protocol_variation',
            new_name='variation',
        ),
    ]
