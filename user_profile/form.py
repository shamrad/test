from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django import  forms

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput) #TODO: add validator
    class Meta:
        model=User
        fields=['username','email','password']


class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        password_field = self.fields['password']
        username_field = self.fields['username']

        username_field.widget.attrs = {'class': 'inputA'}
        username_field.label = 'username'

        password_field.widget.attrs = {'class': 'inputA'}
        password_field.label = 'password'