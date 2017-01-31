from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import UpdateView
from django.db.models import Sum
from user_profile.models import Writing, Teacherate


def Teacherindex(request):
    current_user = request.user
    second = Writing.objects.exclude(corrector='').values('author').distinct()
    free = Writing.objects.exclude(author=request.user).filter(score='0').exclude(author__in=second)

    follow = Writing.objects.filter(corrector=request.user.username).values('author').distinct()
    writing = Writing.objects.exclude(author=request.user).filter(author__in=follow, score='0')


    all=Writing.objects.filter(corrector=request.user.username)

    rate=Teacherate.objects.filter(teacher=request.user).aggregate(Sum('rate'))['rate__sum']
    scored =Teacherate.objects.filter(teacher=request.user)

    income=scored.count()-follow.count()
    context={
        'user': current_user,
        'free': free,
        'writing': writing,
        'rate':rate,
        'income':income,
        'all':all
    }
    if current_user.teacher:
        return render(request, 'user_profile/teacherindex.html', context)

    return redirect('user_profile:index') #agar user teacher nabod redirect beshe

class Score(LoginRequiredMixin,UpdateView):
    login_url = 'user_profile:login'
    model = Writing
    template_name = 'user_profile/correctionview.html'
    fields = ['text','score','title','corrector','moshaver', 'grammer', 'vocab', 'oad', 'wordchoice', 'unity','adress','grammersc', 'vocabsc', 'oadsc', 'wordchoicesc', 'unitysc','adresssc' ]
    success_url = reverse_lazy('corrector:teacherindex')

    def get_object(self, *args, **kwargs):
        if self.request.user.teacher:
            wrt = super(Score, self).get_object(*args, **kwargs)
            if wrt.author != self.request.user:
                if (wrt.corrector == self.request.user.username) or (wrt.corrector==None)or (wrt.corrector==''):
                    return wrt
                else:
                    raise PermissionDenied() #matn haye tashih shode baz nemishavad
            else:
                raise PermissionDenied() #shoma nemitavanid matne khudetan ra tashih koni
        raise PermissionDenied()  # or Http404

def ChangePassword(request):
    if request.method == 'POST':
        form=PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('user_profile:index')
        return render(request,'user_profile/editviewteacher.html',{'form':form})
    else:
        form=PasswordChangeForm(user=request.user)
        context={'form':form}
        return render(request,'user_profile/editviewteacher.html', context)

class EditView(LoginRequiredMixin,UpdateView):
    login_url = 'user_profile:login'
    model = User

    template_name = 'user_profile/editviewteacher.html'
    fields = ['first_name','last_name','email','username']

    def get_object(self, queryset=None):
        return self.request.user

    success_url = reverse_lazy('corrector:teacherindex')


