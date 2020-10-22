from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView

from .views import IndexView, MyDraftsView, MyPublicPostsView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),

    path('my/', include([
        path('posts/', include([
            path('drafts', MyDraftsView.as_view(), name='my_drafts'),
            path('public', MyPublicPostsView.as_view(), name='my_public'),
        ])),
    ]))
]
