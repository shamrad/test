# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os
import celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shayan.settings')
app = celery.Celery('shayan')
# print(settings.BROKER_URL)
app.config_from_object('django.conf:settings')
# app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule= {
    'ersal-e-darsname':{
        'task': 'user_profile.tasks.ersal',
        'options': {'queue': 'celery'},
        # 'schedule': crontab(minute=0, hour=9, day_of_week='sat, mon, wed'),
        'schedule': crontab(),
    },
    'notif-e-writing-raigan':{
        'task': 'user_profile.tasks.notif',
        'options': {'queue': 'celery'},
        'schedule' : crontab(hour='9,18', minute='0'),
    },
    # 'test111':{
    #     'task': 'test',
    #     'options': {'queue': 'celery'},
    #     'schedule' : crontab(),
    # },
}

@app.task(bind=True,name='test')
def debug_task(self):
    print('Request: {0!r}'.format(self.request))