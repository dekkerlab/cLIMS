# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-19 16:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wetLab', '0031_auto_20161215_2127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='biosample',
            old_name='biosample_imageObjects',
            new_name='imageObjects',
        ),
        migrations.RenameField(
            model_name='biosample',
            old_name='biosample_protocol',
            new_name='protocol',
        ),
        migrations.RenameField(
            model_name='modification',
            old_name='modification_constructs',
            new_name='constructs',
        ),
        migrations.RenameField(
            model_name='modification',
            old_name='modification_target',
            new_name='target',
        ),
        migrations.RemoveField(
            model_name='biosource',
            name='biosource_SOP_cell_line',
        ),
        migrations.RemoveField(
            model_name='construct',
            name='construct_map',
        ),
        migrations.RemoveField(
            model_name='treatmentrnai',
            name='treatmentRnai_rnai_constructs',
        ),
        migrations.RemoveField(
            model_name='treatmentrnai',
            name='treatmentRnai_target',
        ),
        migrations.AddField(
            model_name='biosource',
            name='protocol',
            field=models.ForeignKey(blank=True, help_text='Standard operation protocol for the cell line as determined by 4DN Cells Working Group', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bioProtocol', to='wetLab.Protocol', verbose_name='biosource_SOP_cell_line'),
        ),
        migrations.AddField(
            model_name='construct',
            name='documents',
            field=models.ForeignKey(blank=True, help_text='Map of the construct - document', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conDoc', to='wetLab.Document', verbose_name='construct_map'),
        ),
        migrations.AddField(
            model_name='treatmentrnai',
            name='constructs',
            field=models.ForeignKey(blank=True, help_text='Recombinant constructs used for RNAi', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rnaiType', to='wetLab.Construct', verbose_name='treatmentRnai_rnai_constructs'),
        ),
        migrations.AddField(
            model_name='treatmentrnai',
            name='target',
            field=models.ForeignKey(blank=True, help_text='The targeted gene or genomic region that is targeted by the modification.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rnaiVendor', to='wetLab.Target', verbose_name='treatmentRnai_target'),
        ),
    ]
