# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-08 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0012_auto_20170108_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='writing',
            name='adress',
            field=models.CharField(blank=True, max_length=10000, null=True),
        ),
    ]
