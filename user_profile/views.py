from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.views.generic.edit import UpdateView

from .form import UserForm, LoginForm
from django.views.generic import View
from .models import Writing
from django.views.generic import CreateView


@login_required()
def index(request):

    #current_user=User.objects.get(username=username)
    current_user = request.user
    exam = current_user.writing_set.all()
    context = {
        'user': current_user,
        'exam': exam
    }
    return render(request, 'user_profile/index.html',context)


def writing(request,pk):
    current_writing=Writing.objects.get(pk=pk)
    return render(request, 'user_profile/writing page.html',{'object':current_writing})






class EditView(UpdateView):
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

            return redirect('user_profile:index')

        return render(request, 'user_profile/login.html', {
            'form': form
        })


class CreateWriting(CreateView):
    model = Writing
    fields = ['title', 'text']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(CreateWriting, self).form_valid(form)


def Logout(request):
    logout(request)
    return  redirect('home')

def Increase(request):
    return render(request, 'user_profile/increase.html')