from celery.task import task
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth import login as auth_login
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.edit import UpdateView
from django.contrib.auth.forms import PasswordChangeForm
# from oauthlib.oauth2 import Client
from suds.client import Client
from simple_email_confirmation.models import EmailAddress
from django.conf import settings

from .form import UserForm, LoginForm, WritingForm, Rate, PriceForm, EmailForm, HamayeshForm
from django.views.generic import View
from .models import Writing, Subject, Teacherate, Buy, Price, Registration, Course, Lesson, Event, Hamayesh
from django.views.generic import CreateView


@login_required(login_url='user_profile:login')
def index(request):
    current_user = request.user
    if current_user.teacher:
        return redirect('corrector:teacherindex')
    exam = current_user.writing_set.all()
    context = {
        'user': current_user,
        'exam': exam
    }
    return render(request, 'user_profile/index.html', context)


@login_required(login_url='user_profile:login')
@csrf_exempt
def writing(request, pk):
    current_writing = Writing.objects.get(pk=pk)
    form = Rate(request.POST)
    rate = Teacherate.objects.filter(writing_id=pk)
    if request.method == "POST":
        user = get_user_model()

        if form.is_valid():
            post = form.save(commit=False)
            post.teacher = user.objects.get(username=current_writing.corrector)
            post.student = request.user
            post.writing = current_writing
            post.save()
            return redirect('user_profile:writing')

    else:
        if current_writing.author == request.user:
            if rate:
                return render(request, 'user_profile/writing page.html', {'object': current_writing})
            else:
                return render(request, 'user_profile/writing page.html', {'object': current_writing, 'form': form})
        else:
            raise PermissionError()


# @login_required(login_url='user_profile:login')
class EditView(LoginRequiredMixin, UpdateView):
    login_url = 'user_profile:login'
    model = User

    template_name = 'user_profile/editview.html'
    fields = ['first_name', 'last_name', 'email', 'username']

    def get_object(self, queryset=None):
        return self.request.user

    success_url = reverse_lazy('user_profile:index')
    # def get_success_url(self):
    #  return  redirect('user_profile:index')


class UserFormView(View):
    form_class = UserForm
    template_name = 'user_profile/register_form.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            email = form.cleaned_data['email']
            user.save()
            msg = render_to_string('user_profile/Email4.html',
                                        {'username': user.first_name,
                                        'site': settings.SITE_URL,
                                        'confkey': user.confirmation_key})
            send_mail('Dear %s! Welcome to Scorize!' % user.first_name,
                      ' www.scorize.com/profile/confirm/%s/ از اینکه به وب سایت اسکورایز پیوستید خوشحالیم. برای استفاده از محتوای سایت با کلیک کردن بر لینک مقابل ایمیل خود را تایید کنید.!' % user.confirmation_key,
                      settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False, html_message=msg)
            karbar = authenticate(username=username, password=password)

            if karbar is not None:

                if karbar.is_active:
                    login(request, karbar)
                    return redirect('user_profile:index')
        return render(request, self.template_name, {'form': form})


def confirmation(request, confirmation_key):
    email = EmailAddress.objects.get(key=confirmation_key)
    user = get_user_model()
    pending_user = user.objects.get(email=email.email)
    pending_user.confirm_email(confirmation_key, save=True)
    pending_user.is_confirmed
    return redirect('user_profile:index')


def resendkey(request):
    email = request.user.email
    data = EmailAddress.objects.get(email=email)
    confkey = data.key
    msg_html = render_to_string('user_profile/Email2.html',
                                {'username': request.user.first_name,
                                 'site': settings.SITE_URL,
                                 'confkey': confkey})
    send_mail('Dear %s! Activation Key!' % request.user.first_name,
              ' www.scorize.com/profile/confirm/%s/ برای استفاده از محتوای سایت با کلیک کردن بر لینک مقابل ایمیل خود را تایید کنید.!' % confkey,
              settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False, html_message=msg_html)
    return redirect('user_profile:emailsent')


def emailsent(request):
    return render(request, 'user_profile/emailsent.html')





class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated():
            if request.user.teacher:
                # return HttpResponse('<h1>test</h1>')
                return redirect('corrector:teacherindex')
            return redirect('user_profile:index')
        form = LoginForm()
        return render(request, 'user_profile/login.html', {
            'form': form
        })

    def post(self, request):
        form = LoginForm(data=request.POST)
        if request.user.is_authenticated():
            return redirect('user_profile:index')

        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if user.teacher:
                return redirect('corrector:teacherindex')
                # return HttpResponse('<p>teacher</p>')
            return redirect('user_profile:index')

        return render(request, 'user_profile/login.html', {
            'form': form
        })


# class CreateWriting(LoginRequiredMixin,CreateView):
#     login_url = 'user_profile:login'
#     model = Writing
#     fields = ['title', 'text']
#     def form_valid(self, form):
#         form.instance.author = self.request.User
#         return super(CreateWriting, self).form_valid(form)
#         # super az form valid creat  view es use mikone
#         # is_f_v = super(CreateWriting, self).form_valid(form)
#         # uhc = self.request.user.credit>9
#         # return is_f_v and uhc



@login_required(login_url='user_profile:login')
def NewWriting(request):
    subject = Subject.objects.all()
    current_user = request.user
    if request.method == "POST":
        form = WritingForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            writing = request.user.writing_set.all().count()
            if writing > 1:
                corrector = Writing.objects.filter(author=current_user).get(pk=1).corrector
                current_user.credit2 -= 1
                current_user.save()
                send_mail('New writing from %s' % current_user.username,
                          '%s has submitted a new writing, and it is avaliable in your profile.' % current_user.username,
                          settings.DEFAULT_FROM_EMAIL, [corrector.email], fail_silently=False)
            return redirect('user_profile:index')
        else:
            raise ValidationError('فیلدها را پر کنید')

    else:
        if current_user.teacher:
            return redirect('corrector:teacherindex')
        else:
            writing = request.user.writing_set.all().count()
            if writing > 0:
                if current_user.credit2 > 0:
                    form = WritingForm()
                    return render(request, 'user_profile/writing_form.html', {'form': form, 'subject': subject})
                else:
                    return redirect('user_profile:credit')
            else:
                form = WritingForm()
                return render(request, 'user_profile/writing_form_test.html', {'form': form, 'subject': subject})


def Logout(request):
    logout(request)
    return redirect('home')


def CommingSoon(request):
    return render(request, 'user_profile/comming_soon.html')


def reference(request):
    return render(request, 'user_profile/manabe.html')


def ChangePassword(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user)

        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('user_profile:index')
        return render(request, 'user_profile/editview.html', {'form': form})
    else:
        form = PasswordChangeForm(user=request.user)
        context = {'form': form}
        return render(request, 'user_profile/editview.html', context)


def conversation(request):
    Mokaleme = Course.objects.get(name='Mokaleme')
    if not Registration.objects.filter(course=Mokaleme, participant=request.user).exists():
        m = Registration(course=Mokaleme, participant=request.user)
        m.save()
        msg_html = render_to_string('user_profile/Email3.html',
                                    {'username': request.user.first_name,
                                     'site': settings.SITE_URL})
        send_mail('ثبت نام شما در دوره مکالمه رایگان اسکورایز با موفقیت انجام شد!',
                  'ثبت نام شدید! منتظر درس های دوره مکالمه باشید. درس ها به مدت 7 هفته در 9 صبح روزهای شنبه و دوشنبه و چهارشنبه به ایمیل شما ارسال می شود.',
                  settings.DEFAULT_FROM_EMAIL, [request.user.email], fail_silently=False, html_message=msg_html)
        messages.success(request, 'ثبت نام با موفقیت انجام شد.')
    else:
        messages.error(request, 'شما قبلا در این دوره ثبت نام کرده اید!')
    return redirect('user_profile:index')


@login_required(login_url='user_profile:login')
def Etebar(request):
    form = PriceForm()
    price = Price.objects.last()
    current_user = request.user
    if request.method == "GET":
        if request.user.teacher:
            return redirect('corrector:teacherindex')
        return render(request, 'user_profile/increase.html', {'form': form, 'price': price})
    else:
        form = PriceForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            credit = form.number
            amount = form.wallet

            current_user.credit = credit
            current_user.amount = amount
            current_user.save()
            return redirect('user_profile:Send_request')  # bayad adrese banko bedim
        else:
            return render(request, 'user_profile/increase.html', {'form': form})


MMERCHANT_ID = 'fbac782a-dfa6-11e6-8ef4-000c295eb8fc'  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
# amount = 10000  # Amount will be based on Toman  Required
# email = 'user@userurl.ir'  # Optional


@login_required(login_url='user_profile:login')
def Send_request(request):
    client = Client(ZARINPAL_WEBSERVICE)
    description = u'خرید خدمات تصحیح متن انگلیسی'  # Required
    amount = request.user.amount
    email = request.user.email
    mobile = '09123456789'  # Optional
    result = client.service.PaymentRequest(MMERCHANT_ID,
                                           amount,
                                           description,
                                           email,
                                           mobile,
                                           'http://scorize.com' + reverse('user_profile:verify'))
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return HttpResponse(result.Status)


# @login_required(login_url='user_profile:login')
def verify(request):
    client = Client(ZARINPAL_WEBSERVICE)
    current_user = request.user
    amount1 = current_user.amount
    credit1 = current_user.credit
    amount2 = current_user.amount2
    credit2 = current_user.credit2
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.GET['Authority'],
                                                    amount1)
        if result.Status == 100:
            current_user.amount2 = int(amount1) + int(amount2)
            current_user.credit2 = int(credit1) + int(credit2)
            current_user.save()
            buy = Buy.objects.create(user=current_user)
            buy.authority = request.GET['Authority']
            buy.amount = amount1
            buy.number = credit1
            buy.save()
            messages.success(request, 'تراکنش با موفقیت انجام شد.')
            return redirect('user_profile:index')
        elif result.Status == 101:
            messages.success(request, 'پرداخت شما با موفقیت انجام شد.')
            return redirect('user_profile:index')
        else:
            messages.error(request, 'Transaction failed.')
            return redirect('user_profile:index')
    else:
        messages.warning(request, 'Transaction failed or canceled by user.')
        return redirect('user_profile:index')

# event=Event.objects.filter(pk=1)


def hamayesh_reg(request,pk):
    event = Event.objects.get(pk=pk)
    if request.method == "POST":
        form = HamayeshForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.event=event
            amount=event.expense
            description=event.description
            client = Client(ZARINPAL_WEBSERVICE)
            result = client.service.PaymentRequest(MMERCHANT_ID,
                                                   amount,
                                                   description,
                                                   post.email,
                                                   post.mobile,
                                                   'https://scorize.com' + reverse('verify_event',kwargs={'pk':pk,'postid':post.id}))
            if result.Status == 100:
                return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
            else:
                return HttpResponse(result.Status)
            # return generate_pdf(request, pk=pk , id=post.id)
    else:
            form = HamayeshForm()
    return render(request, 'user_profile/hamayesh.html',{'form': form, 'event': event})


def verify_event(request,pk, postid):
    event = Event.objects.get(pk=pk)
    user=Hamayesh.objects.get(pk=postid)
    client = Client(ZARINPAL_WEBSERVICE)
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.GET['Authority'],
                                                    event.expense)
        if result.Status == 100:
            messages.success(request, 'تراکنش با موفقیت انجام شد.')
            msg = render_to_string('user_profile/Email4.html')
            send_mail('ثبت نام با موفقیت انجام شد','Registration is Completed!',
                  settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False, html_message=msg),
            return redirect('home')
        elif result.Status == 101:
            messages.success(request, 'پرداخت شما با موفقیت انجام شد.')
            return HttpResponse('ok')
        else:
            messages.error(request, 'Transaction failed.')
            return redirect('home')
    else:
        messages.warning(request, 'Transaction failed or canceled by user.')
        return redirect('home')


# from user_profile.utils import render_to_pdf


# def generate_pdf(request, pk, id):
#     event= Event.objects.get(pk= pk)
#     reg= Hamayesh.objects.get(pk=id)
#     data = {
#          'reg': reg,
#          'event': event,
#      }
#     pdf = render_to_pdf('user_profile/ticket.html', data)
#     return HttpResponse(pdf, content_type='application/pdf')