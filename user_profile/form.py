from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from simple_email_confirmation.models import EmailAddress

from .models import User, Writing, Teacherate, Price
from django import  forms


# from user_profile.models import Credit


class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput) #TODO: add validator


    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("این ایمیل قبلا استفاده شده است")
        return data

    class Meta:
        model=User
        fields=['first_name','last_name','username','email','password']



class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        password_field = self.fields['password']
        username_field = self.fields['username']

        username_field.widget.attrs = {'class': 'inputA'}
        username_field.label = 'username'

        password_field.widget.attrs = {'class': 'inputA'}
        password_field.label = 'password'



class WritingForm(forms.ModelForm):
    class Meta:
        model= Writing
        fields = ['title', 'text']

class Rate(forms.ModelForm):
    class Meta:
        model=Teacherate
        fields=['rate']


class EmailForm (forms.ModelForm):

    # def check_email(self):
    #     data = self.cleaned_data['email']
    #     if data not in EmailAddress.objects.all().email:
    #         raise forms.ValidationError("قبلا ثبت نام نکرده اید")
    #     return data

    class Meta:
        model=User
        fields=['email']


class PriceForm(forms.ModelForm):
    class Meta:
        model= Price
        fields = ['wallet','number']