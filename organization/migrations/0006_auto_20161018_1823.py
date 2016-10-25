# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-18 18:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0003_auto_20161018_1823'),
        ('wetLab', '0001_initial'),
        ('organization', '0005_experiment'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='exp_biosample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expBio', to='wetLab.Biosample'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='exp_document',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expDoc', to='wetLab.Document'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='exp_project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expProject', to='organization.Project'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='exp_protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expPro', to='wetLab.Protocol'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='exp_publication',
            field=models.ManyToManyField(related_name='expPub', to='organization.Publication'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='exp_run',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expRun', to='dryLab.SeqencingRun'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='exp_set',
            field=models.ManyToManyField(related_name='expSet', to='organization.ExperimentSet'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='exp_tag',
            field=models.ManyToManyField(related_name='expTag', to='organization.Tag'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='exp_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expType', to='organization.JsonkeyField'),
        ),
    ]
