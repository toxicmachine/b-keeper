from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _


from .models import User


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин',
                               widget=forms.TextInput(attrs={'class': 'form-control text-center mb-2',}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control text-center',}))
    error_messages = {
        "invalid_login": _(
            "Неверный логин или пароль!"
        ),
    }

    class Meta:
        model = User
        fields = ['username', 'password']
