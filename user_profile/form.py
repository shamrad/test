from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import MaxLengthValidator

from .models import User, Writing
from django import  forms


# from user_profile.models import Credit


class UserForm(forms.ModelForm):
    # password=forms.CharField(widget=forms.PasswordInput) #TODO: add validator

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("این ایمیل قبلا استغاده شده است")
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


class WritingFormTest(forms.ModelForm):
    text = forms.CharField(
        max_length=1000,
        widget=forms.Textarea
    )
    class Meta:
        model= Writing
        fields = ['title', 'text']


