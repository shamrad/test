from __future__ import absolute_import, unicode_literals

from celery import Celery
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

import user_profile
from user_profile.models import Registration, Lesson, Writing

app = Celery()


@app.task(name='user_profile.tasks.ersal')
def ersal():
    pending_requests = Registration.objects.filter(is_finished=False)
    for i in pending_requests:
        pending_lesson=Lesson.objects.filter(whichcourse=i.course).get(order=i.last_email_received+1)
        send_mail('dars shomare %s' % pending_lesson.order, pending_lesson.content, settings.DEFAULT_FROM_EMAIL,
                  [i.participant.email],fail_silently=False)
        i.last_email_received += 1
        if i.last_email_received == i.course.number_of_sessions:
            i.is_finished = True


@app.task(name='user_profile.tasks.notif')
def notif():
    User=get_user_model()
    free_writings=Writing.objects.filter(corrector=None)
    teachers=User.objects.filter(teacher=True)
    for x in teachers:
        send_mail('notif', '%s new free writings are available in your profile.' %free_writings.count(),
                  settings.DEFAULT_FROM_EMAIL,[x.email],fail_silently=False)

