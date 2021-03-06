# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-16 22:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dryLab', '0023_auto_20161116_1619'),
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_path', models.FilePathField()),
            ],
        ),
        migrations.RemoveField(
            model_name='analysis',
            name='analysis_paste',
        ),
        migrations.AddField(
            model_name='images',
            name='image_analysis',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dryLab.Analysis'),
        ),
    ]
