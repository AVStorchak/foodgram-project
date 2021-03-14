from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('success_redirect')
    template_name = 'reg.html'


class LoginAfterPasswordChangeView(PasswordChangeView):
    template_name = 'changePassword.html'

    @property
    def success_url(self):
        return reverse_lazy('index')


def success_redirect(request):
    return render(request, 'customPage.html')


login_after_password_change = login_required(LoginAfterPasswordChangeView.as_view())
