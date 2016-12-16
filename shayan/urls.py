
from django.conf.urls import url,include
from django.contrib import admin
from .views import khane, service,aboutus

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', khane, name='home'),
    url(r'^profile/', include('user_profile.urls')),
    url(r'^toefl-learning/', service, name='service'),
    url(r'^about-us/', aboutus, name='aboutus'),

]
