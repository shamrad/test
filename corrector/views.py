from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import UpdateView

from user_profile.models import Writing

def Teacherindex(request):
    current_user = request.user
    writing=Writing.objects.filter(score='0')
    if current_user.teacher:
        context={
            'user': current_user,
            'writing': writing
        }
        return render(request, 'user_profile/teacherindex.html', context)

    return redirect('user_profile:index')

class Score(LoginRequiredMixin,UpdateView):
    login_url = 'user_profile:login'
    model = Writing
    template_name = 'user_profile/correctionview.html'
    fields = ['text','score','title','corrector','moshaver']

    success_url = reverse_lazy('corrector:teacherindex')


#
# def Score(request,id):
#     current_user= request.user
#     if current_user.teacher:
#         def get(self, request):
#             form=Writing
#
#     return redirect('user_profile:index')