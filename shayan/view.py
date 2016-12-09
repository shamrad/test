from django.http import HttpResponse
from django.shortcuts import render,redirect



def Home(request):
    if request.user.is_authenticated():
        return render(request, 'home/home.html')
