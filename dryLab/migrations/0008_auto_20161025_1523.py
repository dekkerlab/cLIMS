# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-25 15:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0007_auto_20161025_1523'),
        ('dryLab', '0007_auto_20161025_1523'),
    ]

    operations = [
        migrations.DeleteModel(
            name='SeqencingRun',
        ),
        migrations.AddField(
            model_name='sequencingrun',
            name='run_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='runProject', to='organization.Project'),
        ),
        migrations.AddField(
            model_name='seqencingfile',
            name='SequencingFile_run',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fileRun', to='dryLab.SequencingRun'),
            preserve_default=False,
        ),
    ]
