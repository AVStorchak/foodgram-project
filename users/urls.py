from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('success_redirect/', views.success_redirect, name='success_redirect'),
    path(
        'login/',
        auth_views.LoginView.as_view(template_name='authForm.html'),
        name='login'
    ),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path(
        'password_change/',
        views.login_after_password_change,
        name='change-password'
    ),
]

urlpatterns += [
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
