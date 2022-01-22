from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import forms as auth_forms
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import CreateTournamentForms
from .models import Tournament

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


class CreateTournamentView(CreateView):
    template_name_suffix = '_create_form'
    model = Tournament
    form_class = CreateTournamentForms

    def get_success_url(self):
        # return reverse('tournament-detail', kwargs={'pk': self.object.pk})
        return reverse('home')
