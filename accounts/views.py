from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView

from accounts.models import User
from accounts.forms import SignUpForm, LoginForm
# Create your views here.


class SignUpView(CreateView):
    model = User
    template_name = 'registration/sign_up_form.html'
    form_class = SignUpForm


class Login(LoginView):
    form_class = LoginForm


class Logout(LogoutView):
    pass
