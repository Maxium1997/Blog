from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from accounts.models import User, Box
from accounts.forms import SignUpForm, LoginForm
# Create your views here.


class SignUpView(CreateView):
    model = User
    template_name = 'registration/sign_up_form.html'
    form_class = SignUpForm

    def form_valid(self, form):
        user = form.save()
        Box.objects.create(owner=user).save()
        auth.login(self.request, user)
        return redirect('index')

    def get_success_url(self):
        return redirect('index')


class Login(LoginView):
    form_class = LoginForm
