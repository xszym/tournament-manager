from django import forms

from .models import Team, Tournament, TeamTournamentRequest


class LoginForm(forms.Form):
    loginClass = forms.TextInput(attrs={'class': 'form-control'})
    passwordClass = forms.PasswordInput(attrs={'class': 'form-control'})
    login = forms.CharField(
        widget=loginClass, label='Login', max_length=50, required=True)
    password = forms.CharField(
        widget=passwordClass, label='Password', max_length=50, required=True)


class RegisterForm(forms.Form):
    loginClass = forms.TextInput(attrs={'class': 'form-control'})
    passwordClass = forms.PasswordInput(attrs={'class': 'form-control'})
    emailClass = forms.EmailInput(attrs={'class': 'form-control'})
    login = forms.CharField(
        widget=loginClass, label='Login', max_length=50, required=True)
    email = forms.EmailField(widget=emailClass, label='Email', required=True)
    password = forms.CharField(
        widget=passwordClass, label='Password', max_length=50, required=True)


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class CreateTournamentForms(forms.ModelForm):
    class Meta:
        model = Tournament
        fields = ['name', 'location', 'start_date', 'end_date', 'type_of_elimination', 'game']
        widgets = {
            'start_date': DateInput(attrs={'class': 'form-control'}),
            'end_date': DateInput(attrs={'class': 'form-control'}),
        }

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name']


class TeamTournamentRequestForm(forms.ModelForm):
    class Meta:
        model = TeamTournamentRequest
        fields = ['tournament', 'team']

    def __init__(self, **kwargs):
        user = kwargs.pop('user', None)
        super(TeamTournamentRequestForm, self).__init__(**kwargs)
        self.fields['team'].queryset = Team.objects.filter(team_manager=user.pk)

