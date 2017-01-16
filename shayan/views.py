
from django.shortcuts import render,redirect


def khane(request):
        return render(request, 'user_profile/home.html')

def service(request):

        return render(request, 'user_profile/service.html')
def aboutus(request):
        return render(request, 'user_profile/aboutus.html')



# test
def test(request):
        return render(request, 'user_profile/500.html')