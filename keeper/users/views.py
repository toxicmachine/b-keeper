from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView
from django.shortcuts import render
from django.urls import resolve, reverse_lazy
from django.views.generic import TemplateView

from .forms import LoginUserForm

class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = ''
    extra_context = {
        'title': 'Хранитель резервных копий',
        'header': 'Хранитель резервных копий',
    }

