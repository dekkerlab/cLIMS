# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-29 16:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0048_auto_20170329_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biosample',
            name='biosample_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='biosource',
            name='biosource_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='construct',
            name='construct_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='doc_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='enzyme',
            name='enzyme_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='genomicregions',
            name='genomicRegions_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='individual',
            name='individual_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='modification',
            name='modification_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='protocol',
            name='protocol_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='target',
            name='target_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='treatmentchemical',
            name='treatmentChemical_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='treatmentrnai',
            name='treatmentRnai_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=10, unique=True),
        ),
    ]
