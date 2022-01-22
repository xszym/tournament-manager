from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import forms as auth_forms
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render


@login_required
def welcome(request):
    return render(request, 'tournament/home.html')


class RegisterView(FormView):
    form_class = auth_forms.UserCreationForm
    template_name = 'registration/register.html'
    success_url = '/login'

    def form_valid(self, form: auth_forms.UserCreationForm) -> HttpResponse:
        form.save()
        messages.success(self.request, 'Poprawnie utworzono użytkownika')
        return redirect('/login')
