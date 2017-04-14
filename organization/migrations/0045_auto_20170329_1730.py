# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-03-29 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0044_auto_20170329_1602'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='experiment_alias',
        ),
        migrations.RemoveField(
            model_name='experimentset',
            name='experimentSet_alias',
        ),
        migrations.RemoveField(
            model_name='project',
            name='project_alias',
        ),
        migrations.RemoveField(
            model_name='publication',
            name='publication_alias',
        ),
        migrations.AddField(
            model_name='experiment',
            name='dcic_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=20),
        ),
        migrations.AddField(
            model_name='experimentset',
            name='dcic_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=20),
        ),
        migrations.AddField(
            model_name='publication',
            name='dcic_alias',
            field=models.CharField(db_index=True, default='', help_text='Provide an alias name for the object for DCIC submission.', max_length=20),
        ),
    ]