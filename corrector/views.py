from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def correctorindex(request):
    return render(request,'user_profile/correctorindex.html')