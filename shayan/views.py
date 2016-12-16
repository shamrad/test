
from django.shortcuts import render,redirect
from user_profile.models import Comment

def khane(request):
        return render(request, 'user_profile/home.html')

def service(request):
        coment=Comment.objects.all()
        return render(request,'user_profile/service.html')
def aboutus(request):
        return render(request,'user_profile/aboutus.html')
