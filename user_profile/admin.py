from django.contrib import admin
from .models import Writing,User
from corrector.models import Corrector

admin.site.register(Writing)
admin.site.register(User)
admin.site.register(Corrector)

