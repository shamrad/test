# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-21 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0004_auto_20161221_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='writing',
            name='moshaver',
            field=models.TextField(default='نظر مشاور ثبت نشده است.'),
        ),
    ]