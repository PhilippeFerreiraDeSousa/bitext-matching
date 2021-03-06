# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-05 00:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_match', models.IntegerField()),
                ('bitext', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches', to='core.Bitext')),
            ],
        ),
        migrations.AddField(
            model_name='paragraph',
            name='match',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='paragraphs', to='core.Match'),
        ),
    ]
