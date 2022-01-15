from django import forms


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
