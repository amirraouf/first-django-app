# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-17 12:52
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0014_auto_20160416_0207'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_dir',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='course_watch_later',
            name='person',
            field=models.ForeignKey(blank=None, default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]