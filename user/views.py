from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserAuthenticationForm
# Create your views here.


def base(request):
    return render(request, "base.html")


def say_hello(request):
    return HttpResponse('hello from user')


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/user/')
        else:
            return HttpResponse(form.errors)
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {'form': form})
