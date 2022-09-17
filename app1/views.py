from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.conf import settings

from .forms import UserRegisterForm

User = settings.AUTH_USER_MODEL


class RegisterView(CreateView):
    # model = User
    form_class = UserRegisterForm
    template_name = 'register.html'
    success_url = '/login'

