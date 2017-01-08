from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin, UserManager
from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import post_save
from django.dispatch import receiver
from model_utils.models import TimeStampedModel
# from django_jalali.db import models as jmodels
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


# User._meta.get_field('email').unique

class User(AbstractUser):
    credit= models.CharField(max_length=10, null=True, blank=True)
    teacher=models.BooleanField(
        _('teacher'),
        default=False,
        help_text=_(
            'Designates whether this user can edit the scor??. '

        ),
    )

class Writing(models.Model):
    author=models.ForeignKey(User)
    text=models.TextField(max_length=10000)
    title = models.CharField(max_length=3000,  default='untitled')
    time = models.DateTimeField(auto_now_add=True)
    moshaver=models.TextField(default='نظر مشاور ثبت نشده است.')
    corrector=models.CharField(max_length=30, null=True, blank=True)


    score=models.CharField(max_length=10, default='0')
    grammer=models.CharField(max_length=10000, null=True, blank=True)
    vocab=models.CharField(max_length=10000, null=True, blank=True)
    unity=models.CharField(max_length=10000, null=True, blank=True)
    oad=models.CharField(max_length=10000, null=True, blank=True)
    wordchoice=models.CharField(max_length=10000, null=True, blank=True)
    adress=models.CharField(max_length=10000, null=True, blank=True)



    def get_absolute_url(self):
        return reverse('user_profile:index')

    def __str__(self):
        return self.author.username + '-' + self.title + '-' + self.score+ '-'


class Comment(models.Model):
    name=models.CharField(max_length=100)
    coment=models.CharField(max_length=10000)
    email=models.CharField(max_length=100)
    page=models.CharField(max_length=100)


class Subject(models.Model):
    title=models.CharField(max_length=20)
    topic=models.TextField()
    tpo=models.BooleanField(default=True)

    def __str__(self):
        return  self.title

# class Credit(models.Model):
#     WALLET=(
#         ('1','تصحیح یک متن - 9 هزار تومان'),
#         ('2','تصحیح 5 متن - 39 هزار تومان')
#     )
#     customer=models.OneToOneField(User)
#     wallet=models.CharField(max_length=2, choices= WALLET)


