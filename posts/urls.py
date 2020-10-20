from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import LoginView, LogoutView

from posts.views import IndexView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('accounts/', include([
        path('login', LoginView.as_view(), name='login'),
        path('logout', LogoutView.as_view(), name='logout'),
    ]))
]