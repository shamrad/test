# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-28 13:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0006_auto_20161228_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='writing',
            name='corrector',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
