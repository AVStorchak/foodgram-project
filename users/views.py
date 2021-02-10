from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('success_redirect')
    template_name = 'reg.html'


def success_redirect(request):
    return render(request, 'customPage.html')
