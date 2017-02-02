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
    credit= models.IntegerField(null=True, blank=True)
    credit2= models.IntegerField(null=True, blank=True, default=0)
    amount= models.IntegerField(null=True, blank=True)
    amount2= models.IntegerField(null=True, blank=True,default=0)
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


    score=models.IntegerField( default=0)

    grammer=models.CharField(max_length=10000, null=True, blank=True)
    vocab=models.CharField(max_length=10000, null=True, blank=True)
    unity=models.CharField(max_length=10000, null=True, blank=True)
    oad=models.CharField(max_length=10000, null=True, blank=True)
    wordchoice=models.CharField(max_length=10000, null=True, blank=True)
    adress=models.CharField(max_length=10000, null=True, blank=True)


    grammersc=models.IntegerField(null=True, blank=True)
    vocabsc=models.IntegerField(null=True, blank=True)
    unitysc=models.IntegerField(null=True, blank=True)
    oadsc=models.IntegerField(null=True, blank=True)
    wordchoicesc=models.IntegerField(null=True, blank=True)
    adresssc=models.IntegerField(null=True, blank=True)



    def get_absolute_url(self):
        return reverse('user_profile:index')

    def __str__(self):
        return self.author.username + '-' + self.title + '-'


class Teacherate(models.Model):
    teacher=models.ForeignKey(User,null=False, related_name='teacherscore' )
    student = models.ForeignKey(User, null=False, related_name='student')
    rate=models.IntegerField()
    writing=models.ForeignKey(Writing, null=False)

    def __str__(self):
        return self.teacher.username + ' by ' + self.student.username


class Subject(models.Model):
    title=models.CharField(max_length=20)
    topic=models.TextField()
    tpo=models.BooleanField(default=True)

    def __str__(self):
        return  self.title

class Price(models.Model):
    wallet=models.IntegerField(  )
    number=models.IntegerField( default=0)
    wallet2=models.IntegerField( default=0)
    number2=models.IntegerField( default=0)
    wallet3=models.IntegerField( default=0)
    number3=models.IntegerField( default=0)


class Buy(models.Model):
    user=models.ForeignKey(User)
    amount=models.IntegerField()
    number=models.IntegerField()
    date=models.DateTimeField(auto_now_add=True)
    authority=models.IntegerField(default=0)
    def __str__(self):
        return self.user + ' buy '+ self.number
