from django.contrib import admin
from .models import Writing,User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# class CreditInline(admin.StackedInline):
#     model = Credit
#     can_delete = False
#     verbose_name_plural = 'credit'
#
#
# class UserAdmin(BaseUserAdmin):
#     inlines = (CreditInline, )
#
#
# # Re-register UserAdmin
# admin.site.unregister(User)
# admin.site.register(User,UserAdmin)

admin.site.register(Writing)
admin.site.register(User)
# admin.site.register(Credit)
