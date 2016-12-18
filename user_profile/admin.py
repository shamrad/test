from django.contrib import admin
from .models import Writing , Credit
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


class CreditInline(admin.StackedInline):
    model = Credit
    can_delete = False
    verbose_name_plural = 'credit'


class UserAdmin(BaseUserAdmin):
    inlines = (CreditInline, )


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User,UserAdmin)

admin.site.register(Writing)
admin.site.register(Credit)
