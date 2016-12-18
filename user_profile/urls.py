from django.conf.urls import url
from .views import UserFormView, index, LoginView, writing, CreateWriting, Logout, EditView, CreditView

app_name='user_profile'

urlpatterns = [
    url(r'^register/', UserFormView.as_view(), name='register'),
    # url(r'^login/', views.login , name='login'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^$', index, name='index'),
    url(r'^logout', Logout, name='logout'),


    url(r'^(?P<pk>[0-9]+)/$', writing, name='writing'),
    url(r'^addnew/$', CreateWriting.as_view(), name='newriting'),
    url(r'^increase-credit/$', CreditView , name='increase'),
    url(r'edit/$', EditView.as_view(), name='edit'),



]
