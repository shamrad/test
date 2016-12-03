
from django.conf.urls import url,include
from django.contrib import admin
from .view import Home



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', Home, name='home'),
    url(r'^profile/', include('user_profile.urls')),

]
