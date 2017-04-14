# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-04-03 17:19
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0052_auto_20170331_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='name',
            field=models.CharField(db_index=True, default='', max_length=100, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='experiment_name',
            field=models.CharField(db_index=True, default='', max_length=100, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='experimentset',
            name='experimentSet_name',
            field=models.CharField(default='', max_length=100, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(db_index=True, default='', help_text='Name of the project', max_length=200, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')]),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_title',
            field=models.CharField(default='', help_text='Title of the publication or communication.', max_length=200),
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_name',
            field=models.CharField(db_index=True, default='', max_length=100, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z-]*$', 'Only alphanumeric characters and dashes are allowed in names.')]),
        ),
    ]