# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-18 11:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0029_remove_writing_corrector'),
    ]

    operations = [
        migrations.AddField(
            model_name='writing',
            name='corrector',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
