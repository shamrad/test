# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-23 10:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0017_auto_20170123_1340'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='amount',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='amount2',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='credit2',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
