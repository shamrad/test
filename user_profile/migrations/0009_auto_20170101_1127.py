# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-01 07:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0008_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='topic',
            field=models.TextField(),
        ),
    ]
