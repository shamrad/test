from audioop import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import login as auth_login
from django.views import generic
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


# class EditView(UpdateView):
#     model = User
#     template_name = 'user_profile/editview.html'
#     fields = ['email','username']
#
#
#     def get_object(self):
#             return User.objects.get(pk=self.request.GET.get('pk'))  # or request.POST
#
# class EditUserProfileView(UpdateView): #Note that we are using UpdateView and not FormView
#     model = User
#     form_class = UserForm
#     template_name = "user_profile/editview.html"
#
#     def get_object(self, *args, **kwargs):
#         user = get_object_or_404(User, pk=self.kwargs)
#
#         # We can also get user object using self.request.user  but that doesnt work
#         # for other models.
#
#         return user.userprofile
#
#     def get_success_url(self, *args, **kwargs):
#         return reverse("some url name")


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