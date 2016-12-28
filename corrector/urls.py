from django.conf.urls import url,include

from corrector.views import Teacherindex, Score

app_name='corrector'
urlpatterns = [
    url(r'^$', Teacherindex, name='teacherindex'),
    url(r'^(?P<pk>[0-9]+)/$', Score.as_view(), name='score'),

]