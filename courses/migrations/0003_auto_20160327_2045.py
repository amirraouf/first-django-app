# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-27 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_auto_20160327_2044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialization',
            name='description',
            field=models.CharField(blank=True, max_length=300),
        ),
    ]
