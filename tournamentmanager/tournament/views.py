from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import forms as auth_forms
from django.urls import reverse
from django.views.generic import CreateView, ListView, FormView, TemplateView, DetailView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http.request import HttpRequest
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.shortcuts import get_object_or_404

from .forms import CreateTeamForm, CreateTournamentForms, TeamTournamentRequestForm
from .models import Game, Team, TeamTournamentRequestStatusType, Tournament, TeamTournamentRequest
from .helpers import slug_to_uuid


class IndexView(TemplateView):
    template_name = 'tournament/home.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['last_tournaments'] = Tournament.objects.order_by('-created')[:3]
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

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.referee_list.add(self.request.user)
        return response

    def get_success_url(self):
        # return reverse('tournament-detail', kwargs={'pk': self.object.pk})
        return reverse('home')


class CreateTeamView(LoginRequiredMixin, CreateView):
    template_name_suffix = '_create_form'
    model = Team
    form_class = CreateTeamForm

    def form_valid(self, form):
        form.instance.team_manager = self.request.user
        response = super().form_valid(form)
        return response

    def get_success_url(self):
        # return reverse('team-management', kwargs={'pk': self.object.pk})
        return reverse('home')


class TournamentListView(ListView):
    template_name = 'tournament/tournament_list.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(TournamentListView, self).get_context_data(**kwargs)

        categories = Game.objects.all()
        context['games'] = categories

        tournaments_list = Tournament.objects.all()

        game_val = self.request.GET.get('game', '')
        if game_val != '':
            tournaments_list = tournaments_list.filter(game__name=game_val)

        name_val = self.request.GET.get('name', '')
        if name_val != '':
            tournaments_list = tournaments_list.filter(name__icontains=name_val)
        page = self.request.GET.get('page')

        paginator = Paginator(tournaments_list, self.paginate_by)
        try:
            tournaments_list = paginator.page(page)
        except PageNotAnInteger:
            tournaments_list = paginator.page(1)
        except EmptyPage:
            tournaments_list = paginator.page(paginator.num_pages)
        context['tournaments'] = tournaments_list
        return context

    def get_queryset(self):
        name_val = self.request.GET.get('name', '')
        game_val = self.request.GET.get('game', '')

        new_context = Tournament.objects.order_by('-created')
        if game_val != '':
            new_context = new_context.filter(game__name=game_val)

        if name_val != '':
            new_context = new_context.filter(name__icontains=name_val)

        return new_context

    def get_kwargs(self, arg_name):
        try:
            arg = self.kwargs[arg_name]
            return arg
        except:
            return ''


class TeamListView(LoginRequiredMixin, ListView):
    template_name = 'tournament/team_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        teams_list = Team.objects.all()

        teams_list_manager = teams_list.filter(team_manager=self.request.user)
        teams_list_member = teams_list.filter(members__in=(self.request.user,))

        context['teams_manager'] = teams_list_manager
        context['teams_member'] = teams_list_member
        return context

    def get_queryset(self):
        return Team.objects.all()


class CreateTeamTournamentRequestView(LoginRequiredMixin, CreateView):
    template_name_suffix = '_create_form'
    model = TeamTournamentRequest
    form_class = TeamTournamentRequestForm

    def form_valid(self, form):
        response = super().form_valid(form)
        # print(self.request.user)
        self.object.status = TeamTournamentRequestStatusType.PENDING
        return response

    def get_success_url(self):
        # return reverse('tournament-detail', kwargs={'pk': self.object.pk})
        return reverse('home')

    def get_form_kwargs(self, **kwargs):
        form_kwargs = super(CreateTeamTournamentRequestView, self).get_form_kwargs(**kwargs)
        form_kwargs["user"] = self.request.user
        return form_kwargs

class TournamentManageView(LoginRequiredMixin, ListView):
    template_name = 'tournament/tournament_manage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        tournaments = Tournament.objects.filter(referee_list=self.request.user)

        context['tournaments'] = []

        for tournament in tournaments:
            request_list = TeamTournamentRequest.objects.all()
            request_list = request_list.filter(tournament=tournament.pk)
            context['tournaments'].append([tournament, request_list])

        return context

    def get_queryset(self):
        return Team.objects.all()

def change_TeamTournamentRequest_status(request, request_id, new_status):
    request = get_object_or_404(TeamTournamentRequest, pk=request_id)
    print("change_TeamTournamentRequest_status", request)
    # if request.tournament.
    try:
        request.status = TeamTournamentRequestStatusType(new_status).name
        if request.status == TeamTournamentRequestStatusType.ACCEPTED.name:
            request.tournament.team_list.add(request.team)
        request.save()

    except (KeyError, request.DoesNotExist):
        # Redisplay the question voting form.
        return reverse('tournament_manage')
    return HttpResponseRedirect(reverse('tournament_manage'))

  
class TeamDetailsView(DetailView):
    model = Team

    def get_object(self, queryset = None):
        try:
            self.kwargs['pk'] = slug_to_uuid(self.kwargs.get('slug'))
            return super().get_object(queryset)
        except ValueError:
            raise Http404('Invalid team id format')
