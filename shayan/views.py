from django.http import HttpResponse
from django.shortcuts import render,redirect


def khane(request):
        return render(request, 'user_profile/home.html')
