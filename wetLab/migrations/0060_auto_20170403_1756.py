# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-03 17:56
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0059_auto_20170403_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genomicregions',
            name='genomicRegions_genome_assembly',
            field=models.ForeignKey(default='', help_text='The genome assembly from which the region was derived', on_delete=django.db.models.deletion.CASCADE, related_name='genAsmChoice', to='organization.Choice', validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')]),
        ),
    ]
