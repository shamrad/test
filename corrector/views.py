from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import UpdateView

from user_profile.models import Writing

def Teacherindex(request):
    current_user = request.user
    second = Writing.objects.exclude(corrector='').values('author').distinct()
    free = Writing.objects.exclude(author=request.user).filter(score='0').exclude(author__in=second)

    follow = Writing.objects.filter(corrector=request.user.username).values('author').distinct()
    writing = Writing.objects.exclude(author=request.user).filter(author__in=follow, score='0')

    if current_user.teacher:
        context={
            'user': current_user,
            'free': free,
            'writing': writing
        }
        return render(request, 'user_profile/teacherindex.html', context)

    return redirect('user_profile:index') #agar user teacher nabod redirect beshe

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