# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-11-21 16:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0027_auto_20161120_2025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biosource',
            name='biosource_SOP_cell_line',
            field=models.ForeignKey(blank=True, help_text='Standard operation protocol for the cell line as determined by 4DN Cells Working Group', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bioProtocol', to='wetLab.Protocol'),
        ),
        migrations.AlterField(
            model_name='biosource',
            name='biosource_cell_line_tier',
            field=models.ForeignKey(blank=True, help_text='Tier into which the cell line has been classified', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bioCellChoice', to='organization.Choice'),
        ),
        migrations.AlterField(
            model_name='biosource',
            name='biosource_vendor',
            field=models.ForeignKey(blank=True, help_text='The Lab or Vendor that provided the biosource.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sourceVendor', to='wetLab.Vendor'),
        ),
    ]
