# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-01-23 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0015_auto_20170116_1649'),
    ]

    operations = [
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet', models.CharField(choices=[('1', 'تصحیح یک متن - 9 هزار تومان'), ('2', 'تصحیح 5 متن - 39 هزار تومان')], max_length=2)),
            ],
        ),
    ]
