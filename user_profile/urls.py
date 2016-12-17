from django.conf.urls import url,include
from .views import UserFormView, index, LoginView, writing, CreateWriting, Logout, EditView, Increase, Credit
from django.contrib.auth import views
from django.contrib.auth.views import password_reset,password_reset_done



app_name='user_profile'

urlpatterns = [
    url(r'^register/', UserFormView.as_view(), name='register'),
    # url(r'^login/', views.login , name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^$', index, name='index'),
    url(r'^logout', Logout, name='logout'),


    url(r'^(?P<pk>[0-9]+)/$', writing, name='writing'),
    url(r'^addnew/$', CreateWriting.as_view(), name='newriting'),
    url(r'^increase-credit/$', Increase , name='increase'),
    url(r'edit/$', EditView.as_view(), name='edit'),

    # jadid
    url(r'increas/$', Credit, name='credit'),

    url(r'password/$', password_reset, name='reset_password'),
    url(r'password/done$', password_reset_done, name='password_reset_done'),

]
