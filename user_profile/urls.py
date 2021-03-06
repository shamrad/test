from django.conf.urls import url
from .views import UserFormView, index, LoginView, writing, Logout, EditView, NewWriting, CommingSoon, \
    ChangePassword, Etebar, Send_request, verify, emailsent, confirmation, hamayesh_reg, verify_event

app_name='user_profile'

urlpatterns = [
    url(r'^register/', UserFormView.as_view(), name='register'),
    # url(r'^login/', views.login , name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^$', index, name='index'),
    url(r'^logout', Logout, name='logout'),

    url(r'^email-sent/$', emailsent, name='emailsent'),
    url(r'^confirm/(?P<confirmation_key>[\w]+)/$', confirmation, name='confirmation'),

    url(r'^(?P<pk>[0-9]+)/$', writing, name='writing'),
    url(r'edit/$', EditView.as_view(), name='edit'),
    url(r'change-password/$', ChangePassword, name='ChangePassword'),


    url(r'NewWriting/$', NewWriting, name='NewWriting'),




    url(r'^آزمون-تافل/', CommingSoon, name='exam'),
    url(r'^اسپیکینگ/', CommingSoon, name='speaking'),
    url(r'^مشاوره-زبان-تافل/', CommingSoon, name='moshavere'),


    url(r'^etebar/', Etebar, name='credit'),


    # bank
    url(r'^Send_request/', Send_request, name='Send_request'),
    # url(r'^verify?Authority=(?P<Authority>[0-9]+)&Status=(?P<Status>[A-Z]+)/', verify, name='verify'),
    url(r'^verify/', verify, name='verify'),


]
