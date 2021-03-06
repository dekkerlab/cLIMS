# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-19 22:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0024_experimentset_experimentset_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='tag_color',
        ),
        migrations.AddField(
            model_name='experimentset',
            name='project',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='expSetProject', to='organization.Project'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tag',
            name='project',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='tagProject', to='organization.Project'),
            preserve_default=False,
        ),
    ]
