from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http.request import HttpRequest


@login_required
def welcome(request):
    return render(request, 'tournament/home.html')


def app_register(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = auth_forms.UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Poprawnie utworzono użytkownika')
            return redirect('/register')
    else:
        form = auth_forms.UserCreationForm()
    return render(request, 'tournament/register.html', {'form': form})
