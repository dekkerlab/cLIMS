# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-14 21:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0065_auto_20170414_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biosample',
            name='document',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Document'),
        ),
        migrations.AlterField(
            model_name='biosource',
            name='document',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Document'),
        ),
        migrations.AlterField(
            model_name='enzyme',
            name='document',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Document'),
        ),
        migrations.AlterField(
            model_name='individual',
            name='document',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Document'),
        ),
        migrations.AlterField(
            model_name='modification',
            name='document',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Document'),
        ),
        migrations.AlterField(
            model_name='othertreatment',
            name='document',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Document'),
        ),
        migrations.AlterField(
            model_name='target',
            name='document',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Document'),
        ),
        migrations.AlterField(
            model_name='treatmentchemical',
            name='document',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Document'),
        ),
        migrations.AlterField(
            model_name='treatmentrnai',
            name='document',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.SET_NULL, to='wetLab.Document'),
        ),
    ]
