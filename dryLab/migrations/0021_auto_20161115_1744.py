# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-15 17:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0020_auto_20161115_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sequencingrun',
            name='run_Add_Barcode',
            field=models.CharField(choices=[('addBarcode', 'Yes'), ('detailProject', 'No')], default='showProject', max_length=13),
        ),
    ]
