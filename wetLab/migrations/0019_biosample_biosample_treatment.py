# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-07 19:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0017_remove_publication_publication_exp'),
        ('wetLab', '0018_auto_20161107_1627'),
    ]

    operations = [
        migrations.AddField(
            model_name='biosample',
            name='biosample_treatment',
            field=models.ForeignKey(default=1, help_text='Select the treatment', on_delete=django.db.models.deletion.CASCADE, related_name='biosamChoice', to='organization.Choice'),
            preserve_default=False,
        ),
    ]