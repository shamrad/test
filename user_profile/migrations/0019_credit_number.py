# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-23 10:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0018_auto_20170123_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='credit',
            name='number',
            field=models.CharField(default=0, max_length=2),
        ),
    ]
