from django.contrib.auth.models import User
from django.db import models
from django.core.urlresolvers import reverse
from model_utils.models import TimeStampedModel
from django_jalali.db import models as jmodels

class Writing(models.Model):
    author=models.ForeignKey(User)
    text=models.CharField(max_length=10000)
    score=models.CharField(max_length=10, default='0')
    title = models.CharField(max_length=30, null=True, default='untitled')
    time = models.DateTimeField(auto_now_add=True)
    corrector=models.CharField(max_length=10, default='noOne')

    def get_absolute_url(self):
        return reverse('user_profile:index')

    def __str__(self):
        return self.author.username + '-' + self.title + '-' + self.title

class Comment(models.Model):
    name=models.CharField(max_length=100)
    coment=models.CharField(max_length=10000)
    email=models.CharField(max_length=100)
    page=models.CharField(max_length=100)