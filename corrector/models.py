# from django.core import validators
# from django.db import models
# from django.utils.translation import ugettext_lazy as _
# # Create your models here.
#
#
#
# class Corrector(models.Model):
#     name=models.CharField(max_length=20)
#     email=models.EmailField(('email address'), blank=True)
#     username=models.CharField(
#         _('username'),
#         max_length=30,
#         unique=True,
#         help_text=_('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         validators=[
#             validators.RegexValidator(
#                 r'^[\w.@+-]+$',
#                 _('Enter a valid username. This value may contain only '
#                   'letters, numbers ' 'and @/./+/-/_ characters.')
#             ),
#         ],
#         error_messages={
#             'unique': _("A user with that username already exists."),
#         },
#     )
#     password=models.CharField(_('password'), max_length=128)
#     wallet=models.CharField(max_length=10, blank=True, null=True)
#
#     def __str__(self):
#         return self.name