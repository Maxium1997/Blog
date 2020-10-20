from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import PasswordResetView


from accounts.views import SignUpView, Login, Logout

urlpatterns = [
    path('accounts/', include([
        path('sign-up', SignUpView.as_view(), name='sign_up'),
        path('login', Login.as_view(template_name='registration/login.html'), name='login'),
        path('logout', Logout.as_view(template_name='registration/logged_out.html'), name='logout'),

        # path('password_change/', include([
        #     path('', PasswordChangeView.as_view(), name='password_change'),
        #     path('done', PasswordChangeDoneView.as_view(), name='password_change_done'),
        # ])),
        #
        # path('password_reset/', include([
        #     path('', PasswordChangeView.as_view(), name='password_reset'),
        #     path('done', PasswordChangeDoneView.as_view(), name='password_reset_done'),
        # ])),
        #

    ])),
]
