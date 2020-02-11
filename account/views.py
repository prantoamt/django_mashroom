from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from account.models import UserProfile
from django.contrib.auth import get_user_model
from .forms import loginForm, RegisterForm
from orders.utils import id_generator


User = get_user_model()
# Create your views here.
def loginView(request):
    form = loginForm(request.POST or None)
    template = "account/login.html"
    context = {'form': form}
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            try:
                login(request, user)
                context['form'] = loginForm()
                return HttpResponseRedirect(reverse("products"))
            except:
                raise Http404
        else:
            messages.error = (request, "Invalid username or password")            
    return render(request, template, context)


def logoutView(request):
    logout(request)
    return HttpResponseRedirect (reverse('products'))

def register(request):
    form = RegisterForm()

    if(request.method=='POST'):
        form = RegisterForm(request.POST)
        if (form.is_valid()):
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')
            user = authenticate(username=username, password=password)
            user_profile = UserProfile(user=user)
            user_profile.email_confirmed = False
            varification_code = id_generator()
            user_profile.hashcode = varification_code
            user_profile.save()
            ##send_mail(subject, msg, from, to_list, fail_silently=True)
            subject = "Account info of mushroom firm"
            msg = "Dear "+user.first_name+", \nCongratulations! your account has been created. Please varify your email from your account option. Use this code while varifying your email: "+varification_code 
            from_email = settings.EMAIL_HOST_USER
            to_email = [email, settings.EMAIL_HOST_USER]
            send_mail(subject, msg, from_email, to_email, fail_silently=True)
            messages.success = (request, "Your account has ben created successfully!")
            return HttpResponseRedirect(reverse('login'))
    context = {'form': form}
    template = 'account/register.html'
    return render(request, template, context) 
