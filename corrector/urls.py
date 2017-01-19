from django.conf.urls import url,include

from corrector.views import Teacherindex, Score
from .views import EditView, ChangePassword

app_name='corrector'
urlpatterns = [
    url(r'^$', Teacherindex, name='teacherindex'),
    url(r'^(?P<pk>[0-9]+)/$', Score.as_view(), name='score'),
    url(r'edit/$', EditView.as_view(), name='edit'),
    url(r'change-password/$', ChangePassword, name='ChangePassword')
]