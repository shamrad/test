from __future__ import absolute_import, unicode_literals


from celery import Celery
from celery.worker.control import rate_limit
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from time import sleep

import user_profile
from user_profile.models import Registration, Lesson, Writing

app = Celery()


@app.task(name='user_profile.tasks.getrequest')
def getrequest():
    pending_requests = Registration.objects.filter(is_finished=False)
    for request in pending_requests:
        ersal(request)

rate_limit("user_profile.tasks.ersal", "20/h")
@app.task(name='user_profile.tasks.ersal')
def ersal(i):
    pending_lesson = Lesson.objects.filter(whichcourse=i.course).get(order=i.last_email_received + 1)
    msg_html = render_to_string('user_profile/Email.html',
                                {'username': i.participant.username,
                                 'number': pending_lesson.order,
                                 'content': pending_lesson.content,
                                 'site': settings.SITE_URL,
                                 'music_file': 'dars ha/' + pending_lesson.whichcourse.name + '/Lesson ' + str(
                                     pending_lesson.order) + '.mp3',
                                 'text_file': 'dars ha/' + pending_lesson.whichcourse.name + '/' + str(
                                     pending_lesson.order) + '.pdf'})
    send_mail('دانلود درس شماره %s' % pending_lesson.order, pending_lesson.content, settings.DEFAULT_FROM_EMAIL,
              [i.participant.email], fail_silently=False, html_message=msg_html)
    i.last_email_received += 1
    if i.last_email_received == i.course.number_of_sessions:
        i.is_finished = True
    i.save()


@app.task(name='user_profile.tasks.notif')
def notif():
    User = get_user_model()
    free_writings = Writing.objects.filter(corrector=None)
    teachers = User.objects.filter(teacher=True)
    for x in teachers:
        send_mail('New Writings Notification',
                  'Dear Professor, %s new free writings are available in your profile. Scorize Team' % free_writings.count(),
                  settings.DEFAULT_FROM_EMAIL, [x.email], fail_silently=False)