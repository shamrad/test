# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-12-27 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0002_remove_writing_corrector'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='teacher',
            field=models.BooleanField(default=False, help_text='Designates whether this user can edit the scor??. ', verbose_name='teacher'),
        ),
    ]
