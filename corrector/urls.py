from django.conf.urls import url

from corrector.views import correctorindex

app_name='corrector'

urlpatterns = [
    url(r'^$', correctorindex, name='index'),


]
