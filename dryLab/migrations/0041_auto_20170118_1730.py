# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-01-18 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0040_auto_20161120_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencingrun',
            name='run_Add_Barcode',
            field=models.CharField(choices=[('addBarcode', 'Yes'), ('detailProject', 'No')], default='detailProject', max_length=13),
        ),
    ]
