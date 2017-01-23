from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth import login as auth_login
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import PasswordChangeForm
from oauthlib.oauth2 import Client

from .form import UserForm, LoginForm, WritingForm, Rate, Price
from django.views.generic import View
from .models import Writing, Subject, Teacherate
from django.views.generic import CreateView


@login_required(login_url='user_profile:login')
def index(request):

    #current_user=User.objects.get(username=username)
    current_user = request.user
    if current_user.teacher :
        return redirect('corrector:teacherindex')
    exam = current_user.writing_set.all()
    context = {
        'user': current_user,
        'exam': exam
    }
    return render(request, 'user_profile/index.html',context)

@login_required(login_url='user_profile:login')
def writing(request,pk):
    current_writing = Writing.objects.get(pk=pk)
    form = Rate(request.POST)
    rate = Teacherate.objects.filter(writing_id=pk)
    if request.method == "POST":
        user = get_user_model()

        if form.is_valid():
            post = form.save(commit=False)
            post.teacher = user.objects.get(username=current_writing.corrector)
            post.student = request.user
            post.writing = current_writing
            post.save()
            return redirect('user_profile:index')
        return HttpResponse('afasf')
    else:
        if current_writing.author == request.user:
            if rate:
                return render(request, 'user_profile/writing page.html', {'object': current_writing})
            else:
                return render(request, 'user_profile/writing page.html', {'object': current_writing, 'form': form})
        else:
            raise PermissionError()


# @login_required(login_url='user_profile:login')
class EditView(LoginRequiredMixin,UpdateView):
    login_url = 'user_profile:login'
    model = User

    template_name = 'user_profile/editview.html'
    fields = ['first_name','last_name','email','username']

    def get_object(self, queryset=None):
        return self.request.user

    success_url = reverse_lazy('user_profile:index')
    # def get_success_url(self):
    #  return  redirect('user_profile:index')


class UserFormView(View):
    form_class=UserForm
    template_name='user_profile/register_form.html'

    def get(self,request):
        form=self.form_class(None)
        return render(request,self.template_name, {'form':form})

    def post(self,request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user=authenticate(username=username, password=password)

            if user is not None:

                if user.is_active:
                    login(request,user)
                    return redirect('user_profile:index')
        return render(request, self.template_name, {'form': form})


class LoginView(View):

    def get(self, request):
        if request.user.is_authenticated():
            if request.user.teacher:
                # return HttpResponse('<h1>test</h1>')
                return redirect('corrector:teacherindex')
            return redirect('user_profile:index')
        form = LoginForm()
        return render(request, 'user_profile/login.html', {
            'form': form
        })

    def post(self, request):
        form = LoginForm(data=request.POST)
        if request.user.is_authenticated():
            return redirect('user_profile:index')

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.teacher:
                return redirect('corrector:teacherindex')
                # return HttpResponse('<p>teacher</p>')
            return redirect('user_profile:index')

        return render(request, 'user_profile/login.html', {
            'form': form
        })


# class CreateWriting(LoginRequiredMixin,CreateView):
#     login_url = 'user_profile:login'
#     model = Writing
#     fields = ['title', 'text']
#     def form_valid(self, form):
#         form.instance.author = self.request.User
#         return super(CreateWriting, self).form_valid(form)
#         # super az form valid creat  view es use mikone
#         # is_f_v = super(CreateWriting, self).form_valid(form)
#         # uhc = self.request.user.credit>9
#         # return is_f_v and uhc



@login_required(login_url='user_profile:login')
def NewWriting(request):
    subject = Subject.objects.all()
    current_user=request.user
    if request.method=="POST":
        form=WritingForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=request.user
            post.save()
            return redirect('user_profile:index')

    else:
        if current_user.teacher:
            return redirect('corrector:teacherindex')
        else:
            writing = request.user.writing_set.all().count()
            if writing >0:
                form = WritingForm()
                return render(request, 'user_profile/writing_form.html', {'form': form, 'subject': subject})
            else:
                form = WritingForm()
                return render(request,'user_profile/writing_form_test.html', {'form':form , 'subject':subject})



def Logout(request):
    logout(request)
    return  redirect('home')


def CommingSoon(request):
    return render(request, 'user_profile/comming_soon.html')

def ChangePassword(request):
    if request.method == 'POST':
        form=PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('user_profile:index')
        return render(request,'user_profile/editview.html',{'form':form})
    else:
        form=PasswordChangeForm(user=request.user)
        context={'form':form}
        return render(request,'user_profile/editview.html', context)



def Credit(request):
    form = Price(request.POST)
    if request.method=="GET":
        return render(request,'user_profile/input test.html',{'form':form})
    else:

        if form.is_valid():
            form=form.save(commit=False)
            credit = form.number
            amount = form.wallet
            current_user = request.user
            current_user.credit = credit
            current_user.amount = amount
            current_user.save()
            return redirect('user_profile:index')
        else:
            return HttpResponse('narini')


MMERCHANT_ID = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
# amount = 1000  # Amount will be based on Toman  Required
description = u'توضیحات تراکنش تستی'  # Required
# email = 'user@userurl.ir'  # Optional
# mobile = '09123456789'  # Optional



def Send_request(request):
    client = Client(ZARINPAL_WEBSERVICE)
    amount=request.user.credit
    email=request.user.email
    result = client.service.PaymentRequest(MMERCHANT_ID,
                                           amount,
                                           description,
                                           email,
                                           str(url_for('verify', _external=True)))
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return 'Error'

