from django import forms

from .models import Tournament


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
        fields = ['name', 'location', 'start_date',
                  'end_date', 'match_time', 'type_of_elimination', ]
        widgets = {
            'start_date': DateInput(attrs={'class': 'form-control'}),
            'end_date': DateInput(attrs={'class': 'form-control'}),
            'match_time': TimeInput(attrs={'class': 'form-control'}),
        }
