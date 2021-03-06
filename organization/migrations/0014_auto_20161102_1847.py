# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-02 18:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0006_auto_20161031_2148'),
        ('organization', '0013_experiment_experiment_enzyme'),
    ]

    operations = [
        migrations.AddField(
            model_name='experiment',
            name='dbxrefs',
            field=models.CharField(blank=True, help_text='Unique identifiers from external resources.', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='experiment',
            name='documents',
            field=models.ForeignKey(blank=True, help_text='Documents that provide additional information (not data file).', null=True, on_delete=django.db.models.deletion.CASCADE, to='wetLab.Document'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='references',
            field=models.ForeignKey(blank=True, help_text='The publications that provide more information about the object.', null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.Publication'),
        ),
        migrations.AddField(
            model_name='experiment',
            name='url',
            field=models.URLField(blank=True, help_text='An external resource with additional information about the object', null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_identifiers',
            field=models.CharField(blank=True, help_text='The identifiers that reference data found in the object.', max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='publication_volume',
            field=models.CharField(blank=True, help_text='The volume of the publication.', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='experiment_biosample',
            field=models.ForeignKey(help_text='Starting biological material.', on_delete=django.db.models.deletion.CASCADE, related_name='expBio', to='wetLab.Biosample'),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='experiment_description',
            field=models.CharField(blank=True, help_text='A short description of the experiment', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='experiment_enzyme',
            field=models.ForeignKey(help_text='The enzyme used for digestion of the DNA.', on_delete=django.db.models.deletion.CASCADE, related_name='expEnz', to='wetLab.Enzyme'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_active',
            field=models.BooleanField(default=True, help_text='Is project currently in progress?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_name',
            field=models.CharField(db_index=True, default='', help_text='Name of the project', max_length=200, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='project_notes',
            field=models.TextField(blank=True, help_text='Notes for the project.', null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_abstract',
            field=models.CharField(blank=True, help_text='Abstract of the publication or communication.', max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_exp',
            field=models.ManyToManyField(help_text='List of experiment sets to be associated with the publication.', related_name='pubExp', to='organization.Experiment'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_issue',
            field=models.CharField(default='', help_text='The issue of the publication.', max_length=200),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_journal',
            field=models.CharField(default='', help_text='The journal of the publication.', max_length=200),
        ),
        migrations.AlterField(
            model_name='publication',
            name='publication_title',
            field=models.CharField(default='', help_text='Title of the publication or communication.', max_length=200),
        ),
    ]
