# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-25 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0059_auto_20170425_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='finalize_dcic_submission',
            field=models.BooleanField(default=False, help_text='This object and related entries have been submitted to DCIC'),
        ),
    ]
