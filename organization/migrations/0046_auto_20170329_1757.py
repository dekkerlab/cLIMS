# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-29 17:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0045_auto_20170329_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='experiment',
            name='dcic_alias',
            field=models.CharField(db_index=True, help_text='Provide an alias name for the object for DCIC submission.', max_length=20),
        ),
        migrations.AlterField(
            model_name='experimentset',
            name='dcic_alias',
            field=models.CharField(db_index=True, help_text='Provide an alias name for the object for DCIC submission.', max_length=20),
        ),
        migrations.AlterField(
            model_name='publication',
            name='dcic_alias',
            field=models.CharField(db_index=True, help_text='Provide an alias name for the object for DCIC submission.', max_length=20),
        ),
    ]
