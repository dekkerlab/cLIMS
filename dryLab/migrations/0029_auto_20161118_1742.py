# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-18 17:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0018_auto_20161118_1742'),
        ('dryLab', '0028_auto_20161117_0017'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sequencingrun',
            old_name='run_project',
            new_name='project',
        ),
        migrations.AddField(
            model_name='seqencingfile',
            name='project',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='fileProject', to='organization.Project'),
            preserve_default=False,
        ),
    ]