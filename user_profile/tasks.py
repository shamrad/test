from __future__ import absolute_import, unicode_literals

from celery.task import task
from django.core.mail import send_mail

from user_profile.models import Registration, Lesson


@task(name='shayan.tasks.ersal')
def ersal():
    pending_requests=Registration.objects.filter(is_finished=False)
    for i in pending_requests:
        pending_lesson=Lesson.objects.filter(whichcourse=i.course).filter(order=i.last_email_received+1)
        send_mail('dars shomare %s' % pending_lesson.order, pending_lesson.content, 'info@scorize.com',[i.participant.email],fail_silently=False)
        i.last_email_received += 1
        if i.last_email_received == i.course.number_of_sessions:
            i.is_finished = True