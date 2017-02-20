# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-02-20 19:02
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_email_confirmation.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.')], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('credit', models.IntegerField(blank=True, null=True)),
                ('credit2', models.IntegerField(blank=True, default=0, null=True)),
                ('amount', models.IntegerField(blank=True, null=True)),
                ('amount2', models.IntegerField(blank=True, default=0, null=True)),
                ('teacher', models.BooleanField(default=False, help_text='Designates whether this user can edit the scor??. ', verbose_name='teacher')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=(models.Model, simple_email_confirmation.models.SimpleEmailConfirmationUserMixin),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField()),
                ('number', models.IntegerField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('authority', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('number_of_sessions', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.TextField()),
                ('order', models.IntegerField()),
                ('whichcourse', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Course')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wallet', models.IntegerField()),
                ('number', models.IntegerField(default=0)),
                ('wallet2', models.IntegerField(default=0)),
                ('number2', models.IntegerField(default=0)),
                ('wallet3', models.IntegerField(default=0)),
                ('number3', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_email_received', models.IntegerField(default=0)),
                ('is_finished', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Course')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('topic', models.TextField()),
                ('tpo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacherate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to=settings.AUTH_USER_MODEL)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='teacherscore', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Writing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(max_length=10000)),
                ('title', models.CharField(default='untitled', max_length=3000)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('moshaver', models.TextField(default='نظر مشاور ثبت نشده است.')),
                ('corrector', models.CharField(blank=True, max_length=30, null=True)),
                ('score', models.IntegerField(default=0)),
                ('grammer', models.CharField(blank=True, max_length=10000, null=True)),
                ('vocab', models.CharField(blank=True, max_length=10000, null=True)),
                ('unity', models.CharField(blank=True, max_length=10000, null=True)),
                ('oad', models.CharField(blank=True, max_length=10000, null=True)),
                ('wordchoice', models.CharField(blank=True, max_length=10000, null=True)),
                ('adress', models.CharField(blank=True, max_length=10000, null=True)),
                ('grammersc', models.IntegerField(blank=True, null=True)),
                ('vocabsc', models.IntegerField(blank=True, null=True)),
                ('unitysc', models.IntegerField(blank=True, null=True)),
                ('oadsc', models.IntegerField(blank=True, null=True)),
                ('wordchoicesc', models.IntegerField(blank=True, null=True)),
                ('adresssc', models.IntegerField(blank=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='teacherate',
            name='writing',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_profile.Writing'),
        ),
        migrations.AddField(
            model_name='course',
            name='student',
            field=models.ManyToManyField(through='user_profile.Registration', to=settings.AUTH_USER_MODEL),
        ),
    ]
