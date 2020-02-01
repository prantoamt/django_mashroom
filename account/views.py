from django.shortcuts import render, HttpResponseRedirect, reverse
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from .forms import loginForm
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
            print(messages[0])             
    return render(request, template, context)


def logoutView(request):
    logout(request)
    return HttpResponseRedirect (reverse('products'))