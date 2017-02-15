
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from django.template import RequestContext


def khane(request):
        return render(request, 'user_profile/home.html')

def service(request):
        return render(request, 'user_profile/service.html')


def faq(request):
        return render(request, 'user_profile/faq.html')

def aboutus(request):
        return render(request, 'user_profile/aboutus.html')

def barname(request):
        return render(request, 'user_profile/barname.html')

def nini(request):
        return render(request, 'user_profile/nini.html')



# test
def test(request):
        return render(request, 'user_profile/500.html')



def handler404(request):
    response = render_to_response('user_profile/404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('user_profile/500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response