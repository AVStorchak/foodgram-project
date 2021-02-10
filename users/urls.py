from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('success_redirect/', views.success_redirect, name='success_redirect'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='authForm.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(template_name='changePassword.html'), name='change-password'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='resetPassword.html'), name='reset-password'),
]