from django.shortcuts import render
from django.views.generic import CreateView

from .form import TrialForm


class TrialCreate(CreateView):
    form_class = TrialForm
    template_name = 'Trial/trials_form.html'
    success_url = '/trial/create/'
