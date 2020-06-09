from django.shortcuts import render
from django.views.generic import CreateView, ListView
from Sample.models import Trials
from .form import TrialForm


class TrialCreate(CreateView):
    form_class = TrialForm
    template_name = 'Trial/trials_form.html'
    success_url = '/trial/create/'


class TrialListView(ListView):
    model = Trials
    template_name = 'Trial/trials_list.html'