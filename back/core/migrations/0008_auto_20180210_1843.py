# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-10 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20180210_1727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bitext',
            name='alignments_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='bitext',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]