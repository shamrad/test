
from django.conf.urls import url,include
from django.contrib import admin

from user_profile.views import resendkey
from .views import khane, service,aboutus, test, faq, barname, nini
from django.contrib.auth.views import password_reset,password_reset_done,password_reset_confirm, password_reset_complete

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', khane, name='home'),
    url(r'^profile/', include('user_profile.urls')),
    url(r'^toefl-learning-آموزش-تافل/', service, name='service'),
    url(r'^toefl-faq/', faq, name='faq'),
    url(r'^about-us/', aboutus, name='aboutus'),
    url(r'^toefl-120-برنامه/', barname, name='barname'),
    url(r'^مکالمه-به-روش-کودکان/', nini, name='nini'),

    url(r'password/$', password_reset,{'template_name': 'user_profile/password_reset.html'}, name='reset_password'),
    url(r'password/done/$', password_reset_done,{'template_name': 'user_profile/password_reset_done.html'}, name='password_reset_done'),
    url(r'password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm,{'template_name': 'user_profile/password_reset_confirm.html'}, name='password_reset_confirm'),
    # url(r'password/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', password_reset_confirm,name='password_reset_confirm'),
    url(r'password/complete/$', password_reset_complete,{'template_name': 'user_profile/password_reset_complete.html'}, name='password_reset_complete'),
    url(r'resend-key/$', resendkey, name='resendkey'),


    # test url
    url(r'^test/', test, name='test'),


    # teacher
    url(r'^teacher/', include('corrector.urls')),


 ]
