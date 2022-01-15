from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.http.request import HttpRequest

from .forms import LoginForm, RegisterForm


def welcome(request ):
    return render(request, 'tournament/home.html')
    if(request.user.is_authenticated):
        return HttpResponse("Hi " + request.user.username)
    else:
        return HttpResponse("Please login or register!")


def app_login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if(user is not None):
                login(request, user)
                messages.success(request, 'Zalogowano pomyślnie!')
            else:
                messages.warning(request, 'Wprowadzono błędne dane')
    if request.user.is_authenticated:
        return render(request, 'tournament/login.html')
    else:
        form = LoginForm()
        return render(request, 'tournament/login.html', {'form': form})


def app_register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['login']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user, created = User.objects.get_or_create(
                username=username, email=email)
            if created:
                user.set_password(password)
                user.save()
                messages.success(
                    request, 'Poprawnie utworzono użytkownika')
                return redirect('/login/')
            else:
                messages.warning(
                    request, 'Użytkownik o podanym loginie lub adresie email już istnieje')
            if not request.user.is_authenticated:
                form = RegisterForm()
                return render(request, 'tournament/register.html', {'form': form})
            else:
                return redirect('/login/')
    if request.user.is_authenticated:
        return render(request, 'tournament/register.html')
    else:
        form = RegisterForm()
        return render(request, 'tournament/register.html', {'form': form})
