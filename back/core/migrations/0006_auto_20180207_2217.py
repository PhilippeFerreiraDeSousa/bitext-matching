# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-07 22:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20180206_1204'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='word',
            name='sentences',
        ),
        migrations.AddField(
            model_name='translation',
            name='sentence_1',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='sentences_1', to='core.Sentence'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='translation',
            name='sentence_2',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='sentences_2', to='core.Sentence'),
            preserve_default=False,
        ),
    ]
