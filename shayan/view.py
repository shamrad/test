from django.http import HttpResponse
from django.shortcuts import render,redirect

def Home(request):
    return HttpResponse('<h1>this is home page</h1>')