from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Writing,User, Subject, Teacherate, Price, Buy, Course, Lesson, Registration, Hamayesh, Event

class MemberAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'last_login', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    ordering = ('date_joined', 'last_login', 'email')
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(Writing)
admin.site.register(User, MemberAdmin)
admin.site.register(Subject)
admin.site.register(Teacherate)
admin.site.register(Price)
admin.site.register(Buy)
admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(Registration)
admin.site.register(Hamayesh)
admin.site.register(Event)

