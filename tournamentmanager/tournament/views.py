from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import forms as auth_forms
from django.urls import reverse
from django.views.generic import FormView
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import CreateTournamentForms
from .models import Tournament


class IndexView(TemplateView):
    template_name = 'tournament/home.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['last_tournaments'] = Tournament.objects.order_by('-created')[:5]
        return context


class RegisterView(FormView):
    form_class = auth_forms.UserCreationForm
    template_name = 'registration/register.html'
    success_url = '/login'

    def form_valid(self, form: auth_forms.UserCreationForm) -> HttpResponse:
        form.save()
        messages.success(self.request, 'Poprawnie utworzono użytkownika')
        return redirect('/login')


class CreateTournamentView(LoginRequiredMixin, CreateView):
    template_name_suffix = '_create_form'
    model = Tournament
    form_class = CreateTournamentForms

    def get_success_url(self):
        # return reverse('tournament-detail', kwargs={'pk': self.object.pk})
        return reverse('home')
