# -*- coding: utf-8 -*-
from __future__ import absolute_import

import celery
import os
from django.conf import settings

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shayan.settings')
# app = celery.Celery('scorize', broker=settings.BROKER_URL)
# print(settings.BROKER_URL)
# app.config_from_object('django.conf:settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
