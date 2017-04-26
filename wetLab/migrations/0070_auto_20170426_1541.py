# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-26 15:41
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0069_auto_20170425_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='barcode',
            name='barcode_name',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='biosample',
            name='biosample_name',
            field=models.CharField(db_index=True, default='', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='biosource',
            name='biosource_name',
            field=models.CharField(db_index=True, default='', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='construct',
            name='construct_name',
            field=models.CharField(db_index=True, default='', help_text='Short name for construct - letters, numbers, hyphens or underscores allowed (no spaces)', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='document',
            name='name',
            field=models.CharField(db_index=True, default='', help_text='Name of the document', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='enzyme',
            name='enzyme_name',
            field=models.CharField(db_index=True, default='', help_text='The name of the digestion enzyme.', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='genomicregions',
            name='genomicRegions_genome_assembly',
            field=models.ForeignKey(default='', help_text='The genome assembly from which the region was derived', on_delete=django.db.models.deletion.CASCADE, related_name='genAsmChoice', to='organization.Choice', validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='genomicregions',
            name='name',
            field=models.CharField(db_index=True, default='', help_text='Please give a name.', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='individual',
            name='individual_name',
            field=models.CharField(db_index=True, default='', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='modification',
            name='modification_name',
            field=models.CharField(db_index=True, default='', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='othertreatment',
            name='name',
            field=models.CharField(default='', max_length=50, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='protocol',
            name='name',
            field=models.CharField(db_index=True, default='', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='target',
            name='name',
            field=models.CharField(db_index=True, default='', help_text='Please give a name.', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='treatmentchemical',
            name='treatmentChemical_name',
            field=models.CharField(db_index=True, default='', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='treatmentrnai',
            name='treatmentRnai_name',
            field=models.CharField(db_index=True, default='', max_length=50, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_title',
            field=models.CharField(db_index=True, default='', help_text='The complete name of the originating lab or vendor.', max_length=100, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-.]*$', 'Only alphanumeric characters, dashes, dots are allowed in names.')]),
        ),
    ]
